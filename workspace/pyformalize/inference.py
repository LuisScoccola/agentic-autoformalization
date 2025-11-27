import asyncio
import aristotlelib
import subprocess
import os
import tempfile


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


def inference_claude(prompt_text):
    # Save to temporary file created in current path and set prompt_file to that file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, dir="/workspace/tmp"
    ) as tmp:
        tmp.write(prompt_text)
        prompt_file = tmp.name

    command = f"claude --dangerously-skip-permissions --print 'Follow the prompt in {prompt_file}.'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    os.remove(prompt_file)

    return result.stdout


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


# Not used. For our purposes, Claude works better.
def inference_deepseek_ocr(input_file, output_file):
    url = "https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference"

    # Build the curl command
    cmd = ["curl", "-X", "POST", url, "-F", f"file=@{input_file}"]

    # Run curl and redirect stdout to output file
    with open(output_file, "w") as out:
        subprocess.run(cmd, stdout=out, check=True)
