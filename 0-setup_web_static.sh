#!/usr/bin/env bash
# sets up web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
ufw allow 'Nginx HTTP'
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

nginx_config="location /hbnb_static {
    alias /data/web_static/current/;
    index index.html;
}"

echo "$nginx_config" | sudo tee /etc/nginx/sites-available/default

sudo service nginx restart

exit 0
