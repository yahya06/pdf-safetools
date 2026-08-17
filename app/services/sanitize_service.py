from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import pikepdf

from app.services.pdf_service import _ensure_new_output, validate_pdf
from app.services.scan_service import ScanResult, calculate_sha256, scan_pdf

Preset = Literal["Standard", "JKN Safe Mode", "Custom"]

STANDARD_RULES = frozenset({"javascript", "open_action", "external_uri", "launch", "embedded_file"})
JKN_RULES = frozenset(
    {
        "javascript", "open_action", "additional_actions", "external_uri", "launch",
        "goto_remote", "goto_embedded", "submit_form", "import_data", "embedded_file",
        "rich_media", "movie", "sound", "3d", "external_annotation",
    }
)


@dataclass(frozen=True)
class SanitizeResult:
    output: Path
    original_sha256: str
    output_sha256: str
    is_safe: bool
    scan: ScanResult
    removed: dict[str, int]


def sanitize_pdf(
    source: Path,
    output: Path,
    preset: Preset = "JKN Safe Mode",
    rules: frozenset[str] | set[str] | None = None,
) -> SanitizeResult:
    validate_pdf(source)
    _ensure_new_output(output)
    selected = _rules_for(preset, rules)
    removed = {rule: 0 for rule in selected}
    with pikepdf.Pdf.open(source) as pdf:
        _sanitize_dictionary(pdf.Root, selected, removed)
        for page in pdf.pages:
            if "/Annots" in page:
                existing: Any = page.Annots
                annotations = []
                for annotation in list(existing):
                    if _remove_annotation(annotation, selected, removed):
                        continue
                    annotations.append(annotation)
                if annotations:
                    page.Annots = annotations
                else:
                    page_node: Any = page
                    del page_node["/Annots"]
            _sanitize_dictionary(page, selected, removed)
        pdf.save(output)
    result = scan_pdf(output)
    return SanitizeResult(
        output=output,
        original_sha256=calculate_sha256(source),
        output_sha256=calculate_sha256(output),
        is_safe=not result.findings,
        scan=result,
        removed={key: value for key, value in removed.items() if value},
    )


def _rules_for(preset: Preset, rules: frozenset[str] | set[str] | None) -> frozenset[str]:
    if preset == "Standard":
        return STANDARD_RULES
    if preset == "JKN Safe Mode":
        return JKN_RULES
    if preset == "Custom" and rules is not None:
        return frozenset(rules)
    raise ValueError("Custom sanitization requires rules")


def _sanitize_dictionary(
    value: Any, rules: frozenset[str], removed: dict[str, int]
) -> None:
    keys = {"/OpenAction": "open_action", "/AA": "additional_actions"}
    for key, rule in keys.items():
        if rule in rules and key in value:
            del value[key]
            removed[rule] += 1
    if "/Names" in value:
        names = value.Names
        if "embedded_file" in rules and "/EmbeddedFiles" in names:
            del names["/EmbeddedFiles"]
            removed["embedded_file"] += 1
        if "javascript" in rules and "/JavaScript" in names:
            del names["/JavaScript"]
            removed["javascript"] += 1
    if "javascript" in rules and "/JS" in value:
        del value["/JS"]
        removed["javascript"] += 1


def _remove_annotation(annotation: Any, rules: frozenset[str], removed: dict[str, int]) -> bool:
    if not isinstance(annotation, pikepdf.Dictionary):
        return False
    node: Any = annotation
    action: Any = node.get("/A")
    action_type = str(action.get("/S", "")) if action is not None else ""
    rule = {
        "/JavaScript": "javascript", "/URI": "external_uri", "/Launch": "launch",
        "/GoToR": "goto_remote", "/GoToE": "goto_embedded", "/SubmitForm": "submit_form",
        "/ImportData": "import_data",
    }.get(action_type)
    subtype_rule = {
        "/RichMedia": "rich_media", "/Movie": "movie", "/Sound": "sound", "/3D": "3d",
    }.get(str(node.get("/Subtype", "")))
    target = subtype_rule or rule
    if target and target in rules:
        removed[target] += 1
        return True
    if rule and "external_annotation" in rules:
        removed["external_annotation"] += 1
        return True
    return False
