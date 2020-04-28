# Download PHAR file
curl https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o wp-cli.phar

# Grant it execution permission and move it to user's execution path
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp

# Show WP CLI information
wp --info
