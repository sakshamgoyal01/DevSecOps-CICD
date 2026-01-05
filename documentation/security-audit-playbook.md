# Security Audit Playbook

## Q: How do you prevent secrets from entering Git?

A: Gitleaks scans both locally and in CI. Any detected secret blocks commits
and pipeline execution.

## Q: How is insecure code detected?

A: Semgrep performs SAST using OWASP-aligned and custom security rules.

## Q: How are vulnerable dependencies handled?

A: Trivy scans dependencies and blocks builds if CRITICAL CVEs exist.

## Q: How do you know what is inside deployed images?

A: SBOMs are generated using Syft for every build.

## Q: How is Kubernetes hardened?

A: RBAC, NetworkPolicies, Pod Security Contexts, and config scanning enforce
least privilege and Zero Trust.

## Q: What happens after deployment if an attack occurs?

A: Falco detects runtime anomalies and generates alerts for incident response.
