from pyformalize import Formalizer

workspace = "/workspace"
filename = "KrullSchmidt"
lean_project_name = "Autoformalization"

formalizer = Formalizer(workspace, lean_project_name)
log = formalizer.formalize(filename, verbose=True)

print(log)

for log_entry in log:
    print(log_entry)
