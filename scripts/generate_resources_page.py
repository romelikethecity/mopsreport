#!/usr/bin/env python3
"""
Generate the marketing ops resources page with native MOps Report branding.
Canonical points to thegtmindex.com/marketing-ops/.
"""

import os
import sys
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import get_page_wrapper, write_page, breadcrumb_html
import templates

PROJECT_ROOT = os.path.dirname(script_dir)

CANONICAL_URL = "https://thegtmindex.com/marketing-ops/"
TITLE = "Best Resources for Marketing Ops Professionals in 2026"
DESCRIPTION = "Curated list of the best newsletters, communities, tools, and career resources for marketing operations professionals."
INTRO = """Marketing operations is the technical backbone of every marketing team. You own the martech stack, manage data flows, build automations, and make sure campaigns actually reach the right people.

We built this list for MOPs professionals who want to level up without wading through vendor content marketing. Every resource here was recommended by practitioners."""

SECTIONS = [
    {"title": "Newsletters", "items": [
        {"name": "Marrina Decisions Newsletter", "url": "https://marrinadecisions.com/", "desc": "Weekly playbooks for Marketing Ops, RevOps, and MarTech leaders."},
        {"name": "MarTech Daily Brief", "url": "https://martech.org/newsletters/", "desc": "Free daily newsletter delivering news and analysis on marketing technology and operations."},
        {"name": "The Martech Weekly", "url": "https://themartechweekly.com/blog/", "desc": "Weekly newsletter and blog covering the marketing technology ecosystem."},
    ]},
    {"title": "Blogs & Websites", "items": [
        {"name": "MarTech.org (MOPs Section)", "url": "https://martech.org/topic/marketing-operations/", "desc": "Marketing operations news, trends, and how-to guides from a major MarTech publication."},
        {"name": "ChiefMarTec", "url": "https://chiefmartec.com/blog/", "desc": "Scott Brinker's blog on marketing technology landscape. Publishes the annual MarTech supergraphic."},
        {"name": "Martech Zone", "url": "https://martech.zone/", "desc": "Weekly newsletter digest and publication for researching sales and marketing platforms."},
        {"name": "MOPs Report", "url": "https://mopsreport.com/", "desc": "Career intelligence and market data for marketing operations professionals.", "owned": True},
    ]},
    {"title": "Communities", "items": [
        {"name": "MO Pros (MarketingOps.com)", "url": "https://marketingops.com/", "desc": "#1 MOPs community with Slack group, forums, and Pro memberships for marketing ops professionals."},
        {"name": "MOPsPROs", "url": "https://www.mopspros.com/", "desc": "3,400+ member community with monthly MOPsTalks meetings, MOPsCON conference, and MOPsJOBs board."},
    ]},
    {"title": "Courses & Training", "items": [
        {"name": "HubSpot Academy", "url": "https://academy.hubspot.com/", "desc": "Free marketing automation certifications and courses covering ops-relevant skills."},
    ]},
]


def build_body():
    """Build the body HTML for the resource page."""
    accent = "var(--mops-accent, #0891B2)"
    text_sec = "var(--text-secondary, #E2E8F0)"
    text_muted = "var(--text-muted, #94A3B8)"

    html = []

    # Breadcrumb
    html.append(breadcrumb_html([("Home", "/"), (TITLE, None)]))

    # Hero
    html.append(f'''
<section style="max-width:800px;margin:0 auto;padding:2rem 1.5rem 1rem;">
  <h1 style="font-size:2.25rem;font-weight:800;margin-bottom:1rem;line-height:1.15;">{TITLE}</h1>
''')
    for para in INTRO.strip().split("\n\n"):
        html.append(f'  <p style="color:{text_sec};font-size:1.05rem;line-height:1.7;margin-bottom:1rem;">{para}</p>')
    html.append('</section>')

    # Sections
    for section in SECTIONS:
        html.append(f'''
<section style="max-width:800px;margin:0 auto;padding:1rem 1.5rem 2rem;">
  <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:1.25rem;padding-bottom:0.5rem;border-bottom:2px solid rgba(8,145,178,0.3);">{section["title"]}</h2>
  <ol style="list-style:none;padding:0;margin:0;">
''')
        for i, item in enumerate(section["items"], 1):
            owned_badge = f' <span style="display:inline-block;background:rgba(8,145,178,0.15);color:{accent};font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:4px;margin-left:8px;vertical-align:middle;letter-spacing:0.5px;">OUR PICK</span>' if item.get("owned") else ""
            html.append(f'''    <li style="margin-bottom:1.25rem;padding:1rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
      <span style="color:{accent};font-weight:700;margin-right:0.5rem;">{i}.</span>
      <a href="{item["url"]}" target="_blank" rel="noopener" style="color:{accent};font-weight:600;text-decoration:none;">{item["name"]}</a>{owned_badge}
      <p style="color:{text_sec};font-size:0.95rem;margin:0.5rem 0 0;line-height:1.6;">{item["desc"]}</p>
    </li>''')
        html.append('  </ol>\n</section>')

    # How We Curated
    html.append(f'''
<section style="max-width:800px;margin:0 auto;padding:1rem 1.5rem 2rem;">
  <div style="background:rgba(8,145,178,0.06);border:1px solid rgba(8,145,178,0.2);border-radius:12px;padding:1.5rem 2rem;">
    <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;">How We Curated This List</h3>
    <p style="color:{text_sec};font-size:0.95rem;line-height:1.7;margin-bottom:0.75rem;">Every resource on this page was evaluated based on editorial independence, content depth, community engagement, and practitioner recommendations. We prioritize sources that provide original analysis over aggregated content.</p>
    <p style="color:{text_sec};font-size:0.95rem;line-height:1.7;">This page is part of <a href="https://thegtmindex.com/" target="_blank" rel="noopener" style="color:{accent};">The GTM Index</a>, a curated directory of the best resources across go-to-market disciplines.</p>
  </div>
</section>
''')

    return "\n".join(html)


def main():
    output_dir = os.path.join(PROJECT_ROOT, "output")
    pages_dir = os.path.join(PROJECT_ROOT, "pages")
    templates.OUTPUT_DIR = output_dir
    templates.SKIP_OG = True

    body = build_body()

    page = get_page_wrapper(
        title=TITLE,
        description=DESCRIPTION,
        canonical_path="/best-marketing-ops-resources/",
        body_content=body,
    )

    # Replace the auto-generated canonical with our cross-site canonical
    page = re.sub(
        r'<link rel="canonical" href="https://mopsreport\.com/best-marketing-ops-resources/">',
        f'<link rel="canonical" href="{CANONICAL_URL}">',
        page
    )

    # Write to output/
    out_path = os.path.join(output_dir, "best-marketing-ops-resources", "index.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Wrote {out_path}")

    # Write to pages/
    pages_path = os.path.join(pages_dir, "best-marketing-ops-resources", "index.html")
    os.makedirs(os.path.dirname(pages_path), exist_ok=True)
    with open(pages_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Wrote {pages_path}")

    print("Done: MOPs Report resource page generated.")


if __name__ == "__main__":
    main()
