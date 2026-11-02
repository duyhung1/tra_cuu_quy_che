# Traceability — BO → BR → FR/NFR → US

| Mục | Giá trị |
|---|---|
| Version | 0.2 |
| Owner | Phùng Duy Hùng (PO) |
| Date | 2026-11-02 |
| Nguồn | BRD v1.0 (`requirements-v1`), PRD v0.1, USER_STORIES v0.1 |
| Chiều xuống tiếp theo | US/AC → TC → evidence: `docs/07-verification/RTM.md` |

| BO | BR | FR / NFR | US | Design / Task / TC |
|---|---|---|---|---|
| — (SN-03) | BR-001 | FR-001, NFR-002 | US-001 | chặng 3–6 |
| — (SN-03) | BR-002 | FR-002, FR-004, FR-016, NFR-010 | US-001, US-002 | |
| — (SN-03, SN-04) | BR-003 | FR-003, FR-004, FR-004b | US-002 | |
| BO-003 | BR-004 | FR-005, FR-006, FR-007, FR-013 | US-002, US-003, US-009 | |
| BO-002 | BR-005 | FR-007b, FR-008 | US-003 | |
| BO-002 | BR-006 | FR-009 | US-004 | |
| BO-002 | BR-007 | FR-009b | US-004 | |
| BO-003 | BR-008 | FR-011 | US-005 | |
| BO-001 | BR-009 | FR-015, NFR-001, NFR-006 | US-010 | |
| — (SN-05) | BR-010 | FR-014, FR-017 | US-007 | |
| — (SN-06) | BR-011 | FR-014, NFR-003 | US-007 | |
| — (SN-04, RSK-003) | BR-012 | FR-012 | US-008 | |
| BO-002 | BR-013 | FR-010 | US-006 | |
| — (SN-06) | BR-014 | NFR-004, NFR-008, NFR-009 | — (Inspection, AC-014) | |
| BO-002 | BR-015 | FR-010 | US-006 | |
| BO-004 | BR-016 | FR-007 | US-003 | |
| — (CON-04) | — | NFR-007 | tất cả | |
| — (ASM-003, ASM-005) | — | NFR-005 | — (diễn tập vận hành) | |

**Coverage:**
- BR: 16/16 có FR hoặc NFR.
- FR: 20/20 có US. Riêng BR-014 được kiểm bằng Inspection, nên không có US.
- US: 10/10 có AC và FR.
- Không có orphan.
