#!/usr/bin/env python3
"""Build a tenant-specific, Studio-ready copy of DemoInvoiceLoader_V4 from repo-safe sources."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / "deploy.local.json"
PUBLISHED_PROJECT_NAME = "DemoInvoiceLoader_V4"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Missing local config: {CONFIG_PATH}\n"
            f"Create it from {PROJECT_DIR / 'deploy.local.example.json'} first."
        )
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def build_output_dir(config: dict) -> Path:
    configured = config.get("output_dir")
    if configured:
        return Path(configured)
    return PROJECT_DIR / ".deploy" / f"{PUBLISHED_PROJECT_NAME}_{config['tenant_id']}"


def get_preserve_output_paths(config: dict) -> list[str]:
    preserved = config.get("preserve_output_paths", [])
    if not isinstance(preserved, list):
        raise ValueError("preserve_output_paths must be a list of relative paths")
    invalid = [value for value in preserved if not isinstance(value, str) or not value.strip()]
    if invalid:
        raise ValueError("preserve_output_paths contains invalid entries")
    return preserved


def snapshot_preserved_entries(output_dir: Path, preserve_paths: list[str]) -> tuple[Path | None, list[str]]:
    if not output_dir.exists() or not preserve_paths:
        return None, []

    snapshot_root = Path(tempfile.mkdtemp(prefix="demo_invoice_loader_v2_preserve_"))
    captured: list[str] = []

    for relative_path in preserve_paths:
        source_path = output_dir / relative_path
        if not source_path.exists():
            continue

        target_path = snapshot_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if source_path.is_dir():
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)

        captured.append(relative_path)

    if not captured:
        shutil.rmtree(snapshot_root, ignore_errors=True)
        return None, []

    return snapshot_root, captured


def restore_preserved_entries(snapshot_root: Path | None, output_dir: Path, preserve_paths: list[str]) -> list[str]:
    if snapshot_root is None or not preserve_paths:
        return []

    restored: list[str] = []

    for relative_path in preserve_paths:
        snapshot_path = snapshot_root / relative_path
        if not snapshot_path.exists():
            continue

        target_path = output_dir / relative_path
        if not should_restore_preserved_entry(relative_path, snapshot_path, target_path):
            continue

        if target_path.exists():
            if target_path.is_dir():
                shutil.rmtree(target_path)
            else:
                target_path.unlink()

        target_path.parent.mkdir(parents=True, exist_ok=True)
        if snapshot_path.is_dir():
            shutil.copytree(snapshot_path, target_path)
        else:
            shutil.copy2(snapshot_path, target_path)

        restored.append(relative_path)

    return restored


def should_restore_preserved_entry(relative_path: str, snapshot_path: Path, target_path: Path) -> bool:
    if snapshot_path.is_dir() or not target_path.exists() or target_path.is_dir():
        return True

    if Path(relative_path).name != "ExtractOCRData.xaml":
        return True

    snapshot_content = snapshot_path.read_text(encoding="utf-8")
    target_content = target_path.read_text(encoding="utf-8")

    snapshot_has_extract_activity = "ExtractDataActivity" in snapshot_content
    target_has_extract_activity = "ExtractDataActivity" in target_content
    snapshot_has_placeholder = "LIVE_ACTIVITY_PENDING" in snapshot_content
    target_has_placeholder = "LIVE_ACTIVITY_PENDING" in target_content

    if target_has_extract_activity and not snapshot_has_extract_activity:
        return False

    if not target_has_placeholder and snapshot_has_placeholder:
        return False

    return True


def copy_project_tree(output_dir: Path) -> None:
    if output_dir.exists():
        def handle_remove_readonly(func, path, _exc_info):
            os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(output_dir, onerror=handle_remove_readonly)

    def ignore(_src: str, names: list[str]) -> set[str]:
        ignored = {".deploy", "deploy.local.json", "__pycache__"}
        return {name for name in names if name in ignored}

    shutil.copytree(PROJECT_DIR, output_dir, ignore=ignore)


def patch_project_json(output_dir: Path, config: dict) -> None:
    project_json_path = output_dir / "project.json"
    project_data = json.loads(project_json_path.read_text(encoding="utf-8"))

    tenant_metadata = project_data.get("tenantMetadata", [])
    if not tenant_metadata:
        raise ValueError("project.json has no tenantMetadata entries")

    tenant_metadata[0]["tenantId"] = config["tenant_id"]
    tenant_metadata[0]["processId"] = config["process_id"]
    project_data["name"] = PUBLISHED_PROJECT_NAME
    project_data["description"] = "Deterministic V4 invoice automation workflow"
    if config.get("project_version"):
        tenant_metadata[0]["projectVersion"] = config["project_version"]

    for entry in project_data.get("sourceFiles", []):
        entry["filePath"] = str(output_dir)

    project_json_path.write_text(
        json.dumps(project_data, indent=2) + "\n",
        encoding="utf-8",
    )


def replace_activity_attr(content: str, attr_name: str, value: str) -> str:
    pattern = rf'({re.escape(attr_name)}=\")([^\"]*)(\")'
    updated, count = re.subn(
        pattern,
        lambda match: f"{match.group(1)}{value}{match.group(3)}",
        content,
        count=1,
    )
    if count != 1:
        raise ValueError(f"Could not replace Activity attribute {attr_name}")
    return updated


def patch_mainpage(output_dir: Path, config: dict) -> None:
    mainpage_path = output_dir / "MainPage.xaml"
    content = mainpage_path.read_text(encoding="utf-8")

    replacements = {
        "this:Workflow.configurationFolder": config["configuration_folder"],
        "this:Workflow.inputFolderPath": config["input_folder_path"],
        "this:Workflow.tenantURL": config["tenant_url"],
        "this:Workflow.warehouse": config["warehouse"],
        "this:Workflow.terms": config["terms"],
        "this:Workflow.site": config["site"],
        "this:Workflow.recipientUserId": config.get("recipient_user_id", ""),
        "this:Workflow.enableNotifications": str(config.get("enable_notifications", False)),
        "this:Workflow.enableDebugMode": str(config.get("enable_debug_mode", False)),
    }

    for attr_name, value in replacements.items():
        content = replace_activity_attr(content, attr_name, value)

    source_pattern = r'(<Variable x:TypeArguments="x:String" Default=")([^"]*)(" Name="projectPathSource" />)'
    content, count = re.subn(
        source_pattern,
        lambda match: f"{match.group(1)}{str(output_dir)}{match.group(3)}",
        content,
        count=1,
    )
    if count != 1:
        raise ValueError("Could not replace projectPathSource default in MainPage.xaml")

    mainpage_path.write_text(content, encoding="utf-8")


def patch_internal_workflow_defaults(output_dir: Path, config: dict) -> None:
    workflow_files = [
        output_dir / "ProcessDocumentBatch.xaml",
        output_dir / "SingleDocumentController.xaml",
        output_dir / "ExecuteIdoLoad.xaml",
        output_dir / "ExecuteIdoUpdate.xaml",
    ]

    replacements = {
        "YOUR_PROJECT_PATH": str(output_dir),
        "https://mingle-ionapi.inforcloudsuite.com/YOUR_TENANT/": config["tenant_url"],
        "YOUR_SITE": config["site"],
    }

    for workflow_path in workflow_files:
        content = workflow_path.read_text(encoding="utf-8")
        for needle, value in replacements.items():
            content = content.replace(needle, value)
        workflow_path.write_text(content, encoding="utf-8")


def validate_output(output_dir: Path) -> None:
    project_json_path = output_dir / "project.json"
    mainpage_path = output_dir / "MainPage.xaml"

    project_data = json.loads(project_json_path.read_text(encoding="utf-8"))
    source_paths = {entry["filePath"] for entry in project_data.get("sourceFiles", [])}
    if source_paths != {str(output_dir)}:
        raise ValueError("Generated project.json still contains unexpected source file paths")

    mainpage_content = mainpage_path.read_text(encoding="utf-8")
    if "<YOUR_" in mainpage_content or "&lt;YOUR_" in mainpage_content:
        raise ValueError("Generated MainPage.xaml still contains unresolved placeholders")


def main() -> int:
    config = load_config()
    output_dir = build_output_dir(config)
    preserve_paths = get_preserve_output_paths(config)
    snapshot_root, captured_paths = snapshot_preserved_entries(output_dir, preserve_paths)

    try:
        copy_project_tree(output_dir)
        patch_project_json(output_dir, config)
        patch_mainpage(output_dir, config)
        patch_internal_workflow_defaults(output_dir, config)
        restored_paths = restore_preserved_entries(snapshot_root, output_dir, preserve_paths)
        validate_output(output_dir)
    finally:
        if snapshot_root is not None and snapshot_root.exists():
            shutil.rmtree(snapshot_root, ignore_errors=True)

    print(f"Prepared deployable V2 project at: {output_dir}")
    if captured_paths:
        print(f"Captured preserved entries from previous deploy: {', '.join(captured_paths)}")
    if restored_paths:
        print(f"Restored preserved entries into new deploy: {', '.join(restored_paths)}")
    print("Open that generated folder in RPA Studio for tenant-specific deployment/testing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
