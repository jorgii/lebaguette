eval "$(ssh-agent -s)" # Start the ssh agent
chmod 600 ~/.ssh/prod_rsa # This key should have push access
ssh-add ~/.ssh/prod_rsa
git remote add deploy $PROD_REPO_URI
git push prod master
