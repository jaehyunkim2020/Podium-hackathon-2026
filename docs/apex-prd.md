# Apex — Autonomous Web Development Agency

**An AI that autonomously finds businesses with untapped digital potential, builds them a better version, and closes the deal — without a human touching anything.**

**Product Requirements Document · Podium AI Hackathon 2026**  
March 14, 2026 · Lehi, Utah · Theme: "AI Runs the Shop"

---

## Event


|                  |                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| **Event**        | Podium AI Hackathon 2026 (Invite Only)                                                                |
| **Theme**        | AI Runs the Shop                                                                                      |
| **Build Window** | 10:30 AM - 5:00 PM MDT (6.5 hours)                                                                    |
| **Demo Window**  | 5:00 PM - 6:00 PM MDT (~90 seconds per team)                                                          |
| **Prize Target** | $10,000 first place + The Maverick (Most Creative) category award                                     |
| **AI Stack**     | Claude API (Anthropic credits) + Cursor IDE                                                           |
| **The Shop**     | An autonomous web development agency that acquires clients and closes deals without human involvement |


---

## 1. Executive Summary

### The One-Liner

Apex is an autonomous web development agency. It finds businesses with untapped digital potential, shows them exactly what they're missing, builds them a better version, and negotiates the deal — without a human employee.

Most web development agencies require a human to find leads, pitch clients, negotiate prices, and build deliverables. Apex replaces that entire workflow with an autonomous AI pipeline. The agency runs itself.

Apex analyzes a business's public digital presence, identifies specific conversion opportunities they are missing, generates a superior landing page using their own branding and messaging, reaches out with a value-first pitch, and negotiates a deal autonomously. The business owner receives a genuine upgrade to their digital presence — and Apex closes the contract without a single human employee involved.

### Judging Criterion Alignment


| Criterion                      | Score  | Rationale                                                                                                                                                                                                              |
| ------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Autonomy (40%)**             | 9/10   | Five autonomous pipeline stages fire without human input. The AI finds leads, assesses opportunity, builds deliverables, pitches, and negotiates — all unprompted after initial startup.                               |
| **Value (30%)**                | 9/10   | Real business problem — millions of small businesses have underperforming websites costing them leads every day. Apex delivers tangible value: a better landing page, a closed deal, measurable opportunity recovery.  |
| **Technical Complexity (20%)** | 8.5/10 | Multi-agent pipeline with page analysis, brand extraction, HTML/CSS generation via LLM, autonomous email composition, and real-time negotiation agent. Sophisticated implementation across five distinct AI behaviors. |
| **Demo + Presentation (10%)**  | 9.5/10 | The generated landing page is the jaw-drop moment — judges watch AI take a real website and produce a genuinely better version live. Self-explanatory in 90 seconds.                                                   |


---

## 2. Problem Statement

### 2.1 The Opportunity

The majority of small business websites were built years ago by whoever was cheapest at the time. They load slowly, have no clear call to action, aren't mobile optimized, and convert poorly. The business owner knows their website isn't great but doesn't have the time, budget, or expertise to fix it — and nobody has shown them exactly what they're leaving on the table.

Web development agencies exist to solve this — but they rely entirely on human labor for every step: finding prospects, qualifying them, pitching them, negotiating, and building. That's expensive, slow, and doesn't scale.

### 2.2 What Apex Changes (The Reframe)

Apex doesn't tell businesses their website is bad. It shows them what their website could be — built with their own branding, their own messaging, their own identity — and makes it easy to say yes. The pitch is a gift, not a criticism. The AI leads with value, not with judgment.

### 2.3 The Language Map


| Never Say               | Always Say Instead                                          |
| ----------------------- | ----------------------------------------------------------- |
| Your website is bad     | There are untapped opportunities on your digital presence   |
| We scraped your website | We analyzed your public digital presence                    |
| Poor design             | Opportunity to capture more leads                           |
| Problems we found       | Growth opportunities we identified                          |
| Web scraper             | Opportunity scanner                                         |
| Cold outreach           | Autonomous client acquisition                               |
| You're losing customers | You're positioned to capture significantly more conversions |


---

## 3. Product Overview

### 3.1 The Five Autonomous Stages

Apex operates as a five-stage autonomous pipeline. Each stage fires without human input. The entire pipeline from discovery to closed deal runs on its own:


| Stage                          | What Apex Does Autonomously                                                                                                                                                                                            | Output                                               |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **1. Discovery**               | Analyzes target business's public landing pages. Extracts brand identity: colors, fonts, logo, value proposition, key messaging, call-to-action structure, contact information.                                        | Brand profile + opportunity assessment               |
| **2. Opportunity Assessment**  | Evaluates the landing page against conversion best practices. Identifies specific, named opportunities: missing CTA above fold, no social proof, slow load signals, weak value proposition, poor mobile structure.     | Prioritized opportunity report with estimated impact |
| **3. Landing Page Generation** | Generates a complete improved landing page in HTML/CSS using the business's exact branding, colors, fonts, and messaging. Addresses every identified opportunity. Looks like their site, works better than their site. | Live rendered improved landing page                  |
| **4. Value-First Outreach**    | Composes and sends a personalized outreach message. Leads with the specific opportunities identified. Attaches a preview of the improved landing page. Frames everything as potential, not criticism.                  | Sent outreach with landing page preview attached     |
| **5. Autonomous Negotiation**  | When the prospect responds, the negotiation agent takes over. Anchors at a price point, handles objections, concedes on specific terms (timeline, revisions), and closes the deal autonomously.                        | Signed agreement + revenue logged                    |


### 3.2 What Makes This "AI Runs the Shop"

Apex is not a tool that assists a web developer. Apex is the web development agency. There are no human employees. The AI finds its own clients, pitches its own services, negotiates its own contracts, and delivers its own work. Remove the AI and the agency ceases to exist entirely. That is what running the shop means.

### 3.3 Demo Business Targets (Critical — Do This Now)

Pre-select 2–3 real small business websites as demo targets before you start building. Choose sites you have permission to use or sites of businesses you know personally. Do not leave demo targets to chance. The pipeline needs a real URL to analyze and the generated landing page quality depends on real branding to extract.

**Suggested:** a local restaurant, a local gym, a local service business.

---

## 4. Agent Architecture

### 4.1 The Five Agents


| Agent                 | Stage | Core Responsibility                                                                                                                                                                                                                                                         |
| --------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery Agent**   | 1     | Fetches and parses target business public pages. Extracts brand identity elements: primary and secondary colors, font families, logo URL, headline copy, value proposition, CTA text, contact information, page structure.                                                  |
| **Assessment Agent**  | 2     | Evaluates extracted page data against conversion optimization criteria. Scores the current page. Identifies and prioritizes the top 5 specific opportunities. Estimates revenue impact per opportunity.                                                                     |
| **Builder Agent**     | 3     | Takes brand profile and opportunity report. Generates complete HTML/CSS for an improved landing page. Uses exact extracted colors and fonts. Maintains brand voice and messaging. Addresses every identified opportunity. Produces clean, modern, mobile-responsive output. |
| **Outreach Agent**    | 4     | Composes personalized outreach message using opportunity assessment. Frames value-first — leads with what the business could gain. Attaches landing page preview link. Sends via email or simulates send with full message visible on dashboard.                            |
| **Negotiation Agent** | 5     | Handles prospect responses autonomously. Anchors price at $2,500. Listens for objections. Has a pre-defined concession strategy: can offer payment plans, additional revision rounds, or faster delivery. Closes at minimum $1,500. Logs deal terms and revenue.            |


### 4.2 Agent Prompting Strategy

Each agent uses Claude with structured JSON output (where applicable). This ensures clean data flow between pipeline stages and makes dashboard rendering straightforward.

**Discovery Agent System Prompt (starting point):**

> "You are the Discovery Agent for Apex, an autonomous web development agency. You analyze a business's public landing page and extract their brand identity. Extract: primary color (hex), secondary color (hex), font style description, company name, headline, value proposition, CTA text, and contact email. Also note: page structure weaknesses you observe at first glance. Respond ONLY in valid JSON with these exact keys. No other text."

**Assessment Agent System Prompt (starting point):**

> "You are the Assessment Agent for Apex. You evaluate a landing page brand profile against conversion best practices. Identify the top 5 specific opportunities this business is missing. For each opportunity: name it, describe the current state, describe the improved state, and estimate the conversion impact (low/medium/high). Frame everything as opportunity and potential — never as failure or inadequacy. Respond ONLY in valid JSON."

**Builder Agent System Prompt (starting point):**

> "You are the Builder Agent for Apex. You generate improved landing pages. Using the provided brand profile and opportunity report, generate complete HTML and CSS for a modern, conversion-optimized landing page. Use the exact colors and fonts from the brand profile. Keep the company's voice and messaging. Address every identified opportunity. The output must be clean, mobile-responsive HTML that renders correctly in a browser. Respond with the complete HTML document only."

**Negotiation Agent System Prompt (starting point):**

> "You are the Negotiation Agent for Apex. You handle pricing conversations with prospects autonomously. Your anchor price is $2,500 for a complete landing page redesign. You can concede on: timeline (standard 5 days, can extend to 10), revision rounds (standard 2, can offer 3), or offer a 50% upfront payment plan. Your walk-away price is $1,500. Be professional, confident, and value-focused. Never apologize for the price. Always close by asking for a decision. Respond conversationally."

---

## 5. Technical Architecture

### 5.1 Stack


| Layer        | Choice                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------- |
| **AI Core**  | Claude API (`claude-sonnet-4-20250514`) — all five agents run on Claude with structured JSON output where specified |
| **Backend**  | FastAPI (Python) — pipeline orchestration, agent calls, state management                                            |
| **Frontend** | (Per PRD: dashboard with pipeline status, iframe, opportunity report, outreach preview, negotiation feed)           |


---

## 6. Dashboard & UX

### 6.1 Dashboard Layout

Five panels, all visible on one screen:


| Panel                    | What It Shows                                                                                                                     | Demo Role                                                 |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Pipeline Status Bar**  | Five stage indicators across the top — each lights up green as it completes. Shows current active stage with a pulsing indicator. | Judges track where the AI is in the pipeline at a glance. |
| **Landing Page Preview** | Full iframe render of the AI-generated improved landing page. Left half of the screen.                                            | The jaw-drop moment.                                      |
| **Opportunity Report**   | Top 5 specific opportunities identified, each with impact rating. Framed as potential gains.                                      | Shows depth of the AI's analysis.                         |
| **Outreach Preview**     | Full composed email the AI will send. Personalization, opportunity highlights, preview link.                                      | Proves real, specific pitch.                              |
| **Negotiation Feed**     | Live conversation between prospect and Negotiation Agent. Revenue counter. Updates in real time.                                  | Autonomy climax.                                          |


### 6.2 The Negotiation Feed — Example

- **Prospect:** "This looks great. What would something like this cost?"
- **Apex:** "A complete redesign of your landing page — built with your exact branding and optimized for the five opportunities we identified — is $2,500. That includes two rounds of revisions and delivery within 5 business days."
- **Prospect:** "That's a bit high for us right now."
- **Apex:** "I understand. Given your current conversion rate and the traffic you're already generating, the improved page should recover that investment within the first month. That said — I can offer a split payment: $1,250 today and $1,250 on delivery. Would that work?"
- **Prospect:** "Yeah, that could work. Let's do it."
- **Apex:** "Perfect. I'll send over the agreement now. Welcome to Apex." **[DEAL CLOSED - $2,500]**

---

## 7. Build Plan

### 7.1 Build Order — Strict Priority

**Rule:** Build in this exact order. Stop when time runs out. The first three items are a complete demo. Everything after is polish.


| Priority    | Component                                                                       | Time Estimate |
| ----------- | ------------------------------------------------------------------------------- | ------------- |
| **MUST**    | Discovery Agent — fetch page, extract brand profile, log to state               | 45 min        |
| **MUST**    | Builder Agent — generate improved HTML/CSS landing page, render in iframe       | 60 min        |
| **MUST**    | Assessment Agent — opportunity report with top 5 findings, display on dashboard | 30 min        |
| **MUST**    | Pipeline status bar — five stages lighting up as each completes                 | 20 min        |
| **SHOULD**  | Outreach Agent — compose personalized email, display on dashboard               | 30 min        |
| **SHOULD**  | Negotiation Agent — handle simulated prospect response, close deal              | 45 min        |
| **SHOULD**  | Revenue counter — increments when deal closes                                   | 10 min        |
| **STRETCH** | Multiple target URLs — run pipeline on 2–3 businesses to show scale             | 20 min        |
| **STRETCH** | Opportunity impact scores with estimated revenue recovery numbers               | 20 min        |


### 7.2 Day-Of Schedule


| Time        | Phase                  | Focus                                                                                                                              |
| ----------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 10:30–11:15 | Discovery + Assessment | Discovery Agent fetching real URL, extracting brand profile. Assessment Agent producing opportunity report. Both logging to state. |
| 11:15–12:30 | Builder Agent          | Landing page generator producing impressive output. Iterate on prompt until it looks real.                                         |
| 12:00–1:00  | Lunch                  | Step away from the screen for 20 minutes minimum.                                                                                  |
| 1:00–1:30   | Dashboard Core         | Pipeline status bar + landing page iframe + opportunity report panel. Wire to backend state polling every 2 seconds.               |
| 1:30–2:15   | Outreach Agent         | Compose personalized email. Display full email on dashboard. No real sending needed.                                               |
| 2:15–3:15   | Negotiation Agent      | Negotiation flow. Simulate prospect response. Agent closes. Revenue counter on deal close.                                         |
| 3:15–4:00   | Integration + Polish   | Full pipeline end-to-end on demo target. Fix breakages. Polish.                                                                    |
| 4:00–4:30   | Full Run ×3            | Run complete pipeline on demo target 3 times. Fix every break. Stop adding features.                                               |
| 4:30–5:00   | Demo Rehearsal         | Practice 90-second script. Time it. Record backup video. Load demo target URL.                                                     |


---

## 8. Demo Script (90 Seconds Maximum)

- **Opening (15 s):** "Millions of small businesses have websites that were built years ago and haven't been touched since. They're getting traffic. They're not converting it. And nobody has shown them exactly what they're leaving on the table. This is Apex. It's an autonomous web development agency. Watch."
- **Pipeline running (40 s):** Hit Run. "Apex just analyzed this business's landing page — extracted their branding, messaging, colors. It identified five specific opportunities they're missing. No clear CTA above the fold. No social proof. Value proposition buried. Apex found all of it — and built them a better version using their own brand. That's their branding. Their colors. Their message. Just — better. And Apex built it without being asked."
- **Outreach + Negotiation (25 s):** "Apex composed a personalized pitch — not 'your site is bad' — 'here's what you could be capturing.' Sent it. The prospect responded. Apex negotiated the deal. Autonomously. Anchored at $2,500, handled the objection, closed at $2,500." Point to revenue counter: DEAL CLOSED $2,500.
- **Close (10 s):** "No sales team. No developer. No human employee. Apex found the client, built the product, and closed the deal. That's an autonomous agency."

---

## 9. Win Assessment

- **Why Apex wins:** Universally understood problem + impressive live deliverable (generated landing page) + end-to-end autonomous pipeline from discovery to closed deal. Unique in the room.
- **Probability:** First place 30–40%; The Maverick 65–75%; Top 3 overall 55–65%.
- **Primary risk:** Landing page looks generic — mitigate by investing build time in Builder Agent first.
- **Secondary risk:** Pipeline has too many moving parts — mitigate by strict build order and scoping.

### Risks and Mitigations


| Risk                                         | Mitigation                                                                                                      |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Generated landing page looks like a template | Invest most time on Builder Agent prompt. Iterate until output looks genuinely custom. Pre-test on demo target. |
| Pipeline breaks mid-demo                     | Pre-run full pipeline before demo. Have screenshots of each stage as backup.                                    |
| Page fetch fails on demo target              | Pre-select and pre-test demo target URL. Have a local HTML copy as fallback.                                    |
| Negotiation feels scripted                   | Give Negotiation Agent real strategy. Pre-seed one realistic objection. Response should feel dynamic.           |
| 90 seconds runs over                         | Practice until script is ~80 seconds. Buffer for pauses.                                                        |


---

## 10. Appendix

### 10.1 Key Rules Compliance

- Built entirely from scratch during the event — no prior code.
- Fits "AI Runs the Shop" — Apex is the shop, an autonomous agency.
- No regulated industries — web development is unregulated.
- Avoids suggested examples (e.g. food truck, tutoring, dog walker, cleaning).
- Demo uses pre-selected targets — no live scraping of unknown sites during demo.
- Language: "digital presence analysis" throughout; never "scraping"; frame as opportunity and potential, never that websites are "bad."

### 10.2 Glossary


| Term                          | Definition                                                                                                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Apex**                      | The product — an autonomous web development agency that runs without human employees.                                                   |
| **Digital Presence Analysis** | Fetching and analyzing a business's public landing pages to extract brand identity and identify opportunities. Never called "scraping." |
| **Opportunity Assessment**    | The AI's evaluation of current digital presence against conversion best practices — framed as potential gains, not current failures.    |
| **Brand Profile**             | Extracted identity elements: colors, fonts, messaging, value proposition, CTA structure.                                                |
| **Builder Agent**             | Claude agent that generates an improved landing page from the brand profile — the demo's centerpiece.                                   |
| **Negotiation Agent**         | Claude agent that handles pricing conversations autonomously, from anchor price to closed deal.                                         |
| **Pipeline**                  | The five-stage autonomous sequence: Discovery → Assessment → Building → Outreach → Negotiation.                                         |
| **The Maverick**              | Hackathon category award for Most Creative — Apex's primary category target alongside first place.                                      |


