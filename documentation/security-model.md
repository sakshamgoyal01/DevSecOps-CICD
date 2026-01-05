# Security Model – Defense in Depth

## Philosophy

Security is enforced at multiple independent layers so that failure of one control
does not compromise the system.

## Security Layers

| Layer        | Control                           |
| ------------ | --------------------------------- |
| Secrets      | Gitleaks                          |
| Source Code  | Semgrep                           |
| Dependencies | Trivy FS                          |
| Containers   | Trivy Image                       |
| Kubernetes   | Trivy Config, RBAC, NetworkPolicy |
| Runtime      | Falco                             |

## Policy Enforcement

- CRITICAL issues block deployment
- Policies are version-controlled
- No manual overrides in production

## Secret Handling

- Secrets never stored in Git
- Injected at runtime only
- Protected via Kubernetes RBAC
