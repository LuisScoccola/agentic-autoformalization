import asyncio
from inference import (
    inference_claude,
    inference_aristotle,
)
from prompts import prompt_skeleton_formalization, prompt_pdf_to_md

location_pdf = "/workspace/informal_references/" + "krull-schmidt.pdf"
location_output_md_file = "/workspace/informal_references/" + "krull-schmidt.md"

location_of_lean_project = "/workspace/lean_project/"
formalization_file = "Autoformalization/krull-schmidt.lean"

output_lean_file_path  = "Autoformalization/krull-schmidt-aristotle.lean"

# 1. Convert PDF to Markdown
if False:
    prompt = prompt_pdf_to_md(location_pdf, location_output_md_file)
    out = inference_claude(prompt)
    print(out)

# 2. Formalize with sorry
if False:
    location_of_informal_result = location_output_md_file

    prompt = prompt_skeleton_formalization(
        location_of_informal_result, location_of_lean_project, formalization_file
    )
    out = inference_claude(prompt)
    print(out)

# 3. Fill in sorry
if True:

    asyncio.run(
       inference_aristotle(
           location_of_lean_project,
           input_lean_file_path=formalization_file,
           output_lean_file_path=output_lean_file_path,
       )
    )
