# Incident Response Plan

## Detection

- Falco detects suspicious runtime behavior
- Alerts include pod, namespace, and container metadata

## Response Flow

Falco Alert
→ Identify affected pod
→ Inspect logs
→ Scale deployment to zero
→ Rotate secrets
→ Rebuild and redeploy

## Forensics

- Container logs
- Kubernetes events
- Image SBOM review
