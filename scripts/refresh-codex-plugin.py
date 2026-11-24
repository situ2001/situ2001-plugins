#!/usr/bin/env python3
"""Install or refresh this checkout's situ2001 plugin in Codex."""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "situ2001"


def run(*command, capture_output=False):
    return subprocess.run(
        command, cwd=ROOT, check=True, text=True, capture_output=capture_output
    ).stdout


def list_plugins(marketplace, *options):
    result = run(
        "codex", "plugin", "list", "--marketplace", marketplace, "--json", *options,
        capture_output=True,
    )
    return json.loads(result)


def configure_marketplace(home, marketplace_path, marketplace):
    plugins = marketplace.setdefault("plugins", [])
    entry = next((plugin for plugin in plugins if plugin["name"] == PLUGIN_NAME), None)
    local_path = home / "plugins" / PLUGIN_NAME

    if entry is not None:
        source = entry["source"]
        if source["source"] != "local":
            sys.exit(f"{PLUGIN_NAME} already has a non-local source in {marketplace_path}.")
        configured_path = home / source["path"]
        if configured_path.resolve() == ROOT:
            return
        if configured_path != local_path:
            sys.exit(f"{PLUGIN_NAME} already points to {configured_path}. Expected {ROOT}.")

    if local_path.resolve() != ROOT:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            local_path.symlink_to(ROOT, target_is_directory=True)
        except FileExistsError:
            sys.exit(f"{local_path} already exists. Expected it to point to {ROOT}.")

    if entry is not None:
        return

    plugins.append(
        {
            "name": PLUGIN_NAME,
            "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }
    )
    destination = marketplace_path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=destination.parent) as temp_dir:
        temporary_path = Path(temp_dir) / destination.name
        temporary_path.write_text(
            json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        temporary_path.replace(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--setup-marketplace", action="store_true",
        help="add this checkout to the personal marketplace before installing",
    )
    parser.add_argument(
        "skills", nargs="*", metavar="SKILL_DIR", help="changed skill directories to validate"
    )
    args = parser.parse_args()

    home = Path.home()
    marketplace_path = home / ".agents/plugins/marketplace.json"
    try:
        manifest = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if not args.setup_marketplace:
            sys.exit(f"No personal marketplace at {marketplace_path}. Run with --setup-marketplace.")
        manifest = {"name": "situ2001-plugins", "interface": {"displayName": "situ2001 Plugins"}}

    marketplace = manifest["name"]
    if args.setup_marketplace:
        configure_marketplace(home, marketplace_path, manifest)

    selector = f"{PLUGIN_NAME}@{marketplace}"
    plugins = list_plugins(marketplace, "--available")
    source = next(
        (
            plugin["source"]
            for plugin in plugins["installed"] + plugins["available"]
            if plugin["pluginId"] == selector
        ),
        None,
    )
    if source is None or source["source"] != "local" or Path(source["path"]).resolve() != ROOT:
        sys.exit(f"{selector} must point to this checkout ({ROOT}). Check --setup-marketplace.")

    run("claude", "plugin", "validate", ".claude-plugin/plugin.json")
    run("claude", "plugin", "validate", ".claude-plugin/marketplace.json")
    validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    for skill in args.skills:
        run(sys.executable, validator, skill)

    run(sys.executable, ROOT / "scripts/refresh-plugin-version.py")
    manifest_path = ROOT / ".codex-plugin/plugin.json"
    version = json.loads(manifest_path.read_text(encoding="utf-8"))["version"]
    run("git", "diff", "--check", "HEAD")

    run("codex", "plugin", "add", selector)
    installed = list_plugins(marketplace)["installed"]
    if not any(
        plugin["pluginId"] == selector and plugin["version"] == version and plugin["enabled"]
        for plugin in installed
    ):
        sys.exit(f"Codex did not report {selector} as enabled at version {version}.")

    print(f"Installed and enabled {selector} {version}. Start a new Codex task to load it.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        if error.stderr:
            print(error.stderr.strip(), file=sys.stderr)
        sys.exit(str(error))
    except (OSError, json.JSONDecodeError) as error:
        sys.exit(str(error))
