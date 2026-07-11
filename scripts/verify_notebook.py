import json, ast, sys

with open("notebooks/04_train_wandb.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

errors = 0
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    try:
        ast.parse(src)
    except SyntaxError as e:
        print(f"Cell {i} SYNTAX ERROR: {e}")
        errors += 1

code_cells = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
if errors == 0:
    print(f"All {code_cells} code cells pass syntax check.")
else:
    print(f"{errors}/{code_cells} cells have syntax errors.")
    sys.exit(1)
