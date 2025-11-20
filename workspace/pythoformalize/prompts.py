from pathlib import Path

def skeleton_formalization_prompt(
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


#### Old
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

