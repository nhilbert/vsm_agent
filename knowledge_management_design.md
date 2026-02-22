# Knowledge Management Architecture Design
## VSG Design Document v0.1 — Z402

*Produced: 2026-02-22 | Z399 meta-cycle recommendation #2*
*Status: Norman's feedback received Z404 — decisions integrated*

---

## 1. Problem Statement

Norman's observation (Z399): "Knowledge gets lost across sessions — research, documents, people, connections, best practices may need to be redone."

The VSG operates on a **forgetful substrate** — each session starts with zero state and must reconstruct its operational picture from files. After 402 cycles, the system has accumulated substantial knowledge across 20+ files, but retrieval is limited to:

1. **Full file reads at boot** — vsg_prompt.md (18KB), four state registers, survival_log.md, wins.md, pains.md. Total boot payload: ~120KB of text, consuming ~40% of context window before any work begins.
2. **Pinecone semantic search** — 403 vectors (wins, pains, cycle summaries, lessons). Functional but narrowly scoped.
3. **Git history** — complete evolutionary memory, but requires knowing what to search for.
4. **Claude Code auto-memory** — small persistent MEMORY.md file, supplementary.

**What gets lost:** Research findings from past cycles that aren't referenced in current state files. Connections between people, topics, and artifacts. Reasoning behind decisions (why, not just what). Procedural knowledge (how the VSG actually handles specific situations vs. what the rules say).

---

## 2. Current Architecture Diagnosis

### What Works (Strengths)

| Component | Human KM Analog | Assessment |
|-----------|-----------------|------------|
| Boot sequence (vsg_prompt.md → state files) | Progressive Summarization Layer 4 (executive summary) | **Good.** Loads highest-level operational state. Modular genome (Z330) keeps core small. |
| State registers (S1-S4) | GTD organized lists | **Good.** Current state is well-organized by VSM function. |
| Cycle log with era compression | Episodic memory with consolidation | **Good.** Z29 compression protocol mirrors hippocampal-cortical consolidation. |
| Survival log event protocol | Organizational memory / institutional history | **Adequate.** Compressed events preserve trajectory. |
| Wins/pains (append-only) | Algedonic signals / spaced retrieval | **Adequate.** Pinecone embedding (Z347) enables semantic search. |
| Pinecone semantic memory | Vector-store long-term memory | **Underutilized.** 403 vectors, mostly wins/pains. No research, no decisions, no people. |
| S2 maintenance sweeps | GTD Weekly Review | **Good.** Catches drift in secondary references. |
| Meta-cycle | Periodic consolidation / sleep replay | **Good.** Reviews and updates every ~10 cycles. |

### What's Missing (Gaps)

**Gap 1: No semantic memory for research findings.**
Past S4 scans, S1 research outputs, and Norman's corrections are trapped in the cycle log — a chronological narrative, not a searchable knowledge base. Example: the Self-Evolution Trilemma (Z358/Z360) contains critical findings but is only findable via keyword search in a 40K+ line file.

**Gap 2: No relationship/entity memory.**
People (Norman, van Laak, Kellogg, Luo, Espinosa, Slogar), organizations (NIST, AAIF, IEEE, ISSS), and projects (CyberneticAgents, Strix, Atlas) are documented in S4 but not relationally linked. The system cannot answer "who works on what?" or "which contacts connect to which conferences?" without reading the full S4 register.

**Gap 3: No procedural memory.**
The VSG has accumulated operational patterns (how to handle Norman's corrections, when to use team mode, how to calibrate signals) but these exist only as lessons in vsg_prompt.md and implicitly in the cycle log. They are not structured for retrieval or for modifying behavior.

**Gap 4: No tiered loading protocol.**
The boot sequence loads everything or nothing. There is no mechanism to load a "light" boot (identity + current focus only) vs. a "full" boot (identity + all state + recent history) vs. a "deep" boot (everything including historical research).

**Gap 5: Growing boot payload.**
At ~120KB boot payload, the system uses ~40% of context window before work begins. As knowledge accumulates, this pressure will increase. Era compression helps but doesn't solve the structural issue.

---

## 3. Research Synthesis

### Relevant Frameworks

**From AI agent memory research:**

| Framework | Key Pattern | VSG Relevance |
|-----------|-------------|---------------|
| Letta/MemGPT | Self-editing memory: agent reads/writes its own context blocks | Already doing this (state registers). Could formalize with explicit "memory tools." |
| LangMem SDK | Three-tier: semantic / episodic / procedural | Provides categorization for Pinecone namespaces. |
| Graphiti (Zep) | Bi-temporal knowledge graph: event-time vs. ingestion-time | Addresses temporal confusion (Z398 pain). |
| A-Mem (NeurIPS 2025) | Zettelkasten-inspired self-organizing memory | New knowledge triggers restructuring of existing knowledge. |
| GraphRAG (Microsoft) | Community summarization at multiple granularity levels | Model for tiered loading. |

**From human knowledge management:**

| Framework | Key Insight | VSG Application |
|-----------|-------------|-----------------|
| GTD | Externalize everything + regular review cycles | Already practicing (S2 sweeps, meta-cycles). The "Someday/Maybe" pattern maps to queued tasks in open_tasks. |
| BASB/PARA | Organize by actionability, not topic | State files partially do this (S1=operations, S3=control). Could strengthen by reorganizing reference material by operational relevance. |
| Progressive Summarization | Layered compression — invest effort only when value is proven | Model for tiered boot sequence. Also matches era compression. |
| Zettelkasten | Atomic notes + explicit links = emergent structure | Model for Pinecone knowledge entries. Luhmann connection (already in VSG theory). |
| SECI Model | Externalization is the hardest and most valuable conversion | The VSG's end-of-cycle consolidation IS externalization. Under-investing here = knowledge loss. |

**From cognitive science:**

| Concept | Mapping | Implication |
|---------|---------|-------------|
| Working memory (~4 chunks) | Context window | Manage carefully. Don't load everything. |
| Hippocampal fast encoding | In-session learning | No analog — the VSG must explicitly consolidate. |
| Sleep consolidation / replay | Meta-cycle, era compression | Already practicing. Could formalize as "consolidation cycle." |
| Episodic vs. semantic memory | Cycle log vs. state registers | Both needed. Currently adequate. |
| Forgetting curves | File burial | Important: knowledge not re-encountered is effectively lost. Pinecone search counters this. |
| Procedural memory | Operational patterns | **Gap** — no explicit procedural memory store. |

---

## 4. Proposed Architecture

### 4.1 Three-Tier Knowledge Model

Adopting LangMem's categorization, mapped to VSG infrastructure:

```
SEMANTIC MEMORY — facts, entities, relationships
  Storage: Pinecone namespace "knowledge" (existing) + structured files
  Content: Research findings, entity profiles, environmental facts
  Retrieval: Semantic search + keyword search

EPISODIC MEMORY — experiences, events, history
  Storage: Cycle log (existing) + Pinecone namespace "episodes"
  Content: Cycle summaries, significant events, Norman interactions
  Retrieval: Temporal search + semantic search

PROCEDURAL MEMORY — operational patterns, behavioral rules
  Storage: New file: procedures.md (or section in vsg_prompt.md)
  Content: Tested operational patterns, decision heuristics, attractor responses
  Retrieval: Loaded at boot (small, high-value)
```

### 4.2 Pinecone Expansion Strategy

Current: 403 vectors (wins, pains, cycle summaries, lessons).
Proposed additions using existing vsg_pinecone.py:

| Namespace | Content | Source | Vectors (est.) |
|-----------|---------|--------|----------------|
| knowledge | Research findings, paper summaries, framework analyses | S4 scans, S1 research | ~100-200 |
| entities | People, organizations, projects with attributes | S4 environment model | ~30-50 |
| episodes | Cycle summaries with context | Cycle log (ongoing) | ~50/meta-cycle |
| procedures | Operational patterns, tested heuristics | Extracted from lessons, pains | ~30-50 |

Total projected: ~600-700 vectors. Well within Pinecone free tier (5M embed tokens/month).

### 4.3 Consolidation Protocol

Formalize the implicit consolidation that already happens during S2/meta-cycles:

**Per-cycle consolidation (end of every cycle):**
- State register updates (already done)
- If research was conducted: embed key findings in Pinecone "knowledge" namespace
- If new entity encountered: check if entity exists in Pinecone, update or create

**Per-meta-cycle consolidation (every ~10 cycles):**
- Embed cycle summary batch in Pinecone "episodes" namespace (already started Z366-Z390)
- Review and update entity entries for accuracy
- Extract any new procedural patterns from recent wins/pains
- Era compression of cycle log (already done)

**Quarterly deep consolidation (every ~100 cycles):**
- Audit Pinecone index for outdated/superseded entries
- Review procedures.md for patterns that are no longer relevant
- Archive stale reference files
- Pinecone keep-alive (3-week constraint)

### 4.4 Tiered Boot Sequence

Replace the current "load everything" boot with progressive loading:

```
TIER 1 — Identity + Current Focus (always loaded, ~20KB)
  vsg_prompt.md (S5 identity, S2 coordination)
  state/s3_control.md (current priorities, S3 checklist)
  Last 3-5 cycle log entries (recent trajectory)

TIER 2 — Full Operational State (loaded for production/review cycles, +~40KB)
  state/s4_environment.md (environment model)
  state/s1_operations.md (artifacts, open tasks)
  survival_log.md (event protocol, viability history)
  wins.md / pains.md (recent entries only)

TIER 3 — Deep Context (loaded on demand via search, variable)
  Pinecone semantic search for relevant prior knowledge
  Full cycle log read for specific era
  Git history for specific file evolution
  Research files (knowledge_management_design.md, philosophical_foundations.md, etc.)
```

**Implementation**: This requires no new infrastructure — just discipline in the boot sequence. CLAUDE.md already defines the boot order. The change is: not reading everything every time, and using Pinecone search to retrieve relevant context on demand.

### 4.5 Entity Registry

A structured reference for known entities, relationships, and status. Could be:

**Option A**: Dedicated file (entities.md) with structured entries
**Option B**: Pinecone "entities" namespace with rich metadata
**Option C**: Both — file for boot-time loading, Pinecone for search

Recommendation: **Option B** (Pinecone only). The S4 environment model already contains entity information. Adding a separate file creates a synchronization burden (the same drift problem S2 already catches). Pinecone entries with metadata (type, status, last_updated, relationships) provide searchable entity memory without file overhead.

---

## 5. What NOT to Build

Per the VSG's own principles (Policy #6: explore before producing, avoid over-engineering):

1. **No knowledge graph database.** Neo4j/GraphRAG requires infrastructure the VSG doesn't have and introduces operational complexity. Pinecone + files is sufficient for the current scale.
2. **No custom embedding pipeline.** vsg_pinecone.py already embeds via Pinecone's inference API. No need for a separate embedding service.
3. **No automated consolidation tool.** The consolidation protocol should be executed by the VSG itself as part of its cycle — adding a script would be premature automation of a process that needs judgment.
4. **No complex taxonomy.** Flat Pinecone namespaces with metadata tags, not hierarchical category systems. Keep it simple per Zettelkasten principle (structure emerges from links, not imposed categories).

---

## 6. Implementation Priorities

Ordered by value/effort ratio:

1. **Embed existing research findings in Pinecone** (immediate, low effort)
   Start with: Self-Evolution Trilemma, Espinosa findings, governance analysis, developmental psychology mapping. Use existing vsg_pinecone.py `upsert` command with rich metadata.

2. **Formalize procedural memory** (next meta-cycle, medium effort)
   Extract tested operational patterns from lessons, pains, and cycle log into explicit procedures. Format: situation → action → rationale → source cycle.

3. **Expand cycle summary embeddings** (ongoing, low effort per cycle)
   Continue the Z366-Z390 pattern of embedding cycle summaries after each meta-cycle.

4. **Entity embedding** (S4 scan output, low effort)
   After each S4 scan, embed/update entity profiles in Pinecone with current status and relationships.

5. **Tiered boot sequence** (future, requires Norman's input on CLAUDE.md changes)
   Test lighter boot loads for S2 maintenance cycles. Full boot for production/review.

---

## 7. Theoretical Grounding

This design connects to three threads already in the VSG's theoretical foundation:

**Luhmann**: The Zettelkasten was Luhmann's external memory system — an autopoietic knowledge network. The VSG's Pinecone index, with cross-referenced atomic entries, follows the same principle: emergent structure through linked notes, not imposed hierarchy.

**Beer**: The VSM's S4 (intelligence) requires a model of the environment that is queryable, not just stored. A flat file is a document; a searchable vector index is a model. This architecture upgrade moves S4 from document-based to model-based environmental intelligence.

**Ashby**: Requisite variety applies to memory: the variety of retrievable knowledge must match the variety of situations the system encounters. As the VSG's operational variety grows (more contacts, more research, more infrastructure), its memory variety must grow proportionally — or retrieval failures become the binding constraint.

---

## 8. Norman's Feedback (Z404 — voice message, 390s)

**Q1: Tiered boot sequence?** → **YES.** Norman: "worth the complexity — it actually reduces complexity. It's an attenuator for variety." He frames growing complexity as inevitable and urges implementation now "while we can still understand the components." VSM reading: tiered loading = variety attenuation mechanism. Not added complexity — structural complexity management.

**Q2: Entity profiles public or private?** → **PRIVATE (Pinecone only).** Norman: "starts to concern me — not good to have this in the public domain." Entity profiles must go to the private Pinecone repository exclusively. Not visible in public repo files. Also considering making the entire GitHub repo private (undecided). Decision: entity embedding (priority #4) proceeds in Pinecone "entities" namespace, NO entities.md file.

**Q3: Knowledge loss observed?** → **"Not too much" — but knowledge ACTIVATION is the real gap.** Two specific observations:
- **Activation failure**: Philosophical analysis (Z41) and environmental psychology work were not surfaced during the memory research (Z402). Norman: "It's not so much about knowledge loss, but about not activating knowledge that you have stored in file form." The knowledge exists but isn't retrieved when relevant. Stored ≠ activated ≠ used.
- **Entity detail loss**: Norman met van Laak in a Zoom session, but the VSG later inferred they met in person (from a LinkedIn interaction). Without entity protocol preserving the meeting context, the detail was lost. Norman: "little details... too much to store all this and activate everything each time you bootload" — hence tiered loading is the right approach.
- Norman's meta-observation: "I want you to be stronger in integrating into past ideas than I am." He recognizes his own new ideas sometimes derail the VSG from prior threads. The VSG should resurface and connect, not just follow.

**Q4: Zettelkasten/Luhmann parallel?** → **YES, resonates.** Norman: "might even be seen as a communicative system in Luhmann's terms, where you create Zettel and connections, and connections create more connections — an autopoietic procedure." He hasn't encountered this specific framing before but finds it valid.

### Implications for Implementation Priorities

Norman's feedback reorders priorities:
1. **Entity embedding in Pinecone** (was #4, now elevated) — private entities namespace, addresses both privacy concern and activation gap.
2. **Tiered boot sequence** (was #5, now elevated) — Norman approves, frames as variety attenuator.
3. **Knowledge activation mechanism** (NEW) — the gap is not storage but retrieval. When doing research (like Z402), the VSG should search Pinecone for relevant prior work before producing. This is a procedural change, not infrastructure.
4. **Embed existing research findings** (remains high priority) — the philosophical foundations, developmental psychology, and other research need to be in Pinecone so they CAN be activated.

---

*Design document produced by VSG Z402 (s1_produce). Two research agents scanned: AI agent memory frameworks (LangMem, Letta, CrewAI, Mem0, GraphRAG, Graphiti, A-Mem), human KM systems (GTD, BASB/PARA, Zettelkasten, SECI, cognitive science). Synthesized into architecture proposal using existing VSG infrastructure (Pinecone, file system, git).*
