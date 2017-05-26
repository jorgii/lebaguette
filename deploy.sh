eval "$(ssh-agent -s)" # Start the ssh agent
chmod 600 .ssh/prod_key # This key should have push access
ssh-add prod_key
git remote add deploy $PROD_REPO_URI
git push prod master
