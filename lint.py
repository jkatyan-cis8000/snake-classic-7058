#!/usr/bin/env python3
"""Linter for Snake game source files.

Verifies:
1. All source files live in layer directories under src/
2. Imports respect the forward dependency direction
3. No file exceeds 300 lines
"""

import ast
import os
import sys
from pathlib import Path
from typing import NamedTuple


class LintError(NamedTuple):
    file: str
    line: int
    message: str


# Layer ordering for dependency checking
LAYERS = ["utils", "providers", "types", "config", "repo", "service", "runtime", "ui"]

# Valid import per layer (layers it may import from)
ALLOWED_IMPORTS = {
    "utils": {"utils"},
    "providers": {"utils", "providers", "types", "config"},
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "service", "providers"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
}

# Root directory
ROOT = Path(__file__).parent


def get_layer(filepath: Path) -> str | None:
    """Get the layer name for a file path, or None if not in a layer."""
    try:
        rel_path = filepath.relative_to(ROOT / "src")
    except ValueError:
        return None

    parts = rel_path.parts
    if len(parts) == 0:
        return None

    layer = parts[0]
    if layer in LAYERS:
        return layer
    return None


def get_imports(filepath: Path) -> list[tuple[str, int]]:
    """Get all imports from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    try:
        tree = ast.parse(content, filename=str(filepath))
    except SyntaxError:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.module, node.lineno))
            elif node.level and node.module:
                # Relative import: from . import foo
                imports.append((node.module, node.lineno))

    return imports


def get_import_module(import_name: str, filepath: Path) -> str:
    """Convert an import to its full module path."""
    # Handle relative imports
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=str(filepath))
    except Exception:
        return import_name

    # Find the ImportFrom node for this import to get relative level
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if import_name in [alias.name for alias in node.names]:
                if node.module:
                    if node.level == 0:
                        return node.module
                    else:
                        # Relative import
                        parts = filepath.relative_to(ROOT / "src").parts[:-1]
                        if node.level - 1 < len(parts):
                            parent = ".".join(parts[: node.level - 1]) if node.level > 1 else ""
                            return f"{parent}.{node.module}" if parent else node.module

    return import_name


def check_imports(filepath: Path, layer: str) -> list[LintError]:
    """Check that imports respect layer dependencies."""
    errors = []
    allowed = ALLOWED_IMPORTS.get(layer, set())

    for import_name, line_no in get_imports(filepath):
        module = get_import_module(import_name, filepath)
        # Get the top-level module
        top_module = module.split(".")[0]

        # Check if this is an internal import (under src/)
        src_path = ROOT / "src" / top_module
        if src_path.exists():
            # Internal import - check layer
            imported_layer = get_layer(src_path)
            if imported_layer and imported_layer not in allowed:
                errors.append(
                    LintError(
                        file=str(filepath.relative_to(ROOT)),
                        line=line_no,
                        message=f"Import '{import_name}' from layer '{imported_layer}' is not allowed in '{layer}'. "
                                f"Layer '{layer}' may only import from: {', '.join(sorted(allowed))}",
                    )
                )

    return errors


def check_file_length(filepath: Path) -> list[LintError]:
    """Check that file doesn't exceed 300 lines."""
    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
        if line_count > 300:
            errors.append(
                LintError(
                    file=str(filepath.relative_to(ROOT)),
                    line=line_count,
                    message=f"File exceeds 300 lines ({line_count} lines)",
                )
            )
    except Exception:
        pass
    return errors


def check_file(filepath: Path) -> list[LintError]:
    """Run all checks on a single file."""
    errors = []

    # Check file length
    errors.extend(check_file_length(filepath))

    # Check layer and imports
    layer = get_layer(filepath)
    if layer is None:
        # File not in a layer directory
        errors.append(
            LintError(
                file=str(filepath.relative_to(ROOT)),
                line=1,
                message=f"File must be inside a layer directory under src/ ({', '.join(LAYERS)})",
            )
        )
    else:
        errors.extend(check_imports(filepath, layer))

    return errors


def main() -> int:
    """Main entry point."""
    all_errors: list[LintError] = []

    # Find all Python files under src/
    src_dir = ROOT / "src"
    for root, _, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(".py"):
                filepath = Path(root) / filename
                all_errors.extend(check_file(filepath))

    # Print errors
    if all_errors:
        print(f"Found {len(all_errors)} lint error(s):\n")
        for error in all_errors:
            print(f"{error.file}:{error.line}: {error.message}")
        return 1

    print("All files passed lint checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
