
# Installation

TODO: abstract /Users/luisscoccola
TODO: mention .env
TODO: abstract lean version in Docker

You should only need to run the following once.

1. Make directories and put stuff there:
    - `./workspace`
    - `./workspace/informal_references`
    - `./workspace/lean_project`
        - Put the target Lean project here.
        - It's recommended to not have the `.git` files for the project in `workspace`, but rather somewhere else, so that the agents don't have access to those.
    - `./workspace/tmp`
2. Set up Docker
    - `./docker/compile.sh`.
    - Add `.env` to `./docker` with `ARISTOTLE_API_KEY=XXX`
3. Start the Docker server.
    - Run `./docker/serve.sh`.
    - Build lean project.
        - Go to `workspace/lean_project`.
        - Run `lake exe chache get`.
        - Run `lake update`.
        - Run `lake build`.
    - Install lean-lsp-mcp
        - `claude mcp add lean-lsp uvx lean-lsp-mcp`
    - Log in Claude and install Lean 4 skills
        - From within that session, run `claude` and authenticate.
        - Follow installation instructions [here](https://github.com/cameronfreer/lean4-skills/blob/main/INSTALLATION.md).
    - Close the session.
