#!/bin/bash

# Django Quiz Bot Deployment Script
echo "🚀 Preparing Django Quiz Bot for deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing git repository..."
    git init
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Django Quiz Bot ready for deployment - $(date)"

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Please add your GitHub repository as origin:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/django-quiz-bot.git"
    echo ""
    echo "📋 Next steps:"
    echo "1. Create a repository on GitHub: https://github.com/new"
    echo "2. Run: git remote add origin YOUR_REPO_URL"
    echo "3. Run: git push -u origin main"
    echo "4. Deploy on Railway: https://railway.app"
else
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
    echo ""
    echo "✅ Code pushed to GitHub!"
fi

echo ""
echo "🎉 Your Django Quiz Bot is ready for deployment!"
echo ""
echo "🌟 Recommended deployment platforms:"
echo "   1. Railway (easiest): https://railway.app"
echo "   2. Render (free tier): https://render.com"
echo "   3. Heroku (paid): https://heroku.com"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions!"
