# scripts/build.py
# Main build pipeline: generates all pages, sitemap, robots, CNAME.
# Data + page generators live here. HTML shell lives in templates.py.
# Site constants live in nav_config.py.

import os
import sys
import re
import shutil
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import *
import templates
from templates import (get_page_wrapper, write_page, get_homepage_schema,
                       get_breadcrumb_schema, get_faq_schema,
                       get_article_schema,
                       breadcrumb_html, newsletter_cta_html, faq_html, ALL_PAGES)
from salary_pages import build_all_salary_pages
from tools_pages import build_all_tools_pages
from glossary_pages import build_all_glossary_pages
from build_companies import build_all_company_pages
from report_pages import build_all_report_pages
from conferences_pages import build_conferences_index

# OG image generation state
SKIP_OG = "--skip-og" in sys.argv


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

# Wire up templates module
templates.OUTPUT_DIR = OUTPUT_DIR
templates.SKIP_OG = SKIP_OG


# ---------------------------------------------------------------------------
# Page generators: Homepage
# ---------------------------------------------------------------------------

def build_homepage():
    """Generate the homepage with Organization+WebSite schema."""
    title = "MOps Salary Data and Career Intelligence"
    description = (
        "Salary benchmarks, tool reviews, and career data for marketing operations professionals."
        " Updated weekly. Vendor-neutral. Free."
    )

    body = '''<section class="hero">
    <div class="hero-inner">
        <h1>Marketing Operations, Finally Mapped Out</h1>
        <p class="hero-subtitle">Salary data, tool reviews, career paths, and job listings. Everything the marketing ops profession has been missing in one place.</p>
        <div class="stat-grid">
            <div class="stat-block">
                <span class="stat-value">15,000+</span>
                <span class="stat-label">Roles Tracked</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">$65K&#8209;$200K+</span>
                <span class="stat-label">Salary Range</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">42%</span>
                <span class="stat-label">YoY Growth</span>
            </div>
        </div>
        <form class="hero-signup" onsubmit="return false;">
            <input type="email" placeholder="Your email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Get the Weekly Brief</button>
        </form>
        <p class="hero-signup-note">Free weekly newsletter. Salary shifts, tool intel, job data.</p>
    </div>
</section>

<section class="logo-bar">
    <p class="logo-bar-label">Tracking hiring data from companies like</p>
    <div class="logo-bar-row">
        <span class="logo-name">Marketo</span>
        <span class="logo-name">HubSpot</span>
        <span class="logo-name">Salesforce</span>
        <span class="logo-name">6sense</span>
        <span class="logo-name">LeanData</span>
        <span class="logo-name">Demandbase</span>
        <span class="logo-name">Drift</span>
        <span class="logo-name">Chili Piper</span>
        <span class="logo-name">Clearbit</span>
        <span class="logo-name">Segment</span>
    </div>
</section>

<section class="section-previews">
    <h2 class="section-previews-heading">Explore MOps Intelligence</h2>
    <div class="preview-grid">
        <a href="/salary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128176;</span></div>
            <h3>Salary Data</h3>
            <p>Breakdowns by seniority, location, and company stage. Side-by-side comparisons with RevOps, Demand Gen, and adjacent roles.</p>
            <span class="preview-link">Browse salary data &rarr;</span>
        </a>
        <a href="/tools/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128295;</span></div>
            <h3>Tool Reviews</h3>
            <p>Practitioner-tested reviews of Marketo, HubSpot, Pardot, and dozens more tools across MAP, CDP, attribution, and routing categories.</p>
            <span class="preview-link">Browse tools &rarr;</span>
        </a>
        <a href="/careers/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128200;</span></div>
            <h3>Career Guides</h3>
            <p>How to break in, level up, and negotiate. Interview prep, skill maps, and role comparisons for every stage of a MOps career.</p>
            <span class="preview-link">Browse guides &rarr;</span>
        </a>
        <a href="/insights/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128161;</span></div>
            <h3>Insights</h3>
            <p>Data-driven analysis of the MOps job market, salary trends, tool adoption, and hiring patterns across B2B and B2C companies.</p>
            <span class="preview-link">Browse insights &rarr;</span>
        </a>
        <a href="/glossary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128218;</span></div>
            <h3>MOps Glossary</h3>
            <p>Clear definitions for marketing operations terms. Lead scoring, MQL, attribution models, data hygiene, and more.</p>
            <span class="preview-link">Browse glossary &rarr;</span>
        </a>
        <a href="/newsletter/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128232;</span></div>
            <h3>Weekly Newsletter</h3>
            <p>Salary shifts, tool intel, and hiring trends delivered every Monday. Data from 15,000+ tracked job postings.</p>
            <span class="preview-link">Get the weekly brief &rarr;</span>
        </a>
    </div>
</section>

'''
    body += newsletter_cta_html()

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/",
        body_content=body,
        active_path="/",
        extra_head=get_homepage_schema(),
        body_class="page-home",
    )
    write_page("index.html", page)
    print(f"  Built: index.html")


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

def build_about_page():
    """Generate the about page with BreadcrumbList schema."""
    title = "About MOps Report: Independent MOps Data"
    description = (
        "MOps Report offers vendor-neutral salary benchmarks, tool stack reviews,"
        " and career guides for marketing operations professionals. Updated weekly."
    )

    crumbs = [("Home", "/"), ("About", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>About MOps Report: Independent MOps Data</h1>
</section>
<div class="container">
    <p>MOps Report is an independent resource for marketing operations professionals. We track salary data, review tools, and analyze the job market so you don't have to piece it together from LinkedIn posts and vendor blogs.</p>
    <p>Every data point comes from real job postings. We scrape, normalize, and cross-reference thousands of listings across B2B and B2C companies, from seed-stage startups to public enterprises.</p>
    <p>No vendor affiliations drive our rankings. No pay-to-play reviews. When we say a tool is good, it's because practitioners use it and the data backs it up.</p>
    <h2>What you'll find here</h2>
    <ul>
        <li><strong><a href="/salary/">Salary benchmarks</a></strong> broken down by seniority, location, and company stage</li>
        <li><strong><a href="/tools/">Tool reviews</a></strong> from someone who has built marketing operations systems, not just written about them</li>
        <li><strong><a href="/careers/">Career guides</a></strong> for breaking into and advancing in marketing operations</li>
        <li><strong><a href="/insights/">Insights</a></strong> and data-driven analysis of the MOps job market</li>
    </ul>
    <p>Built by <strong>Rome Thorndike</strong>.</p>
</div>
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/about/",
        body_content=body,
        active_path="/about/",
        extra_head=get_breadcrumb_schema(crumbs),
        body_class="page-inner",
    )
    write_page("about/index.html", page)
    print(f"  Built: about/index.html")


# ---------------------------------------------------------------------------
# Core pages (newsletter, privacy, terms, 404)
# ---------------------------------------------------------------------------

def build_newsletter_page():
    title = "The Weekly Brief: MOps Newsletter"
    description = (
        "Get weekly marketing operations salary data, tool intel, and job market analysis."
        " Free newsletter built from 15,000+ tracked job postings. Every Monday."
    )
    crumbs = [("Home", "/"), ("Newsletter", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<div class="newsletter-page">
    <section class="page-header">
        <h1>The Weekly Brief: MOps Newsletter</h1>
    </section>
    <p class="lead">Every Monday: salary shifts, tool intel, hiring trends, and job market data for marketing operations professionals. Built from 15,000+ tracked job postings.</p>
    <form class="hero-signup" onsubmit="return false;">
        <input type="email" placeholder="Your email" aria-label="Email address" required>
        <button type="submit" class="btn btn--primary">Get the Weekly Brief</button>
    </form>
    <ul class="newsletter-features">
        <li><strong>Salary movements:</strong> week-over-week changes in MOps compensation across seniority levels and locations</li>
        <li><strong>Tool trends:</strong> which tools are showing up in job postings, which are fading, and what's emerging</li>
        <li><strong>Hiring signals:</strong> which companies are scaling marketing operations teams and what that tells us about the market</li>
        <li><strong>Career intel:</strong> job market data, interview insights, and skill demand shifts</li>
    </ul>
    <p style="color: var(--mops-text-secondary);">Free. No spam. Unsubscribe anytime.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/newsletter/",
        body_content=body, active_path="/newsletter/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("newsletter/index.html", page)
    print(f"  Built: newsletter/index.html")


def build_privacy_page():
    title = "Privacy Policy for MOps Report Website"
    description = (
        "MOps Report privacy policy: how we collect, use, and protect your data."
        " We collect minimal information, never sell it, and respect your inbox."
    )
    crumbs = [("Home", "/"), ("Privacy Policy", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Privacy Policy for MOps Report Website</h1>
</section>
<div class="legal-content">
    <p>Last updated: April 3, 2026</p>
    <h2>What We Collect</h2>
    <p>When you subscribe to our newsletter, we collect your email address. That's it. We don't track you across the web, sell your data, or build advertising profiles.</p>
    <h2>How We Use Your Email</h2>
    <p>Your email address is used to send you The Weekly Brief newsletter. We may also send occasional product updates or announcements. Every email includes an unsubscribe link that works immediately.</p>
    <h2>Email Service Provider</h2>
    <p>We use <a href="https://resend.com">Resend</a> to manage our email list and send newsletters. Your email address is stored in Resend's infrastructure. Resend's privacy policy governs their handling of your data.</p>
    <h2>Analytics</h2>
    <p>We use privacy-respecting analytics to understand which pages are visited and how people find the site. We don't use cookies for tracking, and we don't collect personally identifiable information through analytics.</p>
    <h2>Cookies</h2>
    <p>MOps Report does not set tracking cookies. Our site functions without cookies. Third-party services (Google Fonts, Fontshare) may set their own cookies per their respective policies.</p>
    <h2>Data Retention</h2>
    <p>Email addresses are retained as long as you're subscribed. When you unsubscribe, your email is removed from our active list within 30 days. Backup copies may persist for up to 90 days.</p>
    <h2>Your Rights</h2>
    <p>You can unsubscribe from our newsletter at any time using the link in any email. To request deletion of your data, email us and we'll process it within 30 days.</p>
    <h2>Changes to This Policy</h2>
    <p>We'll update this page when our practices change. Material changes will be noted at the top of this page with the updated date.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Reach out to Rome Thorndike at the email address listed on the <a href="/about/">About</a> page.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/privacy/",
        body_content=body, active_path="/privacy/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("privacy/index.html", page)
    print(f"  Built: privacy/index.html")


def build_terms_page():
    title = "Terms of Service for MOps Report Website"
    description = (
        "MOps Report terms of service. Free salary data, tool reviews, and career"
        " guides for marketing operations professionals. Updated April 2026."
    )
    crumbs = [("Home", "/"), ("Terms of Service", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Terms of Service for MOps Report Website</h1>
</section>
<div class="legal-content">
    <p>Last updated: April 3, 2026</p>
    <h2>Using This Site</h2>
    <p>MOps Report provides salary data, tool reviews, and career resources for marketing operations professionals. The content is free to read and share with attribution. You agree to use the site lawfully and not to scrape, republish, or redistribute our content at scale without permission.</p>
    <h2>Content Accuracy</h2>
    <p>Our salary data comes from analysis of public job postings. While we work to be accurate, this data is for informational purposes only. It should not be your sole source for salary negotiations, hiring decisions, or compensation planning. Individual compensation depends on factors we can't capture in aggregate data.</p>
    <h2>Newsletter</h2>
    <p>Subscribing to The Weekly Brief is free. We send one email per week plus occasional announcements. You can unsubscribe at any time. We will never sell your email address or share it with third parties for marketing purposes.</p>
    <h2>Affiliate Links</h2>
    <p>Some tool reviews contain affiliate links. When you purchase through these links, we may earn a commission at no additional cost to you. Affiliate relationships never influence our ratings or recommendations. We disclose affiliate relationships on relevant pages.</p>
    <h2>Intellectual Property</h2>
    <p>All original content on MOps Report (text, data analysis, graphics, code) is owned by MOps Report. You may quote short excerpts with attribution and a link back to the source page. Reproducing full articles or datasets requires written permission.</p>
    <h2>Limitation of Liability</h2>
    <p>MOps Report provides information as-is. We're not liable for decisions you make based on our salary data, tool reviews, or career advice. Use your judgment and consult relevant professionals for significant career or financial decisions.</p>
    <h2>Changes</h2>
    <p>We may update these terms. Continued use of the site after changes constitutes acceptance. Material changes will be noted with an updated date at the top of this page.</p>
    <h2>Contact</h2>
    <p>Questions about these terms? Reach out via the <a href="/about/">About</a> page.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/terms/",
        body_content=body, active_path="/terms/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("terms/index.html", page)
    print(f"  Built: terms/index.html")


def build_careers_index():
    """Generate the careers index page."""
    title = "Marketing Operations Career Guides"
    description = (
        "Career guides for marketing operations professionals. How to break into MOps,"
        " job market growth, salary expectations, and skills you need to advance."
    )
    crumbs = [("Home", "/"), ("Careers", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Marketing Operations Career Guides</h1>
    <p class="lead">Practical career guidance for every stage of a marketing operations career. Built on real job posting data, not guesswork.</p>
</section>
<div class="container">
    <p>Marketing operations is one of the fastest-growing functions in B2B and B2C organizations. Companies that once had a single "marketing automation admin" now build full MOps teams with specialists in data, tooling, analytics, and campaign operations. The career path has expanded, and so have the questions.</p>
    <p>These guides answer the questions we see most from people entering the field, leveling up, or evaluating their next move.</p>

    <h2>Getting Started</h2>
    <ul>
        <li><a href="/careers/how-to-break-into-mops/">How to Break Into Marketing Operations</a> - Skills, certifications, tools, and paths into the field</li>
        <li><a href="/careers/job-growth/">Marketing Ops Job Market Growth</a> - Demand trends, hiring patterns, and where the market is headed</li>
    </ul>

    <h2>Salary and Compensation</h2>
    <p>Understanding your market value is the foundation of career planning. Our salary data comes from analysis of real job postings, not self-reported surveys.</p>
    <ul>
        <li><a href="/salary/">Salary Index</a> - Complete MOps salary benchmarks</li>
        <li><a href="/salary/entry/">Entry-Level Salaries</a> - What to expect starting out</li>
        <li><a href="/salary/senior/">Senior-Level Salaries</a> - Compensation at the IC peak</li>
        <li><a href="/salary/director/">Director-Level Salaries</a> - Management track compensation</li>
        <li><a href="/salary/calculator/">Salary Calculator</a> - Estimate your market rate</li>
    </ul>

    <h2>Skills and Tools</h2>
    <p>The tools you know shape the roles you qualify for. Our tool reviews show which platforms employers actually require, based on job posting analysis.</p>
    <ul>
        <li><a href="/tools/">MOps Tool Reviews</a> - Rankings by job posting frequency</li>
        <li><a href="/tools/category/marketing-automation/">Marketing Automation Platforms</a> - Marketo, HubSpot, Eloqua, and more</li>
        <li><a href="/tools/category/crm/">CRM Platforms</a> - Salesforce, HubSpot CRM, Dynamics 365</li>
        <li><a href="/tools/category/analytics/">Analytics and BI</a> - Tableau, Looker, Power BI, Domo</li>
    </ul>

    <h2>What Makes a Strong MOps Professional</h2>
    <p>Marketing operations sits at the intersection of marketing strategy, data management, and technology. The best MOps professionals share a few traits:</p>
    <ul>
        <li><strong>Systems thinking.</strong> They see how tools, data, and processes connect across the full revenue cycle, not just their piece of it.</li>
        <li><strong>Technical depth with business context.</strong> They can build a complex lead scoring model and explain why it matters to the CMO in the same conversation.</li>
        <li><strong>Data discipline.</strong> They care about data quality because they have seen what happens when CRM records degrade: bad routing, wrong reporting, lost deals.</li>
        <li><strong>Vendor independence.</strong> They evaluate tools based on fit, not marketing. They know that every platform has trade-offs.</li>
    </ul>
    <p>Whether you are just entering the field or planning your next move, these guides give you the data and context to make informed decisions.</p>
</div>
'''
    body += newsletter_cta_html("Career intel for MOps professionals, delivered weekly.")

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/",
        body_content=body,
        active_path="/careers/",
        extra_head=get_breadcrumb_schema(crumbs),
        body_class="page-inner",
    )
    write_page("careers/index.html", page)
    print(f"  Built: careers/index.html")


def build_careers_break_into_mops():
    """Generate the 'How to Break Into MOps' guide."""
    title = "How to Break Into Marketing Operations"
    description = (
        "A practical guide to starting a career in marketing operations. Skills to learn,"
        " certifications that matter, tools to know, career paths, and salary expectations."
    )
    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("How to Break Into MOps", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Do I need a degree to work in marketing operations?",
         "No specific degree is required. MOps professionals come from marketing, business, IT, analytics, and other backgrounds. Employers care more about platform certifications, hands-on experience, and the ability to work with data than about the name on your diploma."),
        ("What is the best certification for marketing operations?",
         "The most valuable certifications depend on the tools your target employers use. Marketo Certified Expert, HubSpot Marketing Software Certification, and Salesforce Administrator are the three most commonly requested. Start with the platform that dominates your local job market."),
        ("How long does it take to break into MOps?",
         "Most people can land their first MOps role within 6 to 12 months of focused preparation. That timeline assumes you earn at least one platform certification, build hands-on experience (even with free tiers), and can demonstrate data literacy in interviews."),
        ("What salary should I expect as an entry-level MOps professional?",
         "Entry-level MOps roles (Marketing Operations Coordinator, Marketing Automation Specialist) typically pay $55,000 to $75,000 depending on market, company size, and your existing skills. See our salary data for current benchmarks."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>How to Break Into Marketing Operations: A Complete Guide</h1>
    <p class="lead">Everything you need to start a career in MOps. Skills, certifications, tools, paths in, and what to expect when you get there.</p>
</section>
<div class="container">
    <p>Marketing operations is not a field most people plan to enter. It is a field people discover after realizing that marketing campaigns run on systems, and someone needs to build and maintain those systems. If you are organized, curious about technology, and comfortable with data, you are already closer than you think.</p>
    <p>This guide covers what you need to know and do to land your first MOps role.</p>

    <h2>What Marketing Operations Actually Is</h2>
    <p>Marketing operations is the function that makes marketing run. MOps teams manage the technology stack, data infrastructure, campaign execution processes, analytics, and reporting that marketing depends on. When a lead fills out a form and ends up routed to the right sales rep with the right score and the right nurture track, that is MOps at work.</p>
    <p>The scope varies by company. At smaller organizations, one MOps person might manage the entire marketing technology stack. At enterprise companies, MOps teams have specialists for automation, analytics, data management, and tool administration.</p>

    <h2>Skills You Need</h2>
    <p>MOps roles require a combination of technical and business skills. Here is what employers look for, based on our analysis of thousands of job postings:</p>

    <h3>Technical Skills</h3>
    <ul>
        <li><strong>Marketing automation platform proficiency.</strong> Marketo, HubSpot, Pardot, or Eloqua. Pick one and learn it deeply. Marketo and HubSpot appear in the most job postings.</li>
        <li><strong>CRM knowledge.</strong> Salesforce is the default. Understanding objects, fields, campaigns, and how data flows between your CRM and MAP is essential.</li>
        <li><strong>Data management.</strong> List imports, deduplication, normalization, lead scoring, and lifecycle management. This is where MOps earns its keep.</li>
        <li><strong>HTML and CSS basics.</strong> Email templates and landing pages still require hands-on markup. You do not need to be a front-end developer, but you need to be comfortable editing code.</li>
        <li><strong>Analytics and reporting.</strong> Building dashboards, creating attribution reports, and translating data into business recommendations. SQL is increasingly valuable.</li>
        <li><strong>Integration concepts.</strong> APIs, webhooks, iPaaS tools (Zapier, Make, Workato). Connecting tools is half the job.</li>
    </ul>

    <h3>Business Skills</h3>
    <ul>
        <li><strong>Process design.</strong> Mapping out lead flows, campaign operations processes, and SLAs between marketing and sales.</li>
        <li><strong>Stakeholder communication.</strong> Translating technical decisions into business impact for marketing leadership.</li>
        <li><strong>Project management.</strong> MOps teams run campaigns, migrations, integrations, and ongoing maintenance simultaneously.</li>
        <li><strong>Vendor evaluation.</strong> Knowing how to assess tools, negotiate contracts, and plan implementations.</li>
    </ul>

    <h2>Certifications That Matter</h2>
    <p>Certifications signal platform proficiency to employers. They are not a replacement for experience, but they get your resume past the initial screen. Here are the ones worth pursuing:</p>

    <h3>Marketo Certifications</h3>
    <ul>
        <li><strong>Adobe Certified Professional: Marketo Engage Business Practitioner.</strong> The entry-level Marketo cert. Covers campaign setup, lead management, and basic program building.</li>
        <li><strong>Adobe Certified Expert: Marketo Engage Business Practitioner.</strong> The advanced cert that most job postings reference when they say "Marketo certified." Covers complex programs, revenue cycle analytics, and advanced scoring.</li>
    </ul>

    <h3>HubSpot Certifications</h3>
    <ul>
        <li><strong>HubSpot Marketing Software Certification.</strong> Free and accessible. Covers inbound methodology, email, forms, and workflows. Good starting point.</li>
        <li><strong>HubSpot Marketing Hub Software Certification.</strong> More tactical. Covers the Marketing Hub features that MOps teams manage daily.</li>
        <li><strong>HubSpot Revenue Operations Certification.</strong> Newer cert that aligns with the growing overlap between MOps and RevOps.</li>
    </ul>

    <h3>Salesforce Certifications</h3>
    <ul>
        <li><strong>Salesforce Administrator.</strong> The most valuable CRM cert for MOps professionals. Understanding Salesforce administration is required in most enterprise MOps roles.</li>
        <li><strong>Salesforce Marketing Cloud Email Specialist.</strong> Relevant if you target organizations running SFMC.</li>
    </ul>

    <h3>Other Valuable Certifications</h3>
    <ul>
        <li><strong>Google Analytics Certification.</strong> Free and widely recognized. Useful for attribution and web analytics responsibilities.</li>
        <li><strong>SQL fundamentals (various providers).</strong> Not a formal cert, but SQL proficiency is increasingly expected. DataCamp, Mode, or Codecademy all offer solid SQL courses.</li>
    </ul>

    <h2>Tools to Learn First</h2>
    <p>You cannot learn every tool before your first job. Focus on the platforms that appear most frequently in job postings:</p>
    <ol>
        <li><strong>One MAP:</strong> HubSpot (free tier available) or Marketo (request a sandbox through Adobe)</li>
        <li><strong>Salesforce:</strong> Get a free Developer Edition org and learn the basics of objects, fields, campaigns, and reports</li>
        <li><strong>One integration tool:</strong> Zapier (free tier) or Make (free tier) to understand how tools connect</li>
        <li><strong>Excel or Google Sheets:</strong> Data manipulation, VLOOKUP, pivot tables. This is foundational.</li>
        <li><strong>Basic SQL:</strong> Mode Analytics or BigQuery sandbox. Even basic SELECT/JOIN/GROUP BY puts you ahead.</li>
    </ol>
    <p>For a full ranking of tools by job posting frequency, see our <a href="/tools/">MOps tool reviews</a>.</p>

    <h2>Career Paths Into MOps</h2>
    <p>People enter marketing operations from several directions:</p>

    <h3>From Marketing</h3>
    <p>The most common path. You start as a marketing coordinator or campaign manager, develop a reputation as the person who fixes the email templates and cleans the list imports, and gradually take on more technical work. Eventually, the title catches up to the work you are already doing.</p>

    <h3>From Sales Operations or RevOps</h3>
    <p>If you already manage Salesforce for a sales team, moving into MOps means learning the MAP side. The CRM skills transfer directly, and understanding the sales process is a real advantage in MOps.</p>

    <h3>From IT or Engineering</h3>
    <p>Technical people who want to be closer to business outcomes. The technical skills are there; the learning curve is marketing terminology, campaign strategy, and understanding what the marketing team actually needs.</p>

    <h3>From Analytics</h3>
    <p>Data analysts who want to move upstream from reporting into building the systems that generate the data. SQL, BI tools, and data modeling skills are directly applicable.</p>

    <h3>Career Changers</h3>
    <p>People from completely different fields. A certification, a free-tier platform project, and a willingness to start at the coordinator level gets you in the door. The field is growing fast enough that companies hire for aptitude, not just experience.</p>

    <h2>Salary Expectations</h2>
    <p>Marketing operations compensation varies significantly by seniority, location, and company size. Here are approximate ranges based on our <a href="/salary/">salary data</a>:</p>
    <ul>
        <li><strong>Entry-level (Coordinator, Specialist):</strong> $55,000 to $75,000</li>
        <li><strong>Mid-level (Manager, Senior Specialist):</strong> $80,000 to $120,000</li>
        <li><strong>Senior (Senior Manager, Principal):</strong> $110,000 to $160,000</li>
        <li><strong>Director and above:</strong> $140,000 to $200,000+</li>
    </ul>
    <p>Remote roles, major metro locations, and enterprise companies tend to pay at the higher end. See our <a href="/salary/calculator/">salary calculator</a> for a more personalized estimate.</p>

    <h2>How to Get Your First MOps Role</h2>
    <ol>
        <li><strong>Earn one certification.</strong> HubSpot Marketing Software (free) or Marketo Engage Business Practitioner.</li>
        <li><strong>Build something real.</strong> Set up a HubSpot free account, build a lead capture workflow, create a lead scoring model, and document it as a portfolio project.</li>
        <li><strong>Learn the vocabulary.</strong> Read our <a href="/glossary/">MOps glossary</a> so you can speak the language in interviews.</li>
        <li><strong>Target the right job titles.</strong> Marketing Operations Coordinator, Marketing Automation Specialist, Marketing Technology Associate, CRM Coordinator.</li>
        <li><strong>Network in MOps communities.</strong> MO Pros, MarketingOps.com, and LinkedIn MOps groups are where practitioners share openings and advice.</li>
        <li><strong>Apply broadly.</strong> The field is growing at over 40% year-over-year. Companies are hiring faster than the talent pool is growing.</li>
    </ol>

    <h2>What to Expect in Your First Year</h2>
    <p>Your first MOps role will likely involve a mix of campaign execution, list management, email QA, report building, and putting out fires. You will spend time learning the company's specific tech stack, data model, and internal processes. The learning curve is steep, but the skills compound quickly.</p>
    <p>Within 12 to 18 months, you should understand the full lead lifecycle, be comfortable building campaigns independently, and start forming opinions about how to improve the systems you manage. That is when the career starts to accelerate.</p>
</div>
'''
    body += newsletter_cta_html("Weekly career intel for marketing operations professionals.")
    body += faq_html(faq_pairs)

    word_count = len(body.split())
    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + get_article_schema(title, description, "how-to-break-into-mops", "2026-04-01", word_count, url_path="/careers/how-to-break-into-mops/")
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/how-to-break-into-mops/",
        body_content=body,
        active_path="/careers/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("careers/how-to-break-into-mops/index.html", page)
    print(f"  Built: careers/how-to-break-into-mops/index.html")


def build_careers_job_growth():
    """Generate the 'Job Market Growth' page."""
    title = "Marketing Operations Job Market Growth in 2026"
    description = (
        "Marketing operations job market trends and growth data. Hiring patterns,"
        " in-demand skills, remote vs onsite, and where the MOps market is headed."
    )
    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("Job Market Growth", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("How fast is the MOps job market growing?",
         "Marketing operations job postings have grown roughly 40% year-over-year based on our tracking data. The growth is driven by increased marketing technology adoption, the shift to data-driven marketing, and the expansion of RevOps functions that include MOps."),
        ("Is marketing operations a good career in 2026?",
         "Yes. Demand for MOps professionals continues to outpace supply. Salaries are competitive, remote options are common, and the skills are transferable across industries. The biggest risk is platform concentration: building your career around a single tool that loses market share."),
        ("What MOps skills are most in demand?",
         "Salesforce, HubSpot, Marketo, and data analysis skills appear most frequently in MOps job postings. SQL, BI tools (Tableau, Power BI, Looker), and integration platform experience (Zapier, Workato) are growing in demand. See our tools page for current rankings."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>Marketing Operations Job Market Growth: 2026 Trends</h1>
    <p class="lead">Where the MOps job market is, where it is going, and what it means for your career. Data from thousands of tracked job postings.</p>
</section>
<div class="container">
    <p>Marketing operations has gone from a niche function to a core team at most growth-stage and enterprise companies. The data tells a clear story: more companies are hiring MOps professionals, the roles are getting more specialized, and compensation continues to rise.</p>
    <p>This page covers the trends shaping the MOps job market in 2026.</p>

    <h2>Market Growth by the Numbers</h2>
    <p>Based on our analysis of 15,000+ marketing operations job postings, here is what the data shows:</p>
    <ul>
        <li><strong>Year-over-year posting growth:</strong> approximately 42%, measured by volume of new MOps-specific job listings</li>
        <li><strong>Average time to fill:</strong> MOps roles stay open longer than general marketing roles, reflecting a talent shortage</li>
        <li><strong>Salary trajectory:</strong> median MOps compensation has increased 8-12% annually over the past three years</li>
        <li><strong>Remote availability:</strong> approximately 35-40% of MOps roles offer full remote, significantly higher than marketing roles overall</li>
    </ul>

    <h2>What Is Driving the Growth</h2>

    <h3>Marketing Technology Proliferation</h3>
    <p>The average enterprise marketing team uses 12 to 15 tools. Someone has to integrate, manage, and optimize that stack. That someone is the MOps team. As companies add tools, they add MOps headcount to manage them.</p>

    <h3>Revenue Operations Expansion</h3>
    <p>The RevOps model, which unifies marketing, sales, and customer success operations under one function, is creating new demand for MOps skills. Companies building RevOps teams need people who understand marketing technology, data flows, and campaign infrastructure. MOps professionals fit naturally.</p>

    <h3>Data-Driven Marketing Mandates</h3>
    <p>CMOs are under pressure to prove ROI on marketing spend. That requires attribution models, clean data, proper tracking, and reliable reporting. All of those are MOps responsibilities. The shift from "we think marketing works" to "we can prove marketing works" is a permanent change that sustains MOps demand.</p>

    <h3>AI and Automation Adoption</h3>
    <p>The adoption of AI tools in marketing (content generation, predictive scoring, intent data, chatbots) creates new infrastructure to manage. MOps teams are responsible for evaluating, implementing, and maintaining these tools. AI does not replace MOps; it expands the scope of what MOps manages.</p>

    <h2>Hiring Patterns and Trends</h2>

    <h3>Company Size Distribution</h3>
    <p>MOps hiring is concentrated in mid-market (200 to 2,000 employees) and enterprise (2,000+) companies. Startups under 50 people rarely have dedicated MOps roles; the work is usually handled by a generalist marketer. The inflection point tends to happen around 100 to 200 employees, when marketing technology complexity justifies a specialist.</p>

    <h3>Industry Distribution</h3>
    <p>B2B SaaS companies dominate MOps hiring, followed by financial services, healthcare technology, and e-commerce. However, every industry with a mature marketing function hires MOps professionals. The skills transfer across verticals because the tools and processes are largely the same.</p>

    <h3>Remote vs. Onsite</h3>
    <p>MOps is well-suited to remote work. The job is platform management, data analysis, and cross-functional coordination, all of which work over a screen. Our data shows 35-40% of MOps postings are fully remote, 30-35% are hybrid, and 25-30% are onsite. The remote share has stabilized after post-pandemic adjustments.</p>

    <h3>Specialization Trends</h3>
    <p>Early MOps roles were generalist: one person doing everything from email sends to CRM admin. The market is increasingly specialized:</p>
    <ul>
        <li><strong>Marketing Automation Manager:</strong> focused on MAP administration and campaign operations</li>
        <li><strong>Marketing Data Analyst:</strong> focused on attribution, reporting, and data quality</li>
        <li><strong>Marketing Technology Manager:</strong> focused on tool evaluation, integration, and vendor management</li>
        <li><strong>Campaign Operations Specialist:</strong> focused on email, landing pages, and program execution</li>
        <li><strong>MOps Director/VP:</strong> strategic leadership, team building, and budget management</li>
    </ul>

    <h2>Skills Demand Shifts</h2>
    <p>The skills employers want are shifting. Based on changes in job posting requirements over the past 12 months:</p>

    <h3>Growing in Demand</h3>
    <ul>
        <li><strong>SQL and data analysis:</strong> showing up in more postings as companies expect MOps to query databases directly</li>
        <li><strong>CDP and data platform experience:</strong> Segment, Hightouch, Census, and RudderStack mentions are increasing</li>
        <li><strong>Revenue attribution:</strong> multi-touch attribution modeling is now expected at the senior level</li>
        <li><strong>Integration platforms:</strong> Workato, Make, and n8n are appearing alongside (and sometimes replacing) Zapier</li>
        <li><strong>AI tool management:</strong> experience evaluating and implementing AI-powered marketing tools</li>
    </ul>

    <h3>Stable Demand</h3>
    <ul>
        <li><strong>Salesforce:</strong> still the most-mentioned tool in MOps job postings by a wide margin</li>
        <li><strong>HubSpot:</strong> strong and growing, especially in the mid-market</li>
        <li><strong>Marketo:</strong> still required for enterprise B2B roles, though growing more slowly than HubSpot</li>
        <li><strong>Excel/Sheets:</strong> still mentioned in a majority of postings. The basics remain foundational.</li>
    </ul>

    <h3>Declining in Mentions</h3>
    <ul>
        <li><strong>Pardot (Marketing Cloud Account Engagement):</strong> declining as Salesforce shifts investment to Marketing Cloud</li>
        <li><strong>Google Analytics (UA):</strong> replaced by GA4. The skill is still needed, but the specific tool reference is changing.</li>
    </ul>

    <h2>Compensation Trends</h2>
    <p>MOps salaries continue to rise faster than general marketing roles. The combination of technical skill requirements, talent shortages, and business-critical responsibilities creates upward pressure on compensation.</p>
    <p>Key trends:</p>
    <ul>
        <li>Entry-level MOps roles now start $10,000 to $15,000 higher than equivalent marketing coordinator positions</li>
        <li>The premium for Marketo certification is approximately 15-20% at the mid-level</li>
        <li>Director-level MOps roles at enterprise companies routinely exceed $170,000 base</li>
        <li>Remote roles have narrowed the geographic salary gap, but top-market premiums (SF, NYC, Boston) persist</li>
    </ul>
    <p>For current salary data, see our <a href="/salary/">salary benchmarks</a> and <a href="/salary/calculator/">salary calculator</a>.</p>

    <h2>What This Means for Your Career</h2>
    <p>The MOps job market in 2026 favors practitioners who:</p>
    <ol>
        <li><strong>Invest in platform depth.</strong> Knowing one MAP and one CRM deeply is more valuable than surface-level familiarity with five tools.</li>
        <li><strong>Add data skills.</strong> SQL, BI tools, and basic data modeling increasingly separate senior MOps professionals from the pack.</li>
        <li><strong>Stay platform-aware.</strong> The CDP and reverse ETL space is evolving fast. Understanding warehouse-native data activation is becoming a differentiator.</li>
        <li><strong>Build business context.</strong> The MOps professionals who advance fastest can connect technical decisions to revenue impact.</li>
    </ol>
    <p>The market is not slowing down. If you are in MOps, the trajectory is in your favor. If you are considering entering the field, now is a good time. See our guide on <a href="/careers/how-to-break-into-mops/">how to break into marketing operations</a> for a step-by-step plan.</p>
</div>
'''
    body += newsletter_cta_html("Weekly MOps job market data and career intelligence.")
    body += faq_html(faq_pairs)

    word_count = len(body.split())
    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + get_article_schema(title, description, "job-growth", "2026-04-01", word_count, url_path="/careers/job-growth/")
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/job-growth/",
        body_content=body,
        active_path="/careers/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("careers/job-growth/index.html", page)
    print(f"  Built: careers/job-growth/index.html")


def build_insights_page():
    """Generate the insights hub page."""
    title = "MOps Insights: Data and Analysis"
    description = (
        "Data-driven insights for marketing operations. Salary trends, tool adoption,"
        " career guides, and job market analysis from MOps Report."
    )
    crumbs = [("Home", "/"), ("Insights", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>MOps Insights: Data-Driven Analysis</h1>
    <p class="lead">Salary trends, tool adoption, career intelligence, and job market analysis for marketing operations professionals.</p>
</section>
<div class="container">
    <p>MOps Report publishes data-driven analysis on the marketing operations profession. Every insight is built on real job posting data, tool usage patterns, and market research. No vendor spin, no pay-to-play rankings.</p>

    <h2>Salary Intelligence</h2>
    <p>Compensation data based on analysis of thousands of marketing operations job postings. Updated regularly.</p>
    <ul>
        <li><a href="/salary/">Salary Index</a> - Complete MOps salary benchmarks by seniority</li>
        <li><a href="/salary/entry/">Entry-Level MOps Salaries</a> - Starting compensation for coordinators and specialists</li>
        <li><a href="/salary/senior/">Senior MOps Salaries</a> - Compensation at the experienced IC level</li>
        <li><a href="/salary/director/">Director-Level MOps Salaries</a> - Leadership track compensation</li>
        <li><a href="/salary/vp/">VP of Marketing Operations Salaries</a> - Executive-level compensation</li>
        <li><a href="/salary/remote/">Remote vs. Onsite Salaries</a> - How work arrangement affects pay</li>
        <li><a href="/salary/vs-revops/">MOps vs. RevOps Salaries</a> - Side-by-side compensation comparison</li>
        <li><a href="/salary/calculator/">Salary Calculator</a> - Estimate your market rate</li>
    </ul>

    <h2>Tool Reviews and Rankings</h2>
    <p>Tool reviews ranked by employer demand. See which platforms companies actually require, not which ones have the biggest marketing budgets.</p>
    <ul>
        <li><a href="/tools/">MOps Tool Index</a> - All tools ranked by job posting frequency</li>
        <li><a href="/tools/category/marketing-automation/">Marketing Automation</a> - Marketo, HubSpot, Eloqua, Braze</li>
        <li><a href="/tools/category/crm/">CRM Platforms</a> - Salesforce, HubSpot, Dynamics 365</li>
        <li><a href="/tools/category/analytics/">Analytics and BI</a> - Tableau, Looker, Power BI, Domo</li>
        <li><a href="/tools/category/cdp/">Customer Data Platforms</a> - Segment, Hightouch, Census, RudderStack</li>
        <li><a href="/tools/category/integration/">Integration and Automation</a> - Zapier, Make, Workato, n8n</li>
        <li><a href="/tools/category/data-management/">Data Management</a> - ZoomInfo, RingLead, Clay, LeanData</li>
    </ul>

    <h2>Career Guides</h2>
    <p>Practical guidance for entering and advancing in marketing operations.</p>
    <ul>
        <li><a href="/careers/">Career Guides Index</a> - All career resources</li>
        <li><a href="/careers/how-to-break-into-mops/">How to Break Into Marketing Operations</a> - Skills, certs, paths, and salary expectations</li>
        <li><a href="/careers/job-growth/">MOps Job Market Growth</a> - Hiring trends and demand data</li>
    </ul>

    <h2>Reference</h2>
    <ul>
        <li><a href="/glossary/">MOps Glossary</a> - Definitions for marketing operations terms</li>
        <li><a href="/about/">About MOps Report</a> - Our methodology and approach</li>
    </ul>
</div>
'''
    body += newsletter_cta_html("Weekly insights for marketing operations professionals.")

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/insights/",
        body_content=body,
        active_path="/insights/",
        extra_head=get_breadcrumb_schema(crumbs),
        body_class="page-inner",
    )
    write_page("insights/index.html", page)
    print(f"  Built: insights/index.html")


def build_blog_redirect():
    """Generate /blog/ that redirects to /insights/ via meta refresh."""
    content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=/insights/">
    <link rel="canonical" href="https://mopsreport.com/insights/">
    <title>Redirecting to MOps Insights</title>
</head>
<body>
    <p>Redirecting to <a href="/insights/">MOps Insights</a>...</p>
</body>
</html>'''
    from templates import write_page as wp, OUTPUT_DIR as od
    full_path = os.path.join(od, "blog/index.html")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: blog/index.html (redirect to /insights/)")


def build_404_page():
    title = "Page Not Found (404) on MOps Report Site"
    description = (
        "The page you're looking for doesn't exist on MOps Report. Browse marketing operations"
        " salary data, tool reviews, and career guides, or head back to the homepage."
    )
    body = '''<div class="error-page">
    <div class="error-code">404</div>
    <h1>Page Not Found (404) on MOps Report</h1>
    <p>The page you're looking for doesn't exist or has been moved. Try one of these instead:</p>
    <div style="display:flex;flex-direction:column;gap:0.75rem;align-items:center;">
        <a href="/" class="btn btn--primary">Back to Homepage</a>
        <a href="/salary/" class="btn btn--ghost">Browse Salary Data</a>
        <a href="/newsletter/" class="btn btn--ghost">Get the Newsletter</a>
    </div>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/404.html",
        body_content=body, body_class="page-inner",
    )
    write_page("404.html", page)
    print(f"  Built: 404.html")


# ---------------------------------------------------------------------------
# Sitemap + Robots
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = ""
    for page_path in ALL_PAGES:
        clean = page_path.replace("index.html", "")
        if not clean.startswith("/"):
            clean = "/" + clean
        if not clean.endswith("/"):
            clean += "/"
        if clean == "//":
            clean = "/"
        urls += f"  <url>\n    <loc>{SITE_URL}{clean}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>\n"

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  Built: sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml

# AI/LLM crawlers - explicitly allowed for AI search citations
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GoogleOther
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


def build_llms_txt():
    content = f"""# MOps Report

> MOps Report is an independent career intelligence platform for marketing operations professionals. The site provides salary benchmarks by seniority and location, vendor-neutral tool reviews for marketing automation platforms, CDPs, integration tools, and analytics, a searchable glossary of MOps terminology, and career guides for breaking into and advancing in marketing operations. All data is updated weekly and free to access.

## Core Pages
- [Homepage]({SITE_URL}/)
- [About]({SITE_URL}/about/)
- [Newsletter]({SITE_URL}/newsletter/)

## Salary Data
- [Salary Index]({SITE_URL}/salary/): Aggregate MOps salary benchmarks
- [Entry-Level]({SITE_URL}/salary/entry/)
- [Mid-Level]({SITE_URL}/salary/mid/)
- [Senior]({SITE_URL}/salary/senior/)
- [Director]({SITE_URL}/salary/director/)
- [VP]({SITE_URL}/salary/vp/)
- [Remote]({SITE_URL}/salary/remote/)
- [Salary Calculator]({SITE_URL}/salary/calculator/)

### Salary Comparisons
- [MOps vs RevOps]({SITE_URL}/salary/vs-revops/)
- [MOps vs Sales Ops]({SITE_URL}/salary/vs-sales-ops/)
- [MOps vs Data Analyst]({SITE_URL}/salary/vs-data-analyst/)
- [MOps vs Demand Gen]({SITE_URL}/salary/vs-demand-gen/)

## Tool Reviews
- [Tools Index]({SITE_URL}/tools/): All MOps tools reviewed
- [Marketing Automation]({SITE_URL}/tools/category/marketing-automation/)
- [CDP]({SITE_URL}/tools/category/cdp/)
- [Data Management]({SITE_URL}/tools/category/data-management/)
- [Analytics]({SITE_URL}/tools/category/analytics/)
- [Integration]({SITE_URL}/tools/category/integration/)

### Tool Comparisons
- [Marketo vs HubSpot]({SITE_URL}/tools/compare/marketo-vs-hubspot/)
- [Salesforce vs HubSpot]({SITE_URL}/tools/compare/salesforce-vs-hubspot/)
- [Make vs Zapier]({SITE_URL}/tools/compare/make-vs-zapier/)
- [Tableau vs Looker]({SITE_URL}/tools/compare/tableau-vs-looker/)

## Career Resources
- [Career Guides]({SITE_URL}/careers/)
- [How to Break Into MOps]({SITE_URL}/careers/how-to-break-into-mops/)
- [Job Market Growth]({SITE_URL}/careers/job-growth/)

## Glossary
- [Glossary Index]({SITE_URL}/glossary/): MOps terminology defined
- [Marketing Automation Platform]({SITE_URL}/glossary/marketing-automation-platform/)
- [Customer Data Platform]({SITE_URL}/glossary/customer-data-platform/)
- [Lead Scoring]({SITE_URL}/glossary/lead-scoring/)
- [Marketing Attribution]({SITE_URL}/glossary/marketing-attribution/)
- [Email Deliverability]({SITE_URL}/glossary/email-deliverability/)
"""
    with open(os.path.join(OUTPUT_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: llms.txt")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"=== MOps Report Build ({BUILD_DATE}) ===\n")

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print("  Cleaned output/")

    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print("  Copied assets/")

    # Copy static pages (resource directories, etc.)
    pages_dir = os.path.join(PROJECT_DIR, "pages")
    if os.path.exists(pages_dir):
        for item in os.listdir(pages_dir):
            src = os.path.join(pages_dir, item)
            dst = os.path.join(OUTPUT_DIR, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        print("  Copied pages/")

    print("\n  Building core pages...")
    build_homepage()
    build_about_page()
    build_newsletter_page()
    build_privacy_page()
    build_terms_page()
    build_404_page()

    print("\n  Building career pages...")
    build_careers_index()
    build_careers_break_into_mops()
    build_careers_job_growth()

    print("\n  Building insights and blog...")
    build_insights_page()
    build_blog_redirect()

    print("\n  Building salary pages...")
    build_all_salary_pages(PROJECT_DIR)

    print("\n  Building tools pages...")
    build_all_tools_pages(PROJECT_DIR)

    print("\n  Building glossary pages...")
    build_all_glossary_pages(PROJECT_DIR)

    build_all_company_pages(PROJECT_DIR)

    build_all_report_pages(PROJECT_DIR)

    print("\n  Building conference pages...")
    build_conferences_index()

    print("\n  Building meta files...")
    build_sitemap()
    build_robots()
    build_llms_txt()

    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("mopsreport.com\n")
    print("  Built: CNAME")

    # Google Search Console verification file
    if GOOGLE_SITE_VERIFICATION:
        verification_path = os.path.join(OUTPUT_DIR, GOOGLE_SITE_VERIFICATION)
        with open(verification_path, "w", encoding="utf-8") as f:
            f.write(f"google-site-verification: {GOOGLE_SITE_VERIFICATION}")
        print(f"  Generated {GOOGLE_SITE_VERIFICATION}")

    print(f"\n=== Build complete: {len(ALL_PAGES)} pages ===")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")


if __name__ == "__main__":
    main()
