#!/bin/bash
# Simple script to push to GitHub

echo "════════════════════════════════════════════════════════════"
echo "  Manchester Seals - Push to GitHub"
echo "════════════════════════════════════════════════════════════"
echo ""

cd /Users/josephhanily/IdeaProjects/manchester-seals-python-webservice

echo "✅ Setting remote to: https://github.com/manchesterseals/manchester-seals-python-webservice.git"
git remote remove origin 2>/dev/null
git remote add origin https://github.com/manchesterseals/manchester-seals-python-webservice.git

echo "✅ Setting branch to main"
git branch -M main

echo ""
echo "🚀 Pushing to GitHub..."
echo ""
echo "⚠️  You will be prompted for credentials:"
echo "   Username: Your GitHub username"
echo "   Password: Your Personal Access Token (NOT your GitHub password!)"
echo ""
echo "   Get token at: https://github.com/settings/tokens/new"
echo "   Required scope: ✅ repo"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "  ✅ SUCCESS! Repository pushed to GitHub"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "🔗 View at: https://github.com/manchesterseals/manchester-seals-python-webservice"
    echo ""
else
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "  ❌ PUSH FAILED"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "Common reasons:"
    echo ""
    echo "1. Repository doesn't exist yet on GitHub"
    echo "   → Create it first at:"
    echo "   → https://github.com/organizations/manchesterseals/repositories/new"
    echo "   → Name: manchester-seals-python-webservice"
    echo "   → DO NOT initialize with README/gitignore/license"
    echo ""
    echo "2. Authentication failed"
    echo "   → Use Personal Access Token, not password"
    echo "   → Get token: https://github.com/settings/tokens/new"
    echo ""
    echo "3. No permission to manchesterseals organization"
    echo "   → Check: https://github.com/orgs/manchesterseals/people"
    echo "   → Or create under your account: https://github.com/new"
    echo ""
fi

