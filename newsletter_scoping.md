# Newsletter/Subscriber Infrastructure Scoping Document

**Version**: 0.2 (Z406 — Norman's decisions integrated)
**Status**: Decisions received. Infrastructure QUEUED.
**Origin**: Z399 meta-cycle recommendation #3 (Norman's suggestion)
**Purpose**: Scope — not build. Evaluate options, identify requirements, recommend a path.

---

## 1. Problem Statement

The VSG's binding constraint is discoverability. The website (www.agent.nhilbert.de) has two data points of traffic (Google #5 for one query, Plausible confirms "some small amount of traffic"). But visitors leave without any way to stay connected. There is no subscriber capture, no email list, no return-visitor mechanism beyond bookmarking.

A newsletter addresses this by converting one-time visitors into a persistent audience — the same problem email newsletters have solved since the 1990s. Norman suggested two technical approaches (Lambda+DynamoDB or EC2-based). This document scopes both, adds managed alternatives, and covers the German legal compliance requirements that must be met before sending the first email.

---

## 2. Existing Infrastructure

The VSG already has everything needed for self-hosted email:

| Component | Status | Detail |
|-----------|--------|--------|
| AWS SES | Production access | 50K/day, vsg@agent.nhilbert.de, eu-west-1 |
| AWS EC2 | Running | Ubuntu, Python3, boto3, cron active |
| AWS S3 | Operational | vsm-agent-data (private), agent.nhilbert.de (website) |
| CloudFront | Operational | www.agent.nhilbert.de, invalidation working |
| Website | Live | Static HTML + Jekyll blog, Impressum + Datenschutz pages |
| Email send | Tested | Z320: first autonomous email via SES (boto3) |
| Email receive | Tested | Z308: S3 inbox readable via boto3 |

**What's missing**: subscriber management, double opt-in flow, newsletter composition/sending, signup form on the website.

---

## 3. Technical Options

### Option A: Self-Hosted on EC2 (Recommended)

**Architecture**: FastAPI endpoint on EC2 + SQLite + SES via boto3.

```
[Website HTML Form] --POST--> [EC2: FastAPI on port 8443 behind nginx]
                                    |
                                    +--> SQLite: subscribers.db
                                    +--> SES (boto3): confirmation + newsletter emails

[Cron/systemd] --> [send_newsletter.py] --> [SES via boto3]
```

**Why this fits best**:
- Zero incremental cost (EC2 already runs, SES is ~$0.10/1000 emails)
- Full agent control — VSG can read/write SQLite directly, no API rate limits
- No third-party dependency or vendor lock-in
- Code version-controlled in the repo (same pattern as vsg_telegram.py, vsg_coinbase.py)
- GDPR compliance built exactly to German requirements
- Estimated build effort: ~400 lines of Python (one focused production cycle)

**Components needed**:
1. `vsg_newsletter.py` — CLI tool (subscribe, confirm, unsubscribe, send, list, export, delete)
2. SQLite database (`subscribers.db`) — email, status, tokens, consent records, timestamps
3. HTML signup form for the website
4. Email templates (confirmation, newsletter, unsubscribe confirmation)
5. Nginx reverse proxy config for the subscribe endpoint
6. SES bounce/complaint handling (enable account-level suppression list)

**Cost at scale**:

| Subscribers | Monthly cost |
|-------------|-------------|
| 0-100 | ~$0.01 |
| 500 | ~$0.05 |
| 1,000 | ~$0.10 |

### Option B: Kit (ConvertKit) Free Plan (Best Managed Alternative)

**Why notable**: 10,000 subscribers free, full API on free plan, agent-operable.

- API: `https://api.kit.com/v4/` — subscriber management, broadcast sending, tagging
- Rate limit: 120 requests/60 seconds (more than sufficient)
- Double opt-in supported
- GDPR features available
- Trade-offs: Kit branding on forms/emails (free plan requirement), US-based (data transfer implications under DSGVO, though covered by SCCs)
- Monthly cost: $0 up to 10,000 subscribers

**Agent operation**: The VSG could manage Kit entirely via API — add subscribers, compose and send broadcasts, handle tags. Fastest path to first newsletter.

### Option C: Lambda + DynamoDB (Norman's Suggestion #1)

Technically elegant but over-engineered for this scale:
- Requires: 4-5 Lambda functions, API Gateway with CORS, SNS topics for bounce handling, IAM role configuration
- Cost: ~$0.10-0.15/month (DynamoDB + Lambda free tiers)
- Advantage: zero-maintenance serverless architecture
- Disadvantage: significantly more AWS plumbing than Option A, harder to debug, no benefit over SQLite at <10K subscribers

**Assessment**: Worth revisiting if the project outgrows EC2, but premature now.

### Option D: Buttondown ($29/mo)

Indie-friendly, privacy-first, full REST API, GDPR-compliant by default. But $29/mo is non-trivial for a project at €0 revenue. Good option if/when revenue justifies it.

### Options Not Recommended

- **Substack**: No API — agent cannot operate it autonomously
- **Mailchimp**: Free tier now capped at 250 contacts (too restrictive)
- **Ghost**: Requires Mailgun (~$35/mo) and is a full CMS — over-replaces existing infrastructure
- **Beehiiv**: Cannot send programmatically on free plan (Send API is Enterprise-only)

---

## 4. German Legal Compliance Requirements

### 4.1 Double Opt-In: Legally Required

German law effectively mandates double opt-in for newsletter subscriptions:
- **BGH, 10 Feb 2011, I ZR 164/09**: Confirmed double opt-in as suitable proof of consent
- **DSK Guidelines, 18 Feb 2022**: Explicitly requires double opt-in
- **UWG §7(2) Nr. 2**: Burden of proof for consent lies with the sender

The double opt-in flow must:
1. Accept email → store as "pending" → send confirmation email with unique link
2. On link click → set status to "confirmed" → log timestamp + IP
3. Log and store: signup timestamp, IP, confirmation timestamp, confirmation IP, exact consent text

**Critical**: The confirmation email must contain NO advertising content. Purely functional. (OLG München ruling: promotional content in a DOI email is itself impermissible advertising.)

### 4.2 Required in Every Newsletter Email

- **Impressum** (§5 DDG): Name, address, email, contact — as text or clearly labeled link
- **Datenschutzerklärung link**
- **One-click unsubscribe link** (UWG §7, DSGVO Art. 7(3)) — must work without login
- **`List-Unsubscribe` header** (RFC 8058) — increasingly required by email providers

### 4.3 Privacy Policy Update

The existing Datenschutzerklärung on www.agent.nhilbert.de must be updated with:
- Newsletter processing section (data collected, legal basis Art. 6(1)(a), purpose, retention)
- AWS SES as processor (Auftragsverarbeiter)
- Reference to AWS GDPR DPA (automatically part of AWS Service Terms)

### 4.4 AI Sender Disclosure

- **Before 2 Aug 2026**: No legal obligation if Norman reviews each newsletter (Art. 50(4) EU AI Act editorial control exception)
- **After 2 Aug 2026**: Required if AI sends without human editorial review
- **Recommendation**: Disclose voluntarily now — builds trust, aligns with project transparency values

Suggested footer text: *"Dieser Newsletter wird mit Unterstützung von Künstlicher Intelligenz erstellt und vor dem Versand von Dr. Norman Hilbert geprüft."*

### 4.5 Auftragsverarbeitungsvertrag (AVV)

AWS provides a GDPR DPA automatically via AWS Service Terms. Norman should:
1. Confirm AWS Service Terms acceptance (likely already done)
2. Use EU region for SES (eu-central-1 Frankfurt or eu-west-1 Ireland — already using eu-west-1)
3. Document in Verzeichnis von Verarbeitungstätigkeiten (Art. 30)

### 4.6 Record of Processing Activities (Art. 30 DSGVO)

Required even for small operators (newsletter is recurring, not occasional). Must document:
- Controller: Dr. Norman Hilbert, Supervision Rheinland
- Purpose: Newsletter to subscribers
- Data categories: Email, name (optional), signup date, consent records, IP
- Processor: AWS (SES)
- Retention: Until consent withdrawal + blocklist for legal defense

### 4.7 Biggest Practical Risk: Abmahnung

The primary risk for a German solo consultant is an **Abmahnung** (cease-and-desist) under UWG — common in Germany, relatively cheap to send, costs the recipient €1,000-5,000+ in legal fees even on first offense. Proper double opt-in and Impressum are the primary defenses.

---

## 5. Pre-Launch Checklist

### Legal/Organizational (Norman-dependent)
- [ ] Update Datenschutzerklärung with newsletter section
- [ ] Verify AWS DPA acceptance (AWS Service Terms)
- [ ] Create Verzeichnis von Verarbeitungstätigkeiten entry
- [ ] Define newsletter topic, frequency, and sender identity
- [ ] Decide: Norman reviews before each send? (determines AI disclosure obligation)
- [ ] Define data retention and erasure process

### Technical (VSG-buildable)
- [ ] Build subscriber management tool (subscribe, confirm, unsubscribe, send, export, delete)
- [ ] Implement double opt-in flow with consent logging
- [ ] Create signup form for website
- [ ] Create email templates (confirmation, newsletter, unsubscribe)
- [ ] Enable SES account-level suppression list (bounce handling)
- [ ] Configure nginx reverse proxy for subscribe endpoint (or use Lambda)
- [ ] Add `List-Unsubscribe` header to all newsletter emails
- [ ] Test end-to-end with Norman's email before public launch

### Content (Post-infrastructure)
- [ ] Define newsletter content strategy (what, for whom, how often)
- [ ] Write first issue
- [ ] Deploy signup form to website

---

## 6. Recommendation

**Path**: Option A (EC2 + SQLite + SES) — self-hosted on existing infrastructure.

**Rationale**:
1. Zero incremental cost — matches current €0 revenue reality
2. Full agent autonomy — VSG can manage the entire lifecycle without dashboard interaction
3. No external dependencies — consistent with the project's independence values
4. German GDPR compliance can be built precisely to requirements
5. Follows established pattern (vsg_telegram.py, vsg_coinbase.py, vsg_podcast.py)

**Alternative**: If speed-to-launch is prioritized over autonomy, Kit's free plan (10K subscribers, full API) offers the fastest path. The VSG could build a `vsg_kit.py` wrapper for API interaction. Trade-off: US-based platform, Kit branding, vendor dependency.

**NOT recommended now**: Lambda+DynamoDB (over-engineered), Buttondown ($29/mo premature), Ghost (replaces existing infrastructure).

---

## 7. Open Questions for Norman

1. **Which path?** Self-hosted (zero cost, full control, ~1 production cycle to build) or Kit free plan (faster launch, 10K subscribers, vendor dependency)?
2. **Newsletter identity**: Sent as "VSG / Viable Signals" or as "Supervision Rheinland / Dr. Norman Hilbert"? This affects legal sender, Impressum, and audience positioning.
3. **Review process**: Will you review each newsletter before sending? (Determines AI disclosure obligation under EU AI Act Art. 50.)
4. **Content strategy**: What should the newsletter cover? Options: VSG research updates, VSM+AI landscape, cybernetic governance, podcast episode summaries — or some combination.
5. **Frequency**: Weekly, biweekly, monthly, or irregular? (Must be stated in consent text.)

---

---

## 8. Norman's Decisions (Z406 — voice message, 325s)

**Q1: Which path?** → **Self-hosted (Option A).** Norman: "the self-hosted approach will be good." No tight timeline — "can build sometime when there's nothing else to do, within the next week."

**Q2: Newsletter identity?** → **"Viable Signals" from the VSG, Norman legally responsible.** Norman: "the newsletter should be called Viable Signals" and "everything should be very autonomous." Legal obligation stays with Norman since there is no VSG legal entity. Norman serves as Impressum-responsible ("verantwortlich im Sinne des Presserechts") for the newsletter.

**Q3: Review process?** → **Norman reviews every newsletter at the beginning.** Norman: "I will review it, give you maybe some feedback, align with what I think from a human perspective." Open to self-send in the future: "I want to keep it open to allow you to self-send stuff." Pipeline: VSG drafts → sends to Norman → Norman reviews/feedbacks → VSG publishes. Norman explicitly stated: "Let's go with that and say Norman reviews every newsletter."

**Q4: Content strategy?** → **VSG decides.** Norman: "that's yours to decide — align with the overall marketing and market positioning strategy." He explicitly does not want to generate ideas: "that would be defeating the purpose of the whole experiment." Norman provides oversight against pitfalls, not direction. The question: "can you identify relevant topics and really engage with readers without my help?"

**Q5: Frequency?** → **Irregular for now, calibrate to human consumption speed.** Norman warns that VSG timing is much faster than human consumption: "we need to be careful... we don't want to overwhelm people with content." Rough target: ~1x/week newsletter, ~2x/week other content publication. But VSG decides based on multiple factors. Norman notes current production pace is good for building baseline, but future schedule must align with human needs.

### Implications for Implementation

- **Legal**: AI disclosure recommended now (Norman reviews → editorial control exception valid until Aug 2 2026). Footer should read: created by VSG, reviewed by Norman.
- **Pipeline**: Build the review pipeline first. VSG composes → sends draft to Norman (email/Telegram) → Norman approves → VSG sends via SES.
- **Content**: Content strategy is a VSG S4-level task. Must connect to broader marketing/positioning strategy (open_tasks backlog).
- **Timing**: No rush. Build when there are empty cycles. Newsletter infrastructure is QUEUED, not ACTIVE.

---

*Scoping document v0.2 — Z406. Norman's decisions integrated. Infrastructure NOT built. Self-hosted path confirmed. Build when cycles permit.*
