import asyncio
from formal_proof_agent import inference_claude, inference_aristotle, load_aristotle_API_key


async def main():
    load_aristotle_API_key()

    lean_project_path = "./my_lean_project/MyLeanProject/"

    input_lean_file_path = "TestAristotle.lean"
    output_lean_file_path = "OutputAristotleTest.lean"

    await inference_aristotle(
        lean_project_path,
        input_lean_file_path=input_lean_file_path,
        output_lean_file_path=output_lean_file_path,
    )


if __name__ == "__main__":
    asyncio.run(main())

