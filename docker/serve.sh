#!/bin/bash

docker run -it \
  --hostname agent-container \
  --env-file ./docker/.env \
  -v ./workspace:/workspace \
  -v ./docker/root-directory:/home/agent \
  agent-container
