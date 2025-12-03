from pathlib import Path
import asyncio
from .external_agents import (
    claude,
    aristotle,
)
import os

PROMPT_DIR = Path(__file__).parent / "prompts"


class Formalizer:
    """
    Coordinates a PDF-to-Lean formalization pipeline.

    Parameters
    ----------
    workspace : str
        Path to a directory containing `informal_references/` and a `lean_project/`.
    lean_project_name : str
        Name of the Lean project subdirectory inside `workspace/lean_project/`.
    """

    def __init__(self, workspace, lean_project_name):
        self._workspace = Path(workspace)
        self._lean_project = (
            self._workspace / Path("lean_project") / Path(lean_project_name)
        )

    def formalize(self, filename, check_for_semantic_gap_and_fix=0, verbose=False):
        """
        Executes the formalization pipeline for the given base filename.
        Returns a log (list of messages) describing the steps performed.
        The pipeline generates intermediate files, and skips steps for which the intermediate files exist.

        Parameters
        ----------
        filename : str
            Base name (without extension) of the reference to formalize.
            It expects a file `informal_references/{filename}.pdf` with the informal math.

        verbose : bool, optional
            If True, print progress information during the process.

        Returns
        -------
        list[str]
            Messages describing the steps executed during formalization.
        """

        workspace = self._workspace
        pdf = workspace / Path("informal_references") / Path(filename + ".pdf")
        md = workspace / Path("informal_references") / Path(filename + ".md")
        # blueprint = "informal_references/KrullSchmidt_blueprint.md"
        lean_project = self._lean_project
        skeleton_formalization_file = lean_project / Path(filename + "Skeleton.lean")
        formalization_file = lean_project / Path(filename + ".lean")

        log = []

        if not os.path.exists(str(md)):
            if verbose:
                print("Converting...")
            converter = PdfMdConverter()
            converter.convert(pdf, md, log=log)
        else:
            if verbose:
                print(str(md), "exists. No need to convert.")

        # if build_blueprint:
        #    if verbose:
        #        print("Building blueprint...")
        #    blueprint_builder = BlueprintBuilder(workspace)
        #    blueprint_builder.build(md, blueprint, log=log)
        # to_formalize = parse_blueprint_from_file()

        if not os.path.exists(str(skeleton_formalization_file)):
            if verbose:
                print("Formalizing skeleton...")
            skeleton_formalizer = SkeletonFormalizer()
            skeleton_formalizer.formalize(
                md, lean_project, skeleton_formalization_file, log=log
            )
        else:
            if verbose:
                print(
                    str(skeleton_formalization_file),
                    "exists. No need to formalize skeleton.",
                )

        if verbose:
            print("Checking for semantic gaps...")

        fix_rounds_left = check_for_semantic_gap_and_fix
        while fix_rounds_left:
            semantic_gap_checker = SemanticGapChecker()
            semantic_gap = semantic_gap_checker.check(
                md, lean_project, skeleton_formalization_file, log=log
            )
            if not semantic_gap:
                break
            semantic_gap_fixer = SemanticGapFixer()
            semantic_gap_fixer.fix(
                md, lean_project, skeleton_formalization_file, log=log
            )
            fix_rounds_left -= 1

        if verbose:
            print("Filling sorry...")
        sorry_filler = SorryFiller()
        sorry_filler.fill(
            skeleton_formalization_file,
            formalization_file,
            verbose=verbose,
            log=log,
        )

        return log


class PdfMdConverter:

    def __init__(self):
        pass

    def convert(self, pdf, md, log=None):
        prompt = self._prompt_pdf_to_md(pdf, md)
        if log:
            log.append("PdfMdConverter")
        return claude(prompt, log=log)

    @staticmethod
    def _prompt_pdf_to_md(
        location_pdf,
        location_output_md,
    ):
        template_path = PROMPT_DIR / "pdf_to_md.txt"
        template_text = Path(template_path).read_text()

        return template_text.format(
            location_pdf=location_pdf,
            location_output_md=location_output_md,
        )


class BlueprintBuilder:

    def __init__(self):
        pass

    def build(
        self,
        informal_result,
        blueprint,
        log=None,
    ):
        prompt = self._prompt_blueprint(
            informal_result,
            blueprint,
        )
        if log:
            log.append("BlueprintBuilder")
        return claude(prompt, log=log)

    @staticmethod
    def _prompt_blueprint(
        location_of_informal_result,
        location_of_blueprint,
    ) -> str:
        template_path = PROMPT_DIR / "create_blueprint.txt"
        template_text = Path(template_path).read_text()

        return template_text.format(
            location_of_informal_result=location_of_informal_result,
            location_of_blueprint=location_of_blueprint,
        )


class SkeletonFormalizer:

    def __init__(self):
        pass

    def formalize(
        self,
        informal_result,
        lean_project,
        skeleton_formalization,
        log=None,
    ):

        prompt = self._prompt_skeleton_formalization(
            informal_result,
            lean_project,
            skeleton_formalization,
        )
        if log:
            log.append("SkeletonFormalizer")
        return claude(prompt, log=log)

    @staticmethod
    def _prompt_skeleton_formalization(
        location_of_informal_result,
        location_of_lean_project,
        formalization_file,
    ):
        header_path = PROMPT_DIR / "header.txt"
        template_path = PROMPT_DIR / "skeleton_formalization.txt"
        header_text = Path(header_path).read_text()
        template_text = Path(template_path).read_text()

        return header_text + template_text.format(
            location_of_informal_result=location_of_informal_result,
            location_of_lean_project=location_of_lean_project,
            formalization_file=formalization_file,
        )


class SemanticGapChecker:

    def __init__(self):
        pass

    def check(
        self,
        informal_result,
        lean_project,
        skeleton_formalization,
        log=None,
    ):

        prompt = self._prompt_semantic_gap_checker(
            informal_result,
            lean_project,
            skeleton_formalization,
        )
        if log:
            log.append("SemanticGapChecker")
        out = claude(prompt, output=True, log=log)
        print(out)
        return out == "1"

    @staticmethod
    def _prompt_semantic_gap_checker(
        location_of_informal_result,
        location_of_lean_project,
        formalization_file,
    ):
        template_path = PROMPT_DIR / "semantic_gap_checker.txt"
        template_text = Path(template_path).read_text()

        return template_text.format(
            location_of_informal_result=location_of_informal_result,
            location_of_lean_project=location_of_lean_project,
            formalization_file=formalization_file,
        )

class SemanticGapFixer:

    def __init__(self):
        pass

    def fix(
        self,
        informal_result,
        lean_project,
        skeleton_formalization,
        log=None,
    ):

        prompt = self._prompt_semantic_gap_fixer(
            informal_result,
            lean_project,
            skeleton_formalization,
        )
        if log:
            log.append("SemanticGapFixer")
        return claude(prompt, log=log)

    @staticmethod
    def _prompt_semantic_gap_fixer(
        location_of_informal_result,
        location_of_lean_project,
        formalization_file,
    ):
        template_path = PROMPT_DIR / "semantic_gap_fixer.txt"
        template_text = Path(template_path).read_text()

        return template_text.format(
            location_of_informal_result=location_of_informal_result,
            location_of_lean_project=location_of_lean_project,
            formalization_file=formalization_file,
        )




class SorryFiller:

    def __init__(self):
        pass

    def fill(
        self,
        skeleton_formalization_file,
        output_file,
        verbose=False,
        log=None,
    ):

        if log:
            log.append("SorryFiller")

        return asyncio.run(
            aristotle(
                input_lean_file_path=skeleton_formalization_file,
                output_lean_file_path=output_file,
                verbose=verbose,
            )
        )
