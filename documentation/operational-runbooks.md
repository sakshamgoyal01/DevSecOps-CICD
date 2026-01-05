# Operational Runbooks

## Secret Rotation

- Update secret in Kubernetes
- Restart affected pods
- No image rebuild required

## Scaling

- Horizontal Pod Autoscaler adjusts replicas
- CPU-based scaling enabled

## Rollback

- Git revert
- Re-run CI/CD
- Kubernetes applies previous known-good state
