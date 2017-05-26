eval "$(ssh-agent -s)" # Start the ssh agent
echo "$PROD_KEY" > prod_key.pem
chmod 600 prod_key.pem # This key should have push access
ssh-add prod_key.pem
git remote add deploy $PROD_REPO_URI
git push prod master
