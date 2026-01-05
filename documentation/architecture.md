# System Architecture

## High-Level Architecture

User Traffic
→ Ingress Controller
→ Frontend Service
→ Backend API
→ PostgreSQL Database

## Kubernetes Design

- Dedicated namespace per environment
- Stateless frontend & backend
- Stateful database with PV/PVC
- Internal service-to-service communication
- External access only via Ingress

## Control Plane Responsibilities

- API Server: Validates manifests
- Scheduler: Assigns pods to worker nodes
- Controller Manager: Maintains desired state
- etcd: Stores cluster state

## Worker Node Responsibilities

- Run application pods
- Enforce network policies
- Apply pod security constraints

## Security Design Principle

No component trusts another implicitly.
Every interaction is explicitly allowed.
