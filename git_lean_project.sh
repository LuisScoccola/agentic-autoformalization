#!/bin/bash

git --git-dir=/Users/luisscoccola/code/agentic-lean/autoformalization.git \
    --work-tree=/Users/luisscoccola/code/agentic-lean/workspace/lean_project "$@"
