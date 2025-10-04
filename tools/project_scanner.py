# tools/project_scanner.py
import os


def read_directory_structure(root_dir: str) -> str:
    """
    Scans a directory and creates a text-based tree structure.
    Ignores common, noisy directories like node_modules.
    """
    tree = []
    ignore_dirs = {'node_modules', '.git', 'dist', '.vscode', '__pycache__'}

    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to prevent walking into ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}📂 {os.path.basename(root)}/")

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            tree.append(f"{sub_indent}📄 {f}")

    return "\n".join(tree)
