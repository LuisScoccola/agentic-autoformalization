import asyncio
import aristotlelib
import subprocess
import os
import tempfile
from datetime import datetime


async def aristotle(
    input_lean_content=None,
    input_lean_file_path=None,
    #context_lean_file_paths=None,
    output_lean_file_path=None,
    verbose=False,
):
    poll_every = 20
    # Create a new project
    project = await aristotlelib.Project.create()
    if verbose:
        print(f"Created project: {project.project_id}")

    #if context_lean_file_paths:
    #    # Add context files
    #    await project.add_context(
    #        [
    #            lean_project_path + lean_file_path
    #            for lean_file_path in context_lean_file_paths
    #        ]
    #    )

    assert input_lean_content or input_lean_file_path
    # Solve with input content
    if input_lean_content:
        await project.solve(input_content=input_lean_content)
    else:
        await project.solve(input_file_path=input_lean_file_path)

    # Wait for completion and get solution
    while project.status not in [
        aristotlelib.ProjectStatus.COMPLETE,
        aristotlelib.ProjectStatus.FAILED,
    ]:
        await asyncio.sleep(poll_every)
        await project.refresh()
        now = datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if verbose:
            print(f"{now_string} Status: {project.status}")

    if project.status == aristotlelib.ProjectStatus.COMPLETE:
        if not output_lean_file_path:
            output_lean_file_path = "OutputAristotle.lean"
        solution_path = await project.get_solution(
            output_path=output_lean_file_path
        )
        if verbose:
            print(f"Solution saved to: {solution_path}")


def claude(prompt_text, model="claude-sonnet-4-5", output=False, log=None):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, dir="/workspace/pyformalize/tmp"
    ) as tmp:
        tmp.write(prompt_text)
        prompt_file = tmp.name

    if output:
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".txt", delete=False, dir="/workspace/pyformalize/tmp"
        ) as tmp:
            output_file = tmp.name

    prompt = f"Follow the prompt in {prompt_file}."
    if output:
        prompt += f" If the prompt describes an OUTPUT, write it in {output_file}."

    command = (
        "claude --dangerously-skip-permissions "
        f"--model {model} "
        f"--print '{prompt}'"
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if log:
        log.append(result.stdout)

    os.remove(prompt_file)

    if output:
        with open(output_file, "r", encoding="utf-8") as tmp:
            out = tmp.read()
        os.remove(output_file)
        return out


def gemini(prompt_text, model="gemini-2.5-pro", output=False, log=None):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, dir="/workspace/pyformalize/tmp"
    ) as tmp:
        tmp.write(prompt_text)
        prompt_file = tmp.name

    if output:
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".txt", delete=False, dir="/workspace/pyformalize/tmp"
        ) as tmp:
            output_file = tmp.name

    prompt = f"Follow the prompt in {prompt_file}."
    if output:
        prompt += f" If the prompt describes an OUTPUT, write it in {output_file}."

    command = (
        "gemini --yolo "
        f"--model {model} "
        f"'{prompt}'"
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if log:
        log.append(result.stdout)

    os.remove(prompt_file)

    if output:
        with open(output_file, "r", encoding="utf-8") as tmp:
            out = tmp.read()
        os.remove(output_file)
        return out

