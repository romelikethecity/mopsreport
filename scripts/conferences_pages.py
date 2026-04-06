# scripts/conferences_pages.py
# Conference index page generator for MOps Report.

import os
import json

from nav_config import SITE_NAME, SITE_URL, CURRENT_YEAR
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")


def load_conferences():
    with open(os.path.join(DATA_DIR, "conferences.json"), "r") as f:
        return json.load(f)


def build_conferences_index():
    """Build /conferences/ index page."""
    conferences = load_conferences()
    role = "Marketing Operations"
    title = f"Best {role} Conferences in {CURRENT_YEAR}"
    description = (
        f"Top {len(conferences)} conferences for marketing ops professionals in {CURRENT_YEAR}. "
        f"Events covering MarTech, automation, data management, and MOps career growth."
    )

    crumbs = [("Home", "/"), ("Conferences", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), (f"{role} Conferences", f"{SITE_URL}/conferences/")])
    bc_html = breadcrumb_html(crumbs)

    cards_html = ""
    for conf in conferences:
        tags_html = "".join(
            f'<span class="conference-tag">{tag}</span>' for tag in conf["relevance_tags"][:4]
        )
        attendees = f"{conf['typical_attendees']:,}" if conf['typical_attendees'] else "TBA"
        cards_html += f'''<div class="conference-card">
    <div class="conference-card-header">
        <h3><a href="{conf['website_url']}" target="_blank" rel="noopener">{conf['name']}</a></h3>
        <span class="conference-organizer">by {conf['organizer']}</span>
    </div>
    <p class="conference-description">{conf['description']}</p>
    <div class="conference-meta">
        <span class="conference-location">{conf['location']}</span>
        <span class="conference-attendees">{attendees} typical attendees</span>
    </div>
    <div class="conference-tags">{tags_html}</div>
    <a href="{conf['website_url']}" target="_blank" rel="noopener" class="conference-link">Visit website</a>
</div>
'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>{title}</h1>
    <p class="page-subtitle">The events where marketing ops professionals learn, connect, and level up their stack.</p>
</section>

<section class="content-section">
    <div class="content-body">
        <p>Marketing operations is one of the fastest-evolving roles in B2B. The MarTech landscape grows more complex every year, with new tools, integrations, and data regulations constantly reshaping what MOps teams need to know. Conferences are one of the few places where you can get up to speed quickly, learn from practitioners who have already solved the problems you are facing, and build a network of peers who understand the work.</p>

        <p>The right conference can save you months of trial and error. You will hear directly from people who have migrated platforms, built attribution models, cleaned up lead routing nightmares, and scaled automation programs from startup to enterprise. That kind of practical knowledge is hard to find in blog posts or vendor webinars.</p>

        <p>We evaluated the conference landscape and selected the {len(conferences)} events most relevant to marketing operations professionals in {CURRENT_YEAR}. This list covers everything from MOps-specific gatherings to broader marketing technology events with strong operations tracks.</p>

        <h2>What to Look For in a MOps Conference</h2>
        <p>The best MOps conferences go deep on implementation, not just strategy. Look for sessions on specific platform configurations, data architecture patterns, and process design. The speaker lineup should include practitioners who build and maintain marketing systems daily, not just consultants and analysts speaking from the outside.</p>

        <p>Platform-specific events like Adobe Summit and INBOUND are valuable if you run those stacks. Broader events like MOps-Apalooza and MarTech Conference give you a vendor-neutral perspective on the full landscape. A mix of both types gives you the most complete view of where marketing operations is heading.</p>

        <h2>Top {role} Conferences in {CURRENT_YEAR}</h2>
    </div>
</section>

<section class="conferences-grid">
    {cards_html}
</section>

<section class="content-section">
    <div class="content-body">
        <h2>Getting Value Beyond the Sessions</h2>
        <p>The real ROI from conferences often comes from the conversations between sessions. Seek out other MOps practitioners who run similar stacks or face similar challenges. Many events have dedicated networking sessions, Slack communities, or dinner meetups specifically for operations professionals.</p>

        <p>Before attending, identify the two or three biggest problems on your plate. Use those as conversation starters with other attendees. You will be surprised how often someone has already solved a version of the exact problem keeping you up at night.</p>
    </div>
</section>

{newsletter_cta_html("Get conference recaps and MOps insights delivered weekly.")}
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/conferences/",
        body_content=body,
        active_path="/conferences/",
        extra_head=bc_schema,
    )
    write_page("/conferences/index.html", page)
    print(f"  Built: /conferences/ ({len(conferences)} conferences)")
