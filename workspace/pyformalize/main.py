from agents import PdfMdConverter, SkeletonFormalizer, SorryFiller, BlueprintBuilder
from blueprint import parse_blueprint_from_file


def pipeline(
    workspace=None,
    pdf=None,
    md=None,
    blueprint=None,
    lean_project=None,
    skeleton_formalization_file=None,
    formalization_file=None,
    convert=False,
    build_blueprint=False,
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

    if build_blueprint:
        if verbose:
            print("Building blueprint...")
        blueprint_builder = BlueprintBuilder(workspace)
        blueprint_builder.build(md, blueprint, log=log)

    to_formalize = parse_blueprint_from_file()

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

    return log


workspace = "/workspace"
pdf = "informal_references/KrullSchmidt.pdf"
md = "informal_references/KrullSchmidt.md"
blueprint = "informal_references/KrullSchmidt_blueprint.md"
lean_project = "lean_project/"
skeleton_formalization_file = "Autoformalization/KrullSchmidtSkeleton.lean"
formalization_file = "Autoformalization/KrullSchmidt.lean"

# log = pipeline(
#   workspace=workspace,
#   pdf=pdf,
#   md=md,
#   lean_project=lean_project,
#   skeleton_formalization_file=skeleton_formalization_file,
#   formalization_file=formalization_file,
#   convert=True,
#   formalize_skeleton=True,
#   fill_sorry=True,
#   verbose=True,
# )
#
# for log_entry in log:
#   print(log_entry)
