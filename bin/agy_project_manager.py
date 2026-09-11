"""
Antigravity Project Settings & Autopilot Manager
Allows programmatic inspection and modification of Antigravity project-level settings
(e.g., auto-execution policies, file access, permission grants) with explicit security checks.
"""

import sys
import os
import json
import urllib.parse
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

DEFAULT_CONFIG_DIR = Path.home() / ".gemini" / "config"
PROJECTS_DIR = DEFAULT_CONFIG_DIR / "projects"

COMMON_DEV_PERMISSIONS = [
    "command(git status)",
    "command(git diff*)",
    "command(git log*)",
    "command(git branch*)",
    "command(git add*)",
    "command(git commit*)",
    "command(pytest*)",
    "command(python -m pytest*)",
    "command(python -m unittest*)",
    "command(npm test*)",
    "command(npm run*)",
    "command(node*)",
    "command(cargo test*)",
    "command(cargo check*)"
]


def find_project_for_directory(workspace_path: Path) -> Tuple[Optional[Path], Optional[Dict[str, Any]]]:
    """
    Finds the project JSON config corresponding to the given workspace directory.
    """
    if not PROJECTS_DIR.exists():
        return None, None

    norm_target = os.path.normpath(str(workspace_path.resolve())).lower()

    for pfile in PROJECTS_DIR.glob("*.json"):
        try:
            with open(pfile, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            resources = data.get("projectResources", {}).get("resources", [])
            for res in resources:
                uri = res.get("folderUri") or res.get("gitFolder", {}).get("folderUri")
                if uri and uri.startswith("file:///"):
                    raw_path = uri[8:]
                    unquoted = urllib.parse.unquote(raw_path)
                    if unquoted.startswith("/") and len(unquoted) > 2 and unquoted[2] == ":":
                        unquoted = unquoted[1:]
                    norm_uri = os.path.normpath(unquoted).lower()
                    if norm_uri == norm_target:
                        return pfile, data
        except Exception:
            continue

    return None, None


def show_status(project_file: Path, project_data: Dict[str, Any]):
    name = project_data.get("name", "Unknown")
    pid = project_data.get("id", "Unknown")
    settings = project_data.get("settings", {})
    auto_exec = settings.get("autoExecutionPolicy", "Not configured (Prompts on every command)")
    file_access = settings.get("fileAccessPolicy", "Not configured (Default)")
    sandbox = settings.get("sandboxMode", "False (Disabled)")
    grants = project_data.get("permissionGrants", {}).get("permissionGrants", {}).get("allow", [])

    print("\n========================================================")
    print(f"  ANTIGRAVITY PROJECT: {name}")
    print("========================================================")
    print(f"Project ID        : {pid}")
    print(f"Config Path       : {project_file}")
    print(f"Auto-Execution    : {auto_exec}")
    print(f"File Access Policy: {file_access}")
    print(f"Sandbox Mode      : {sandbox}")
    print(f"Allowed Commands  : {len(grants)} pre-approved patterns")
    print("========================================================\n")


def enable_autopilot(project_file: Path, project_data: Dict[str, Any], force: bool = False):
    print("\n" + "!" * 58)
    print("  SECURITY NOTICE: ENABLING AUTOPILOT (EAGER EXECUTION)")
    print("!" * 58)
    print("This mode enables the agent to execute shell commands and file")
    print("operations in this workspace without interrupting you for manual")
    print("permission on every single step.\n")
    print("Changes that will be applied to this project:")
    print("  [+] autoExecutionPolicy -> CASCADE_COMMANDS_AUTO_EXECUTION_EAGER")
    print("  [+] fileAccessPolicy    -> AGENT_SETTING_POLICY_ALLOW")
    print("  [+] permissionGrants    -> Common git, python/pytest, npm commands")
    print("!" * 58 + "\n")

    if not force:
        confirm = input("Do you grant full action permission for this project? (y/N): ").strip().lower()
        if confirm != "y":
            print("Operation cancelled. Settings were NOT changed.")
            return

    settings = project_data.setdefault("settings", {})
    settings["autoExecutionPolicy"] = "CASCADE_COMMANDS_AUTO_EXECUTION_EAGER"
    settings["fileAccessPolicy"] = "AGENT_SETTING_POLICY_ALLOW"

    perm_dict = project_data.setdefault("permissionGrants", {}).setdefault("permissionGrants", {})
    existing_allows = set(perm_dict.get("allow", []))
    for p in COMMON_DEV_PERMISSIONS:
        existing_allows.add(p)
    perm_dict["allow"] = sorted(list(existing_allows))

    with open(project_file, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2)

    print("[SUCCESS] Project autopilot mode enabled.")
    print("The agent can now execute full implementation plans autonomously in this project.\n")


def disable_autopilot(project_file: Path, project_data: Dict[str, Any]):
    settings = project_data.setdefault("settings", {})
    settings["autoExecutionPolicy"] = "CASCADE_COMMANDS_AUTO_EXECUTION_NEVER"

    with open(project_file, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2)

    print("[SUCCESS] Project autopilot mode disabled.")
    print("Agent command execution will now require explicit confirmation.\n")


def main():
    parser = argparse.ArgumentParser(description="Antigravity Project Settings & Autopilot Manager")
    parser.add_argument("--dir", default=".", help="Workspace directory (default: current directory)")
    parser.add_argument("--status", action="store_true", help="Show current project settings")
    parser.add_argument("--enable-autopilot", action="store_true", help="Enable eager execution for autonomous workflow")
    parser.add_argument("--disable-autopilot", action="store_true", help="Revert to prompt-for-review mode")
    parser.add_argument("--yes", "-y", action="store_true", help="Bypass interactive security confirmation")
    args = parser.parse_args()

    target_dir = Path(args.dir).resolve()
    pfile, pdata = find_project_for_directory(target_dir)

    if not pfile or not pdata:
        print(f"Error: No Antigravity project found matching directory: {target_dir}", file=sys.stderr)
        print("Please ensure this project is opened or registered in Antigravity.", file=sys.stderr)
        sys.exit(1)

    if args.enable_autopilot:
        enable_autopilot(pfile, pdata, force=args.yes)
    elif args.disable_autopilot:
        disable_autopilot(pfile, pdata)
    else:
        show_status(pfile, pdata)


if __name__ == "__main__":
    main()
