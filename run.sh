#!/bin/bash

git pull origin main

docker compose up -d postgres minio

docker compose up -d --build --force-recreate api
