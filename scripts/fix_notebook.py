import json

with open("notebooks/04_train_wandb.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cell = nb["cells"][9]  # ensemble cell
src = "".join(cell["source"])

# Fix 1: replace string concat with os.path.join
old1 = 'Config.REPORTS_DIR / f"confusion_matrix_{ensemble_name}.png"'
new1 = 'os.path.join(Config.REPORTS_DIR, f"confusion_matrix_{ensemble_name}.png")'
src = src.replace(old1, new1)

# Fix 2: fix variable name mismatch
src = src.replace("plt.savefig(cmf_path)", "plt.savefig(cm_path)")
src = src.replace("wandb.Image(cmf_path)", "wandb.Image(cm_path)")

cell["source"] = [src]

with open("notebooks/04_train_wandb.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Fixed.")
