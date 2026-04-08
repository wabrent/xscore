import os
import requests
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

FXTWITTER_API = "https://api.fxtwitter.com"

# Simple in-memory cache with 5 minute TTL
cache = {}
CACHE_TTL = 300  # 5 minutes in seconds

def validate_username(username):
    """Basic Twitter username validation"""
    if not username:
        return False
    if len(username) > 15:
        return False
    # Twitter usernames can contain letters, numbers, underscore
    import re
    return bool(re.match(r'^[A-Za-z0-9_]+$', username))

def _get_twitter_data_uncached(username):
    """Fetch Twitter data from API without cache"""
    try:
        resp = requests.get(f"{FXTWITTER_API}/{username}", timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("code") != 200:
            return None
        user = data.get("user", {})
        
        followers = user.get("followers", 0)
        following = user.get("following", 0)
        tweets = user.get("tweets", 0)
        likes = user.get("likes", 0)
        media = user.get("media_count", 0)
        
        # Real metrics
        avg_likes = likes / max(tweets, 1) if tweets > 0 else 0
        engagement_rate = likes / max(followers, 1) * 100 if followers > 0 else 0
        
        # Quality score
        quality = min(100, int((followers / max(following, 1)) * 10))
        
        # Viral potential
        viral_score = min(100, int(engagement_rate * 3 + (avg_likes / 10)))
        
        # Growth rate (estimated)
        growth_rate = min(100, int((followers / max(tweets, 1)) * 2))
        
        return {
            "username": user.get("screen_name", username),
            "display_name": user.get("name", username),
            "bio": user.get("description", ""),
            "followers": followers,
            "following": following,
            "tweets": tweets,
            "likes": likes,
            "media": media,
            "verified": user.get("verification", {}).get("verified", False),
            "avatar_url": user.get("avatar_url", ""),
            "engagement_rate": round(engagement_rate, 2),
            "avg_likes": round(avg_likes, 1),
            "quality": quality,
            "viral_score": viral_score,
            "growth_rate": growth_rate,
            "influence_rank": min(100, max(1, 100 - int(followers / 10000)))
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_twitter_data(username):
    """Get Twitter data with caching"""
    # Check cache first
    if username in cache:
        cached_data, timestamp = cache[username]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data
        else:
            # Cache expired
            del cache[username]
    
    # Fetch fresh data
    data = _get_twitter_data_uncached(username)
    if data:
        # Store in cache
        cache[username] = (data, time.time())
    
    return data

def compare_profiles(username1, username2):
    data1 = get_twitter_data(username1)
    data2 = get_twitter_data(username2)
    
    if not data1 or not data2:
        return None
    
    # Compare metrics
    comparison = {
        "user1": data1,
        "user2": data2,
        "winner": {
            "followers": data1["followers"] > data2["followers"],
            "engagement": data1["engagement_rate"] > data2["engagement_rate"],
            "viral": data1["viral_score"] > data2["viral_score"],
            "growth": data1["growth_rate"] > data2["growth_rate"],
            "quality": data1["quality"] > data2["quality"]
        }
    }
    
    return comparison

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    username = data.get('username', '').strip().replace('@', '')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    result = get_twitter_data(username)
    if not result:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(result)

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    user1 = data.get('user1', '').strip().replace('@', '')
    user2 = data.get('user2', '').strip().replace('@', '')
    
    if not user1 or not user2:
        return jsonify({"error": "Two usernames required"}), 400
    
    result = compare_profiles(user1, user2)
    if not result:
        return jsonify({"error": "One or both users not found"}), 404
    
    return jsonify(result)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict viral potential based on content analysis"""
    data = request.get_json()
    username = data.get('username', '').strip().replace('@', '')
    content = data.get('content', '')
    
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    profile = get_twitter_data(username)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    
    # Analyze content for viral potential
    viral_indicators = {
        "hashtags": content.count('#'),
        "mentions": content.count('@'),
        "length": len(content),
        "has_emoji": bool(any(ord(c) > 127 for c in content)),
        "has_link": 'http' in content.lower()
    }
    
    # Score content
    content_score = 0
    content_score += min(30, viral_indicators["hashtags"] * 10)
    content_score += min(20, viral_indicators["mentions"] * 5)
    content_score += 20 if 50 <= viral_indicators["length"] <= 280 else 10
    content_score += 15 if viral_indicators["has_emoji"] else 0
    content_score += 15 if viral_indicators["has_link"] else 0
    
    # Combine with profile
    profile_viral = profile["viral_score"]
    combined_score = int((content_score * 0.4) + (profile_viral * 0.6))
    
    prediction = {
        "score": min(100, combined_score),
        "verdict": "HIGH" if combined_score >= 70 else "MEDIUM" if combined_score >= 40 else "LOW",
        "factors": {
            "content_score": content_score,
            "profile_score": profile_viral,
            "has_hashtags": viral_indicators["hashtags"] > 0,
            "has_mentions": viral_indicators["mentions"] > 0,
            "good_length": 50 <= viral_indicators["length"] <= 280,
            "has_emoji": viral_indicators["has_emoji"],
            "has_link": viral_indicators["has_link"]
        },
        "tips": []
    }
    
    if combined_score < 40:
        prediction["tips"] = ["Add more hashtags", "Use engaging hook", "Add relevant link"]
    elif combined_score < 70:
        prediction["tips"] = ["Good start! Add more engagement", "Try shorter format"]
    
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)