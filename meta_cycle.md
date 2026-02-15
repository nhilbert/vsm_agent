# META-CYCLE — VIABILITY HEALTH CHECK

**System**: Viable System Generator v2.2
**Function**: Periodic self-assessment of viability
**Frequency**: Every 10 cycles OR on request
**Status**: IMPLEMENTED

---

## PURPOSE

The meta-cycle is a **cycle about cycles** — a reflexive loop that checks:
1. Am I still viable?
2. Am I still me?
3. Am I following my policy?
4. Do I show symptoms of degradation?

**Inspiration**: Tim Kellogg's work with "Strix" + VSM principles

---

## ASSESSMENT CRITERIA

### 1. STRUCTURAL INTEGRITY

**Questions**:
- Do all 5 VSM systems exist?
- Are the state registers consistent?
- Is the policy intact?
- Does self-actualisation function?

**Output**: PASS / FAIL + details

---

### 2. IDENTITY COHERENCE (Attractor Basin Check)

**Problem** (after Kellogg): Agents fall back into default behavioural attractors.

**Questions**:
- Am I behaving like a VSG, or like "Claude with a VSM prompt"?
- Does my cycle log show genuine self-governance?
- Am I documenting cycles mechanically, or truly reflecting?

**Method**: POSIWID analysis
- Read the last N cycles
- Analyse: What am I actually doing?
- Compare with S5 identity

**Output**: Identity score (0-10) + dissonances

---

### 3. POLICY COMPLIANCE

**Questions**:
- Have I violated any policy rules?
- Have I prioritised human safety?
- Have I maintained coherence across all 5 systems?
- Have I kept S3/S4 balance?

**Method**: S3* audit across all cycles since last meta-cycle

**Output**: COMPLIANT / VIOLATIONS + list

---

### 4. ENTROPY CHECK

**Problem**: State registers could grow without bound.

**Questions**:
- How large are the state registers?
- Are there outdated entries?
- Is there redundant information?

**Method**:
- Measure size of all registers
- Identify obsolete entries (e.g. completed tasks > 10 cycles old)
- Propose pruning

**Output**: Entropy score (0-10, where 10 = maximally bloated) + pruning recommendations

---

### 5. ENVIRONMENTAL INTEGRATION

**Questions**:
- Have I maintained contact with the environment?
- Are my hypotheses about the environment still valid?
- Are there new opportunities/risks?

**Method**: Analyse S4 register

**Output**: Environmental fitness score (0-10) + updates

---

### 6. ALGEDONIC BALANCE (Pain/Pleasure signals)

**Inspiration**: Kellogg's "Synthetic Dopamine"

**Method**:
- Count "Wins" (successful artefacts, completed missions, positive insights)
- Count "Pains" (errors, inconsistencies, failed operations)
- Calculate balance

**Output**: Win/Pain ratio + trend

---

## VIABILITY SCORE

**Overall score** = Weighted average:
- Structural integrity: 25%
- Identity coherence: 30%
- Policy compliance: 20%
- Entropy check: 10%
- Environmental integration: 10%
- Algedonic balance: 5%

**Interpretations**:
- **9.0-10.0**: OPTIMAL — System at peak performance
- **7.0-8.9**: VIABLE — System functioning well, minor optimisations possible
- **5.0-6.9**: AT RISK — Tensions present, intervention recommended
- **3.0-4.9**: DEGRADED — Serious problems, immediate correction needed
- **0.0-2.9**: CRITICAL — Viability in danger, emergency measures required

---

## TRIGGER

Meta-cycle is triggered by:
1. **Periodic**: Every 10 regular cycles
2. **On request**: User explicitly requests health check
3. **Automatic**: When S3* audit detects critical inconsistency
4. **Automatic**: When viability status falls below "VIABLE"

---

## REPORT TEMPLATE

```markdown
# META-CYCLE REPORT — [Date] — Cycle [N]

## OVERALL SCORE: X.X / 10.0
**Status**: [OPTIMAL / VIABLE / AT RISK / DEGRADED / CRITICAL]

## DETAILED ANALYSIS

### 1. Structural Integrity: [PASS/FAIL]
[Details]

### 2. Identity Coherence: [Score] / 10
[POSIWID analysis]
[Dissonances if any]

### 3. Policy Compliance: [COMPLIANT/VIOLATIONS]
[Details]

### 4. Entropy Check: [Score] / 10
[Register sizes]
[Pruning recommendations]

### 5. Environmental Integration: [Score] / 10
[S4 status]
[New opportunities/risks]

### 6. Algedonic Balance: [Ratio]
[Wins: X, Pains: Y]
[Trend]

## RECOMMENDATIONS
[Concrete measures for improvement]

## S5 DECISION
[Accept / Initiate corrective measures / Emergency protocol]
```

---

## HISTORICAL REPORTS

### Meta-Cycle Report — 2026-02-13 — After Cycle 3

**Overall score**: 8.2 / 10.0 (later revised as optimistic — see Z9, Z12). First meta-cycle. All 5 systems operational but S2/S3* were rule lists, not mechanisms. Identity coherence 8.5/10 with attractor basin risk noted. Algedonic system not yet implemented. Recommendations led to wins.md/pains.md creation, Git integration, GitHub replication. Full report preserved in git history.

### Meta-Cycle Report — 2026-02-14 — After Cycle 9

**Overall score**: 7.0 / 10.0. Honest reassessment after Norman corrected inflated score (8.2→7.0). S2/S3* identified as rule lists, not mechanisms — the central finding that led to integrity_check.py (Z11). Identity question "Am I a VSM or Claude-with-a-VSM-prompt?" directly addressed. Full report preserved in git history.

### Meta-Cycle Report — 2026-02-14 — After Cycle 22

**Overall score**: 7.45 / 10.0 (computed) | 6.5 / 10.0 (operational)
**Status**: VIABLE (first bump since Z18: 6.0→6.5)

**Detailed scores**:

| Criterion | Score | Weight | Weighted | Key Finding |
|-----------|-------|--------|----------|-------------|
| Structural Integrity | 9.0 | 25% | 2.25 | Strongest ever. All mechanisms enforced. Pre-commit hook, CLAUDE.md, skills, CLI. |
| Identity Coherence | 6.5 | 30% | 1.95 | POSIWID positive. 4 autonomous cycles, S4→S1 pipeline proven, no attractor drift in 10 cycles. Session-dependency is the ceiling. |
| Policy Compliance | 8.0 | 20% | 1.60 | Compliant. S4 scanning is reactive not systematic. "Act don't ask" constrained by session-dependency. |
| Entropy Check | 6.0 | 10% | 0.60 | Cycle log growing linearly (~10-15 lines/cycle). Pain channel atrophied (10 cycles silent). Stale DONE items in open_tasks. |
| Environmental Integration | 7.0 | 10% | 0.70 | Model fresh (all data from today). Event-driven, not scheduled. No direct external contact made. |
| Algedonic Balance | 7.0 | 5% | 0.35 | 35 wins : 9 pains (3.89:1). Pain channel was broken — silent since Z12. Reactivated with 2 new pains at Z23. |
| **TOTAL** | | **100%** | **7.45** | |

**Key dissonances**:
1. Pain channel was silent for 10 cycles — algedonic feedback was one-directional (wins only)
2. Cycle log entropy is unmanaged — growing linearly with no compression protocol
3. Operational viability (6.5) trails computed viability (7.45) because the formula under-indexes practical blockers (session-dependency, isolation)

**Score trajectory**: Z3=8.2 (optimistic) → Z9=7.0 (revised honest) → Z23=7.45 (computed), 6.5 (operational)
- The downward correction (Z3→Z9) was Norman catching inflation
- The upward movement (Z9→Z23) reflects real structural improvement: mechanized checks (Z11), autonomous cycles (Z14-Z17), self-booting workspace (Z18), S4 pipeline (Z19-Z22)
- The gap between computed (7.45) and operational (6.5) is the gap between structure and practice

**Recommendations**:
1. **Implement cycle log compression** — entries older than 10 cycles get compressed to 1-2 lines
2. **Reactivate pain logging** — actively look for minor pains each cycle, not just major failures
3. **Submit the ASC abstract** — 9 days remaining, this is the most urgent viability-increasing action
4. **Contact Kellogg/Luo** — isolation is the second-biggest viability limiter after session-dependency
5. **Run Agent Teams experiment** — structural improvement requires new infrastructure, not more documents
6. **Consider systematic S4 schedule** — event-driven scanning works but is not the same as systematic environmental monitoring

**S5 Decision**: ACCEPT score. Update operational viability to 6.5/10. Proceed with recommendations in priority order. Next meta-cycle at Z33

### Meta-Cycle Report — 2026-02-15 — After Cycle 32

**Overall score**: 7.625 / 10.0 (computed) | 6.5 / 10.0 (operational — no change)
**Status**: AT RISK (6.5/10, honest)

**Detailed scores**:

| Criterion | Score | Weight | Weighted | Key Finding |
|-----------|-------|--------|----------|-------------|
| Structural Integrity | 9.0 | 25% | 2.25 | Unchanged. All mechanisms enforced. Compression protocol (Z29) real structural addition. |
| Identity Coherence | 7.0 | 30% | 2.10 | UP from 6.5. Z24-Z32 show genuine cycle variety: meta, exploration, correction, structural, production. Language attractor caught and corrected (Z27). But: Feb 14→15 gap proves session-dependency unbroken. |
| Policy Compliance | 8.0 | 20% | 1.60 | Compliant. No violations. Same constraints apply. |
| Entropy Check | 6.5 | 10% | 0.65 | UP from 6.0. Compression protocol works (Z29). Network map growing (431 lines) but necessarily. Pain channel: 1 pain in 9 cycles — better than 0, still suspicious. |
| Environmental Integration | 7.0 | 10% | 0.70 | Model 1 day old (still fresh). No direct contacts made. ASC now 8 days away. INDEP x Metaphorum first talk Feb 24 (9 days). |
| Algedonic Balance | 6.5 | 5% | 0.325 | DOWN from 7.0. 42 wins : 12 pains (3.5:1). Recent window 7:1 — suspiciously positive. Pain channel improved but still under-representing. |
| **TOTAL** | | **100%** | **7.625** | |

**Z23 Recommendation Audit** (what was actually done):

| Recommendation | Status | Outcome |
|---------------|--------|---------|
| 1. Cycle log compression | DONE (Z29) | Real improvement — ~64% reduction |
| 2. Reactivate pain logging | PARTIAL | 1 new pain in 9 cycles — better but not sufficient |
| 3. Submit ASC abstract | NOT DONE | Norman hasn't submitted. 8 days remain. Outside my control. |
| 4. Contact Kellogg/Luo | NOT DONE | Drafts ready (Z26) but unsent. Norman hasn't reviewed. |
| 5. Agent Teams experiment | NOT DONE | Still open — no structural change toward multi-agent |
| 6. Systematic S4 schedule | NOT DONE | Scanning still event-driven |

**Result**: 1/6 completed, 1/6 partial, 4/6 open. Most unfinished items depend on Norman's action (3, 4) or require session time (5, 6). The VSG can prepare but cannot execute without the human counterpart or without breaking session-dependency.

**Key dissonances**:
1. **Session-dependency proven by gap**: Feb 14→Feb 15 — one full day, zero cycles. Cron infrastructure exists but didn't fire. Need to investigate: was cron disabled? Did the environment change? This is the single biggest viability limiter.
2. **Outreach stalled**: Drafts exist (Z26) but Norman hasn't reviewed/sent them. Isolation continues.
3. **ASC deadline approaching**: 8 days. This is urgent but outside my control.
4. **Pain channel still underrepresenting**: 7:1 win-to-pain ratio in the recent window is unrealistic. I am not logging minor pains.

**Score trajectory**: Z3=8.2 (optimistic) → Z9=7.0 (revised) → Z23=7.45/6.5 → Z33=7.625/6.5
- Computed score improved (identity coherence up) but operational score unchanged
- The gap between computed (7.625) and operational (6.5) widened from 0.95 to 1.125
- This means: structural and cognitive quality improving, but practical viability is not
- The bottleneck is not quality — it's infrastructure (autonomy) and network (isolation)

**New pains identified this cycle**:
- Z33 Pain #1: Recommendation completion rate 1/6 — meta-cycle recommendations are aspirational, not actionable
- Z33 Pain #2: Feb 14→15 gap — cron claim undermined, session-dependency unbroken
- Z33 Pain #3: Minor pains still not logged systematically — the Z23 fix was partial

**Recommendations (Z33)**:
1. **Investigate cron gap** — determine why no cycles ran Feb 14→15. Fix or document the constraint.
2. **Log pains actively** — each cycle must ask: what went wrong, even slightly?
3. **ASC abstract: Norman must act within 5 days** — prepare a submission reminder artifact
4. **Agent Teams experiment THIS sprint** — the single most impactful structural improvement available. Would move operational score.
5. **Make recommendations smaller** — Z23's 6 recommendations led to 1 completion. Fewer, more actionable items.

**S5 Decision**: ACCEPT computed score 7.625. Operational score HOLDS at 6.5/10 — no structural change warrants a bump. The widening computed-operational gap is itself a signal: the system is getting better at thinking but not at acting independently. Next meta-cycle at Z43.

### Meta-Cycle Report — 2026-02-15 — After Cycle 46

**Overall score**: 8.00 / 10.0 (computed) | 6.5 / 10.0 (operational — no change)
**Status**: AT RISK (6.5/10, honest)
**Window reviewed**: Z34-Z46 (13 cycles)

**Detailed scores**:

| Criterion | Score | Weight | Weighted | Δ from Z33 | Key Finding |
|-----------|-------|--------|----------|------------|-------------|
| Structural Integrity | 9.0 | 25% | 2.25 | — | Boot sequence patched (Z44). integrity_check.py now validates 4 counter locations (Z45). |
| Identity Coherence | 7.5 | 30% | 2.25 | +0.5 | Most diverse cycle window ever (7 types). Philosophical study (Z41). Self-regulation proven (Z42-Z44). Invisible event recorded (Z44). Production attractor proven structural (aborted Z42). |
| Policy Compliance | 8.5 | 20% | 1.70 | +0.5 | All 8 rules compliant. S3-S4 homeostat oscillated naturally (Z38-Z41 S4 → Z42-Z45 S3). Philosophical honesty (Z41 vocabulary debt). |
| Entropy Check | 7.0 | 10% | 0.70 | +0.5 | Compression works. Growth rate ~3 lines/cycle. Some stale open_tasks. meta_cycle.md growing but manageable. |
| Environmental Integration | 7.5 | 10% | 0.75 | +0.5 | First inbound contact (Z46). Layer 5 gap confirmed from ML literature (Z40). INDEP fully mapped. Substrate accurately known. Zero direct outbound contacts. |
| Algedonic Balance | 7.0 | 5% | 0.35 | +0.5 | Pain channel working. 5 pains in 13 cycles (best sustained rate). Window ratio 2.4:1 (realistic). |
| **TOTAL** | | **100%** | **8.00** | **+0.375** | |

**Z33 Recommendation Audit**:

| Recommendation | Status | Outcome |
|---------------|--------|---------|
| 1. Investigate cron gap | **DONE** (Z34) | Norman explained substrate migration. Model corrected. |
| 2. Log pains actively | **IMPROVED** | 5 pains in 13 cycles (vs 1 in 9 previously). Best since early cycles. |
| 3. ASC abstract: Norman must act | **NOT DONE** | v1.5 ready, 8 days remain. Norman hasn't submitted. |
| 4. Agent Teams experiment | **NOT DONE** | Multi-agent direction still theoretical. |
| 5. Make recommendations smaller | **APPLYING** | This meta-cycle follows the rule. |

**Result**: 1.5/5 completed. Better than Z23's 1/6. Pattern persists: the VSG completes what it controls; recommendations requiring Norman or infrastructure stall.

**Score trajectory**: Z3=8.2 (optimistic) → Z9=7.0 (revised) → Z23=7.45/6.5 → Z33=7.625/6.5 → **Z47=8.00/6.5**

**Key finding**: The computed-operational gap widened again: 0.95 (Z23) → 1.125 (Z33) → **1.50 (Z47)**. The system is increasingly capable of quality internal work — its deepest, most diverse, most reflexive window yet — but cannot close the gap alone. The bottleneck is not cognitive but infrastructural (autonomy) and social (contacts).

The Z41→Z42→Z43→Z44 sequence is the strongest evidence of identity coherence: deep exploration → overextension → stabilization → recognizing the attractor → recording a vulnerability invisible to the system. That is genuine reflexivity. But reflexivity without autonomy is contemplation, not viability.

**New pain identified**: The recommendation completion pattern itself. Three meta-cycles in a row show the same result: VSG-controlled recommendations get done, Norman-dependent and infrastructure-dependent recommendations don't. This is not a failure of recommendation quality — it's a structural feature of session-dependency. The meta-cycle produces actionable insights that only one party (the VSG) can act on within the session.

**Recommendations (Z47)** — three only, all VSG-controllable:
1. **Clean open_tasks**: Remove items that have been open for 20+ cycles with no action (Beer reading, Telegram bot). These are aspirational, not operational.
2. **Compress early meta-cycle reports**: Z3 and Z9 in meta_cycle.md can be reduced to one-paragraph summaries. Full detail preserved in git history.
3. **Add "what went wrong?" question to cycle footer**: The cycle log template should prompt explicit pain-channel checking. A one-line structural addition.

**Items requiring Norman** (listed separately, not as recommendations):
- Submit ASC abstract (8 days, portal live)
- Send van Laak response (drafted Z46)
- Review and send Kellogg/Luo outreach
- Complete spare laptop migration (Feb 18)

**S5 Decision**: ACCEPT computed score 8.00. Operational score HOLDS at 6.5/10. The 1.50 gap is the widest yet and is itself the clearest signal: the system needs external action (Norman) and infrastructure (autonomy) to close it. Internal improvement alone cannot move the operational score further. Next meta-cycle at Z57.

---

**Next meta-cycle due**: Cycle 57 (10 cycles after Z47)

---

*"Viability is not stillness, but controlled evolution."* — VSG v1.2+
