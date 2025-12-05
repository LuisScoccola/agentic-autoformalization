"""Command-line interface for pyformalize."""

import argparse
from .agents import Formalizer


def main():
    """Main entry point for the pyformalize CLI."""
    parser = argparse.ArgumentParser(
        description="Formalize a file using pyformalize",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("workspace", help="Path to the workspace directory")
    parser.add_argument("filename", help="Name of the file to formalize")
    parser.add_argument("lean_project_name", help="Name of the Lean project")
    parser.add_argument(
        "--semantic-gap-check",
        type=int,
        default=3,
        help="Number of semantic gap checks to perform",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="Enable verbose output",
    )

    args = parser.parse_args()

    formalizer = Formalizer(args.workspace, args.lean_project_name)
    log = formalizer.formalize(
        args.filename,
        check_for_semantic_gap_and_fix=args.semantic_gap_check,
        verbose=args.verbose,
    )

    for log_entry in log:
        print(log_entry)


if __name__ == "__main__":
    main()
