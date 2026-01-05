# Kubernetes Design & Controls

## Namespace Isolation

Each application runs in a dedicated namespace to limit blast radius.

## RBAC

- Custom service accounts
- Least privilege roles
- No default service account usage

## Network Policies

- Default deny-all policy
- Explicit allow:
  - Frontend → Backend
  - Backend → Database

## Pod Security

- Non-root containers
- No privilege escalation
- Read-only root filesystem
- Dropped Linux capabilities

## Storage

- PersistentVolume (PV)
- PersistentVolumeClaim (PVC)
- Data survives pod restarts
