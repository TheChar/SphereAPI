# SphereAPI
This is an API to give my personal applications access to an internal Postgres database stored on my home-lab server

Spinning up for docker:
pull postgres:latest and start it up on port 5432
cd root directory
docker build -t sphere-api .
start up docker image with env vars, port 8000
docker network apinetwork
docker network connect postgres
docker network connect sphere-api