from pathlib import Path


def prompt_pdf_to_md(
    location_pdf : str,
    location_output_md : str,
) -> str :
    template_path: str = "./prompts/pdf_to_md.txt"
    template_text = Path(template_path).read_text()

    return template_text.format(
        location_pdf = location_pdf,
        location_output_md = location_output_md,
    )


def prompt_skeleton_formalization(
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
