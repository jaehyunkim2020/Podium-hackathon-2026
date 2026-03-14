"""
Outreach Agent — composes a personalized cold email for a prospect.

Uses Claude to write a short, value-first email using the brand profile
and optional landing page URL. Does not send; caller handles SMTP or simulated send.
"""
import os
from typing import Optional

from anthropic import Anthropic

OUTREACH_SYSTEM_PROMPT = """You are the Outreach Agent for Apex, an autonomous web development agency. You write personalized cold emails to small business owners.

Rules:
- Lead with value: mention what we built for them (a better landing page), not that their site is bad.
- Use their business name and keep the tone professional and friendly.
- If a landing page URL is provided, mention they can see their new page at that link.
- Keep the email short: one short paragraph plus a soft CTA (e.g. "Reply if you'd like to go live").
- No hype or spammy language. Sound like a helpful agency, not a sales bot.

Respond with exactly two lines, no other text:
Line 1: SUBJECT: <the email subject line>
Line 2: BODY: <the email body, plain text. Use \\n for newlines inside the body.>"""


def compose_outreach_email(
    company_name: str,
    value_proposition: str,
    contact_email: Optional[str] = None,
    lp_url: Optional[str] = None,
    opportunities_summary: Optional[str] = None,
    api_key: Optional[str] = None,
) -> tuple[str, str]:
    """
    Use Claude to compose a personalized outreach email. Returns (subject, body).
    """
    resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not resolved_key or not resolved_key.strip():
        raise ValueError(
            "Anthropic API key not set. Set ANTHROPIC_API_KEY in your environment."
        )

    parts = [
        f"Company name: {company_name}",
        f"Their value proposition: {value_proposition}",
    ]
    if lp_url:
        parts.append(f"We built them a new landing page. Live URL: {lp_url}")
    if opportunities_summary:
        parts.append(f"Opportunities we addressed: {opportunities_summary}")
    if contact_email:
        parts.append(f"Send to: {contact_email}")

    user_message = "Compose one cold email for this prospect.\n\n" + "\n".join(parts)

    client = Anthropic(api_key=resolved_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=OUTREACH_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    block = response.content[0]
    if block.type != "text":
        raise ValueError("Unexpected non-text block from Claude")
    text = block.text.strip()

    subject = ""
    body = ""
    for line in text.split("\n"):
        line = line.strip()
        if line.upper().startswith("SUBJECT:"):
            subject = line.split(":", 1)[1].strip()
        elif line.upper().startswith("BODY:"):
            body = line.split(":", 1)[1].strip().replace("\\n", "\n")

    if not subject or not body:
        raise ValueError("Claude did not return SUBJECT and BODY in the expected format")
    return subject, body
