from agents import PdfMdConverter, SkeletonFormalizer, SorryFiller


def pipeline(
    workspace=None,
    pdf=None,
    md=None,
    lean_project=None,
    skeleton_formalization_file=None,
    formalization_file=None,
    convert=False,
    formalize_skeleton=False,
    fill_sorry=False,
    verbose=False,
):

    log = []

    if convert:
        if verbose:
            print("Converting...")
        converter = PdfMdConverter(workspace)
        converter.convert(pdf, md, log=log)

    if formalize_skeleton:
        if verbose:
            print("Formalizing skeleton...")
        skeleton_formalizer = SkeletonFormalizer(workspace)
        skeleton_formalizer.formalize(
            md, lean_project, skeleton_formalization_file, log=log
        )

    if fill_sorry:
        if verbose:
            print("Filling sorry...")
        sorry_filler = SorryFiller(workspace)
        sorry_filler.fill(
            skeleton_formalization_file,
            lean_project,
            formalization_file,
            verbose=verbose,
            log=log,
        )


workspace = "/workspace"
pdf = "informal_references/KrullSchmidt.pdf"
md = "informal_references/KrullSchmidt.md"
lean_project = "lean_project/"
skeleton_formalization_file = "Autoformalization/KrullSchmidtSkeleton.lean"
formalization_file = "Autoformalization/KrullSchmidt.lean"

pipeline(
    workspace=workspace,
    pdf=pdf,
    md=md,
    lean_project=lean_project,
    skeleton_formalization_file=skeleton_formalization_file,
    formalization_file=formalization_file,
    convert=True,
    formalize_skeleton=True,
    fill_sorry=True,
    verbose=True,
)
