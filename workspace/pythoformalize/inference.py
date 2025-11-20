import asyncio
import aristotlelib
import subprocess
import os


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


# def inference_claude(prompt_file):
#    command = f"claude --dangerously-skip-permissions --print 'Follow the prompt in {prompt_file}.'"
#    process = subprocess.Popen(
#        command,
#        shell=True,
#        stdout=subprocess.PIPE,
#        stderr=subprocess.STDOUT,
#        text=True
#    )
#
#    # Stream output line-by-line
#    for line in process.stdout:
#        print(line, end="")  # print as it arrives
#
#    process.wait()


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
