# Agentic Autoformalization

> [!NOTE]  
> This is work in progress. Everything is subject to change.

This repository essentially contains a Docker file and Python code implementing an agentic approach to autoformalization of math in Lean 4.
Docker is used to isolate the agents from the rest of the system, so that they can be given complete freedom to edit files and run other commands.

## Installation

You should only need to run the following once.

1. Create directories for Lean project and informal references.
    - Create `./workspace/tmp`
    - Create `./workspace/informal_references`
        - Here you'll put informal math in PDF or markdown.
    - Create `./workspace/lean_project`
        - Put the target Lean project here.
        - It's recommended to not have the `.git` files for the project in `workspace` (so that agents don't have access to those).
        This can be done with the same git commands that people use to track their dotfiles, see, eg, [this tutorial](https://www.atlassian.com/git/tutorials/dotfiles).
2. Set up Docker.
    - Build the Docker image `./docker/compile.sh`.
    - Create a file `./docker/.env` with API keys such as `ARISTOTLE_API_KEY`.
3. Start the Docker server and log into Claude code.
    - From the root of this repository, run `./docker/serve.sh`.
    - Build lean project.
        - Go to `workspace/lean_project`.
        - Run `lake exe chache get`.
        - Run `lake update`.
        - Run `lake build`.
    - Install [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp).
        - Run `claude mcp add lean-lsp uvx lean-lsp-mcp`.
    - Log into Claude and install Lean 4 skills.
        - From within that session, run `claude` and authenticate.
        - Follow installation instructions for Lean 4 skills [here](https://github.com/cameronfreer/lean4-skills/blob/main/INSTALLATION.md).
    - Close the session.

## License

This software is published under the 3-clause BSD license.
