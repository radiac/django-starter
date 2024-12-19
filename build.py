#!/usr/bin/env python
"""
Convert src into cookiecutter
"""

import re
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "Starter"
COOKIE_NAME = "{{ cookiecutter.project_name }}"
SOURCE_SLUG = "starter"
COOKIE_SLUG = "{{ cookiecutter.project_slug }}"
COOKIE_ROOT = "{{ cookiecutter.root_dir }}"

ignore_patterns = [
    r"/__pycache__/",
    r"/compose.yaml",
]

changelog = Path("CHANGELOG.rst").read_text()
if m := re.search(r"\n(\d+\.\d+\.\d+)", changelog):
    version = m.group(1)
else:
    raise ValueError("Could not find version in changelog")


def copy_dir(src_root: Path, dst_root: Path):
    paths: list[Path] = [src_root]
    while paths:
        parent = paths.pop(0)
        for src_path in parent.iterdir():
            # Skip ignored files
            if any(re.search(pattern, str(src_path)) for pattern in ignore_patterns):
                continue

            # Translate src to dst
            rel_path = src_path.relative_to(src_root)
            dst_path = dst_root / rel_path
            dst_path = Path(
                *[
                    part if part != SOURCE_SLUG else COOKIE_SLUG
                    for part in dst_path.parts
                ]
            )

            if src_path.is_file():
                print(
                    "[file]"
                    f" {src_path.relative_to(src_root)}"
                    f" -> {dst_path.relative_to(dst_root)}"
                )

                src = src_path.read_text()
                src = src.replace(SOURCE_NAME, COOKIE_NAME)
                src = src.replace(SOURCE_SLUG, COOKIE_SLUG)
                if src_path.suffix in [".html", ".jinja2"]:
                    src = f"{{% raw %}}{src}{{%- endraw %}}"
                    for cookie_pattern in [
                        "{{ cookiecutter.project_name }}",
                        "{{ cookiecutter.project_slug }}",
                    ]:
                        if cookie_pattern in src:
                            src = f"{{%- endraw %}}{cookie_pattern}{{% raw %}}".join(
                                src.split(cookie_pattern)
                            )

                if str(rel_path) == "cookiecutter.json":
                    src = src.replace("\n}", f',\n  "_version": "{version}"\n}}')
                dst_path.write_text(src)
                dst_path.chmod(src_path.stat().st_mode)

            elif src_path.is_dir():
                # Create dst dir and mark src to look at later
                print(
                    " [dir]"
                    f" {src_path.relative_to(src_root)}"
                    f" -> {dst_path.relative_to(dst_root)}"
                )
                dst_path.mkdir(exist_ok=True)
                paths.append(src_path)


def build(src_root: Path, config_root: Path, cookiecutter_root: Path):
    cookiecutter_root.mkdir(exist_ok=False)
    project_root = cookiecutter_root / COOKIE_ROOT
    project_root.mkdir()
    print("Copying config...")
    copy_dir(config_root, cookiecutter_root)
    print("Copying source...")
    copy_dir(src_root, project_root)
    print("Cookiecutter generated.")


def run():
    src_root = Path("src").resolve()
    config_root = Path("config").resolve()
    cookiecutter_root = Path("cookiecutter").resolve()
    print(f"Source: {src_root}")
    print(f"Config: {config_root}")
    print(f"Cookiecutter: {cookiecutter_root}")

    # Error if src or config not found
    if not src_root.exists():
        print("Source path not found")
        sys.exit(1)
    if not config_root.exists():
        print("Config path not found")
        sys.exit(1)

    # Clean out cookiecutter, if --delete
    if cookiecutter_root.exists() and len(sys.argv) == 2 and sys.argv[1] == "--delete":
        shutil.rmtree(cookiecutter_root)

    # Build new
    build(src_root, config_root, cookiecutter_root)


if __name__ == "__main__":
    run()
