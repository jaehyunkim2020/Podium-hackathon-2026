"""
Pydantic models for pipeline data. Used by agents and API.
"""
from pydantic import BaseModel, Field
from typing import Optional


class BrandProfile(BaseModel):
    """Output of Discovery Agent — extracted brand identity from a landing page."""
    primary_color: str = Field(description="Primary brand color in hex, e.g. #1a1a2e")
    secondary_color: str = Field(description="Secondary brand color in hex")
    font_style_description: str = Field(description="e.g. 'sans-serif, modern' or 'serif, traditional'")
    company_name: str = Field(description="Business name as shown on the page")
    headline: str = Field(description="Main headline text")
    value_proposition: str = Field(description="Core value proposition or tagline")
    cta_text: str = Field(description="Main call-to-action button/link text")
    contact_email: Optional[str] = Field(default=None, description="Contact email if visible")
    page_structure_weaknesses: Optional[str] = Field(
        default=None,
        description="Brief note on structure weaknesses observed at first glance"
    )
