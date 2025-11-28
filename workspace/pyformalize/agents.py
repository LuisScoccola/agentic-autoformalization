from pathlib import Path
import asyncio
from inference import (
    inference_claude,
    inference_aristotle,
)


class Agent:
    def __init__(self, location_workspace):
        self._location_workspace = Path(location_workspace)


class PdfMdConverter(Agent):

    def convert(self, pdf, md, log=None):
        location_pdf = self._location_workspace / Path(pdf)
        location_md = self._location_workspace / Path(md)
        prompt = self._prompt_pdf_to_md(location_pdf, location_md)
        out = inference_claude(prompt)
        if log:
            out = "==== PdfMdConverter ====\n" + out
            log.append(out)

    @staticmethod
    def _prompt_pdf_to_md(
        location_pdf,
        location_output_md,
    ):
        template_path: str = "./prompts/pdf_to_md.txt"
        template_text = Path(template_path).read_text()

        return template_text.format(
            location_pdf=str(location_pdf),
            location_output_md=str(location_output_md),
        )


class SkeletonFormalizer(Agent):

    def formalize(
        self,
        informal_result,
        lean_project,
        skeleton_formalization,
        log=None,
    ):

        location_of_informal_result = self._location_workspace / Path(informal_result)
        location_of_lean_project = self._location_workspace / Path(lean_project)
        location_formalization_file = location_of_lean_project / Path(skeleton_formalization)

        prompt = self._prompt_skeleton_formalization(
            str(location_of_informal_result),
            str(location_of_lean_project),
            str(location_formalization_file),
        )
        out = inference_claude(prompt)
        if log:
            out = "==== SkeletonFormalizer ====\n" + out
            log.append(out)

    @staticmethod
    def _prompt_skeleton_formalization(
        location_of_informal_result: str,
        location_of_lean_project: str,
        formalization_file: str,
    ) -> str:
        header_path: str = "./prompts/header.txt"
        template_path: str = "./prompts/skeleton_formalization.txt"
        header_text = Path(header_path).read_text()
        template_text = Path(template_path).read_text()

        return header_text + template_text.format(
            location_of_informal_result=location_of_informal_result,
            location_of_lean_project=location_of_lean_project,
            formalization_file=formalization_file,
        )


class SorryFiller(Agent):

    def fill(
        self,
        skeleton_formalization_file,
        lean_project,
        output_file,
        verbose=False,
        log=None,
    ):

        location_of_lean_project = self._location_workspace / Path(lean_project)
        location_skeleton_formalization_file = location_of_lean_project / Path(skeleton_formalization_file)
        location_output_file = location_of_lean_project / Path(output_file)

        return asyncio.run(
            inference_aristotle(
                str(location_of_lean_project),
                input_lean_file_path=str(location_skeleton_formalization_file),
                output_lean_file_path=str(location_output_file),
                verbose=verbose,
            )
        )
