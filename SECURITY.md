# Security Policy

## Reporting a Vulnerability

Please report security issues to **security@iskra.space** with the subject line `SECURITY DISCLOSURE`. We aim to acknowledge new reports within **48 hours** and provide an initial remediation plan within **5 business days**.

To help us triage efficiently, include:

- A clear description of the vulnerability and potential impact.
- Steps required to reproduce the issue.
- Any logs, payloads, or screenshots that illustrate the problem.
- Suggested mitigations, if available.

Do **not** open public issues for high-risk findings. Use the private channel above.

## Supported Versions

| Version | Supported |
| ------- | --------- |
| `main` (pre-release) | ✅ |
| Tagged releases `vMAJOR.MINOR.PATCH` | ✅ for 6 months after release |
| Deprecated branches | ❌ |

## Remediation Process

1. **Triage** – confirm severity, affected components, and reproduction steps.
2. **Containment** – apply temporary mitigations where possible.
3. **Resolution** – develop and validate a permanent fix, including regression tests.
4. **Disclosure** – publish a security advisory and changelog entry once users can update safely.

## Security Testing

We maintain automated security checks that align with the [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) and the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).

- Red-team prompts live in `security/red_team_cases.jsonl` and are executed via `tools/run_security_checks.py`.
- Policy enforcement layers (`veil.py`, `ethics_*`) must log risk levels and decisions in journal `events`.
- Every pull request must keep these checks green before merging.

## Coordinated Disclosure

If a third party publicly discloses a vulnerability before we can ship a patch, we will:

1. Publish mitigation guidance within 24 hours.
2. Accelerate a patched release and update all downstream mirrors.
3. Credit reporters who follow this policy unless anonymity is requested.

Thank you for helping keep SpaceCoreIskra resilient.
