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

def calculate_audience_quality(profile):
    """Calculate audience quality score based on real Twitter metrics (0-100, higher = better)"""
    score = 0
    factors = []
    
    # 1. Followers/Following ratio (40% of score)
    # Healthy ratio: followers > following * 2 (score: 40)
    # Neutral: followers ≈ following (score: 20)
    # Poor: following > followers * 2 (score: 0)
    if profile["followers"] == 0:
        ratio_score = 0
        factors.append("No followers")
    else:
        ratio = profile["followers"] / max(profile["following"], 1)
        if ratio >= 2:
            ratio_score = 40
            factors.append("Excellent follower/following ratio")
        elif ratio >= 1:
            ratio_score = 30
            factors.append("Good follower/following ratio")
        elif ratio >= 0.5:
            ratio_score = 20
            factors.append("Average follower/following ratio")
        else:
            ratio_score = 10
            factors.append("Poor follower/following ratio")
    
    score += ratio_score
    
    # 2. Engagement rate (30% of score)
    # High: >5% (score: 30)
    # Medium: 1-5% (score: 20)
    # Low: <1% (score: 10)
    engagement = profile.get("engagement_rate", 0)
    if engagement > 5:
        engagement_score = 30
        factors.append(f"High engagement rate ({engagement:.1f}%)")
    elif engagement >= 1:
        engagement_score = 20
        factors.append(f"Good engagement rate ({engagement:.1f}%)")
    else:
        engagement_score = 10
        factors.append(f"Low engagement rate ({engagement:.1f}%)")
    
    score += engagement_score
    
    # 3. Account completeness (15% of score)
    completeness_score = 0
    bio = profile.get("bio", "")
    if len(bio) > 50:
        completeness_score += 10
        factors.append("Detailed bio")
    elif len(bio) > 10:
        completeness_score += 5
        factors.append("Basic bio")
    else:
        factors.append("Missing or short bio")
    
    if profile.get("verified", False):
        completeness_score += 5
        factors.append("Verified account")
    
    score += completeness_score
    
    # 4. Content quality (15% of score)
    content_score = 0
    if profile["tweets"] > 0:
        media_ratio = profile["media"] / profile["tweets"]
        if media_ratio > 0.3:
            content_score += 10
            factors.append("High media content")
        elif media_ratio > 0.1:
            content_score += 7
            factors.append("Moderate media content")
        else:
            content_score += 3
            factors.append("Low media content")
        
        # Account activity
        tweets_per_month = profile["tweets"] / 36  # Assuming 3 years
        if tweets_per_month > 30:
            content_score += 5
            factors.append("Very active account")
        elif tweets_per_month > 10:
            content_score += 3
            factors.append("Active account")
        else:
            content_score += 1
            factors.append("Inactive account")
    
    score += content_score
    
    # Ensure score is between 0-100
    score = max(0, min(100, int(score)))
    
    # Determine quality level
    if score >= 80:
        quality_level = "EXCELLENT"
        description = "Top-tier audience quality"
    elif score >= 60:
        quality_level = "GOOD"
        description = "Strong audience quality"
    elif score >= 40:
        quality_level = "AVERAGE"
        description = "Moderate audience quality"
    elif score >= 20:
        quality_level = "NEEDS IMPROVEMENT"
        description = "Below average audience quality"
    else:
        quality_level = "POOR"
        description = "Low audience quality"
    
    # Estimate verified followers based on quality score
    # Formula: verified_followers = total_followers * (quality_score/100) * multiplier
    # Higher quality accounts attract more verified followers
    multiplier = 0.4 if profile.get("verified", False) else 0.2
    estimated_verified = int(profile["followers"] * (score / 100) * multiplier)
    
    # Estimate low-quality audience (inactive/suspicious accounts)
    # Formula: low_quality = total_followers * (100 - quality_score)/100 * 0.7
    estimated_low_quality = int(profile["followers"] * ((100 - score) / 100) * 0.7)
    
    # Ensure estimates don't exceed total followers
    estimated_verified = min(estimated_verified, profile["followers"])
    estimated_low_quality = min(estimated_low_quality, profile["followers"] - estimated_verified)
    
    return {
        "quality_score": score,
        "real_percentage": score,  # for backward compatibility
        "risk": quality_level,  # now represents quality level
        "description": description,
        "factors": factors,
        "total_followers": profile["followers"],
        "estimated_real": estimated_verified,  # estimated verified followers
        "estimated_fake": estimated_low_quality  # estimated low-quality audience
    }

def generate_insights(profile):
    """Generate personalized insights from profile data"""
    strengths = []
    weaknesses = []
    recommendations = []
    action_plan = []
    
    # Analyze followers
    if profile["followers"] > 10000:
        followers_str = f"{profile['followers']/1000:.1f}K" if profile['followers'] >= 1000 else str(profile['followers'])
        strengths.append(f"Strong follower base ({followers_str})")
    elif profile["followers"] < 1000:
        weaknesses.append(f"Small audience ({profile['followers']} followers)")
        recommendations.append("Focus on growing your follower base through consistent posting")
        action_plan.append("Post daily for 30 days to increase visibility")
    
    # Analyze engagement rate
    if profile["engagement_rate"] > 5:
        strengths.append(f"High engagement rate ({profile['engagement_rate']}%)")
    elif profile["engagement_rate"] < 1:
        weaknesses.append(f"Low engagement rate ({profile['engagement_rate']}%)")
        recommendations.append("Improve engagement by asking questions and using polls")
        action_plan.append("Add 1-2 questions per tweet to boost replies")
    
    # Analyze tweet frequency
    if profile["tweets"] > 1000:
        strengths.append(f"Active account ({profile['tweets']} tweets)")
    elif profile["tweets"] < 100:
        weaknesses.append(f"Low tweet volume ({profile['tweets']} tweets)")
        recommendations.append("Increase posting frequency to stay relevant")
        action_plan.append("Aim for 3-5 tweets per week minimum")
    
    # Analyze follower/following ratio
    if profile["followers"] > profile["following"] * 2:
        strengths.append("Healthy follower/following ratio")
    elif profile["following"] > profile["followers"] * 2:
        weaknesses.append("Following more than being followed")
        recommendations.append("Focus on creating follow-worthy content")
        action_plan.append("Audit who you follow and unfollow inactive accounts")
    
    # Analyze bio
    bio = profile.get("bio", "")
    if not bio or len(bio) < 10:
        weaknesses.append("Weak or missing bio")
        recommendations.append("Create a compelling bio with keywords")
        action_plan.append("Update bio with 3 key topics you tweet about")
    elif len(bio) > 50:
        strengths.append("Detailed bio with clear messaging")
    
    # Analyze viral score
    if profile["viral_score"] > 70:
        strengths.append(f"High viral potential ({profile['viral_score']}/100)")
    elif profile["viral_score"] < 30:
        weaknesses.append(f"Low viral score ({profile['viral_score']}/100)")
        recommendations.append("Work on creating more shareable content")
        action_plan.append("Study viral tweets in your niche and adapt their patterns")
    
    # Analyze quality score
    if profile["quality"] > 70:
        strengths.append(f"High quality content ({profile['quality']}%)")
    elif profile["quality"] < 30:
        weaknesses.append(f"Content quality needs improvement ({profile['quality']}%)")
        recommendations.append("Focus on value-driven content over quantity")
        action_plan.append("Plan 3 high-value threads per month")
    
    # Default messages if no insights
    if len(strengths) == 0:
        strengths.append("Solid foundation to build upon")
    if len(weaknesses) == 0:
        weaknesses.append("Minor optimizations needed")
    if len(recommendations) == 0:
        recommendations.append("Continue current strategy with minor tweaks")
    if len(action_plan) == 0:
        action_plan.append("Review metrics weekly and adjust based on performance")
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "action_plan": action_plan
    }

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

@app.route('/api/insights', methods=['POST'])
def insights():
    """Generate personalized insights for a user"""
    data = request.get_json()
    username = data.get('username', '').strip().replace('@', '')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    profile = get_twitter_data(username)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    
    # Generate insights
    insights_data = generate_insights(profile)
    
    # Add profile info for display
    result = {
        "avatar_url": profile.get("avatar_url", ""),
        "display_name": profile.get("display_name", profile.get("username", "")),
        "username": profile.get("username", username),
        "followers": profile.get("followers", 0),
        "engagement_rate": profile.get("engagement_rate", 0),
        "tweets": profile.get("tweets", 0),
        "following": profile.get("following", 0),
        "bio": profile.get("bio", ""),
        "viral_score": profile.get("viral_score", 0),
        "quality": profile.get("quality", 0)
    }
    result.update(insights_data)
    return jsonify(result)

@app.route('/api/fake-score', methods=['POST'])
def fake_score():
    """Calculate audience quality score for a user"""
    data = request.get_json()
    username = data.get('username', '').strip().replace('@', '')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    profile = get_twitter_data(username)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    
    result = calculate_audience_quality(profile)
    # Add profile info for display
    result["avatar_url"] = profile.get("avatar_url", "")
    result["display_name"] = profile.get("display_name", profile.get("username", ""))
    result["username"] = profile.get("username", username)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)