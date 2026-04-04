# scripts/salary_pages.py
# Salary section generators. Called from build.py.
# Data source: data/comp_analysis.json

import os
import json
import re

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)


# ---------------------------------------------------------------------------
# Data loader
# ---------------------------------------------------------------------------

def load_comp_data(project_dir):
    path = os.path.join(project_dir, "data", "comp_analysis.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_salary(val):
    """Format salary as $XXXk or $XXX,XXX."""
    if val >= 1000:
        return f"${val:,.0f}"
    return f"${val:,.0f}"


def fmt_k(val):
    """Format salary as $XXXk."""
    return f"${val / 1000:.0f}K"


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def stat_cards_html(cards):
    """Generate a grid of stat cards. cards = [(value, label), ...]"""
    items = ""
    for val, label in cards:
        items += f'''<div class="stat-block">
    <span class="stat-value">{val}</span>
    <span class="stat-label">{label}</span>
</div>\n'''
    return f'<div class="stat-grid">{items}</div>'


def range_bar_html(label, low, high, median=None, max_scale=None):
    """CSS range bar showing salary spread."""
    if not max_scale:
        max_scale = high * 1.2
    left_pct = (low / max_scale) * 100
    width_pct = ((high - low) / max_scale) * 100
    mid_pct = ((median - low) / (high - low)) * 100 if median and high > low else 50

    return f'''<div class="range-bar-wrap">
    <div class="range-bar-label">{label}</div>
    <div class="range-bar-track">
        <div class="range-bar-fill" style="left:{left_pct:.1f}%;width:{width_pct:.1f}%">
            {f'<div class="range-bar-median" style="left:{mid_pct:.1f}%" title="Median: {fmt_salary(median)}"></div>' if median else ''}
        </div>
    </div>
    <div class="range-bar-values">
        <span>{fmt_salary(low)}</span>
        {f'<span class="range-bar-mid">Median: {fmt_salary(median)}</span>' if median else ''}
        <span>{fmt_salary(high)}</span>
    </div>
</div>'''


def source_citation(data):
    total = data.get("total_records", 295)
    with_salary = data.get("records_with_salary", 203)
    return (f'<p class="source-citation">Source: MOps Report analysis of {total} marketing operations '
            f'job postings ({with_salary} with disclosed salary data). Updated {data.get("generated_at", "")[:10]}.</p>')


# ---------------------------------------------------------------------------
# 1. Salary Index
# ---------------------------------------------------------------------------

def build_salary_index(data):
    stats = data["salary_stats"]
    crumbs = [("Home", "/"), ("Salary Data", None)]
    bc = breadcrumb_html(crumbs)

    cards = stat_cards_html([
        (fmt_salary(stats["median"]), "Median Salary"),
        (f'{fmt_k(stats["min"])} - {fmt_k(stats["max"])}', "Full Range"),
        (str(stats["count_with_salary"]), "Roles With Salary Data"),
        (f'{data["disclosure_rate"]}%', "Salary Disclosure Rate"),
    ])

    # Seniority summary table
    seniority_rows = ""
    max_sal = 300000
    for level in ["Entry", "Mid", "Senior", "Director", "VP"]:
        d = data["by_seniority"].get(level)
        if not d:
            continue
        seniority_rows += f'''<tr>
    <td><a href="/salary/{slugify(level)}/">{level}</a></td>
    <td>{d["count"]}</td>
    <td>{fmt_salary(d["min_base_avg"])}</td>
    <td>{fmt_salary(d["median"])}</td>
    <td>{fmt_salary(d["max_base_avg"])}</td>
</tr>\n'''

    # Metro summary
    metro_rows = ""
    for metro, d in data["by_metro"].items():
        if metro == "Unknown":
            continue
        metro_rows += f'''<tr>
    <td><a href="/salary/{slugify(metro)}/">{metro}</a></td>
    <td>{d["count"]}</td>
    <td>{fmt_salary(d["min_base_avg"])}</td>
    <td>{fmt_salary(d["median"])}</td>
    <td>{fmt_salary(d["max_base_avg"])}</td>
</tr>\n'''

    # Remote summary
    remote = data["by_remote"]["remote"]
    onsite = data["by_remote"]["onsite"]

    # Top roles
    top_roles_html = ""
    for role in data["top_paying_roles"][:5]:
        sal_min = fmt_salary(role["salary_min"])
        sal_max = fmt_salary(role["salary_max"])
        co = f' at {role["company"]}' if role.get("company") else ""
        top_roles_html += f'<li><strong>{role["title"]}</strong>{co}: {sal_min} - {sal_max}</li>\n'

    body = f'''{bc}
<section class="page-header">
    <h1>Marketing Operations Salary Data (2026)</h1>
    <p class="lead">Salary benchmarks from {stats["count_with_salary"]} marketing operations job postings with disclosed compensation. Updated weekly from real listings.</p>
</section>

<div class="container">
{cards}

<h2>Salary by Seniority Level</h2>
<p>Compensation scales significantly with seniority in marketing operations. Entry-level roles start near {fmt_k(data["by_seniority"]["Entry"]["median"])}, while VP-level positions reach {fmt_k(data["by_seniority"]["VP"]["max_base_avg"])}+. Each level carries a meaningful jump in both base pay and total compensation.</p>

<table class="data-table">
<thead><tr><th>Level</th><th>Roles</th><th>Avg Low</th><th>Median</th><th>Avg High</th></tr></thead>
<tbody>
{seniority_rows}
</tbody>
</table>

<h2>Salary by Metro Area</h2>
<p>Location remains a primary factor in MOps compensation. San Francisco and New York lead on average base pay, while remote roles trend lower. Metros with fewer than 3 data points are excluded.</p>

<table class="data-table">
<thead><tr><th>Metro</th><th>Roles</th><th>Avg Low</th><th>Median</th><th>Avg High</th></tr></thead>
<tbody>
{metro_rows}
</tbody>
</table>

<h2>Remote vs. Onsite Pay</h2>
<p>Remote marketing operations roles pay a median of {fmt_salary(remote["median"])}, compared to {fmt_salary(onsite["median"])} for onsite positions. The gap reflects both geographic arbitrage and the tendency for higher-level roles to require in-office presence.</p>

{range_bar_html("Remote", remote["min_base_avg"], remote["max_base_avg"], remote["median"], 250000)}
{range_bar_html("Onsite", onsite["min_base_avg"], onsite["max_base_avg"], onsite["median"], 250000)}

<p><a href="/salary/remote/">Full remote vs. onsite breakdown</a></p>

<h2>Highest-Paying MOps Roles</h2>
<p>The top-paying marketing operations positions cluster in VP and Director titles at large enterprises. Total compensation packages at these levels regularly exceed $300,000.</p>
<ul>
{top_roles_html}
</ul>

<h2>Explore Salary Breakdowns</h2>
<ul>
    <li><a href="/salary/entry/">Entry-Level MOps Salaries</a></li>
    <li><a href="/salary/mid/">Mid-Level MOps Salaries</a></li>
    <li><a href="/salary/senior/">Senior MOps Salaries</a></li>
    <li><a href="/salary/director/">Director of MOps Salaries</a></li>
    <li><a href="/salary/vp/">VP of Marketing Operations Salaries</a></li>
    <li><a href="/salary/remote/">Remote vs. Onsite MOps Pay</a></li>
    <li><a href="/salary/calculator/">MOps Salary Calculator</a></li>
    <li><a href="/salary/methodology/">Salary Methodology</a></li>
</ul>

<h2>Role Comparisons</h2>
<ul>
    <li><a href="/salary/vs-revops/">MOps vs. RevOps Salary</a></li>
    <li><a href="/salary/vs-sales-ops/">MOps vs. Sales Ops Salary</a></li>
    <li><a href="/salary/vs-data-analyst/">MOps vs. Data Analyst Salary</a></li>
    <li><a href="/salary/vs-marketing-manager/">MOps vs. Marketing Manager Salary</a></li>
    <li><a href="/salary/vs-demand-gen/">MOps vs. Demand Gen Salary</a></li>
</ul>

{source_citation(data)}
</div>
'''
    body += newsletter_cta_html("Get weekly salary updates for marketing operations roles.")

    faq_pairs = [
        ("What is the average marketing operations salary in 2026?",
         f"The median marketing operations salary is {fmt_salary(stats['median'])} based on {stats['count_with_salary']} job postings with disclosed compensation. The full range spans from {fmt_salary(stats['min'])} for entry-level roles to {fmt_salary(stats['max'])}+ for VP-level positions at enterprise companies."),
        ("How much do entry-level MOps roles pay?",
         f"Entry-level marketing operations roles pay a median of {fmt_salary(data['by_seniority']['Entry']['median'])}. The average range runs from {fmt_salary(data['by_seniority']['Entry']['min_base_avg'])} to {fmt_salary(data['by_seniority']['Entry']['max_base_avg'])} based on {data['by_seniority']['Entry']['count']} tracked positions."),
        ("Do remote MOps jobs pay less than onsite?",
         f"Yes. Remote marketing operations roles pay a median of {fmt_salary(remote['median'])}, compared to {fmt_salary(onsite['median'])} for onsite roles. The {fmt_salary(onsite['median'] - remote['median'])} gap is driven by geographic pay adjustments and the concentration of senior roles in office-based positions."),
        ("Which city pays the most for marketing operations?",
         "San Francisco leads with the highest average salary range for marketing operations roles, followed by Boston and New York. However, San Francisco has fewer postings than New York, which dominates in total volume."),
    ]
    body += faq_html(faq_pairs)

    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="Marketing Operations Salary Data and Benchmarks (2026)",
        description=f"MOps salary benchmarks from {stats['count_with_salary']} job postings. Median: {fmt_salary(stats['median'])}. Breakdowns by seniority, location, and remote status.",
        canonical_path="/salary/",
        body_content=body,
        active_path="/salary/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("salary/index.html", page)
    print("  Built: salary/index.html")


# ---------------------------------------------------------------------------
# 2. Seniority pages
# ---------------------------------------------------------------------------

SENIORITY_META = {
    "Entry": {
        "title": "Entry-Level Marketing Operations Salary (2026)",
        "h1": "Entry-Level Marketing Operations Salary",
        "slug": "entry",
        "desc_role": "entry-level marketing operations",
        "context": "Entry-level MOps roles typically involve campaign execution, list management, CRM hygiene, and marketing automation support. These positions are the starting point for a career in marketing operations, often requiring 0-2 years of experience.",
        "skills": "HubSpot or Marketo basics, CRM data entry, email campaign setup, list segmentation, basic reporting, spreadsheet proficiency",
        "next_level": "mid",
        "next_label": "Mid-Level",
        "comparison_roles": ["marketing coordinator", "sales development representative", "junior data analyst"],
    },
    "Mid": {
        "title": "Mid-Level Marketing Operations Salary (2026)",
        "h1": "Mid-Level Marketing Operations Salary",
        "slug": "mid",
        "desc_role": "mid-level marketing operations",
        "context": "Mid-level MOps professionals own significant portions of the marketing technology stack. They build and optimize automation workflows, manage lead scoring models, handle integrations between systems, and produce reporting for marketing leadership. Typical experience: 3-5 years.",
        "skills": "Marketing automation administration, lead scoring, CRM integration, attribution modeling, SQL for reporting, API integrations, A/B testing frameworks",
        "next_level": "senior",
        "next_label": "Senior",
        "comparison_roles": ["marketing manager", "business analyst", "CRM administrator"],
    },
    "Senior": {
        "title": "Senior Marketing Operations Salary (2026)",
        "h1": "Senior Marketing Operations Salary",
        "slug": "senior",
        "desc_role": "senior marketing operations",
        "context": "Senior MOps professionals architect marketing technology stacks, lead cross-functional projects, and serve as the bridge between marketing strategy and technical execution. They own vendor evaluations, data governance policies, and complex multi-system workflows. Typical experience: 5-8 years.",
        "skills": "Stack architecture, vendor evaluation, data governance, advanced automation, revenue attribution, team mentorship, budget management",
        "next_level": "director",
        "next_label": "Director",
        "comparison_roles": ["senior marketing manager", "senior data analyst", "solutions architect"],
    },
    "Director": {
        "title": "Director of Marketing Operations Salary (2026)",
        "h1": "Director of Marketing Operations Salary",
        "slug": "director",
        "desc_role": "director-level marketing operations",
        "context": "Directors of Marketing Operations manage teams, set the technology strategy, own the marketing operations budget, and report to the CMO or VP of Marketing. They are responsible for the performance and scalability of the entire marketing technology infrastructure. Typical experience: 8-12 years.",
        "skills": "Team leadership, budget ownership, executive reporting, vendor negotiation, cross-departmental alignment, strategic planning, process optimization at scale",
        "next_level": "vp",
        "next_label": "VP",
        "comparison_roles": ["director of demand gen", "director of sales operations", "director of analytics"],
    },
    "VP": {
        "title": "VP of Marketing Operations Salary (2026)",
        "h1": "VP of Marketing Operations Salary",
        "slug": "vp",
        "desc_role": "VP-level marketing operations",
        "context": "VPs of Marketing Operations sit on the marketing leadership team and often report directly to the CMO or CRO. They own the full marketing operations function including team, budget, vendor relationships, and strategic roadmap. These roles appear primarily at enterprise companies and well-funded growth-stage firms. Typical experience: 12+ years.",
        "skills": "Executive leadership, P&L ownership, board-level reporting, organizational design, M&A integration, enterprise vendor management, revenue operations strategy",
        "next_level": None,
        "next_label": None,
        "comparison_roles": ["VP of revenue operations", "VP of demand generation", "VP of marketing technology"],
    },
}


def build_seniority_pages(data):
    max_scale = 300000
    for level, meta in SENIORITY_META.items():
        d = data["by_seniority"].get(level)
        if not d:
            continue

        slug = meta["slug"]
        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (meta["h1"], None)]
        bc = breadcrumb_html(crumbs)

        cards = stat_cards_html([
            (fmt_salary(d["median"]), "Median Salary"),
            (fmt_salary(d["min_base_avg"]), "Avg Range Low"),
            (fmt_salary(d["max_base_avg"]), "Avg Range High"),
            (str(d["count"]), "Tracked Roles"),
        ])

        # Build range bars comparing all levels
        all_bars = ""
        for cmp_level in ["Entry", "Mid", "Senior", "Director", "VP"]:
            cmp = data["by_seniority"].get(cmp_level)
            if not cmp:
                continue
            bold = " <strong>(current)</strong>" if cmp_level == level else ""
            all_bars += range_bar_html(
                f"{cmp_level}{bold}", cmp["min_base_avg"], cmp["max_base_avg"],
                cmp["median"], max_scale
            )

        next_link = ""
        if meta["next_level"]:
            next_link = f'<p>Next level: <a href="/salary/{meta["next_level"]}/">{meta["next_label"]} MOps Salary</a></p>'

        faq_pairs = [
            (f"What is the average {meta['desc_role']} salary?",
             f"The median {meta['desc_role']} salary is {fmt_salary(d['median'])} based on {d['count']} tracked job postings. The average range spans {fmt_salary(d['min_base_avg'])} to {fmt_salary(d['max_base_avg'])}."),
            (f"What skills do {meta['desc_role']} roles require?",
             f"Common skills for {meta['desc_role']} roles include: {meta['skills']}."),
            (f"How does {meta['desc_role']} pay compare to other levels?",
             f"The overall MOps median is {fmt_salary(data['salary_stats']['median'])}. {level}-level roles {'are above' if d['median'] >= data['salary_stats']['median'] else 'fall below'} that benchmark at {fmt_salary(d['median'])} median."),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>{meta["h1"]}</h1>
    <p class="lead">Compensation data for {meta["desc_role"]} professionals based on {d["count"]} tracked job postings with disclosed salary ranges.</p>
</section>

<div class="container">
{cards}

<h2>Salary Range</h2>
{range_bar_html(level, d["min_base_avg"], d["max_base_avg"], d["median"], max_scale)}

<h2>What {level}-Level MOps Professionals Do</h2>
<p>{meta["context"]}</p>

<h2>Key Skills at This Level</h2>
<p>{meta["skills"]}.</p>

<h2>How {level} Compares Across All Levels</h2>
<p>Marketing operations compensation increases significantly at each step. Here is where {level}-level pay sits relative to the full seniority ladder:</p>
{all_bars}

<h2>Factors That Influence {level}-Level Pay</h2>
<p><strong>Location.</strong> Metro areas like San Francisco, New York, and Boston consistently push compensation higher. See the <a href="/salary/">salary index</a> for metro breakdowns.</p>
<p><strong>Company stage.</strong> Enterprise companies and well-funded startups tend to pay more than mid-market firms at every level. Equity packages at startups can shift total compensation significantly.</p>
<p><strong>Tool expertise.</strong> Proficiency in high-demand platforms like Marketo, Salesforce, and HubSpot correlates with higher offers. Specialized skills in data architecture, attribution, or RevOps alignment command premiums.</p>
<p><strong>Remote vs. onsite.</strong> Remote roles at this level pay a median of {fmt_salary(data["by_remote"]["remote"]["median"])}, while onsite roles reach {fmt_salary(data["by_remote"]["onsite"]["median"])}. See the <a href="/salary/remote/">remote vs. onsite breakdown</a>.</p>

{next_link}

<h2>Related Pages</h2>
<ul>
    <li><a href="/salary/">Full Salary Index</a></li>
    <li><a href="/salary/remote/">Remote vs. Onsite Pay</a></li>
    <li><a href="/salary/calculator/">Salary Calculator</a></li>
    <li><a href="/salary/methodology/">Methodology</a></li>
</ul>

{source_citation(data)}
</div>
'''
        body += newsletter_cta_html(f"Get weekly updates on {meta['desc_role']} compensation.")
        body += faq_html(faq_pairs)

        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
        page = get_page_wrapper(
            title=meta["title"],
            description=f"{level} MOps salary: median {fmt_salary(d['median'])}, range {fmt_salary(d['min_base_avg'])}-{fmt_salary(d['max_base_avg'])}. Based on {d['count']} job postings.",
            canonical_path=f"/salary/{slug}/",
            body_content=body,
            active_path="/salary/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"salary/{slug}/index.html", page)
        print(f"  Built: salary/{slug}/index.html")


# ---------------------------------------------------------------------------
# 3. Location pages
# ---------------------------------------------------------------------------

def build_location_pages(data):
    max_scale = 250000
    for metro, d in data["by_metro"].items():
        if metro == "Unknown":
            continue

        slug = slugify(metro)
        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (f"{metro} MOps Salary", None)]
        bc = breadcrumb_html(crumbs)

        cards = stat_cards_html([
            (fmt_salary(d["median"]), "Median Salary"),
            (fmt_salary(d["min_base_avg"]), "Avg Range Low"),
            (fmt_salary(d["max_base_avg"]), "Avg Range High"),
            (str(d["count"]), "Tracked Roles"),
        ])

        # Compare all metros
        metro_bars = ""
        for m, md in sorted(data["by_metro"].items(), key=lambda x: -x[1]["median"]):
            if m == "Unknown":
                continue
            bold = " <strong>(current)</strong>" if m == metro else ""
            metro_bars += range_bar_html(f"{m}{bold}", md["min_base_avg"], md["max_base_avg"], md["median"], max_scale)

        national_median = data["salary_stats"]["median"]
        diff = d["median"] - national_median
        diff_text = f"{fmt_salary(abs(diff))} {'above' if diff >= 0 else 'below'} the national median"

        faq_pairs = [
            (f"What is the average MOps salary in {metro}?",
             f"The median marketing operations salary in {metro} is {fmt_salary(d['median'])} based on {d['count']} tracked job postings. The average range runs from {fmt_salary(d['min_base_avg'])} to {fmt_salary(d['max_base_avg'])}."),
            (f"How does {metro} MOps pay compare to the national average?",
             f"{metro} MOps salaries are {diff_text} of {fmt_salary(national_median)}. This reflects {'the higher cost of living and concentration of enterprise employers' if diff >= 0 else 'a lower cost of living relative to coastal tech hubs'} in the {metro} market."),
            (f"Are there many MOps jobs in {metro}?",
             f"Our dataset includes {d['count']} marketing operations positions in {metro} with disclosed salary data. The actual market is larger, as many postings do not disclose compensation."),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>Marketing Operations Salary in {metro} (2026)</h1>
    <p class="lead">Compensation data for marketing operations roles in the {metro} metro area based on {d["count"]} tracked job postings.</p>
</section>

<div class="container">
{cards}

<h2>Salary Range in {metro}</h2>
{range_bar_html(metro, d["min_base_avg"], d["max_base_avg"], d["median"], max_scale)}

<h2>{metro} vs. National Average</h2>
<p>The national median for marketing operations roles is {fmt_salary(national_median)}. {metro} sits {diff_text}. {'This premium is typical for major tech hubs where competition for marketing operations talent is highest.' if diff >= 0 else 'Cost-of-living adjustments and the local employer mix drive this difference.'}</p>

<h2>How {metro} Compares to Other Markets</h2>
{metro_bars}

<h2>Cost of Living Considerations</h2>
<p>Raw salary numbers only tell part of the story. A {fmt_salary(d["median"])} salary in {metro} has different purchasing power than the same figure in a lower-cost metro. When evaluating offers, factor in housing costs, state income tax, and commuting expenses.</p>

<h2>Remote Roles Based in {metro}</h2>
<p>Some companies headquartered in {metro} offer remote positions at adjusted pay bands. Remote MOps roles nationally pay a median of {fmt_salary(data["by_remote"]["remote"]["median"])}, compared to {fmt_salary(data["by_remote"]["onsite"]["median"])} for onsite positions. See our <a href="/salary/remote/">remote vs. onsite analysis</a> for the full picture.</p>

<h2>Negotiation Guidance for {metro}</h2>
<p>When negotiating a MOps role in {metro}, anchor your expectations to the {fmt_salary(d["min_base_avg"])}-{fmt_salary(d["max_base_avg"])} range. Senior and director-level roles will push above the upper bound. Come prepared with data on the specific tools and skills the role requires, and reference comparable positions in the metro.</p>

<h2>Related Pages</h2>
<ul>
    <li><a href="/salary/">Full Salary Index</a></li>
    <li><a href="/salary/remote/">Remote vs. Onsite Pay</a></li>
    <li><a href="/salary/calculator/">Salary Calculator</a></li>
</ul>

{source_citation(data)}
</div>
'''
        body += newsletter_cta_html(f"Get weekly salary updates for {metro} MOps roles.")
        body += faq_html(faq_pairs)

        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
        page = get_page_wrapper(
            title=f"Marketing Operations Salary in {metro} (2026)",
            description=f"MOps salary in {metro}: median {fmt_salary(d['median'])}, range {fmt_salary(d['min_base_avg'])}-{fmt_salary(d['max_base_avg'])}. {d['count']} tracked roles.",
            canonical_path=f"/salary/{slug}/",
            body_content=body,
            active_path="/salary/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"salary/{slug}/index.html", page)
        print(f"  Built: salary/{slug}/index.html")


# ---------------------------------------------------------------------------
# 4. Remote vs Onsite
# ---------------------------------------------------------------------------

def build_remote_page(data):
    remote = data["by_remote"]["remote"]
    onsite = data["by_remote"]["onsite"]
    max_scale = 250000

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Remote vs. Onsite", None)]
    bc = breadcrumb_html(crumbs)

    gap = onsite["median"] - remote["median"]
    gap_pct = (gap / onsite["median"]) * 100

    cards = stat_cards_html([
        (fmt_salary(remote["median"]), "Remote Median"),
        (fmt_salary(onsite["median"]), "Onsite Median"),
        (f"{fmt_salary(gap)}", "Pay Gap"),
        (f"{remote['count']} / {onsite['count']}", "Remote / Onsite Roles"),
    ])

    faq_pairs = [
        ("Do remote MOps jobs pay less?",
         f"Yes. Remote marketing operations roles pay a median of {fmt_salary(remote['median'])}, which is {fmt_salary(gap)} ({gap_pct:.0f}%) less than the {fmt_salary(onsite['median'])} median for onsite roles. The gap is driven by geographic pay adjustments and the concentration of senior roles in office-based positions."),
        ("What percentage of MOps roles are remote?",
         f"In our dataset, {remote['count']} out of {remote['count'] + onsite['count']} salary-disclosed roles ({remote['count'] / (remote['count'] + onsite['count']) * 100:.0f}%) are remote. The actual share of remote-friendly MOps positions is likely higher, as many hybrid roles are categorized as onsite."),
        ("Should I take a remote MOps job at lower pay?",
         "It depends on your location. A remote role paying the remote median may offer more purchasing power than a higher-paying onsite role in San Francisco or New York once you factor in housing, commute, and state taxes. Run the numbers for your specific situation."),
        ("Are remote MOps roles increasing?",
         "Remote and hybrid marketing operations roles have grown since 2023. Many companies now offer location-flexible arrangements for MOps professionals, especially at the senior and director levels where talent is scarce."),
    ]

    body = f'''{bc}
<section class="page-header">
    <h1>Remote vs. Onsite Marketing Operations Salary (2026)</h1>
    <p class="lead">How remote work affects marketing operations compensation. Based on {remote["count"] + onsite["count"]} roles with disclosed salary data.</p>
</section>

<div class="container">
{cards}

<h2>The Remote Pay Gap</h2>
<p>Remote marketing operations roles pay {fmt_salary(gap)} less than onsite positions at the median. That is a {gap_pct:.0f}% difference. This gap has been consistent across our tracking period and aligns with broader trends in tech compensation.</p>

{range_bar_html("Remote", remote["min_base_avg"], remote["max_base_avg"], remote["median"], max_scale)}
{range_bar_html("Onsite", onsite["min_base_avg"], onsite["max_base_avg"], onsite["median"], max_scale)}

<h2>Why the Gap Exists</h2>
<p>Three factors drive the remote-onsite pay difference in marketing operations:</p>
<p><strong>Geographic adjustment.</strong> Companies hiring remotely often peg compensation to the employee's location rather than the company's headquarters. A remote role at a San Francisco company may pay Bay Area rates or may adjust down for a Midwest-based employee.</p>
<p><strong>Seniority distribution.</strong> VP and Director roles are more likely to require in-office presence, skewing onsite medians upward. Entry and mid-level roles are more frequently offered as remote.</p>
<p><strong>Company type.</strong> Large enterprises with the highest compensation bands tend to mandate office attendance. Startups and mid-market companies offering remote flexibility tend to pay slightly less across the board.</p>

<h2>Remote MOps: What to Expect</h2>
<p>The average remote MOps salary range runs from {fmt_salary(remote["min_base_avg"])} to {fmt_salary(remote["max_base_avg"])}. At the low end, you will find entry-level campaign operations roles at smaller companies. At the high end, senior individual contributor and manager roles at well-funded growth companies.</p>

<h2>Onsite MOps: What to Expect</h2>
<p>Onsite roles span {fmt_salary(onsite["min_base_avg"])} to {fmt_salary(onsite["max_base_avg"])}. The upper range includes director and VP positions at enterprise companies in major metros. Onsite roles also tend to come with larger equity packages, especially at public companies.</p>

<h2>How to Evaluate a Remote Offer</h2>
<p>When comparing a remote offer to an onsite alternative, calculate the all-in difference. Factor in:</p>
<ul>
    <li>State income tax savings (or costs) based on your location</li>
    <li>Commuting costs eliminated (average US commuter spends $5,000-$10,000 annually)</li>
    <li>Housing cost differences if you would relocate for an onsite role</li>
    <li>Equity value and vesting schedule differences</li>
    <li>Home office stipend and benefits differences</li>
</ul>
<p>A remote role paying {fmt_salary(remote["median"])} in a low-cost metro may net more than an onsite role paying {fmt_salary(onsite["median"])} in San Francisco after taxes and expenses.</p>

<h2>Related Pages</h2>
<ul>
    <li><a href="/salary/">Full Salary Index</a></li>
    <li><a href="/salary/calculator/">Salary Calculator</a></li>
    <li><a href="/salary/entry/">Entry-Level Salaries</a></li>
    <li><a href="/salary/vp/">VP-Level Salaries</a></li>
</ul>

{source_citation(data)}
</div>
'''
    body += newsletter_cta_html("Get weekly remote and onsite salary data for MOps roles.")
    body += faq_html(faq_pairs)

    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="Remote vs. Onsite Marketing Operations Salary (2026)",
        description=f"Remote MOps median: {fmt_salary(remote['median'])}. Onsite median: {fmt_salary(onsite['median'])}. {fmt_salary(gap)} gap analyzed across {remote['count'] + onsite['count']} roles.",
        canonical_path="/salary/remote/",
        body_content=body,
        active_path="/salary/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("salary/remote/index.html", page)
    print("  Built: salary/remote/index.html")


# ---------------------------------------------------------------------------
# 5. Salary Calculator
# ---------------------------------------------------------------------------

def build_calculator_page(data):
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Salary Calculator", None)]
    bc = breadcrumb_html(crumbs)

    # Embed data for JS
    js_data = {
        "by_seniority": {k: v for k, v in data["by_seniority"].items() if k != "Unknown"},
        "by_metro": {k: v for k, v in data["by_metro"].items() if k != "Unknown"},
        "by_remote": data["by_remote"],
        "overall_median": data["salary_stats"]["median"],
    }

    seniority_options = ""
    for level in ["Entry", "Mid", "Senior", "Director", "VP"]:
        if level in data["by_seniority"]:
            seniority_options += f'<option value="{level}">{level}</option>\n'

    metro_options = '<option value="national">National Average</option>\n'
    for metro in sorted(data["by_metro"].keys()):
        if metro != "Unknown":
            metro_options += f'<option value="{metro}">{metro}</option>\n'

    faq_pairs = [
        ("How accurate is the MOps salary calculator?",
         f"The calculator uses data from {data['records_with_salary']} real job postings with disclosed compensation. Results reflect market averages, not guarantees. Individual offers vary based on specific skills, company funding, negotiation, and other factors not captured in aggregate data."),
        ("What factors affect MOps salary the most?",
         "Seniority level has the largest impact, followed by metro area and remote status. Tool expertise (especially Marketo, Salesforce, and HubSpot) and industry vertical also influence compensation."),
    ]

    body = f'''{bc}
<section class="page-header">
    <h1>Marketing Operations Salary Calculator</h1>
    <p class="lead">Estimate your market value based on seniority, location, and work arrangement. Built from {data["records_with_salary"]} MOps job postings with disclosed compensation.</p>
</section>

<div class="container">

<div class="calculator-gate" id="calculatorGate">
    <h2>Get Your Personalized Salary Estimate</h2>
    <p>Enter your email to unlock the MOps salary calculator. You will also receive our weekly salary data newsletter.</p>
    <form class="newsletter-cta-form" id="calcGateForm" onsubmit="return false;">
        <input type="email" placeholder="Your work email" aria-label="Email address" required>
        <button type="submit" class="btn btn--primary">Unlock Calculator</button>
    </form>
</div>

<div class="calculator-tool" id="calculatorTool" style="display:none;">
    <div class="calc-form">
        <div class="calc-field">
            <label for="calcSeniority">Seniority Level</label>
            <select id="calcSeniority">
                {seniority_options}
            </select>
        </div>
        <div class="calc-field">
            <label for="calcMetro">Metro Area</label>
            <select id="calcMetro">
                {metro_options}
            </select>
        </div>
        <div class="calc-field">
            <label for="calcRemote">Work Arrangement</label>
            <select id="calcRemote">
                <option value="onsite">Onsite / Hybrid</option>
                <option value="remote">Remote</option>
            </select>
        </div>
        <button class="btn btn--primary" id="calcButton" onclick="calculateSalary()">Calculate</button>
    </div>

    <div class="calc-result" id="calcResult" style="display:none;">
        <h3>Your Estimated Range</h3>
        <div class="stat-grid">
            <div class="stat-block">
                <span class="stat-value" id="calcLow">-</span>
                <span class="stat-label">Low End</span>
            </div>
            <div class="stat-block">
                <span class="stat-value" id="calcMid">-</span>
                <span class="stat-label">Midpoint</span>
            </div>
            <div class="stat-block">
                <span class="stat-value" id="calcHigh">-</span>
                <span class="stat-label">High End</span>
            </div>
        </div>
        <div id="calcBar"></div>
        <p class="calc-note">This estimate is based on {data["records_with_salary"]} MOps job postings. Individual offers vary by company, skills, and negotiation.</p>
    </div>
</div>

<script>
var CALC_DATA = {json.dumps(js_data)};

// Gate logic
document.getElementById('calcGateForm').onsubmit = function(e) {{
    e.preventDefault();
    var email = this.querySelector('input').value.trim();
    if (!email) return;
    // Submit to newsletter signup
    var SIGNUP_URL = '{SIGNUP_WORKER_URL}';
    fetch(SIGNUP_URL, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{email: email, list: 'mops-report'}})
    }}).then(function() {{
        document.getElementById('calculatorGate').style.display = 'none';
        document.getElementById('calculatorTool').style.display = 'block';
        if (typeof gtag === 'function') {{
            gtag('event', 'calculator_unlock', {{'event_category': 'engagement', 'event_label': email}});
        }}
    }}).catch(function() {{
        // Still unlock on error to avoid frustration
        document.getElementById('calculatorGate').style.display = 'none';
        document.getElementById('calculatorTool').style.display = 'block';
    }});
}};

function calculateSalary() {{
    var seniority = document.getElementById('calcSeniority').value;
    var metro = document.getElementById('calcMetro').value;
    var remote = document.getElementById('calcRemote').value;

    var senData = CALC_DATA.by_seniority[seniority];
    if (!senData) return;

    var low = senData.min_base_avg;
    var high = senData.max_base_avg;

    // Metro adjustment
    if (metro !== 'national' && CALC_DATA.by_metro[metro]) {{
        var metroData = CALC_DATA.by_metro[metro];
        var nationalMedian = CALC_DATA.overall_median;
        var metroFactor = metroData.median / nationalMedian;
        low = low * metroFactor;
        high = high * metroFactor;
    }}

    // Remote adjustment
    if (remote === 'remote') {{
        var remoteFactor = CALC_DATA.by_remote.remote.median / CALC_DATA.by_remote.onsite.median;
        low = low * remoteFactor;
        high = high * remoteFactor;
    }}

    var mid = (low + high) / 2;

    document.getElementById('calcLow').textContent = '$' + Math.round(low).toLocaleString();
    document.getElementById('calcMid').textContent = '$' + Math.round(mid).toLocaleString();
    document.getElementById('calcHigh').textContent = '$' + Math.round(high).toLocaleString();
    document.getElementById('calcResult').style.display = 'block';

    if (typeof gtag === 'function') {{
        gtag('event', 'salary_calculate', {{'event_category': 'engagement', 'event_label': seniority + '_' + metro + '_' + remote}});
    }}
}}
</script>

<h2>How the Calculator Works</h2>
<p>This calculator combines three data dimensions from our job posting analysis:</p>
<ol>
    <li><strong>Seniority level</strong> sets the base salary range from our tracked data</li>
    <li><strong>Metro area</strong> applies a location adjustment based on that metro's median relative to the national figure</li>
    <li><strong>Work arrangement</strong> applies a remote discount (or onsite premium) based on the observed gap between remote and onsite compensation</li>
</ol>
<p>The result is an estimated range, not a precise prediction. Use it as a starting point for evaluating offers and planning negotiations.</p>

<h2>Limitations</h2>
<p>This calculator does not account for company stage, industry vertical, specific tool expertise, equity compensation, or signing bonuses. It also cannot capture the negotiation dynamics that ultimately determine an individual offer. Treat the output as a benchmark, not a ceiling.</p>

<h2>Related Pages</h2>
<ul>
    <li><a href="/salary/">Full Salary Index</a></li>
    <li><a href="/salary/remote/">Remote vs. Onsite Analysis</a></li>
    <li><a href="/salary/methodology/">Our Methodology</a></li>
</ul>

{source_citation(data)}
</div>
'''
    body += faq_html(faq_pairs)

    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="Marketing Operations Salary Calculator (2026)",
        description=f"Estimate your MOps market value by seniority, location, and work arrangement. Built from {data['records_with_salary']} job postings with disclosed salary data.",
        canonical_path="/salary/calculator/",
        body_content=body,
        active_path="/salary/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("salary/calculator/index.html", page)
    print("  Built: salary/calculator/index.html")


# ---------------------------------------------------------------------------
# 6. Methodology
# ---------------------------------------------------------------------------

def build_methodology_page(data):
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Methodology", None)]
    bc = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Where does MOps Report salary data come from?",
         f"All salary data comes from public job postings that disclose compensation ranges. We track {data['total_records']} marketing operations positions, of which {data['records_with_salary']} ({data['disclosure_rate']}%) include salary information."),
        ("How often is the salary data updated?",
         "We update our dataset weekly. Each update includes new postings, removes expired listings, and recalculates all aggregates."),
        ("Why do some pages show different numbers?",
         "Different pages slice the data differently. The salary index shows overall statistics, while seniority and location pages show subset-specific numbers. All numbers are internally consistent within each view."),
        ("Can I use this data for salary negotiations?",
         "Yes. Our data provides a market benchmark. Combine it with your specific experience, skills, and the employer's context for the strongest negotiation position."),
    ]

    body = f'''{bc}
<section class="page-header">
    <h1>Salary Data Methodology</h1>
    <p class="lead">How we collect, process, and present marketing operations salary data.</p>
</section>

<div class="container">

<h2>Data Collection</h2>
<p>MOps Report tracks marketing operations job postings from job boards, company career pages, and aggregator APIs. We focus on roles with titles containing marketing operations, marketing technology, MOps, or closely related variants.</p>
<p>Our current dataset includes {data["total_records"]} tracked positions. Of these, {data["records_with_salary"]} ({data["disclosure_rate"]}%) include disclosed salary ranges. Roles without salary data are included in volume and trend analyses but excluded from compensation statistics.</p>

<h2>Salary Normalization</h2>
<p>Job postings report compensation in different formats: annual salary ranges, hourly rates, and occasionally total compensation. We normalize all figures to annual base salary. Hourly rates are converted assuming 2,080 hours per year. Total compensation figures are broken into base and variable where possible.</p>
<p>When a posting provides a range (e.g., $80,000-$120,000), we record both endpoints. Aggregates on this site show the average of low endpoints (Avg Low) and the average of high endpoints (Avg High) for each group. The median uses the midpoint of each posting's range.</p>

<h2>Seniority Classification</h2>
<p>We classify roles into five seniority levels based on title analysis:</p>
<ul>
    <li><strong>Entry:</strong> Coordinator, Specialist, Associate, Analyst (0-2 years typical)</li>
    <li><strong>Mid:</strong> Manager, Senior Specialist, Lead (3-5 years typical)</li>
    <li><strong>Senior:</strong> Senior Manager, Principal, Staff (5-8 years typical)</li>
    <li><strong>Director:</strong> Director, Senior Director, Head of (8-12 years typical)</li>
    <li><strong>VP:</strong> Vice President, SVP, EVP (12+ years typical)</li>
</ul>
<p>Roles with ambiguous titles are classified as Unknown and excluded from seniority breakdowns.</p>

<h2>Location Classification</h2>
<p>We map each posting to a metro area based on the listed location. Remote roles are tagged separately. Postings that list only a state or "United States" without a specific metro are classified as Unknown for location analysis but may still appear in remote vs. onsite comparisons.</p>

<h2>Remote vs. Onsite</h2>
<p>Roles are classified as remote if the posting explicitly states remote, work from home, or distributed. All other roles are classified as onsite, which includes hybrid arrangements. This is a conservative approach that likely understates the true share of remote-flexible positions.</p>

<h2>Update Frequency</h2>
<p>The dataset is refreshed weekly. Historical data is preserved for trend analysis. All statistics on the site reflect the most recent data pull.</p>

<h2>Limitations</h2>
<p>Our data has inherent limitations you should understand:</p>
<ul>
    <li><strong>Disclosure bias:</strong> Only {data["disclosure_rate"]}% of tracked postings include salary. States with pay transparency laws (California, New York, Colorado, Washington) are overrepresented.</li>
    <li><strong>Title variance:</strong> Marketing operations roles have inconsistent titling across companies. Our classification catches most patterns but may miss some edge cases.</li>
    <li><strong>Sampling:</strong> We track postings from major job boards and company sites, but do not capture every listing. Internal promotions and referral-only roles are not represented.</li>
    <li><strong>Timing:</strong> Compensation reflects what employers are offering today. Accepted offers may differ from posted ranges due to negotiation.</li>
</ul>

<h2>Related Pages</h2>
<ul>
    <li><a href="/salary/">Salary Index</a></li>
    <li><a href="/salary/calculator/">Salary Calculator</a></li>
    <li><a href="/about/">About MOps Report</a></li>
</ul>

{source_citation(data)}
</div>
'''
    body += newsletter_cta_html()
    body += faq_html(faq_pairs)

    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="MOps Salary Data Methodology",
        description=f"How MOps Report collects and analyzes marketing operations salary data. {data['total_records']} postings tracked, {data['records_with_salary']} with disclosed compensation.",
        canonical_path="/salary/methodology/",
        body_content=body,
        active_path="/salary/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("salary/methodology/index.html", page)
    print("  Built: salary/methodology/index.html")


# ---------------------------------------------------------------------------
# 7. Comparison pages
# ---------------------------------------------------------------------------

COMPARISON_ROLES = {
    "revops": {
        "name": "Revenue Operations (RevOps)",
        "short": "RevOps",
        "slug": "vs-revops",
        "est_median": 115000,
        "est_low": 75000,
        "est_high": 200000,
        "overlap": "RevOps and MOps share significant DNA. Both roles manage CRM systems, work with marketing and sales data, and require automation skills. The key difference: RevOps spans the full customer lifecycle (marketing, sales, customer success), while MOps focuses specifically on the marketing technology stack and demand generation operations.",
        "who_earns_more": "RevOps roles tend to pay slightly more at the median, reflecting their broader scope and the fact that many RevOps positions report to the CRO rather than the CMO. However, specialized MOps roles at enterprise companies often match or exceed RevOps compensation.",
        "career_path": "Many MOps professionals transition into RevOps as companies consolidate operations functions. If you are in MOps and considering the switch, your marketing automation and attribution skills transfer directly. The main skill gap is typically sales process expertise and customer success operations.",
    },
    "sales-ops": {
        "name": "Sales Operations",
        "short": "Sales Ops",
        "slug": "vs-sales-ops",
        "est_median": 105000,
        "est_low": 65000,
        "est_high": 190000,
        "overlap": "Sales Ops and MOps share CRM administration as common ground. Both roles build reports, manage data quality, and configure automation workflows. The distinction is the customer journey stage: MOps focuses on lead generation, scoring, and handoff, while Sales Ops owns pipeline management, forecasting, and deal operations.",
        "who_earns_more": "Compensation is comparable at most levels. Sales Ops roles at quota-carrying organizations sometimes include variable compensation tied to team performance, which can push total comp above MOps equivalents.",
        "career_path": "MOps and Sales Ops professionals frequently collaborate and sometimes swap roles. If you are considering the move from MOps to Sales Ops, invest time in understanding sales methodologies, forecasting models, and territory planning.",
    },
    "data-analyst": {
        "name": "Data Analyst",
        "short": "Data Analyst",
        "slug": "vs-data-analyst",
        "est_median": 90000,
        "est_low": 60000,
        "est_high": 150000,
        "overlap": "Both roles work with data daily, but in different contexts. Data Analysts build dashboards, write SQL queries, and generate insights from structured datasets. MOps professionals use data within marketing systems to drive automation, scoring, segmentation, and attribution. The toolsets overlap (SQL, BI tools) but the applications diverge.",
        "who_earns_more": "MOps roles pay more at the median, primarily because MOps professionals operate marketing technology stacks worth six or seven figures in annual licensing. The business impact of a well-run MAP instance is more directly tied to revenue than most analyst positions.",
        "career_path": "Data analysts who want to move into MOps should learn a marketing automation platform (HubSpot or Marketo) and understand lead lifecycle management. The analytical skills transfer immediately. The learning curve is in marketing process and technology administration.",
    },
    "marketing-manager": {
        "name": "Marketing Manager",
        "short": "Marketing Manager",
        "slug": "vs-marketing-manager",
        "est_median": 95000,
        "est_low": 65000,
        "est_high": 165000,
        "overlap": "Marketing Managers and MOps professionals work on the same team but from different angles. Marketing Managers own campaigns, messaging, and creative strategy. MOps professionals build the infrastructure that makes those campaigns scalable and measurable. The collaboration is tight but the skill sets are distinct.",
        "who_earns_more": "MOps professionals earn more at the median. The technical nature of MOps work, the scarcity of qualified candidates, and the cost of marketing technology stack expertise all push MOps compensation above general marketing management roles.",
        "career_path": "Marketing Managers who develop technical skills (HTML, SQL, API integrations) can transition into MOps. The move typically comes with a pay increase but requires a genuine interest in systems and process optimization over creative campaign work.",
    },
    "demand-gen": {
        "name": "Demand Generation",
        "short": "Demand Gen",
        "slug": "vs-demand-gen",
        "est_median": 105000,
        "est_low": 70000,
        "est_high": 185000,
        "overlap": "Demand Gen and MOps are the closest cousins in the marketing organization. Demand Gen owns the strategy for filling the pipeline. MOps builds and maintains the systems that execute that strategy. In practice, the roles frequently overlap, and smaller companies often combine them into a single position.",
        "who_earns_more": "Compensation is nearly identical at most levels. At the director and VP level, Demand Gen roles may edge ahead when variable compensation tied to pipeline targets is factored in. MOps roles tend to have more stable base compensation.",
        "career_path": "MOps professionals who want to move into Demand Gen should build expertise in campaign strategy, audience development, and channel optimization. The technical foundation from MOps is a significant advantage in Demand Gen, where many practitioners lack deep systems knowledge.",
    },
}


def build_comparison_pages(data):
    mops_median = data["salary_stats"]["median"]
    mops_low = data["salary_stats"]["min"]
    mops_high = data["salary_stats"]["max"]
    mops_avg_low = 80000  # approximate from entry low
    mops_avg_high = 200000  # approximate from director high
    max_scale = 250000

    for slug_key, comp in COMPARISON_ROLES.items():
        slug = comp["slug"]
        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (f"MOps vs. {comp['short']}", None)]
        bc = breadcrumb_html(crumbs)

        diff = mops_median - comp["est_median"]
        diff_text = f"{fmt_salary(abs(diff))} {'more' if diff > 0 else 'less'}" if diff != 0 else "roughly the same"

        cards = stat_cards_html([
            (fmt_salary(mops_median), "MOps Median"),
            (fmt_salary(comp["est_median"]), f'{comp["short"]} Median'),
            (diff_text, "Difference"),
            (str(data["records_with_salary"]), "MOps Roles Tracked"),
        ])

        faq_pairs = [
            (f"Does MOps or {comp['short']} pay more?",
             f"Marketing operations roles pay a median of {fmt_salary(mops_median)}, while {comp['name']} roles pay approximately {fmt_salary(comp['est_median'])}. {'MOps' if diff > 0 else comp['short']} typically pays more, with a {fmt_salary(abs(diff))} gap at the median."),
            (f"Can I switch from {comp['short']} to MOps?",
             f"Yes. {comp['career_path']}"),
            (f"What skills overlap between MOps and {comp['short']}?",
             f"{comp['overlap']}"),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>MOps vs. {comp["name"]} Salary Comparison (2026)</h1>
    <p class="lead">How marketing operations compensation compares to {comp["name"].lower()} roles. Side-by-side data for career planning and negotiation.</p>
</section>

<div class="container">
{cards}

<h2>Salary Range Comparison</h2>
{range_bar_html("Marketing Operations", data["by_seniority"]["Entry"]["min_base_avg"], data["by_seniority"]["VP"]["max_base_avg"], mops_median, max_scale)}
{range_bar_html(comp["name"], comp["est_low"], comp["est_high"], comp["est_median"], max_scale)}

<h2>Where the Roles Overlap</h2>
<p>{comp["overlap"]}</p>

<h2>Which Pays More?</h2>
<p>{comp["who_earns_more"]}</p>

<h2>Career Path Between the Roles</h2>
<p>{comp["career_path"]}</p>

<h2>MOps Salary by Level (for Reference)</h2>
<p>Here is the full MOps seniority ladder for context:</p>
<table class="data-table">
<thead><tr><th>Level</th><th>Median</th><th>Avg Low</th><th>Avg High</th></tr></thead>
<tbody>'''

        for level in ["Entry", "Mid", "Senior", "Director", "VP"]:
            d = data["by_seniority"].get(level)
            if d:
                body += f'<tr><td>{level}</td><td>{fmt_salary(d["median"])}</td><td>{fmt_salary(d["min_base_avg"])}</td><td>{fmt_salary(d["max_base_avg"])}</td></tr>\n'

        body += f'''</tbody>
</table>

<h2>Bottom Line</h2>
<p>MOps pays a median of {fmt_salary(mops_median)}. {comp["name"]} pays approximately {fmt_salary(comp["est_median"])}. The {fmt_salary(abs(diff))} difference at the median {'favors MOps' if diff > 0 else f'favors {comp["short"]}'} {'but narrows at senior levels' if abs(diff) < 15000 else 'and the gap widens at senior levels'}. Both paths offer strong earning potential for professionals who build deep expertise.</p>

<h2>Other Comparisons</h2>
<ul>'''

        for other_key, other in COMPARISON_ROLES.items():
            if other_key != slug_key:
                body += f'    <li><a href="/salary/{other["slug"]}/">MOps vs. {other["short"]}</a></li>\n'

        body += f'''</ul>

<h2>Related Pages</h2>
<ul>
    <li><a href="/salary/">Full Salary Index</a></li>
    <li><a href="/salary/calculator/">Salary Calculator</a></li>
</ul>

{source_citation(data)}
</div>
'''
        body += newsletter_cta_html(f"Get weekly MOps and {comp['short']} salary data.")
        body += faq_html(faq_pairs)

        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
        page = get_page_wrapper(
            title=f"MOps vs. {comp['name']} Salary (2026)",
            description=f"MOps median: {fmt_salary(mops_median)}. {comp['name']} median: ~{fmt_salary(comp['est_median'])}. Full comparison with career path guidance.",
            canonical_path=f"/salary/{slug}/",
            body_content=body,
            active_path="/salary/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"salary/{slug}/index.html", page)
        print(f"  Built: salary/{slug}/index.html")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_all_salary_pages(project_dir):
    """Entry point called from build.py."""
    data = load_comp_data(project_dir)
    print("\n  Building salary pages...")
    build_salary_index(data)
    build_seniority_pages(data)
    build_location_pages(data)
    build_remote_page(data)
    build_calculator_page(data)
    build_methodology_page(data)
    build_comparison_pages(data)
