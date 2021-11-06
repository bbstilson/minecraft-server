#! /bin/bash

docker pull hexparrot/mineos
docker volume create mineos

export USER_NAME=${MINEOS_UN}
export USER_PASSWORD=${MINEOS_PW}

docker run -td \
  --name=mineos \
  -p 80:8443 \
  -p 25565:25565 \
  -e USER_NAME=$USER_NAME \
  -e USER_PASSWORD=$USER_PASSWORD \
  -v mineos:/var/games/minecraft \
  --restart=unless-stopped \
  hexparrot/mineos:latest
