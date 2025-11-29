import re

def parse_blueprint(raw):
    result = []

    # Regex for definitions
    def_pattern = re.compile(r"<DEFINITION>(.*?)<ENDDEFINITION>", re.DOTALL)
    for match in def_pattern.finditer(raw):
        content = match.group(1).strip()
        result.append(("DEFINITION", content))

    # Regex for theorems with optional proof
    theorem_pattern = re.compile(
        r"<THEOREM>(.*?)<PROOF>(.*?)<ENDTHEOREM>", re.DOTALL
    )
    for match in theorem_pattern.finditer(raw):
        statement = match.group(1).strip()
        proof = match.group(2).strip()
        result.append(("THEOREM", (statement, proof)))

    # Optional: sort by original order in text
    combined_matches = []
    for m in def_pattern.finditer(raw):
        combined_matches.append((m.start(), ("DEFINITION", m.group(1).strip())))
    for m in theorem_pattern.finditer(raw):
        combined_matches.append((m.start(), ("THEOREM", (m.group(1).strip(), m.group(2).strip()))))
    
    combined_matches.sort(key=lambda x: x[0])
    return [item for _, item in combined_matches]


def parse_blueprint_from_file(file):
    with open(file, "rb") as f:
        raw = f.read()
    return parse_blueprint(raw)
