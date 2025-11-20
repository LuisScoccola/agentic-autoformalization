import asyncio
from inference import (
    inference_claude,
    inference_aristotle,
)
from prompts import skeleton_formalization_prompt

tmp_file = "/workspace/tmp/prompt.txt"
location_of_informal_result = "/workspace/informal_references/RTAA-1-1.pdf"
location_of_lean_project = "/workspace/lean_project"
formalization_file = "RTAA-1-1.lean"

query = skeleton_formalization_prompt(
    location_of_informal_result, location_of_lean_project, formalization_file
)

print(query)

#with open(tmp_file, "w") as text_file:
#    text_file.write(query)
#
#inference_claude(tmp_file)

# lean_project_path = "./my_lean_project/MyLeanProject/"
#
# input_lean_file_path = "TestAristotle.lean"
# output_lean_file_path = "OutputAristotleTest.lean"
#
# asyncio.run(
#    inference_aristotle(
#        lean_project_path,
#        input_lean_file_path=input_lean_file_path,
#        output_lean_file_path=output_lean_file_path,
#    )
# )
