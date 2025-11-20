#!/bin/bash

docker run -it \
  -v /Users/luisscoccola/code/agentic-lean/workspace:/workspace \
  -v /Users/luisscoccola/code/agentic-lean/docker/root-directory:/home/claude \
  claude-code-lean4 \
