# Weaviate PoC on GKE – Full Demo Notes

## Why did we start this?
- **Cluster**: A Kubernetes cluster (GKE) gives us infra to deploy apps in scalable way.
- **Vector DB (Weaviate)**: Needed for semantic search. Stores embeddings (vectors) instead of just text.
- **Goal**: Show PoC → Deploy Weaviate + Connect via FastAPI + Enable semantic QnA.

---

## Architecture
1. GKE Cluster (already created).
2. Deploy Weaviate with PVC + ConfigMap + Deployment + Service.
3. Add Transformer service for embeddings (MiniLM model).
4. Create schema (BankNote class with QnA).
5. Insert sample data (ATM PIN reset, overdraft policy).
6. Build FastAPI Search API (insert/get/search).
7. Phase 3 → LiteLLM Gateway to integrate with LLMs.

---

## Step by Step

### 1. PVC (`weaviate-pvc.yaml`)
- Why: Persist Weaviate index data.
- Input: PVC YAML.
- Output: PVC created.

### 2. ConfigMap (`weaviate-configmap.yaml`)
- Why: Pass module settings (vectorizer URL, etc.).
- Input: Env vars YAML.
- Output: Config available in pod.

### 3. Deployment + Service (`weaviate-deployment.yaml`)
- Why: Run Weaviate pods and expose externally.
- Input: Deployment YAML.
- Output: Pod Running + External IP.

### 4. Transformers (`weaviate-transformers.yaml`)
- Why: Model to generate embeddings (MiniLM-L6).
- Input: Deployment + Service.
- Output: Transformers pod + svc.

### 5. Schema (`banknote-schema.json`)
- Why: Define class `BankNote` with `question`, `answer`, vectorizer.
- Input: JSON schema.
- Output: Schema visible via `/v1/schema`.

### 6. Data Insert (curl)
- Why: Add sample QnA.
- Input: curl POST with JSON.
- Output: Object stored.

### 7. FastAPI (`api/main.py`)
- Why: Provide APIs to connect to Weaviate.
- Endpoints:
  - `/` → Health check
  - `/get_all` → Get all objects
  - `/insert` → Insert QnA
  - `/search` → Semantic search

---

## Commands Used
```bash
kubectl apply -f weaviate-pvc.yaml -n weaviate-poc
kubectl apply -f weaviate-configmap.yaml -n weaviate-poc
kubectl apply -f weaviate-deployment.yaml -n weaviate-poc
kubectl apply -f weaviate-transformers.yaml -n weaviate-poc

kubectl get pods -n weaviate-poc
kubectl get svc -n weaviate-poc
```

---

## Troubleshooting
- CrashLoopBackoff → Check logs: `kubectl logs <pod>`
- PVC Forbidden → Adjust storage class.
- nearText error → Add vectorizer in schema.

---

## Phase 3 (Next)
- Deploy LiteLLM Gateway in cluster.
- Configure to connect FastAPI → LiteLLM → Weaviate.
- Finalize pipeline: User query → LLM embedding → Weaviate search → Answer.

---
