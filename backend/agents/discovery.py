"""
Discovery Agent — Stage 1 of the Apex pipeline.

Fetches a business's public landing page, then uses Claude to extract
brand identity (colors, fonts, messaging, CTA, contact) and returns
a structured BrandProfile. No human input after the URL is provided.
"""
import json
import os
from typing import Optional

import httpx
from anthropic import Anthropic

from backend.models import BrandProfile

DISCOVERY_SYSTEM_PROMPT = """You are the Discovery Agent for Apex, an autonomous web development agency. You analyze a business's public landing page and extract their brand identity.

Extract the following. If something is not clearly present, infer from context or use a sensible default (e.g. "Not specified" for missing text, "#333333" for a missing color).

- primary_color: primary brand color as hex (e.g. #1a1a2e)
- secondary_color: secondary/accent color as hex
- font_style_description: brief description of font style (e.g. "sans-serif, modern" or "serif, traditional")
- company_name: business name as shown on the page
- headline: main headline text
- value_proposition: core value proposition or tagline
- cta_text: main call-to-action button or link text
- contact_email: contact email if visible, otherwise null
- page_structure_weaknesses: one or two sentences on page structure weaknesses you notice at first glance (e.g. no clear CTA above fold, dense text). Be concise. If none obvious, say "None noted."

Respond ONLY with a single valid JSON object with exactly these keys. No markdown, no code block wrapper, no other text."""


# Longer connect timeout: some sites are slow or strict on SSL handshake.
# First arg is default for read/write/pool; connect is overridden.
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=25.0)


def fetch_page_html(url: str, timeout: Optional[httpx.Timeout] = None) -> str:
    """
    Fetch the raw HTML of a URL. Used to supply the Discovery Agent with page content.

    Raises httpx.HTTPError on request failure. Caller can catch and return a friendly error.
    """
    timeout = timeout or DEFAULT_TIMEOUT
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.text


def extract_json_from_response(text: str) -> dict:
    """
    Claude sometimes wraps JSON in markdown code blocks. This strips that and
    returns the first JSON object found so we can parse reliably.
    """
    text = text.strip()
    # Remove optional markdown code fence
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    # Find first { ... } and parse
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in response")
    depth = 0
    end = -1
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end == -1:
        raise ValueError("Unbalanced braces in response")
    return json.loads(text[start : end + 1])


def run_discovery(url: str, html: Optional[str] = None, api_key: Optional[str] = None) -> BrandProfile:
    """
    Run the Discovery Agent: optionally fetch HTML from url, then call Claude
    to extract a BrandProfile. If html is provided, url is still passed for context
    but the given html is used (useful for local/demo fallback).

    Args:
        url: Target business landing page URL (for context and when html is None).
        html: Optional pre-fetched HTML. If None, we fetch from url.
        api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY from environment.

    Returns:
        BrandProfile populated from Claude's JSON response.

    Raises:
        httpx.HTTPError: When fetch fails.
        ValueError: When Claude's response doesn't contain valid JSON.
    """
    if html is None:
        html = fetch_page_html(url)

    # Resolve API key: explicit arg > env var
    resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not resolved_key or not resolved_key.strip():
        raise ValueError(
            "Anthropic API key not set. Set the ANTHROPIC_API_KEY environment variable "
            "(e.g. in PowerShell: $env:ANTHROPIC_API_KEY = 'sk-ant-...') and restart the server."
        )

    # Keep prompt size reasonable: cap HTML length so we don't blow context
    max_html_chars = 80_000
    if len(html) > max_html_chars:
        html = html[:max_html_chars] + "\n\n... [truncated for analysis]"

    client = Anthropic(api_key=resolved_key)
    user_message = f"Analyze this landing page HTML and extract the brand profile.\n\nURL: {url}\n\nHTML:\n{html}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=DISCOVERY_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    block = response.content[0]
    if block.type != "text":
        raise ValueError("Unexpected non-text block in Claude response")
    text = block.text

    data = extract_json_from_response(text)
    return BrandProfile.model_validate(data)
