#!/bin/bash

docker run -it \
  --hostname agent-container \
  --env-file /Users/luisscoccola/code/agentic-lean/docker/.env \
  -v /Users/luisscoccola/code/agentic-lean/workspace:/workspace \
  -v /Users/luisscoccola/code/agentic-lean/docker/root-directory:/home/agent \
  agent-container
