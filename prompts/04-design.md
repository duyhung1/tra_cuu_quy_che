# Chặng 3 — Design: tham số chạy prompt

| Mục | Giá trị |
|---|---|
| Prompt SAD | `sdlc-kit/design/SAD_Prompt_IEEE_standard.md` v2.0 → `docs/04-design/SAD.md`, `docs/04-design/adr/` |
| Prompt blueprint | `sdlc-kit/design/bluePrint_design_prompt.md` v2.0 → `docs/04-design/blueprint.md` |
| Prompt sơ đồ | `sdlc-kit/design/componentDiagram_prompt.md`, `sequenceDiagram_prompt.md` v2.0 → `docs/04-design/diagrams/*.drawio` |
| Checklist | `design/SAD_IEEE_1016_Checklist.xlsx` → `sad-audit.md`; `design/BluePrint_Design_IEEE_1016_2009_Checklist.xlsx` → `blueprint-audit.md` |
| Đầu vào | `docs/03-analysis/*` v1.0 (`analysis-v1`), `docs/02-requirements/BRD.md` (`requirements-v1`), `docs/03-analysis/decisions/SRC-006.md` |

```yaml
SYSTEM_NAME: "Tra cứu quy chế (TCQC)"
SAD_DOCUMENT_ID: "TCQC-SAD"
SAD_VERSION: "0.1"
SAD_OWNER: "Phùng Duy Hùng, PO (kiêm Tech Lead)"
SAD_APPROVERS: "Phùng Duy Hùng, PO"
ARCHITECTURE_STYLE: "Modular monolith, ports & adapters"
DEPLOYMENT_TARGET: "Một máy chủ nội bộ (capstone: máy cục bộ Windows)"
MINIMUM_ADRS: 4
OUTPUT_LANGUAGE: "Vietnamese"
SAD_OUTPUT_PATH: "docs/04-design/SAD.md"
ADR_DIR: "docs/04-design/adr"
