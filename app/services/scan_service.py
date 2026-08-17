import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import pikepdf

from app.services.pdf_service import validate_pdf

Severity = Literal["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
RiskLevel = Literal["SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

DEFAULT_SEVERITIES: dict[str, Severity] = {
    "javascript": "CRITICAL",
    "open_action": "HIGH",
    "additional_actions": "MEDIUM",
    "external_uri": "HIGH",
    "launch": "HIGH",
    "goto_remote": "MEDIUM",
    "goto_embedded": "MEDIUM",
    "embedded_file": "HIGH",
    "submit_form": "MEDIUM",
    "import_data": "MEDIUM",
    "rich_media": "MEDIUM",
    "movie": "MEDIUM",
    "sound": "MEDIUM",
    "3d": "MEDIUM",
    "external_annotation": "HIGH",
}

ACTION_TYPES = {
    "/JavaScript": "javascript",
    "/URI": "external_uri",
    "/Launch": "launch",
    "/GoToR": "goto_remote",
    "/GoToE": "goto_embedded",
    "/SubmitForm": "submit_form",
    "/ImportData": "import_data",
}
MEDIA_SUBTYPES = {
    "/RichMedia": "rich_media",
    "/Movie": "movie",
    "/Sound": "sound",
    "/3D": "3d",
}


@dataclass(frozen=True)
class SecurityFinding:
    type: str
    severity: Severity
    count: int
    description: str
    action: Literal["REMOVE"] = "REMOVE"


@dataclass(frozen=True)
class ScanResult:
    findings: list[SecurityFinding]
    risk_level: RiskLevel
    sha256: str
    status: str


def calculate_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_pdf(
    path: Path, severity_map: Mapping[str, Severity] | None = None
) -> ScanResult:
    validate_pdf(path)
    severities = {**DEFAULT_SEVERITIES, **(severity_map or {})}
    counts = {finding_type: 0 for finding_type in DEFAULT_SEVERITIES}
    with pikepdf.Pdf.open(path) as pdf:
        _scan_object(pdf.Root, counts, set())
    findings = [
        SecurityFinding(finding_type, severities[finding_type], count, _description(finding_type))
        for finding_type, count in counts.items()
        if count
    ]
    return ScanResult(
        findings=findings,
        risk_level=_risk_level(findings),
        sha256=calculate_sha256(path),
        status=(
            "No configured findings detected"
            if not findings
            else "Configured findings detected"
        ),
    )


def _scan_object(
    value: Any, counts: dict[str, int], seen: set[tuple[int, int]]
) -> None:
    if not isinstance(value, (pikepdf.Dictionary, pikepdf.Array)):
        return
    objgen = value.objgen
    if objgen != (0, 0):
        if objgen in seen:
            return
        seen.add(objgen)
    node: Any = value
    if isinstance(node, pikepdf.Array):
        items: Any = node
        for item in items:
            _scan_object(item, counts, seen)
        return
    action_type = str(node.get("/S", ""))
    if action_type in ACTION_TYPES:
        counts[ACTION_TYPES[action_type]] += 1
    subtype = str(node.get("/Subtype", ""))
    if subtype in MEDIA_SUBTYPES:
        counts[MEDIA_SUBTYPES[subtype]] += 1
    if str(node.get("/Type", "")) == "/Annot" and "/A" in node:
        counts["external_annotation"] += 1
    for key, item in node.items():
        key_name = str(key)
        if key_name == "/OpenAction":
            counts["open_action"] += 1
        elif key_name == "/AA":
            counts["additional_actions"] += 1
        elif key_name == "/EmbeddedFiles":
            counts["embedded_file"] += 1
        elif key_name in {"/JavaScript", "/JS"} and action_type != "/JavaScript":
            counts["javascript"] += 1
        _scan_object(item, counts, seen)


def _description(finding_type: str) -> str:
    return {
        "javascript": "JavaScript action or script entry detected",
        "open_action": "OpenAction entry detected",
        "additional_actions": "Additional Actions entry detected",
        "external_uri": "External URI action detected",
        "launch": "Launch action detected",
        "goto_remote": "Remote GoTo action detected",
        "goto_embedded": "Embedded GoTo action detected",
        "embedded_file": "Embedded file entry detected",
        "submit_form": "SubmitForm action detected",
        "import_data": "ImportData action detected",
        "rich_media": "RichMedia annotation detected",
        "movie": "Movie annotation detected",
        "sound": "Sound annotation detected",
        "3d": "3D annotation detected",
        "external_annotation": "External action annotation detected",
    }[finding_type]


def _risk_level(findings: list[SecurityFinding]) -> RiskLevel:
    order: tuple[RiskLevel, ...] = ("CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE")
    finding_severities = {finding.severity for finding in findings}
    return next((level for level in order if level in finding_severities), "SAFE")
