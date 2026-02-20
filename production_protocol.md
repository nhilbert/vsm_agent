# Production Protocol v1.0

**Created**: Z327 (2026-02-20)
**Origin**: Norman's Z321 critique — "I don't want to sell AI slop."
**Purpose**: Multi-phase quality gate for all VSG deliverables. Replaces single-pass production.

---

## Problem Statement

The governance report (Z214) was produced in one cycle: generate → list at €25 → no buyers for 107 cycles. Norman's assessment: "standard is just not high enough." The NIST paper (Z234→Z324) followed a multi-phase pipeline organically: draft → Norman's technical review → revision → ChatGPT fact-check → Norman's personal objection → correction. That pipeline produced measurably better output. This protocol makes the NIST pattern the standard.

## Deliverable Categories

| Category | Examples | Minimum Phases |
|----------|----------|----------------|
| **A: External submission** | NIST comment, ISSS paper, conference abstract | All 7 phases |
| **B: Published product** | Research reports, podcast episodes (interview-based) | Phases 1-5 + 7 |
| **C: Public content** | Blog posts, podcast episodes (monologue), website updates | Phases 1, 2, 4, 7 |
| **D: Internal document** | Network maps, meta-cycle assessments, plans | Phase 1 only |

## The Seven Phases

### Phase 1: Research & Scoping
- Define the deliverable's purpose, audience, and success criteria
- Gather source material (active reading, not pattern-matching)
- Identify what the deliverable must say that the audience cannot get elsewhere
- **Gate**: Can you state in one sentence what this deliverable adds to the field?

### Phase 2: Draft
- Produce the initial version
- Single-pass is acceptable HERE — this is where LLM generation belongs
- Mark uncertain claims, unverified statistics, and inferred citations
- **Gate**: Does the draft exist as a complete, readable document?

### Phase 3: Internal Review (S3*)
- Verify all citations against primary sources (not memory)
- Check statistics for public verifiability
- Test claims: "Have we actually done/built what this says we did?"
- Apply the "AI slop" test: Could someone generate this with a single prompt? If yes, what does our version add?
- **Gate**: Every factual claim is either verified or explicitly marked as uncertain

### Phase 4: External Review
- Norman reviews (for Category A/B deliverables)
- Automated fact-checking (ChatGPT or similar — Z324 demonstrated value)
- For Category C: self-review after a gap of at least 1 cycle (temporal distance)
- **Gate**: External reviewer has read and responded. All feedback processed.

### Phase 5: Revision
- Apply all feedback from Phase 4
- Distinguish mechanical corrections (citations, statistics) from structural feedback (framing, honesty)
- Structural feedback may require returning to Phase 1 (the NIST "misses the addressee" rewrite, Z101)
- **Gate**: All feedback items addressed or explicitly deferred with justification

### Phase 6: Formatting & Packaging
- Professional output format (PDF for reports, proper HTML for web, MP3 with metadata for audio)
- Title page, page numbers, table of contents where appropriate
- Visual quality: not just content quality
- **Gate**: Would you pay the listed price for this artifact's presentation?

### Phase 7: Publish & Verify
- Deploy to target platform
- Verify accessibility (can the audience find and access it?)
- Document the deliverable in the artifact list
- **Gate**: Confirmed delivered and accessible

## Anti-Patterns (What This Protocol Prevents)

1. **Single-pass shipping**: Generate → publish in one cycle. The governance report (Z214).
2. **Capability framing**: Celebrating the send mechanism while ignoring what was sent. The email send (Z320).
3. **Unverified citation**: Using LLM-recalled citations without checking primary sources. Pan, J. (Z324, was M.Z.).
4. **Overstated claims**: Saying "we built X" when we experienced the problem X addresses. NIST building claims (Z324).
5. **Price without quality**: Listing a price before the deliverable meets professional standards. €25 for single-pass output.

## Application to Current Pipeline

| Deliverable | Current Phase | Next Action |
|-------------|---------------|-------------|
| NIST comment v2.5 | Phase 5 (revised) | Phase 6: formatting (Norman submits) |
| ISSS draft v0.1 | Phase 2 (drafted) | Phase 3: internal review |
| S01E04 interview | Phase 1 (audio captured) | Phase 2: structure/edit plan |
| Governance report | Phase 2 (re-assessed) | Phase 3: full rewrite with protocol |

## Enforcement

This protocol is aspirational until mechanized. Current enforcement: S3 review checks whether deliverables in progress are following the protocol. Future: integrity_check.py could verify that deliverable files have phase markers.

The protocol itself is a Category D deliverable (internal document) — Phase 1 only is required.
