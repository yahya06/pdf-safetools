# Security Policy

## Scope

PDF SafeTools is a local Windows desktop application. PDF files are treated as sensitive data and are not uploaded by the application to cloud services, third-party APIs, or online scanners.

The scanner performs static PDF object analysis. It does not execute JavaScript, PDF actions, embedded executables, launches, or external URLs.

## Reporting a Vulnerability

Do not include real patient documents, credentials, malware, or other sensitive data in a report.

Report security issues privately to the project maintainer through the project's GitHub security contact or private maintainer channel. Include:

- A short description of the issue.
- Affected version or commit.
- Reproduction steps using a synthetic or sanitized fixture.
- Expected and actual behavior.
- Security impact.

If private reporting is unavailable, open a public issue without including exploit details or sensitive files and request private follow-up.

## Response

Reports are reviewed as soon as practical. The maintainer may request additional reproduction information, create a regression test, and publish a fix or mitigation.

Do not publicly disclose an issue before a fix or mitigation is available unless coordinated disclosure is agreed with the maintainer.

## Security Limitations

PDF SafeTools does not guarantee that a PDF is malware-free, vulnerability-free, or accepted by a particular external system. Scanning and sanitization cover only the configured PDF structures and rules implemented by the current version.

A result such as `No configured findings detected` means that no configured findings were detected. It does not mean that the file is safe in an absolute sense.

## Supported Versions

This project is under development. Only the latest development version is expected to receive security fixes.
