#!/bin/sh

# Update from backend master branch
git checkout master
git pull origin master

# Update from frontend main branch
cd ../getsentiApp
git pull origin main

# back to ReviewAnalyzer repo
cd ../ReviewAnalyzer

docker-compose build
docker-compose down
docker-compose up -d



