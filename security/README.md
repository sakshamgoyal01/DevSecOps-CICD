# 🔐 Security Audit & Compliance Documentation

This document defines the **security audit commands, tools, and processes** implemented in this project to ensure secure development, prevent secret leakage, and align with **DevSecOps best practices**.

The approach follows a **shift-left security model**, where vulnerabilities and misconfigurations are detected as early as possible in the development lifecycle.

---

## 🛡️ Process 1: Secret Detection using Gitleaks

### 🔍 Purpose

To detect **hard-coded secrets** such as:

- API keys
- Tokens
- Passwords
- Database credentials
- Cloud provider secrets

before code is merged, built, or deployed.

---

### 🧰 Tool Used

**Gitleaks**  
An open-source tool for detecting secrets in Git repositories using configurable rulesets.

---

### 📁 Configuration File

A custom configuration file is used to:

- Control detection rules
- Reduce false positives
- Align scans with project-specific requirements

### ▶️ Security Audit Command (Verbose Mode)

```bash
gitleaks detect \
  --source . \
  --config gitleaks.toml \
  --verbose
```

---

### 🧾 Command Breakdown

| Flag                     | Description                         |
| ------------------------ | ----------------------------------- |
| `detect`                 | Performs a full repository scan     |
| `--source .`             | Scans the current project directory |
| `--config gitleaks.toml` | Uses custom security rules          |
| `--verbose`              | Enables detailed audit output       |

---

### 📤 Output Behavior

- Displays detected secrets with:

  - File path
  - Line number
  - Rule ID

- Returns a **non-zero exit code** if secrets are found
- Suitable for integration with:

  - Pre-commit hooks
  - CI/CD pipelines
  - Security quality gates

---

### ✅ Expected Outcome

- ❌ Build fails if secrets are detected
- ✅ Code proceeds only when repository is clean
- ✅ Developers resolve issues before merge or deployment

---

## 🛡️ Process 2: SAST – Source Code Security using Semgrep

### Why this is done

- Detect insecure coding patterns early
- Identify framework-level risks (Flask, Python)
- Prevent OWASP Top 10 vulnerabilities before build/deploy

---

### Command Used

```bash
semgrep --config=auto src/backend/
```

(Custom rules)

```bash
semgrep --config=security/sast/semgrep-config.yaml src/backend/
```

---

### Outcome

- Initial finding: Flask app exposed on `0.0.0.0`
- Risk reviewed and remediated/accepted for containerized environment
- Final scan result: **0 blocking findings**

✅ Code passed SAST security checks
✅ Safe to proceed to dependency scanning

---

## 🛡️ Process 3: Dependency Vulnerability Scanning (Pre-Build)

### Why this is done

- Detect vulnerable third-party libraries **before image creation**
- Reduce software supply-chain risk
- Enforce “secure-by-default” builds

---

### Backend Dependency Scan

```bash
trivy fs src/backend/ \
  --severity HIGH,CRITICAL \
  --format json \
  -o security/dependencies/reports/trivy-backend-fs.json
```

---

### Frontend Dependency Scan

```bash
trivy fs src/frontend/ \
  --severity HIGH,CRITICAL \
  --format json \
  -o security/dependencies/reports/trivy-frontend-fs.json
```

---

### Outcome

- No HIGH or CRITICAL vulnerabilities detected
- Dependency layer approved for image build
- JSON reports stored for audit

✅ Secure dependencies
✅ Build allowed

---

## 🛡️ Process 4: SBOM Generation (Supply Chain Visibility)

### Why this is done

- Maintain Software Bill of Materials (SBOM)
- Enable license, vulnerability, and compliance audits
- Meet modern security standards (SLSA, SOC2, ISO)

---

### Backend SBOM

```bash
syft src/backend/ -o spdx-json \
  > security/dependencies/reports/sbom-backend.spdx.json
```

---

### Project-Wide SBOM

```bash
syft . -o spdx-json \
  > security/dependencies/reports/sbom-project.spdx.json
```

---

### Outcome

- SPDX-compliant SBOM generated
- Complete visibility of packages and executables
- SBOM artifacts stored for audit and governance

✅ Supply chain transparency achieved
✅ Compliance-ready artifacts available

---

## 📁 Security Artifacts

```
security/dependencies/reports/
├── trivy-backend-fs.json
├── trivy-frontend-fs.json
├── sbom-backend.spdx.json
└── sbom-project.spdx.json
```

---

## 🛡️ Process 5: Kubernetes Security (Platform Hardening)

### Why this is done

- Enforce least privilege (RBAC)
- Prevent lateral movement inside the cluster
- Harden pods at runtime
- Detect insecure Kubernetes configurations
- Produce audit-ready security evidence

---

### 5.1 RBAC – Least Privilege Enforcement

#### Commands / Manifests

ServiceAccount, Role, RoleBinding applied:

```bash
kubectl apply -f rbac/
```

Attach ServiceAccount to backend Deployment:

```yaml
serviceAccountName: backend-sa
```

#### Verification

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:secure-app:backend-sa \
  -n secure-app
```

#### Outcome

- Backend pod can access **only required resources**
- Default service account not used

✅ Least-privilege RBAC enforced

---

### 5.2 Pod Security Context – Runtime Hardening

#### Configuration (in Deployment)

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

#### Verification

```bash
kubectl describe pod <pod> -n secure-app | grep -A5 Security
```

#### Outcome

- Pods run as non-root
- Privilege escalation blocked
- Reduced blast radius on compromise

✅ Runtime pod hardening enforced

---

### 5.3 Network Policies – Zero Trust Inside Cluster

#### Default Deny (Namespace-wide)

```bash
kubectl apply -f network-policy/default-deny.yaml
```

#### Allow Frontend → Backend

```bash
kubectl apply -f network-policy/allow-frontend-to-backend.yaml
```

#### Allow Backend → Database

```bash
kubectl apply -f network-policy/allow-backend-to-db.yaml
```

#### Outcome

- Frontend → DB ❌ blocked
- Backend → DB ✅ allowed
- No unrestricted east–west traffic

✅ Zero Trust networking enforced

---

### 5.4 Kubernetes Configuration Scan (Misconfiguration Detection)

#### Command

```bash
trivy config module-4-kubernetes/ \
  --severity HIGH,CRITICAL \
  --format json \
  -o module-5-security/layer-5-kubernetes/config-scan/trivy-k8s-config.json
```

#### Outcome

- Detects missing limits, probes, privileged pods
- Report stored as audit evidence

✅ Kubernetes manifests validated

---

### 5.5 Policy Enforcement (Blocking Insecure Manifests)

```bash
trivy config module-4-kubernetes/ \
  --severity CRITICAL \
  --exit-code 1
```

#### Outcome

- Exit code `1` → deployment blocked
- Exit code `0` → deployment allowed

✅ Insecure configs prevented from deploying

---

## 🛡️ Process 6: Runtime Security & Threat Detection (Falco)

### Why this is done

- Detect attacks **after deployment**
- Identify malicious runtime behavior
- Generate real-time alerts
- Provide incident response evidence

---

### 6.1 Falco Installation (Kubernetes)

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace
```

#### Verification

```bash
kubectl get pods -n falco
```

Expected:

```
falco-xxxxx   Running
```

✅ Runtime security agent active

---

### 6.2 Runtime Detection – Shell Access

#### Attack Simulation

```bash
kubectl exec -it deploy/backend -n secure-app -- /bin/sh
```

#### Check Alerts

```bash
kubectl logs -n falco -l app=falco | tail
```

#### Outcome

- Falco alert generated: shell execution inside container
- Alert includes pod, namespace, container

✅ Interactive shell access detected

---

### 6.3 Custom Runtime Rules (Enterprise Control)

#### Custom Rule

```yaml
- rule: Write below root in container
  desc: Detect any write to root filesystem
  condition: >
    container and write and fd.name startswith "/"
  output: >
    File write detected (file=%fd.name user=%user.name container=%container.name)
  priority: WARNING
```

Apply rule:

```bash
kubectl create configmap falco-custom-rules \
  --from-file=custom-rules.yaml \
  -n falco

kubectl rollout restart daemonset falco -n falco
```

---

### 6.4 Runtime Tampering Test

```bash
kubectl exec -it deploy/backend -n secure-app -- touch /tmp/hacked.txt
```

#### Outcome

- Falco alert triggered for filesystem tampering
- Alert logged with Kubernetes metadata

✅ Runtime integrity monitoring proven

---
