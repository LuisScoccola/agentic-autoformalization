# Agentic Autoformalization


This repository contains a Docker file and Python code implementing agentic approaches to autoformalization of math in Lean 4.
The goal is to try out different approaches and to play around with existing models.
Docker is used to isolate the agents from the rest of the system, so that they can be given complete freedom to edit files and run other commands.

> [!NOTE]
> This work is exploratory in nature. Everything is subject to change.

> [!WARNING]
> Allowing agents (or any other software) to run commands on your computer is always a security risk. Make sure you understand what you are doing before you do it.

## Installation

You should only need to run the following once.

1. Create directories for Lean project and informal references.
    - Create `./workspace/tmp`
    - Create `./workspace/informal_references`
        - Here you'll put informal math in PDF.
    - Create `./workspace/lean_project`
        - Put the target Lean project here.
        - It's recommended to not have the `.git` files for the project in `workspace` (so that agents don't have access to them).
        This can be done with the same git commands that people use to track their dotfiles, see, eg, [this tutorial](https://www.atlassian.com/git/tutorials/dotfiles).
2. Set up Docker.
    - Build the Docker image `./docker/build.sh`.
    - Create a file `./docker/.env` with API keys such as `ARISTOTLE_API_KEY`.
3. Start the Docker server, build Lean project, log into claude code, install Lean tools, log into gemini-cli.
    - From the root of this repository, run `./docker/serve.sh`.
    - Build lean project.
        - Go to `workspace/lean_project`.
        - Run `lake exe chache get`.
        - Run `lake update`.
        - Run `lake build`.
    - Install [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp).
        - Run `claude mcp add lean-lsp uvx lean-lsp-mcp`.
    - Log into claude code and install Lean 4 skills.
        - From within that session, run `claude` and authenticate.
        - Follow installation instructions for Lean 4 skills [here](https://github.com/cameronfreer/lean4-skills/blob/main/INSTALLATION.md).
    - Log into gemini-cli.
        - Run `gemini` and authenticate.
    - Close the session.

## Usage

From the root of this repository, run `./docker/run.sh`, and use the `pyformalize` Python package as in `workspace/example.py`.

## License

This software is published under the 3-clause BSD license.
