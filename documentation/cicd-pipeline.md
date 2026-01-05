# CI/CD Pipeline Design

## Pipeline Trigger

- Pull Requests
- Push to main branch

## Pipeline Stages

1. Secrets scanning (Gitleaks)
2. Static code analysis (Semgrep)
3. Dependency vulnerability scan (Trivy FS)
4. Docker image build
5. Container image scan (Trivy Image)
6. SBOM generation (Syft)
7. Kubernetes configuration scan (Trivy Config)
8. Deployment to Kubernetes

## Security Gates

Deployment occurs only if:

- No secrets detected
- No CRITICAL vulnerabilities found
- Kubernetes configs pass security policy

## Artifacts Produced

- SBOM (SPDX)
- Vulnerability scan reports
- Kubernetes config audit reports
