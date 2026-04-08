# Deploy to Render

## Prerequisites
- GitHub account with repository access
- Render account (sign up at [render.com](https://render.com))

## Deployment Steps

### 1. Push code to GitHub
```bash
git push origin master
```

### 2. Create a new Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository (give Render access if needed)
4. Select the repository `wabrent/xscore`

### 3. Configure the service
- **Name:** `xscore` (or any name)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

Render will automatically detect the `render.yaml` configuration file and use those settings.

### 4. Add environment variables (optional)
No environment variables are required for basic operation. The app uses FXTwitter public API.

### 5. Deploy
- Click "Create Web Service"
- Render will build and deploy your application
- Wait for the build to complete (2-5 minutes)
- Your app will be available at `https://xscore.onrender.com` (or your custom domain)

### 6. Verify deployment
- Visit the provided URL
- Test the Analyze, Compare, Predict, and Insights tabs
- Ensure loading spinners appear during API calls

## Automatic Deploys
By default, Render enables automatic deploys on pushes to the `master` branch.

## Troubleshooting
- **Build fails:** Check build logs for missing dependencies
- **App crashes:** Check runtime logs for Python errors
- **API errors:** FXTwitter API may have rate limits; the app includes caching
- **Static files not loading:** Ensure the `static/` folder exists with background image

## Alternative Platforms
- **Railway:** Similar to Render, supports Python/Flask
- **Heroku:** Requires Procfile (`web: gunicorn app:app`)
- **PythonAnywhere:** Free tier for Flask apps

## Post-Deployment
- Monitor logs in Render dashboard
- Consider adding a custom domain
- Set up alerts for downtime