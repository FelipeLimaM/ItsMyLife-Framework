#!/bin/bash

git stash
sudo docker-compose down
cp docker-compose.yml docker-compose1.yml
cp Dockerfile Dockerfile1

git pull origin master
git stash apply

if `diff docker-compose.yml docker-compose1.yml >/dev/null` && `diff Dockerfile Dockerfile1 >/dev/null`  ; then
  echo "OK"
  sudo docker-compose up -d
else
  echo "Restart"
  sudo docker-compose up -d --build
fi

rm docker-compose1.yml
rm Dockerfile1
