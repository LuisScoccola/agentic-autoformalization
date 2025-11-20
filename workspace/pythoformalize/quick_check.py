import asyncio
from formal_proof_agent import (
    inference_claude,
    skeleton_formalization_query,
    inference_aristotle,
)

tmp_file = "./workspace/tmp/prompt.txt"

query = skeleton_formalization_query("informal_references/RTAA-1-1.pdf", "lean_project", "RTAA-1-1.lean")
with open(tmp_file, "w") as text_file:
    text_file.write(query)

inference_claude(tmp_file)

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
