from dotenv import load_dotenv
import os
import asyncio
import aristotlelib
import subprocess
import os


def load_aristotle_API_key():
    load_dotenv()
    _ = os.getenv("ARISTOTLE_API_KEY")

async def inference_aristotle(
    lean_project_path,
    input_lean_content=None,
    input_lean_file_path=None,
    context_lean_file_paths=None,
    output_lean_file_path=None,
):
    poll_every = 10
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


def inference_claude(prompt_file):
    command = f"claude --dangerously-skip-permissions --print 'Follow the prompt in {prompt_file}.'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def skeleton_formalization_query(
    location_of_informal_result, location_of_lean_project, formalization_file
):

    query = f"""- I am using Lean 4 to formalize mathematics.
- I am doing so in the Lean project at {location_of_lean_project}.
- Formalize all the definitions and statements of results in {location_of_informal_result}. Have one result/definition per result/definition there.
- Do this in a new file {formalization_file} inside the Lean project folder.
- Do not attempt to formalize proofs; instead, just use Lean's keyword sorry.
- Use the mathlib library, so do not formalize anything that has already been formalized there.
- Make sure that the project compiles, and iterate looking at the error messages if necessary.
"""

    return query


def build_query_informal_agent(
    result_name, location_of_informal_result, location_of_partial_progress=None
):
    query = f"""
    I need you to help me formalize a mathematical result in Lean 4.
    The result is "{result_name}".
    The statement of the result can be found in the following document: {location_of_informal_result}.

    This is what I want you to do:
        - Formalize the statement of the result.
        - Do not attempt to formalize the proof of the statements, instead, use the Lean 4 keyword "sorry" for proofs.
        - Use mathlib, which is a Lean 4 library that already contains many definitions and results. The library mathlib can be found here: https://github.com/leanprover-community/mathlib4. Make sure any imports you make are compatible with the library structure.
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

    append = ""
    if location_of_partial_progress:
        append = """
    Also, this result is part of a larger project, which I have started formalizing already.

    Use the following Lean 4 code as a starting point. Do not delete or modify anything in the code, just add any mathlib library imports you may need, and append the formalized result statement that I asked for above.

    LEAN 4 file with partial progress:
    """
        with open(location_of_partial_progress, "r") as f:
            lines = f.readlines()
            for l in lines:
                append += l

    return query + append





def inference_gemini(prompt, pro=True, client=None):
    from google import genai

    model_name = "gemini-2.5-pro" if pro else "gemini-2.5-flash"
    if not client:
        client = genai.Client()
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return response.text
#    _ = os.getenv("GEMINI_API_KEY")
