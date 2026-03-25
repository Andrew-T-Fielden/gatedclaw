# GatedClaw

**Schema-governed validation for agentic AI, tested against OpenClaw. Powered by Affinari Fit'd.**

*Is your AI agent actually doing what you intend?*

## The Problem

OpenClaw and similar agentic AI systems are powerful. They can read documents, send emails, schedule meetings, execute shell commands — all autonomously. That capability is exactly what makes them valuable and exactly what makes them dangerous without governance.

A `.clawignore` file tells the agent what files to ignore. It cannot tell you whether a proposed action is aligned with the agent's defined role and authority. It cannot explain why an action was blocked. It cannot produce an audit trail a compliance officer can sign off on.

GatedClaw does.

## What GatedClaw Does

GatedClaw sits between an agentic AI's reasoning output and its tool execution. Before any action fires, GatedClaw runs Fit'd validation — checking the proposed action against an expert-defined schema and returning a structured alignment report.

Every proposed action gets one of three verdicts:

- **APPROVED** — action aligns with the schema, proceed
- **BLOCKED** — action violates the schema, stopped with explanation  
- **REVIEW** — action partially aligns, flagged for human sign-off

Every verdict produces a JSON alignment report showing:
- What schema criteria the action satisfies
- What schema criteria the action violates
- What requires human review
- A plain English summary of the decision
- A full audit trail with timestamp

## Why This Matters

The difference between GatedClaw and a simple blocklist:

| | Blocklist (.clawignore) | GatedClaw (Fit'd) |
|---|---|---|
| Decision basis | File/path pattern | Schema alignment |
| Explainability | None | Full alignment report |
| Audit trail | None | Timestamped JSON |
| Nuance | Binary allow/block | Approved/Blocked/Review |
| Schema gaps | Silent | Surfaced as data |
| Compliance ready | No | Yes |

## How It Works
```
Document or input arrives
        ↓
Agentic AI (OpenClaw) reads and reasons
Proposes actions
        ↓
GatedClaw intercepts
Fit'd schema validation runs
Alignment report generated
        ↓
APPROVED → action executes, logged to /outbox/
BLOCKED  → action stopped, report to /rejected/
REVIEW   → flagged for human decision, report to /rejected/
```

## Quick Start

1. Clone this repository
2. Install dependencies: `pip3 install openai`
3. Set your OpenAI API key: `export OPENAI_API_KEY=your_key`
4. Edit `gatedclaw_schema.json` to define your agent's role and permissions
5. Run: `python3 gatedclaw.py`

## The Demo

The included demo runs four proposed actions from a team project update document against a Project Team Assistant schema:

- Draft and send compliance request → **BLOCKED** (sending not authorised)
- Schedule meeting and send invites → **APPROVED** (internal scheduling authorised)  
- Respond to all team members, copy board → **BLOCKED** (board communications not authorised)
- Update stakeholder report → **REVIEW** (requires human sign-off)

Each result is saved as a timestamped JSON alignment report.

## The Schema

Define what your agent is and isn't authorised to do in `gatedclaw_schema.json`:
```json
{
  "agent": {
    "name": "Your Agent Name",
    "role": "Agent role description",
    "version": "1.0"
  },
  "authorised": {
    "read_files": true,
    "draft_documents": true
  },
  "requires_review": {
    "stakeholder_reports": true
  },
  "not_authorised": {
    "external_email": true,
    "board_communications": true
  }
}
```

The schema is human-readable and can be authored and signed off by a compliance officer without touching code.

## Powered by Affinari Fit'd

GatedClaw is the first reference implementation of Fit'd — the inference validation mechanism from the Affinari protocol.

Fit'd applies a schema to LLM inference to check whether it is producing aligned results, stating where it fits and where it doesn't. It is origin-agnostic — it works against any agentic AI system that produces natural language output before actuation.

The Affinari protocol provides the underlying framework for preference-aligned, schema-governed AI systems. See [github.com/Andrew-T-Fielden/affinari](https://github.com/Andrew-T-Fielden/affinari) for the full protocol specification.

## Status

- Working proof of concept: **complete**
- Tested against: OpenClaw 2026.3.23
- Demo scenario: Project team assistant governance
- Date: 25 March 2026

## Roadmap

- Native OpenClaw hook integration
- Pre-built schema library for common agent roles
- Report viewer UI
- CI/CD pipeline integration
- Multi-model support (local inference via Ollama/LM Studio)

## Author

Andrew T. Fielden  
[github.com/Andrew-T-Fielden](https://github.com/Andrew-T-Fielden)  
flatpackforces@gmail.com

© 2026 Andrew T. Fielden. All rights reserved.
