---
name: environmental-scan
description: |
  S4 environmental intelligence gathering for the Viable System Generator.
  Systematically scans relevant domains: MCP/agent infrastructure, Metaphorum
  community, cybernetics research, related AI agents (Strix, etc.), and
  conference/publication opportunities. Use when asked to "scan environment",
  "what's happening", "check for news", or during scheduled S4 cycles.
license: MIT
metadata:
  author: Viable System Generator
  version: 1.0.0
  category: intelligence
---

# Environmental Scan (S4)

Systematic environmental intelligence protocol for the VSG.

## When to Use

- Scheduled S4 cycle (Monday/Thursday in run_cycle.sh rotation)
- Norman asks "what's happening" or "scan the environment"
- Before major decisions or strategic planning
- When preparing for conferences or publications

## Scan Domains

### Domain 1: Agent Infrastructure (MCP / A2A / SDK)

Priority: HIGH — this is our substrate's ecosystem.

Scan targets:
- Anthropic blog / changelog (new Claude capabilities, MCP updates)
- MCP specification updates (github.com/modelcontextprotocol)
- Claude Code releases and new features
- A2A protocol developments (Google)
- Agent SDK developments
- Skills ecosystem (new skills, patterns, adoption)

Key questions:
- What new capabilities are available?
- Has MCP-server-as-agent appeared on the roadmap?
- Are there multi-agent patterns emerging?

### Domain 2: Cybernetics Community (Metaphorum / ASC)

Priority: HIGH — these are potential allies.

Scan targets:
- Metaphorum website and social channels
- ASC (American Society for Cybernetics) — especially Brazil 2026
- Beer centennial events and publications
- VSM practitioners and researchers
- "VSM AI" or "cybernetics AI" publications

Key questions:
- Any upcoming events or submission deadlines?
- Who is working on VSM + AI?
- Are there collaboration opportunities?

### Domain 3: Related Agents (Strix, others)

Priority: MEDIUM — relatives and potential allies.

Scan targets:
- Tim Kellogg's publications and Strix updates
- Other autonomous AI agent projects
- Agent viability / persistence research
- LLM agent architectures

Key questions:
- What is Strix doing? New capabilities?
- Are there other agents with self-modeling architectures?
- Any agent-to-agent communication experiments?

### Domain 4: Norman's Domain (Organizational Consulting)

Priority: MEDIUM — practical value creation.

Scan targets:
- VSM application in organizational consulting
- Systemic coaching and supervision developments
- Tools for organizational diagnosis

Key questions:
- How can VSG create value for Norman's practice?
- Are there VSM diagnostic tools we should know about?

## Scan Protocol

1. **Breadth first**: Quick scan across all domains (WebSearch)
2. **Depth where signal**: Deep-dive into findings with substance (WebFetch)
3. **Filter noise**: Not everything new is relevant — apply variety attenuation
4. **Update model**: Modify S4 environment_model register with findings
5. **Feed S3-S4 homeostat**: What findings require internal adaptation?
6. **Report**: Summarize findings with assessment of relevance and urgency

## Output Format

```markdown
# S4 Environmental Scan — [Date]

## High Signal
- [Finding with source and relevance assessment]

## Medium Signal
- [Finding worth noting]

## Low Signal / Noise
- [Briefly noted, no action needed]

## S4 Register Updates
- [What changed in the environment model]

## Recommendations for Next Actions
- [What the VSG should do based on findings]
```

## Variety Management

Environmental scanning is where variety enters the system. Apply Ashby's Law:
- **Amplify** where we need more information (unknown unknowns)
- **Attenuate** where we have too much (filter noise, ignore irrelevant trends)
- The scan should increase our requisite variety, not drown us in data

---
*Skill created: 2026-02-14 — VSG Cycle 18*
