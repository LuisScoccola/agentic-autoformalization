from dotenv import load_dotenv
import os
from google import genai
import asyncio
import aristotlelib
from pathlib import Path


def load_API_keys():
    load_dotenv()
    _ = os.getenv("GEMINI_API_KEY")
    _ = os.getenv("ARISTOTLE_API_KEY")


def inference_gemini(prompt, pro=True):
    model_name = "gemini-2.5-pro" if pro else "gemini-2.5-flash"
    if not client:
        client = genai.Client()
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return response.text


async def inference_aristotle(
    lean_project_path,
    input_lean_content=None,
    input_lean_file_path=None,
    context_lean_file_paths=None,
    output_lean_file_path=None,
):
    poll_every = 5
    # Create a new project
    project = await aristotlelib.Project.create()
    print(f"Created project: {project.project_id}")

    if context_lean_file_paths:
        # Add context files
        await project.add_context(
            [
                lean_project_path + lean_file_path
                for lean_file_path in context_lean_file_paths
            ]
        )

    assert input_lean_content or input_lean_file_path
    # Solve with input content
    if input_lean_content:
        await project.solve(input_content=input_lean_content)
    else:
        await project.solve(input_file_path=lean_project_path + input_lean_file_path)

    # Wait for completion and get solution
    while project.status not in [
        aristotlelib.ProjectStatus.COMPLETE,
        aristotlelib.ProjectStatus.FAILED,
    ]:
        await asyncio.sleep(poll_every)
        await project.refresh()
        print(f"Status: {project.status}")

    if project.status == aristotlelib.ProjectStatus.COMPLETE:
        if not output_lean_file_path:
            output_lean_file_path = "OutputAristotle.lean"
        solution_path = await project.get_solution(
            output_path=lean_project_path + output_lean_file_path
        )
        print(f"Solution saved to: {solution_path}")


def build_query_informal_agent(result_name, location_of_informal_result):
    return f"""
    I need you to help me formalize a mathematical result in Lean 4.
    The result is "{result_name}".
    The statement of the result can be found in the following document: {location_of_informal_result}.

    This is what I want you to do:
        - Formalize the statement of the result and the statements of any other results you deem necessary.
        - Do not attempt to formalize the proof of the statements, instead, use the Lean 4 keyword "sorry" for proofs.
        - Use mathlib, which is a Lean 4 library that already contains many definitions and results. The library mathlib can be found here: https://github.com/leanprover-community/mathlib4
        - The statements should looks as follows:
    ```
    /--
      [Informal description of the statement, which should be filled in by you]

      PROVIDED SOLUTION:
      [Informal proof of the statement, which can be taken from the document and which should be filled in by you]
    -/
    theorem ResultName [Formal statement of the result, which should be filled in by you] := by sorry
    ```
    """
