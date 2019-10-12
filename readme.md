# GoDaddy API Client

A simple godaddy client proxy

## Prerequisite

Python 3.6

## Environment variables

* GODADDY_KEY : your GoDaddy production key
* GODADDY_SECRET : the secret of your production key
* GODADDY_DOMAIN : your GoDaddy domain

## Getting Started

``` bash
> virtualenv env && . /env/bin/activate
> pip install -r requirements.txt
> python godaddyclient.py
```

## Docker

To build and push an image using the docker cli

``` bash
docker build --tag bouchaet/godaddyclient:latest .
docker push bouchaet/godaddyclient:latest
```

To build and push an arm32v7 image

``` bash
docker build --tag bouchaet/godaddyclient:arm32v7 -f ./arm32v7 .
docker push bouchaet/godaddyclient:arm32v7
```

To build, push and run an image using a nginx proxy

``` bash
docker build --tag bouchaet/godaddyclient:nginx -f ./nginx .
docker push bouchaet/godaddyclient:nginx
docker run -d \
-e GODADDY_KEY=$GODADDY_KEY \
-e GODADDY_SECRET=$GODADDY_SECRET \
-e GODADDY_DOMAIN=$GODADDY_DOMAIN \
--name gdcnginx \
-p 8080:80 \
bouchaet/godaddyclient:nginx
```

To stop and remove a container

``` bash
# stop and remove the container
docker container stop gdcnginx
docker container rm  gdcnginx

# or
docker rm --force gdcnginx
```
