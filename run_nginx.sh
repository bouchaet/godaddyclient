docker run -d \
-e GODADDY_KEY=$GODADDY_KEY \
-e GODADDY_SECRET=$GODADDY_SECRET \
-e GODADDY_DOMAIN=$GODADDY_DOMAIN \
--name gdcnginx \
-p 8080:80 \
bouchaet/godaddyclient:nginx
