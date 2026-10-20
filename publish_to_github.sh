#!/usr/bin/env bash
# Publish this folder to a NEW empty GitHub repo.
# First create an empty repo on github.com (do NOT add a README), then run:
#   bash publish_to_github.sh https://github.com/<you>/<repo>.git
set -e
REPO="$1"
[ -z "$REPO" ] && { echo "Usage: bash publish_to_github.sh <your-repo-url.git>"; exit 1; }
git init
git add .
git commit -m "Kisan Voice: engine, 9 dictionaries, mesh simulation, web demo"
git branch -M main
git remote add origin "$REPO"
git push -u origin main
echo "Pushed. Enable the live demo: repo Settings -> Pages -> Deploy from branch -> main -> /(root)"
