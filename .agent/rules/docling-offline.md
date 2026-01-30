---
trigger: always_on
---

# Rule: Docling Offline Configuration

- **Artifact Path:** Always set `artifacts_path="./models/docling_artifacts"` when initializing `PdfPipelineOptions`.
- **Environment:** Explicitly set `os.environ["HF_HUB_OFFLINE"] = "1"` in the main entry point.
- **Validation:** Before initializing the `DocumentConverter`, the code must verify that the `artifacts_path` exists on the local disk.