# scripts/tools_pages.py
# Tool review section generators. Called from build.py.
# Data source: data/market_intelligence.json

import os
import json
import re

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)


# ---------------------------------------------------------------------------
# Data + helpers
# ---------------------------------------------------------------------------

def load_tools_data(project_dir):
    path = os.path.join(project_dir, "data", "market_intelligence.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def pct_of_jobs(mentions, total):
    return round((mentions / total) * 100, 1)


def stat_cards_html(cards):
    items = ""
    for val, label in cards:
        items += f'''<div class="stat-block">
    <span class="stat-value">{val}</span>
    <span class="stat-label">{label}</span>
</div>\n'''
    return f'<div class="stat-grid">{items}</div>'


# ---------------------------------------------------------------------------
# Generic tech filter
# ---------------------------------------------------------------------------

GENERIC_TECH = {
    "Rag", "Rust", "Aws", "Python", "Azure", "Gcp", "Kubernetes", "Docker",
    "Javascript", "Openai", "Langchain", "Claude", "G2",
}


def get_mops_tools(tools_dict):
    """Return dict of MOps-relevant tools only."""
    return {k: v for k, v in tools_dict.items() if k not in GENERIC_TECH}


# ---------------------------------------------------------------------------
# Category definitions
# ---------------------------------------------------------------------------

CATEGORIES = {
    "marketing-automation": {
        "name": "Marketing Automation",
        "description": "Marketing automation platforms (MAPs) are the backbone of modern marketing operations. They handle email campaigns, lead nurturing, scoring, segmentation, and multi-channel orchestration.",
        "tools": ["Marketo", "Hubspot", "Hubspot Marketing", "Salesforce Marketing Cloud", "Eloqua", "Braze", "Klaviyo", "Iterable", "Drip"],
        "buyer_guide": "When evaluating marketing automation platforms, focus on four dimensions: CRM integration depth, lead scoring flexibility, reporting granularity, and total cost of ownership. Enterprise teams running complex multi-touch campaigns need the segmentation and branching logic of Marketo or Eloqua. Growth-stage companies with simpler needs often get more value from HubSpot's all-in-one approach.",
    },
    "cdp": {
        "name": "Customer Data Platforms (CDP)",
        "description": "CDPs unify customer data across sources into a single profile. For MOps teams, they solve identity resolution, audience building, and data activation across channels.",
        "tools": ["Segment", "Rudderstack", "Hightouch", "Census"],
        "buyer_guide": "The CDP market has split into two camps: traditional CDPs (Segment, mParticle) that ingest, unify, and activate data, and reverse ETL tools (Hightouch, Census) that activate data already in your warehouse. If your company has a mature data warehouse, reverse ETL may be the better fit. If you need identity resolution and event tracking from scratch, a traditional CDP makes more sense.",
    },
    "data-management": {
        "name": "Data Management",
        "description": "Data management tools handle the hygiene, deduplication, normalization, and enrichment that keep marketing databases clean. For MOps teams, these tools are the difference between a CRM that works and one that erodes trust.",
        "tools": ["Ringlead", "Ringlead Revops", "Zoominfo", "Clay", "Apollo", "Seamless Ai"],
        "buyer_guide": "Data management is not a single purchase. You need solutions for deduplication, normalization, enrichment, and ongoing monitoring. Some tools (like RingLead) focus on dedup and routing. Others (ZoomInfo, Apollo) combine enrichment with prospecting. Start by auditing your biggest data quality problem and solve that first.",
    },
    "analytics": {
        "name": "Analytics and BI",
        "description": "Analytics and business intelligence tools turn raw marketing data into dashboards, reports, and insights. MOps teams use them to measure campaign performance, track attribution, and provide visibility to marketing leadership.",
        "tools": ["Tableau", "Looker", "Power Bi", "Domo"],
        "buyer_guide": "The BI tool choice often depends on your existing tech stack. Looker pairs naturally with BigQuery and Google Cloud. Power BI integrates tightly with Microsoft environments. Tableau is the most flexible but has the steepest learning curve. Domo targets business users who want self-serve dashboards without SQL.",
    },
    "integration": {
        "name": "Integration and Automation",
        "description": "Integration tools connect marketing systems that do not natively talk to each other. They range from simple point-to-point connectors to enterprise iPaaS platforms that handle complex multi-step workflows.",
        "tools": ["Zapier", "Make", "Workato", "Workato Ipaas", "N8N"],
        "buyer_guide": "For simple two-system connections, Zapier and Make handle most use cases at low cost. When workflows get complex (branching logic, error handling, data transformation), enterprise iPaaS platforms like Workato become necessary. n8n offers a self-hosted option for teams with privacy requirements or high-volume automations where per-task pricing gets expensive.",
    },
    "crm": {
        "name": "CRM",
        "description": "CRM platforms are the system of record for customer data. MOps teams manage CRM configuration, integrations, data quality, and the workflows that connect marketing activity to sales outcomes.",
        "tools": ["Salesforce", "Hubspot", "Dynamics 365"],
        "buyer_guide": "Salesforce dominates enterprise CRM and appears in more MOps job postings than any other tool. HubSpot CRM gains share in the mid-market with its lower total cost of ownership and marketing-native integration. Dynamics 365 shows up in Microsoft-aligned enterprises. Your CRM choice constrains most other technology decisions in the stack.",
    },
}

# Normalize tool name lookup (data uses title case like "Hubspot", we need to match)
def find_tool_mentions(tool_name, tools_dict):
    """Find mentions for a tool, trying common name variants."""
    # Direct match
    if tool_name in tools_dict:
        return tools_dict[tool_name]
    # Case-insensitive match
    lower = tool_name.lower()
    for k, v in tools_dict.items():
        if k.lower() == lower:
            return v
    return 0


# ---------------------------------------------------------------------------
# Tool metadata for individual reviews
# ---------------------------------------------------------------------------

TOOL_META = {
    "Salesforce": {
        "display": "Salesforce",
        "category": "crm",
        "description": "Salesforce is the dominant CRM platform in enterprise marketing operations. It serves as the system of record for customer data, pipeline management, and marketing-sales alignment.",
        "pricing": "Essentials from $25/user/mo, Professional $80/user/mo, Enterprise $165/user/mo, Unlimited $330/user/mo",
        "founded": "1999",
        "hq": "San Francisco, CA",
        "features": [
            "Lead and contact management with custom objects",
            "Opportunity tracking and pipeline management",
            "Campaign influence and multi-touch attribution (with add-ons)",
            "Flow Builder for process automation",
            "AppExchange ecosystem with thousands of integrations",
            "Einstein AI for lead scoring and forecasting",
        ],
        "pros": [
            "Industry standard, required in most enterprise MOps roles",
            "Deepest customization of any CRM platform",
            "Massive ecosystem of integrations and consultants",
            "Strong reporting with cross-object relationships",
        ],
        "cons": [
            "High total cost of ownership (licensing + admin + consulting)",
            "Steep learning curve for advanced configuration",
            "Many core MOps features require paid add-ons",
            "Technical debt accumulates quickly in complex orgs",
        ],
    },
    "Hubspot": {
        "display": "HubSpot",
        "category": "crm",
        "description": "HubSpot combines CRM, marketing automation, and sales tools in a single platform. For MOps teams, it offers the lowest barrier to entry for companies that want integrated marketing and sales operations.",
        "pricing": "Free CRM available. Marketing Hub Starter $20/mo, Professional $890/mo, Enterprise $3,600/mo",
        "founded": "2006",
        "hq": "Cambridge, MA",
        "features": [
            "Native CRM with marketing automation built in",
            "Email marketing, landing pages, and forms",
            "Lead scoring and lifecycle stage management",
            "Attribution reporting (multi-touch in Enterprise)",
            "Workflow automation with branching logic",
            "Operations Hub for data sync and programmable automation",
        ],
        "pros": [
            "All-in-one platform reduces integration complexity",
            "Lower total cost of ownership vs. Salesforce + MAP stack",
            "Strong onboarding and documentation",
            "Operations Hub adds serious MOps functionality",
        ],
        "cons": [
            "Enterprise features require highest pricing tier",
            "Less customizable than Salesforce for complex use cases",
            "Contact-based pricing can get expensive at scale",
            "Reporting is improving but still behind dedicated BI tools",
        ],
    },
    "Marketo": {
        "display": "Marketo (Adobe)",
        "category": "marketing-automation",
        "description": "Marketo Engage is Adobe's enterprise marketing automation platform. It is the MAP of choice for large B2B organizations with complex lead management, scoring, and nurturing requirements.",
        "pricing": "Growth from ~$895/mo, Select ~$1,795/mo, Prime and Ultimate by quote. Adobe bundles available.",
        "founded": "2006 (acquired by Adobe 2018)",
        "hq": "San Jose, CA (Adobe)",
        "features": [
            "Advanced lead scoring with behavioral and demographic dimensions",
            "Multi-stream nurture programs with engagement scoring",
            "Revenue cycle analytics and attribution",
            "Account-based marketing features",
            "Extensive API for custom integrations",
            "Dynamic content and personalization",
        ],
        "pros": [
            "Most powerful B2B marketing automation for complex use cases",
            "Deep Salesforce integration (native connector)",
            "Strong program library and template ecosystem",
            "Best-in-class lead scoring flexibility",
        ],
        "cons": [
            "High price point, especially for smaller teams",
            "User interface has not kept pace with newer competitors",
            "Requires dedicated admin (Marketo-certified professionals are in demand)",
            "Reporting has gaps that require BI tool supplementation",
        ],
    },
    "Salesforce Marketing Cloud": {
        "display": "Salesforce Marketing Cloud",
        "category": "marketing-automation",
        "description": "Salesforce Marketing Cloud is the enterprise marketing automation suite within the Salesforce ecosystem. It handles email, mobile, social, advertising, and journey orchestration at scale.",
        "pricing": "Starting at ~$1,250/mo for email. Full suite pricing varies significantly by modules and volume.",
        "founded": "2000 (ExactTarget, acquired by Salesforce 2013)",
        "hq": "Indianapolis, IN / San Francisco, CA",
        "features": [
            "Journey Builder for multi-channel campaign orchestration",
            "Email Studio with advanced personalization",
            "Audience Builder for segmentation",
            "Data extensions and SQL-based segmentation",
            "Native Salesforce CRM integration",
            "Einstein AI features for send-time optimization and engagement scoring",
        ],
        "pros": [
            "Deepest native integration with Salesforce CRM",
            "Enterprise-grade scalability for high-volume senders",
            "Strong multi-channel orchestration (email, SMS, push, ads)",
            "AMPscript and SSJS for advanced customization",
        ],
        "cons": [
            "Complex pricing across multiple studios and builders",
            "Steep learning curve (AMPscript, SQL, Journey Builder)",
            "Less intuitive than HubSpot or Marketo for basic use cases",
            "Implementation typically requires specialized consultants",
        ],
    },
    "Tableau": {
        "display": "Tableau",
        "category": "analytics",
        "description": "Tableau is the leading visual analytics platform. MOps teams use it to build marketing performance dashboards, attribution reports, and executive-facing data visualizations.",
        "pricing": "Tableau Creator $75/user/mo, Explorer $42/user/mo, Viewer $15/user/mo. Tableau Public is free.",
        "founded": "2003 (acquired by Salesforce 2019)",
        "hq": "Seattle, WA",
        "features": [
            "Drag-and-drop visual analytics with deep drill-down",
            "Live and extract connections to 100+ data sources",
            "Calculated fields and LOD expressions for complex analysis",
            "Dashboard actions and interactivity",
            "Tableau Prep for data cleaning and transformation",
            "Tableau Server/Cloud for enterprise deployment",
        ],
        "pros": [
            "Most flexible visualization tool on the market",
            "Handles large datasets without performance issues",
            "Strong community and learning resources",
            "Salesforce integration is improving post-acquisition",
        ],
        "cons": [
            "Steep learning curve for advanced features (LOD expressions, table calcs)",
            "Licensing costs add up with many users",
            "Not purpose-built for marketing; requires setup for MOps use cases",
            "Self-service for non-technical users is limited",
        ],
    },
    "Looker": {
        "display": "Looker",
        "category": "analytics",
        "description": "Looker is Google Cloud's enterprise BI platform. It uses a modeling layer (LookML) to define metrics centrally, which makes it popular with data-driven organizations that want consistent reporting definitions.",
        "pricing": "Contact Google Cloud for pricing. Typically starts at ~$5,000/mo for small deployments.",
        "founded": "2012 (acquired by Google 2020)",
        "hq": "Santa Cruz, CA (Google Cloud)",
        "features": [
            "LookML modeling language for centralized metric definitions",
            "In-database architecture (queries your warehouse directly)",
            "Embedded analytics for customer-facing dashboards",
            "Explore interface for ad-hoc analysis",
            "API-first design for programmatic access",
            "Native BigQuery integration",
        ],
        "pros": [
            "Single source of truth for metric definitions",
            "Strong for teams with a mature data warehouse",
            "Excellent embedded analytics capabilities",
            "Version-controlled models with Git integration",
        ],
        "cons": [
            "LookML learning curve is real (requires data team investment)",
            "Less visual flexibility than Tableau",
            "Google Cloud lock-in concern for some organizations",
            "Not ideal for quick, ad-hoc visual exploration",
        ],
    },
    "Power Bi": {
        "display": "Power BI",
        "category": "analytics",
        "description": "Microsoft Power BI is the most widely deployed BI tool by user count. Its strength for MOps teams lies in Microsoft ecosystem integration and low per-user cost.",
        "pricing": "Power BI Pro $10/user/mo, Premium Per User $20/user/mo, Premium capacity from $4,995/mo",
        "founded": "2015",
        "hq": "Redmond, WA (Microsoft)",
        "features": [
            "DAX formula language for calculated measures",
            "DirectQuery and import modes for data connectivity",
            "Power Query for data transformation (shared with Excel)",
            "Paginated reports for pixel-perfect output",
            "Dataflows for reusable data preparation",
            "Native integration with Azure, Dynamics 365, and Microsoft 365",
        ],
        "pros": [
            "Lowest per-user cost of major BI platforms",
            "Strong for Microsoft-stack organizations",
            "Power Query skills transfer from Excel",
            "Rapid adoption due to familiar Microsoft interface",
        ],
        "cons": [
            "DAX has a steep learning curve for complex calculations",
            "Linux/Mac support is limited (web-only for non-Windows)",
            "Premium features require significant cost jump",
            "Less flexible than Tableau for complex visualizations",
        ],
    },
    "Zapier": {
        "display": "Zapier",
        "category": "integration",
        "description": "Zapier is the most popular no-code integration platform. MOps teams use it for quick connections between marketing tools, CRMs, and data warehouses without writing code.",
        "pricing": "Free (100 tasks/mo), Starter $19.99/mo, Professional $49/mo, Team $69/mo, Company from $99/mo",
        "founded": "2011",
        "hq": "San Francisco, CA (remote-first)",
        "features": [
            "7,000+ app integrations",
            "Multi-step Zaps with branching logic",
            "Filters, formatters, and data transformation",
            "Webhooks for custom triggers and actions",
            "Paths for conditional logic",
            "Tables for lightweight data storage",
        ],
        "pros": [
            "Largest integration library of any platform",
            "No-code setup accessible to non-technical MOps teams",
            "Fast to deploy for simple integrations",
            "Reliable for low-to-moderate volume workflows",
        ],
        "cons": [
            "Per-task pricing gets expensive at high volume",
            "Limited error handling compared to enterprise iPaaS",
            "Complex workflows become hard to manage and debug",
            "Not suitable for real-time, high-throughput use cases",
        ],
    },
    "Braze": {
        "display": "Braze",
        "category": "marketing-automation",
        "description": "Braze is a customer engagement platform built for mobile-first and multi-channel marketing. It is popular with B2C companies and increasingly adopted by B2B organizations with product-led growth motions.",
        "pricing": "Custom pricing based on monthly active users. Typically starts at ~$50K/year for mid-market.",
        "founded": "2011",
        "hq": "New York, NY",
        "features": [
            "Real-time event-triggered messaging across channels",
            "Canvas flow builder for journey orchestration",
            "Push notifications, in-app messages, email, SMS, and webhooks",
            "Currents data streaming for real-time event export",
            "Content Cards for persistent in-app content",
            "Liquid templating for dynamic personalization",
        ],
        "pros": [
            "Best-in-class for mobile and multi-channel engagement",
            "Real-time event processing with low latency",
            "Strong developer API and SDK ecosystem",
            "Growing presence in B2B PLG companies",
        ],
        "cons": [
            "High entry price excludes smaller companies",
            "B2B features lag behind Marketo and HubSpot",
            "Requires engineering resources for full implementation",
            "Attribution and reporting are less mature than competitors",
        ],
    },
    "Eloqua": {
        "display": "Oracle Eloqua",
        "category": "marketing-automation",
        "description": "Oracle Eloqua is an enterprise marketing automation platform used primarily by large B2B organizations. It offers deep segmentation, lead scoring, and multi-step campaign management.",
        "pricing": "Custom enterprise pricing. Typically $2,000-$4,000+/mo depending on contacts and features.",
        "founded": "1999 (acquired by Oracle 2012)",
        "hq": "Austin, TX (Oracle)",
        "features": [
            "Campaign Canvas for visual campaign design",
            "Advanced segmentation with contact and account filters",
            "Lead scoring with profile and engagement dimensions",
            "Program Builder for automated workflows",
            "CRM integration (native Oracle CX, connectors for Salesforce)",
            "Profiler for sales-visible engagement data",
        ],
        "pros": [
            "Strong for complex B2B campaign orchestration",
            "Deep segmentation capabilities",
            "Good fit for Oracle CX ecosystem companies",
            "Robust contact washing and data management features",
        ],
        "cons": [
            "Declining market share vs. Marketo and HubSpot",
            "Interface feels dated compared to newer platforms",
            "Oracle ecosystem lock-in concerns",
            "Smaller talent pool than Marketo or HubSpot specialists",
        ],
    },
    "Workato": {
        "display": "Workato",
        "category": "integration",
        "description": "Workato is an enterprise integration and automation platform (iPaaS). It handles complex multi-step workflows, data transformations, and cross-system orchestration that no-code tools like Zapier cannot manage.",
        "pricing": "Custom pricing based on recipes and connections. Typically $10,000+/year for mid-market deployments.",
        "founded": "2013",
        "hq": "Mountain View, CA",
        "features": [
            "Recipe-based automation with 1,000+ connectors",
            "Workbot for Slack/Teams-triggered automations",
            "API management and custom connector framework",
            "Enterprise-grade error handling and logging",
            "Workspace for team collaboration on recipes",
            "Autopilot mode for AI-assisted recipe building",
        ],
        "pros": [
            "Enterprise-grade reliability and error handling",
            "Handles complex, multi-step workflows that Zapier cannot",
            "Strong governance and security features",
            "Growing fast in the MOps integration space",
        ],
        "cons": [
            "Significantly more expensive than Zapier or Make",
            "Steeper learning curve for non-technical users",
            "Overkill for simple point-to-point integrations",
            "Pricing opacity can make budgeting difficult",
        ],
    },
    "Make": {
        "display": "Make (formerly Integromat)",
        "category": "integration",
        "description": "Make is a visual integration platform that sits between Zapier (simplicity) and Workato (enterprise power). Its visual workflow builder and per-operation pricing make it popular with cost-conscious MOps teams.",
        "pricing": "Free (1,000 ops/mo), Core $9/mo, Pro $16/mo, Teams $29/mo, Enterprise by quote",
        "founded": "2012 (rebranded from Integromat in 2022)",
        "hq": "Prague, Czech Republic",
        "features": [
            "Visual scenario builder with drag-and-drop modules",
            "1,500+ app integrations",
            "Data transformation with built-in functions",
            "Error handling with retry and fallback routes",
            "Webhooks and HTTP modules for custom connections",
            "Data stores for persistent state between runs",
        ],
        "pros": [
            "Visual builder makes complex workflows transparent",
            "Per-operation pricing is cheaper than Zapier at volume",
            "Better error handling than Zapier",
            "Good balance of power and usability",
        ],
        "cons": [
            "Smaller integration library than Zapier",
            "Less enterprise-grade than Workato",
            "Community is smaller, fewer tutorials available",
            "Some modules lack depth compared to native integrations",
        ],
    },
    "N8N": {
        "display": "n8n",
        "category": "integration",
        "description": "n8n is an open-source workflow automation tool. It can be self-hosted or used as a cloud service, making it attractive to MOps teams with privacy requirements or high-volume workflows where per-task pricing gets prohibitive.",
        "pricing": "Self-hosted: free (open source). Cloud: Starter $20/mo, Pro $50/mo, Enterprise by quote.",
        "founded": "2019",
        "hq": "Berlin, Germany",
        "features": [
            "Open-source with self-hosting option",
            "Visual workflow editor with 400+ integrations",
            "Custom JavaScript/Python code nodes",
            "Webhook triggers and API endpoints",
            "Credential sharing across workflows",
            "Error workflows for automated failure handling",
        ],
        "pros": [
            "Self-hosting eliminates per-execution costs",
            "Open-source transparency and auditability",
            "Custom code nodes for anything not covered by integrations",
            "Active open-source community",
        ],
        "cons": [
            "Self-hosting requires DevOps resources",
            "Fewer integrations than Zapier or Make",
            "Less polished UI than commercial competitors",
            "Enterprise support requires paid plan",
        ],
    },
    "Zoominfo": {
        "display": "ZoomInfo",
        "category": "data-management",
        "description": "ZoomInfo is a B2B data provider and sales intelligence platform. MOps teams use it for contact enrichment, account scoring, and maintaining data quality in the CRM.",
        "pricing": "Custom pricing based on credits and seats. Typically $15,000-$40,000+/year for MOps-focused packages.",
        "founded": "2000",
        "hq": "Vancouver, WA",
        "features": [
            "Company and contact database with 100M+ profiles",
            "Intent data for account-based marketing",
            "CRM enrichment and data cleansing integrations",
            "Website visitor identification",
            "Workflow automation for lead routing",
            "FormComplete for progressive profiling",
        ],
        "pros": [
            "Largest B2B contact database",
            "Intent data adds signal for account prioritization",
            "Strong CRM and MAP integrations",
            "Company hierarchy data useful for ABM",
        ],
        "cons": [
            "Expensive, especially for small-to-mid teams",
            "Data accuracy varies by region and company size",
            "Annual contracts with aggressive renewal tactics",
            "Privacy and compliance concerns in some regions",
        ],
    },
    "Demandbase": {
        "display": "Demandbase",
        "category": "data-management",
        "description": "Demandbase is an account-based marketing and sales intelligence platform. MOps teams use it for account identification, intent signals, and ABM campaign orchestration.",
        "pricing": "Custom pricing. Typically $30,000-$100,000+/year depending on modules and account volume.",
        "founded": "2007",
        "hq": "San Francisco, CA",
        "features": [
            "Account identification and intent data",
            "ABM campaign orchestration",
            "B2B advertising with account targeting",
            "Website personalization by account",
            "Sales intelligence dashboards",
            "Integration with major MAPs and CRMs",
        ],
        "pros": [
            "Best-in-class ABM orchestration",
            "Strong account identification technology",
            "Intent data helps prioritize high-value accounts",
            "Good Salesforce and Marketo integrations",
        ],
        "cons": [
            "Very expensive for mid-market companies",
            "Complex implementation and onboarding",
            "Overlap with ZoomInfo creates tool sprawl questions",
            "ROI attribution for ABM is inherently difficult",
        ],
    },
    "6Sense": {
        "display": "6sense",
        "category": "data-management",
        "description": "6sense is a predictive intelligence platform for B2B revenue teams. It uses AI to identify accounts in market, predict buying stage, and orchestrate outreach timing.",
        "pricing": "Custom pricing. Enterprise deals typically $50,000-$150,000+/year.",
        "founded": "2013",
        "hq": "San Francisco, CA",
        "features": [
            "AI-powered account identification and intent signals",
            "Buying stage prediction (awareness through decision)",
            "Dark funnel visibility for anonymous web traffic",
            "Audience building for advertising and outreach",
            "CRM and MAP integration for orchestration",
            "Revenue AI for pipeline forecasting",
        ],
        "pros": [
            "Strongest predictive capabilities in the ABM space",
            "Dark funnel visibility provides unique insights",
            "Buying stage prediction helps time outreach",
            "Growing integration ecosystem",
        ],
        "cons": [
            "Very high price point limits accessibility",
            "Prediction accuracy varies by industry and data volume",
            "Requires data maturity to get full value",
            "Long implementation timeline for enterprise deployments",
        ],
    },
    "Leandata": {
        "display": "LeanData",
        "category": "data-management",
        "description": "LeanData is a lead-to-account matching and routing platform built natively on Salesforce. MOps teams use it to ensure leads reach the right sales rep and attribute pipeline to the correct campaigns.",
        "pricing": "Starting at ~$39/user/mo for routing. Enterprise pricing for full platform.",
        "founded": "2012",
        "hq": "Sunnyvale, CA",
        "features": [
            "Visual lead routing with drag-and-drop flowcharts",
            "Lead-to-account matching",
            "Round-robin and weighted assignment",
            "BookIt for calendar-based routing",
            "Revenue attribution and influence reporting",
            "Native Salesforce integration (runs in your org)",
        ],
        "pros": [
            "Best visual routing builder in the market",
            "Native Salesforce means no data leaves your org",
            "Solves a real pain point (lead routing accuracy)",
            "Clean UI for complex routing logic",
        ],
        "cons": [
            "Salesforce-only (no HubSpot or Dynamics support)",
            "Pricing adds up with per-user model",
            "Attribution module is newer and less proven",
            "Requires Salesforce admin knowledge for advanced setups",
        ],
    },
    "Dynamics 365": {
        "display": "Microsoft Dynamics 365",
        "category": "crm",
        "description": "Microsoft Dynamics 365 is an enterprise CRM and ERP platform. It appears in MOps roles at Microsoft-aligned organizations, particularly in industries like manufacturing, healthcare, and financial services.",
        "pricing": "Sales Professional $65/user/mo, Sales Enterprise $95/user/mo, Marketing from $1,500/mo",
        "founded": "2016 (evolved from Dynamics CRM)",
        "hq": "Redmond, WA (Microsoft)",
        "features": [
            "Sales, Marketing, Customer Service, and Field Service modules",
            "Power Platform integration (Power BI, Power Automate, Power Apps)",
            "Customer Insights for CDP-like functionality",
            "LinkedIn Sales Navigator integration",
            "AI-driven sales and marketing insights",
            "Azure-native data and security model",
        ],
        "pros": [
            "Strong for Microsoft-stack enterprises",
            "Power Platform extends functionality without code",
            "LinkedIn integration is a differentiator",
            "Competitive pricing vs. Salesforce at similar scale",
        ],
        "cons": [
            "Smaller MOps talent pool than Salesforce or HubSpot",
            "Marketing module is less mature than dedicated MAPs",
            "Implementation complexity rivals Salesforce",
            "Third-party integration ecosystem is smaller",
        ],
    },
    "Segment": {
        "display": "Segment",
        "category": "cdp",
        "description": "Segment is a customer data platform (CDP) that collects, cleans, and routes event data from websites, apps, and servers to downstream tools. For MOps teams, it solves the data collection and identity resolution layer that marketing automation platforms depend on.",
        "pricing": "Free tier available (1,000 visitors/mo). Team from $120/mo. Business pricing is custom based on volume.",
        "founded": "2012 (acquired by Twilio 2020)",
        "hq": "San Francisco, CA (Twilio)",
        "features": [
            "Event tracking across web, mobile, and server sources",
            "Identity resolution and profile unification",
            "300+ pre-built integrations for data routing",
            "Protocols for data quality enforcement and schema validation",
            "Audiences for real-time segmentation and activation",
            "Functions for custom data transformations in JavaScript",
        ],
        "pros": [
            "Industry standard for event data collection and routing",
            "Reduces integration burden by acting as a single data pipe",
            "Strong data governance with Protocols",
            "Large integration catalog covers most marketing tools",
        ],
        "cons": [
            "Volume-based pricing gets expensive at scale",
            "Twilio acquisition has introduced uncertainty about product direction",
            "Warehouse-native alternatives (Hightouch, Census) challenge the traditional CDP model",
            "Implementation requires engineering resources for proper instrumentation",
        ],
    },
    "Rudderstack": {
        "display": "RudderStack",
        "category": "cdp",
        "description": "RudderStack is an open-source customer data platform built for warehouse-first architectures. It collects and routes event data like Segment but is designed to keep the data warehouse as the source of truth.",
        "pricing": "Open-source self-hosted is free. Cloud: Free tier available. Growth from $150/mo. Enterprise by quote.",
        "founded": "2019",
        "hq": "San Francisco, CA",
        "features": [
            "Event streaming with warehouse-first architecture",
            "Open-source core with self-hosting option",
            "200+ pre-built integrations for data routing",
            "Data warehouse as source of truth (not a separate data silo)",
            "Reverse ETL for activating warehouse data in downstream tools",
            "Transformations in JavaScript for real-time data shaping",
        ],
        "pros": [
            "Open-source transparency and self-hosting option",
            "Warehouse-native design avoids data silo problem",
            "More cost-effective than Segment at high volume",
            "Combined event streaming and reverse ETL in one platform",
        ],
        "cons": [
            "Smaller integration library than Segment",
            "Self-hosting requires DevOps investment",
            "Less mature identity resolution compared to Segment",
            "Smaller community and fewer practitioners in the talent pool",
        ],
    },
    "Hightouch": {
        "display": "Hightouch",
        "category": "cdp",
        "description": "Hightouch is a reverse ETL platform that activates data from your warehouse in downstream marketing and sales tools. Instead of building a separate data store, it uses your existing data warehouse as the CDP layer.",
        "pricing": "Free tier available (1 destination). Growth from $350/mo. Business and Enterprise by quote.",
        "founded": "2020",
        "hq": "San Francisco, CA",
        "features": [
            "Reverse ETL from Snowflake, BigQuery, Redshift, and Databricks",
            "Visual audience builder for non-technical users",
            "Customer Studio for self-serve segmentation",
            "Match Booster for identity resolution via partnerships",
            "Alerting and observability for sync monitoring",
            "Experimentation framework for A/B testing audiences",
        ],
        "pros": [
            "Activates existing warehouse data without building a new data silo",
            "Visual audience builder accessible to marketing teams",
            "Fast growing and well-funded with strong product velocity",
            "Eliminates the need for a traditional CDP in warehouse-mature orgs",
        ],
        "cons": [
            "Requires a mature, well-modeled data warehouse",
            "Newer platform with less enterprise track record than Segment",
            "Identity resolution depends on warehouse data quality",
            "Pricing scales with sync volume and destinations",
        ],
    },
    "Census": {
        "display": "Census",
        "category": "cdp",
        "description": "Census is a reverse ETL and data activation platform. It syncs data from your cloud warehouse to 150+ SaaS tools, enabling MOps teams to use warehouse-modeled data directly in their marketing stack without building custom integrations.",
        "pricing": "Free tier available (limited syncs). Growth from $300/mo. Business and Enterprise by quote.",
        "founded": "2018",
        "hq": "San Francisco, CA",
        "features": [
            "Reverse ETL from Snowflake, BigQuery, Redshift, Databricks, and PostgreSQL",
            "Audience Hub for visual segment building on warehouse data",
            "150+ destination connectors for SaaS tools",
            "dbt integration for model-based syncs",
            "Observability dashboard with sync health monitoring",
            "Computed columns for no-code data transformation",
        ],
        "pros": [
            "Strong dbt integration for analytics-engineering-first teams",
            "Audience Hub makes warehouse data accessible to non-technical users",
            "Broad destination coverage for common marketing tools",
            "Developer-friendly with SQL-based configuration",
        ],
        "cons": [
            "Requires a mature data warehouse with clean, modeled data",
            "Smaller company than Hightouch with fewer resources",
            "Some destinations have limited field mapping options",
            "Real-time sync is not as fast as event-streaming CDPs like Segment",
        ],
    },
    "Clay": {
        "display": "Clay",
        "category": "data-management",
        "description": "Clay is a data enrichment and outbound automation platform that chains together 75+ data providers in a spreadsheet-like interface. MOps teams use it to enrich CRM records, build prospect lists, and automate data research workflows.",
        "pricing": "Free tier available (100 credits/mo). Starter $149/mo, Explorer $349/mo, Pro $800/mo. Enterprise by quote.",
        "founded": "2021",
        "hq": "New York, NY",
        "features": [
            "Waterfall enrichment across 75+ data providers",
            "Spreadsheet interface for building enrichment workflows",
            "AI-powered data research and web scraping agents",
            "CRM integrations for enrichment and sync (Salesforce, HubSpot)",
            "Custom formulas and transformations",
            "API access for programmatic enrichment workflows",
        ],
        "pros": [
            "Waterfall enrichment dramatically improves hit rates vs single providers",
            "Accessible spreadsheet UI for non-engineers",
            "Rapidly growing feature set and integration library",
            "Strong community and active product development",
        ],
        "cons": [
            "Credit-based pricing can get expensive for large-scale enrichment",
            "Relatively new platform with a shorter track record",
            "Complex workflows can be difficult to debug",
            "Data quality depends on underlying provider accuracy",
        ],
    },
    "Domo": {
        "display": "Domo",
        "category": "analytics",
        "description": "Domo is a cloud-based business intelligence platform designed for business users. It combines data integration, visualization, and app building in a single platform, targeting teams that want self-serve analytics without heavy SQL or IT dependencies.",
        "pricing": "Custom pricing based on users and data volume. Typically starts around $83/user/mo for standard plans.",
        "founded": "2010",
        "hq": "American Fork, UT",
        "features": [
            "1,000+ pre-built data connectors",
            "Magic ETL for no-code data transformation",
            "Card-based dashboard and visualization system",
            "Domo Appstore for pre-built industry dashboards",
            "Alerts and notifications for metric changes",
            "Mobile-first design with native iOS and Android apps",
        ],
        "pros": [
            "Easiest onboarding for non-technical business users",
            "Strong connector library reduces data engineering burden",
            "Mobile experience is better than most BI competitors",
            "All-in-one approach (ingestion + transformation + visualization)",
        ],
        "cons": [
            "Less flexible than Tableau or Looker for advanced analysis",
            "Pricing is high relative to Power BI",
            "Governance and version control are weaker than Looker",
            "Smaller talent pool compared to Tableau, Looker, or Power BI",
        ],
    },
    "Ringlead": {
        "display": "RingLead",
        "category": "data-management",
        "description": "RingLead (now part of ZoomInfo) is a data management platform focused on deduplication, normalization, routing, and data quality for CRM and MAP databases. MOps teams rely on it to keep Salesforce and marketing automation data clean and correctly routed.",
        "pricing": "Custom pricing through ZoomInfo. Typically bundled with ZoomInfo data packages or available standalone for data management.",
        "founded": "2003 (acquired by ZoomInfo 2020)",
        "hq": "Cedar Knolls, NJ (ZoomInfo)",
        "features": [
            "Duplicate prevention and merging for CRM records",
            "Data normalization for standardizing fields (titles, states, industries)",
            "Lead-to-account routing with territory and ownership rules",
            "Enrichment integration with ZoomInfo data",
            "Cleanse on-demand and scheduled batch processing",
            "Salesforce-native architecture running within the org",
        ],
        "pros": [
            "Strong deduplication engine with flexible matching rules",
            "Salesforce-native means data stays in your org",
            "Normalization reduces manual data cleanup dramatically",
            "Now bundled with ZoomInfo enrichment for a combined solution",
        ],
        "cons": [
            "ZoomInfo acquisition means it is increasingly bundled, not standalone",
            "Primarily Salesforce-focused with limited HubSpot support",
            "UI and configuration can be complex for non-admin users",
            "Pricing transparency has decreased post-acquisition",
        ],
    },
}


# ---------------------------------------------------------------------------
# Comparison definitions
# ---------------------------------------------------------------------------

COMPARISONS = {
    "marketo-vs-hubspot": {
        "tool_a": "Marketo",
        "tool_b": "HubSpot",
        "display_a": "Marketo",
        "display_b": "HubSpot",
        "title": "Marketo vs. HubSpot for Marketing Operations (2026)",
        "summary": "The most common MAP decision in marketing operations. Marketo is the enterprise standard for complex B2B automation. HubSpot is the all-in-one platform gaining ground in the mid-market and moving upmarket.",
        "verdict": "Choose Marketo if you have complex multi-touch nurturing, heavy Salesforce integration needs, and a dedicated MOps admin. Choose HubSpot if you want lower total cost of ownership, an all-in-one platform, and simpler administration. Both are strong choices for different stages and needs.",
    },
    "salesforce-vs-hubspot": {
        "tool_a": "Salesforce",
        "tool_b": "HubSpot",
        "display_a": "Salesforce",
        "display_b": "HubSpot",
        "title": "Salesforce vs. HubSpot CRM for MOps Teams (2026)",
        "summary": "Salesforce is the enterprise default. HubSpot CRM is the growth-stage favorite. For MOps teams, the choice determines your entire technology stack and the type of professionals you need to hire.",
        "verdict": "Choose Salesforce if you are enterprise-scale, need deep customization, and can invest in a dedicated admin. Choose HubSpot CRM if you want integrated marketing and sales in one platform with lower admin overhead. Many companies start on HubSpot and migrate to Salesforce as they scale.",
    },
    "make-vs-zapier": {
        "tool_a": "Make",
        "tool_b": "Zapier",
        "display_a": "Make",
        "display_b": "Zapier",
        "title": "Make vs. Zapier for Marketing Operations (2026)",
        "summary": "Both platforms connect marketing tools without code. Zapier has the largest app library. Make offers better visual workflows and cheaper per-operation pricing. The right choice depends on complexity and volume.",
        "verdict": "Choose Zapier for simple, low-volume integrations where the app library matters most. Choose Make for more complex workflows, higher volume use cases, or when per-operation cost is a concern. For enterprise needs, consider Workato instead.",
    },
    "tableau-vs-looker": {
        "tool_a": "Tableau",
        "tool_b": "Looker",
        "display_a": "Tableau",
        "display_b": "Looker",
        "title": "Tableau vs. Looker for MOps Analytics (2026)",
        "summary": "Tableau is the flexible visualization powerhouse. Looker is the governed, model-driven analytics platform. For MOps teams, the choice often follows the existing data stack.",
        "verdict": "Choose Tableau if you need maximum visualization flexibility and your team has strong analytical skills. Choose Looker if you run on BigQuery, want centralized metric definitions, or need embedded analytics. Power BI is a third option for Microsoft-heavy environments.",
    },
    "tableau-vs-power-bi": {
        "tool_a": "Tableau",
        "tool_b": "Power Bi",
        "display_a": "Tableau",
        "display_b": "Power BI",
        "title": "Tableau vs. Power BI for Marketing Operations (2026)",
        "summary": "Tableau offers more flexibility. Power BI offers lower cost and Microsoft integration. For MOps teams, the decision often depends on what the rest of the organization uses.",
        "verdict": "Choose Tableau if visualization flexibility and data source variety are priorities. Choose Power BI if you are in a Microsoft environment and want the lowest per-user cost. Both handle standard MOps dashboards well.",
    },
    "marketo-vs-eloqua": {
        "tool_a": "Marketo",
        "tool_b": "Eloqua",
        "display_a": "Marketo",
        "display_b": "Oracle Eloqua",
        "title": "Marketo vs. Eloqua for Enterprise Marketing Ops (2026)",
        "summary": "Both are enterprise marketing automation platforms. Marketo has a larger market share and talent pool. Eloqua fits well in Oracle-ecosystem companies. The decision often comes down to existing vendor relationships.",
        "verdict": "Choose Marketo for broader ecosystem support, a larger talent pool, and stronger Adobe integrations. Choose Eloqua if your organization is invested in Oracle CX and values deep segmentation capabilities. Marketo is the safer choice for most organizations.",
    },
    "workato-vs-zapier": {
        "tool_a": "Workato",
        "tool_b": "Zapier",
        "display_a": "Workato",
        "display_b": "Zapier",
        "title": "Workato vs. Zapier: Enterprise iPaaS vs. No-Code (2026)",
        "summary": "Zapier is for quick, simple integrations. Workato is for enterprise workflow automation. They serve different markets, but MOps teams sometimes outgrow Zapier and need to evaluate the step up.",
        "verdict": "Start with Zapier for simple use cases. Move to Workato when you need enterprise error handling, complex multi-step workflows, governance controls, or you are hitting Zapier's volume pricing ceiling.",
    },
    "salesforce-mc-vs-marketo": {
        "tool_a": "Salesforce Marketing Cloud",
        "tool_b": "Marketo",
        "display_a": "Salesforce Marketing Cloud",
        "display_b": "Marketo",
        "title": "Salesforce Marketing Cloud vs. Marketo (2026)",
        "summary": "Salesforce Marketing Cloud excels at multi-channel B2C engagement. Marketo dominates B2B lead management. Both serve enterprise organizations but from different angles.",
        "verdict": "Choose Salesforce Marketing Cloud for B2C or multi-channel (email, SMS, push, ads) at scale, especially if you are already on Salesforce CRM. Choose Marketo for B2B lead scoring, nurturing, and sales alignment. Some large organizations run both.",
    },
}


# ---------------------------------------------------------------------------
# Roundup definitions
# ---------------------------------------------------------------------------

ROUNDUPS = {
    "best-marketing-automation": {
        "title": "Best Marketing Automation Platforms for MOps (2026)",
        "slug": "best-marketing-automation",
        "category": "marketing-automation",
        "description": "A comparison of the top marketing automation platforms used by marketing operations teams. Ranked by job posting frequency, feature depth, and practitioner feedback.",
        "tools": ["Marketo", "Hubspot", "Salesforce Marketing Cloud", "Eloqua", "Braze"],
    },
    "best-cdp": {
        "title": "Best Customer Data Platforms for Marketing Ops (2026)",
        "slug": "best-cdp",
        "category": "cdp",
        "description": "CDPs and reverse ETL tools for marketing operations teams. Coverage of traditional CDPs and the emerging warehouse-native approach.",
        "tools": ["Segment", "Hightouch", "Census", "Rudderstack"],
    },
    "best-data-management": {
        "title": "Best Data Management Tools for MOps Teams (2026)",
        "slug": "best-data-management",
        "category": "data-management",
        "description": "Tools for keeping your CRM and MAP data clean, enriched, and routed correctly. Covers enrichment, deduplication, routing, and hygiene.",
        "tools": ["Zoominfo", "Ringlead", "Clay", "Leandata", "Demandbase", "6Sense"],
    },
    "best-integration-tools": {
        "title": "Best Integration Tools for Marketing Operations (2026)",
        "slug": "best-integration-tools",
        "category": "integration",
        "description": "Integration and automation platforms for connecting your marketing stack. From no-code connectors to enterprise iPaaS.",
        "tools": ["Zapier", "Make", "Workato", "N8N"],
    },
    "best-analytics-bi": {
        "title": "Best Analytics and BI Tools for MOps Teams (2026)",
        "slug": "best-analytics-bi",
        "category": "analytics",
        "description": "Business intelligence and analytics platforms for marketing operations reporting, dashboards, and attribution analysis.",
        "tools": ["Tableau", "Looker", "Power Bi", "Domo"],
    },
}


# ---------------------------------------------------------------------------
# Tools Index
# ---------------------------------------------------------------------------

def build_tools_index(tools_data, total_jobs):
    crumbs = [("Home", "/"), ("Tools", None)]
    bc = breadcrumb_html(crumbs)

    mops_tools = get_mops_tools(tools_data)
    top_tools = sorted(mops_tools.items(), key=lambda x: -x[1])[:15]

    cards = stat_cards_html([
        (str(len(mops_tools)), "MOps Tools Tracked"),
        (str(total_jobs), "Job Postings Analyzed"),
        (f'{pct_of_jobs(top_tools[0][1], total_jobs)}%', f'{top_tools[0][0]} Mention Rate'),
        (str(len(CATEGORIES)), "Tool Categories"),
    ])

    # Top tools table
    tools_table = ""
    for name, count in top_tools:
        pct = pct_of_jobs(count, total_jobs)
        slug = slugify(name)
        link = f'<a href="/tools/{slug}-review/">{name}</a>' if name in TOOL_META else name
        tools_table += f'<tr><td>{link}</td><td>{count}</td><td>{pct}%</td></tr>\n'

    # Category links
    cat_links = ""
    for cat_slug, cat in CATEGORIES.items():
        cat_links += f'<li><a href="/tools/category/{cat_slug}/">{cat["name"]}</a></li>\n'

    # Comparison links
    cmp_links = ""
    for cmp_slug, cmp in COMPARISONS.items():
        cmp_links += f'<li><a href="/tools/compare/{cmp_slug}/">{cmp["display_a"]} vs. {cmp["display_b"]}</a></li>\n'

    # Roundup links
    roundup_links = ""
    for r_slug, r in ROUNDUPS.items():
        roundup_links += f'<li><a href="/tools/{r["slug"]}/">{r["title"]}</a></li>\n'

    faq_pairs = [
        ("What is the most popular MOps tool?",
         f"Salesforce is the most frequently mentioned tool in marketing operations job postings, appearing in {pct_of_jobs(tools_data.get('Salesforce', 0), total_jobs)}% of listings. HubSpot is second at {pct_of_jobs(tools_data.get('Hubspot', 0), total_jobs)}%."),
        ("How are tool rankings determined?",
         "Rankings are based on mention frequency in marketing operations job postings. We track how often each tool appears as a required or preferred skill. This reflects real employer demand, not vendor marketing."),
        ("Do you accept sponsored reviews?",
         "No. All reviews are based on job posting data and practitioner experience. We do not accept payment for favorable reviews or rankings."),
    ]

    body = f'''{bc}
<section class="page-header">
    <h1>Marketing Operations Tools and Software (2026)</h1>
    <p class="lead">Data-driven reviews and comparisons of MOps tools. Rankings based on {total_jobs} analyzed job postings. Updated weekly.</p>
</section>

<div class="container">
{cards}

<h2>Most In-Demand MOps Tools</h2>
<p>The tools below appear most frequently in marketing operations job postings. Mention rate reflects the percentage of all tracked MOps roles that list each tool as required or preferred.</p>

<table class="data-table">
<thead><tr><th>Tool</th><th>Mentions</th><th>% of Roles</th></tr></thead>
<tbody>
{tools_table}
</tbody>
</table>

<h2>Browse by Category</h2>
<ul>
{cat_links}
</ul>

<h2>Head-to-Head Comparisons</h2>
<ul>
{cmp_links}
</ul>

<h2>Roundups and Buyer Guides</h2>
<ul>
{roundup_links}
</ul>

<h2>How We Review Tools</h2>
<p>Our tool reviews are built on job posting data, not vendor briefings. When we say a tool is mentioned in a certain percentage of MOps job postings, that number comes from our analysis of {total_jobs} real listings. We supplement frequency data with practitioner experience and publicly available product information.</p>
<p>We do not accept sponsored placements, paid reviews, or vendor-influenced rankings. Some pages contain affiliate links, which are disclosed where they appear.</p>

</div>
'''
    body += newsletter_cta_html("Get weekly tool trend data for marketing operations.")
    body += faq_html(faq_pairs)

    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="Marketing Operations Tools and Software Reviews (2026)",
        description=f"MOps tool reviews based on {total_jobs} job postings. Salesforce, HubSpot, Marketo, and {len(get_mops_tools(tools_data))}+ tools ranked by employer demand.",
        canonical_path="/tools/",
        body_content=body,
        active_path="/tools/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("tools/index.html", page)
    print("  Built: tools/index.html")


# ---------------------------------------------------------------------------
# Category pages
# ---------------------------------------------------------------------------

def build_category_pages(tools_data, total_jobs):
    for cat_slug, cat in CATEGORIES.items():
        crumbs = [("Home", "/"), ("Tools", "/tools/"), (cat["name"], None)]
        bc = breadcrumb_html(crumbs)

        # Build tool table for this category
        tool_rows = ""
        cat_tools_sorted = []
        for tool_name in cat["tools"]:
            mentions = find_tool_mentions(tool_name, tools_data)
            if mentions > 0:
                cat_tools_sorted.append((tool_name, mentions))
        cat_tools_sorted.sort(key=lambda x: -x[1])

        for name, count in cat_tools_sorted:
            pct = pct_of_jobs(count, total_jobs)
            slug = slugify(name)
            link = f'<a href="/tools/{slug}-review/">{name}</a>' if name in TOOL_META else name
            tool_rows += f'<tr><td>{link}</td><td>{count}</td><td>{pct}%</td></tr>\n'

        # Also list tools with 0 mentions from category
        for tool_name in cat["tools"]:
            mentions = find_tool_mentions(tool_name, tools_data)
            if mentions == 0 and tool_name in TOOL_META:
                slug = slugify(tool_name)
                tool_rows += f'<tr><td><a href="/tools/{slug}-review/">{tool_name}</a></td><td>0</td><td>0%</td></tr>\n'

        total_cat_mentions = sum(m for _, m in cat_tools_sorted)
        cards = stat_cards_html([
            (str(len(cat["tools"])), "Tools in Category"),
            (str(total_cat_mentions), "Total Mentions"),
            (f'{pct_of_jobs(cat_tools_sorted[0][1], total_jobs)}%' if cat_tools_sorted else "N/A", "Top Tool Mention Rate"),
        ])

        # Related comparisons
        related_cmps = ""
        for cmp_slug, cmp in COMPARISONS.items():
            if cmp["tool_a"] in cat["tools"] or cmp["tool_b"] in cat["tools"]:
                related_cmps += f'<li><a href="/tools/compare/{cmp_slug}/">{cmp["display_a"]} vs. {cmp["display_b"]}</a></li>\n'

        faq_pairs = [
            (f"What is the best {cat['name'].lower()} tool for MOps?",
             f"Based on job posting frequency, {cat_tools_sorted[0][0] if cat_tools_sorted else 'varies'} is the most in-demand {cat['name'].lower()} tool among marketing operations teams. However, the best choice depends on your company size, existing tech stack, and specific requirements."),
            (f"How many {cat['name'].lower()} tools do MOps teams typically use?",
             f"Most MOps teams use 1-2 tools in the {cat['name'].lower()} category. Enterprise teams may run multiple solutions for different use cases or business units."),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>{cat["name"]} Tools for Marketing Operations (2026)</h1>
    <p class="lead">{cat["description"]}</p>
</section>

<div class="container">
{cards}

<h2>{cat["name"]} Tools Ranked by Job Posting Frequency</h2>
<p>The table below shows how often each {cat["name"].lower()} tool appears in marketing operations job postings. Higher mention rates indicate stronger employer demand and larger talent pools.</p>

<table class="data-table">
<thead><tr><th>Tool</th><th>Mentions</th><th>% of Roles</th></tr></thead>
<tbody>
{tool_rows}
</tbody>
</table>

<h2>Buyer's Guide: Choosing {cat["name"]} Software</h2>
<p>{cat["buyer_guide"]}</p>

{"<h2>Head-to-Head Comparisons</h2><ul>" + related_cmps + "</ul>" if related_cmps else ""}

<h2>Related Categories</h2>
<ul>'''

        for other_slug, other_cat in CATEGORIES.items():
            if other_slug != cat_slug:
                body += f'    <li><a href="/tools/category/{other_slug}/">{other_cat["name"]}</a></li>\n'

        body += f'''</ul>

<p class="source-citation">Source: MOps Report analysis of {total_jobs} marketing operations job postings. Tool mention counts reflect required or preferred skills.</p>
</div>
'''
        body += newsletter_cta_html(f"Get weekly {cat['name'].lower()} tool trends for MOps teams.")
        body += faq_html(faq_pairs)

        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
        page = get_page_wrapper(
            title=f"Best {cat['name']} Tools for Marketing Operations (2026)",
            description=f"{cat['name']} tools ranked by MOps job posting frequency. {cat_tools_sorted[0][0] if cat_tools_sorted else 'Multiple tools'} leads. Reviews, comparisons, and buyer guidance.",
            canonical_path=f"/tools/category/{cat_slug}/",
            body_content=body,
            active_path="/tools/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"tools/category/{cat_slug}/index.html", page)
        print(f"  Built: tools/category/{cat_slug}/index.html")


# ---------------------------------------------------------------------------
# Individual tool review pages
# ---------------------------------------------------------------------------

def get_software_schema(tool_meta, mentions, total_jobs):
    """SoftwareApplication JSON-LD schema."""
    import json as _json
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool_meta["display"],
        "applicationCategory": "BusinessApplication",
        "description": tool_meta["description"],
        "offers": {
            "@type": "Offer",
            "description": tool_meta["pricing"],
        },
    }
    return f'    <script type="application/ld+json">{_json.dumps(schema)}</script>\n'


def build_tool_review_pages(tools_data, total_jobs):
    for tool_key, meta in TOOL_META.items():
        mentions = find_tool_mentions(tool_key, tools_data)
        if mentions < 2 and tool_key not in ["Segment", "Hightouch", "Census", "Rudderstack",
                                               "Domo", "Chili Piper"]:
            # Still build if explicitly in our metadata
            pass

        slug = slugify(tool_key)
        crumbs = [("Home", "/"), ("Tools", "/tools/"), (f"{meta['display']} Review", None)]
        bc = breadcrumb_html(crumbs)

        pct = pct_of_jobs(mentions, total_jobs)

        cards = stat_cards_html([
            (f'{pct}%', "MOps Job Mention Rate"),
            (str(mentions), f"of {total_jobs} Postings"),
            (meta.get("founded", "N/A"), "Founded"),
            (meta.get("hq", "N/A"), "Headquarters"),
        ])

        features_html = ""
        for f in meta["features"]:
            features_html += f"<li>{f}</li>\n"

        pros_html = ""
        for p in meta["pros"]:
            pros_html += f"<li>{p}</li>\n"

        cons_html = ""
        for c in meta["cons"]:
            cons_html += f"<li>{c}</li>\n"

        # Find related comparisons
        related_cmps = ""
        for cmp_slug, cmp in COMPARISONS.items():
            if cmp["tool_a"] == tool_key or cmp["tool_b"] == tool_key:
                other = cmp["display_b"] if cmp["tool_a"] == tool_key else cmp["display_a"]
                related_cmps += f'<li><a href="/tools/compare/{cmp_slug}/">{meta["display"]} vs. {other}</a></li>\n'

        # Category link
        cat_slug = meta.get("category", "")
        cat_name = CATEGORIES.get(cat_slug, {}).get("name", "")

        faq_pairs = [
            (f"How popular is {meta['display']} in MOps job postings?",
             f"{meta['display']} appears in {pct}% of marketing operations job postings ({mentions} out of {total_jobs} tracked roles). {'This makes it one of the most in-demand tools for MOps professionals.' if pct > 10 else 'While not the most common, it represents a meaningful skill in the MOps market.'}"),
            (f"How much does {meta['display']} cost?",
             f"{meta['pricing']}. Actual costs depend on your user count, contact volume, and selected features."),
            (f"What are the main alternatives to {meta['display']}?",
             f"See our {cat_name} category page for a full comparison of alternatives. The best option depends on your company size, existing stack, and specific requirements."),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>{meta["display"]} Review for Marketing Operations (2026)</h1>
    <p class="lead">{meta["description"]}</p>
</section>

<div class="container">
{cards}

<h2>Overview</h2>
<p>{meta["description"]}</p>
<p>In our analysis of {total_jobs} marketing operations job postings, {meta["display"]} appears in {mentions} listings ({pct}% of all tracked roles). {"This makes it one of the most sought-after skills for MOps professionals." if pct > 10 else "It represents a notable skill within the " + cat_name.lower() + " category."}</p>

<h2>Key Features</h2>
<ul>
{features_html}
</ul>

<h2>Pricing</h2>
<p>{meta["pricing"]}</p>
<p>Pricing for {meta["display"]} varies based on your team size, contact volume, and selected modules. Contact {meta["display"]} directly for a custom quote based on your requirements.</p>

<h2>Pros</h2>
<ul>
{pros_html}
</ul>

<h2>Cons</h2>
<ul>
{cons_html}
</ul>

<h2>Who Should Use {meta["display"]}?</h2>
<p>{meta["display"]} is best suited for MOps teams at {"enterprise" if mentions > 20 else "mid-market to enterprise"} organizations that need {"robust " + cat_name.lower() + " capabilities" if cat_name else "a reliable solution in this category"}. If you are evaluating {meta["display"]}, compare it against the alternatives in our <a href="/tools/category/{cat_slug}/">{cat_name} category</a>.</p>

{"<h2>Comparisons</h2><ul>" + related_cmps + "</ul>" if related_cmps else ""}

<h2>Related Pages</h2>
<ul>
    <li><a href="/tools/">All MOps Tools</a></li>
    <li><a href="/tools/category/{cat_slug}/">{cat_name} Tools</a></li>
</ul>

<p class="source-citation">Source: MOps Report analysis of {total_jobs} marketing operations job postings. Last updated April 2026.</p>
</div>
'''
        body += newsletter_cta_html(f"Get weekly updates on {meta['display']} and MOps tool trends.")
        body += faq_html(faq_pairs)

        sw_schema = get_software_schema(meta, mentions, total_jobs)
        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + sw_schema
        page = get_page_wrapper(
            title=f"{meta['display']} Review for Marketing Operations (2026)",
            description=f"{meta['display']} review for MOps teams. Mentioned in {pct}% of job postings. Features, pricing, pros, cons, and alternatives.",
            canonical_path=f"/tools/{slug}-review/",
            body_content=body,
            active_path="/tools/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"tools/{slug}-review/index.html", page)
        print(f"  Built: tools/{slug}-review/index.html")


# ---------------------------------------------------------------------------
# Comparison pages
# ---------------------------------------------------------------------------

def build_comparison_pages(tools_data, total_jobs):
    for cmp_slug, cmp in COMPARISONS.items():
        tool_a = cmp["tool_a"]
        tool_b = cmp["tool_b"]
        meta_a = TOOL_META.get(tool_a, {})
        meta_b = TOOL_META.get(tool_b, {})

        mentions_a = find_tool_mentions(tool_a, tools_data)
        mentions_b = find_tool_mentions(tool_b, tools_data)
        pct_a = pct_of_jobs(mentions_a, total_jobs)
        pct_b = pct_of_jobs(mentions_b, total_jobs)

        crumbs = [("Home", "/"), ("Tools", "/tools/"),
                   (f"{cmp['display_a']} vs. {cmp['display_b']}", None)]
        bc = breadcrumb_html(crumbs)

        cards = stat_cards_html([
            (f'{pct_a}%', f'{cmp["display_a"]} Mention Rate'),
            (f'{pct_b}%', f'{cmp["display_b"]} Mention Rate'),
            (str(mentions_a), f'{cmp["display_a"]} Mentions'),
            (str(mentions_b), f'{cmp["display_b"]} Mentions'),
        ])

        # Feature comparison table
        feature_rows = ""
        if meta_a.get("features") and meta_b.get("features"):
            max_features = max(len(meta_a["features"]), len(meta_b["features"]))
            for i in range(min(max_features, 6)):
                f_a = meta_a["features"][i] if i < len(meta_a["features"]) else ""
                f_b = meta_b["features"][i] if i < len(meta_b["features"]) else ""
                feature_rows += f"<tr><td>{f_a}</td><td>{f_b}</td></tr>\n"

        # Pros comparison
        pros_a = ""
        for p in meta_a.get("pros", []):
            pros_a += f"<li>{p}</li>\n"
        pros_b = ""
        for p in meta_b.get("pros", []):
            pros_b += f"<li>{p}</li>\n"

        # Cons comparison
        cons_a = ""
        for c in meta_a.get("cons", []):
            cons_a += f"<li>{c}</li>\n"
        cons_b = ""
        for c in meta_b.get("cons", []):
            cons_b += f"<li>{c}</li>\n"

        faq_pairs = [
            (f"Is {cmp['display_a']} or {cmp['display_b']} better for MOps?",
             f"{cmp['verdict']}"),
            (f"Which is more popular in MOps job postings: {cmp['display_a']} or {cmp['display_b']}?",
             f"{cmp['display_a']} appears in {pct_a}% of MOps job postings ({mentions_a} mentions), while {cmp['display_b']} appears in {pct_b}% ({mentions_b} mentions)."),
            (f"Can I switch from {cmp['display_a']} to {cmp['display_b']}?",
             f"Migration between platforms is possible but requires planning. Data migration, workflow rebuild, and team retraining are the primary costs. Budget 2-6 months for a full migration depending on complexity."),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>{cmp["title"]}</h1>
    <p class="lead">{cmp["summary"]}</p>
</section>

<div class="container">
{cards}

<h2>Job Market Demand</h2>
<p>{cmp["display_a"]} appears in {pct_a}% of marketing operations job postings ({mentions_a} of {total_jobs} tracked roles). {cmp["display_b"]} appears in {pct_b}% ({mentions_b} mentions). {"The gap reflects " + cmp["display_a"] + "'s stronger enterprise penetration." if mentions_a > mentions_b else "The gap reflects " + cmp["display_b"] + "'s broader market adoption." if mentions_b > mentions_a else "They are roughly equal in demand."}</p>

{"<h2>Feature Comparison</h2><table class='data-table'><thead><tr><th>" + cmp["display_a"] + "</th><th>" + cmp["display_b"] + "</th></tr></thead><tbody>" + feature_rows + "</tbody></table>" if feature_rows else ""}

<h2>Pricing</h2>
<p><strong>{cmp["display_a"]}:</strong> {meta_a.get("pricing", "Contact vendor for pricing.")}</p>
<p><strong>{cmp["display_b"]}:</strong> {meta_b.get("pricing", "Contact vendor for pricing.")}</p>

<h2>{cmp["display_a"]} Pros</h2>
<ul>{pros_a}</ul>

<h2>{cmp["display_a"]} Cons</h2>
<ul>{cons_a}</ul>

<h2>{cmp["display_b"]} Pros</h2>
<ul>{pros_b}</ul>

<h2>{cmp["display_b"]} Cons</h2>
<ul>{cons_b}</ul>

<h2>Verdict</h2>
<p>{cmp["verdict"]}</p>

<h2>Related Comparisons</h2>
<ul>'''

        for other_slug, other_cmp in COMPARISONS.items():
            if other_slug != cmp_slug:
                body += f'    <li><a href="/tools/compare/{other_slug}/">{other_cmp["display_a"]} vs. {other_cmp["display_b"]}</a></li>\n'

        body += f'''</ul>

<p class="source-citation">Source: MOps Report analysis of {total_jobs} marketing operations job postings. Last updated April 2026.</p>
</div>
'''
        body += newsletter_cta_html("Get weekly MOps tool intelligence.")
        body += faq_html(faq_pairs)

        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
        page = get_page_wrapper(
            title=cmp["title"],
            description=f"{cmp['display_a']} vs. {cmp['display_b']} for MOps. {cmp['display_a']}: {pct_a}% mention rate. {cmp['display_b']}: {pct_b}%. Full comparison with verdict.",
            canonical_path=f"/tools/compare/{cmp_slug}/",
            body_content=body,
            active_path="/tools/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"tools/compare/{cmp_slug}/index.html", page)
        print(f"  Built: tools/compare/{cmp_slug}/index.html")


# ---------------------------------------------------------------------------
# Roundup pages
# ---------------------------------------------------------------------------

def build_roundup_pages(tools_data, total_jobs):
    for r_slug, roundup in ROUNDUPS.items():
        crumbs = [("Home", "/"), ("Tools", "/tools/"), (roundup["title"], None)]
        bc = breadcrumb_html(crumbs)

        # Build ranked list
        ranked = []
        for tool_name in roundup["tools"]:
            mentions = find_tool_mentions(tool_name, tools_data)
            meta = TOOL_META.get(tool_name, {})
            ranked.append((tool_name, mentions, meta))
        ranked.sort(key=lambda x: -x[1])

        cards = stat_cards_html([
            (str(len(ranked)), "Tools Reviewed"),
            (str(sum(m for _, m, _ in ranked)), "Total Mentions"),
            (f'{pct_of_jobs(ranked[0][1], total_jobs)}%' if ranked else "N/A", "Top Tool Mention Rate"),
        ])

        tools_content = ""
        for i, (name, mentions, meta) in enumerate(ranked, 1):
            pct = pct_of_jobs(mentions, total_jobs)
            display = meta.get("display", name)
            slug = slugify(name)
            pricing = meta.get("pricing", "Contact vendor for pricing")

            pros_html = ""
            for p in meta.get("pros", [])[:3]:
                pros_html += f"<li>{p}</li>\n"
            cons_html = ""
            for c in meta.get("cons", [])[:2]:
                cons_html += f"<li>{c}</li>\n"

            tools_content += f'''
<h3>{i}. {display}</h3>
<p><strong>Mention rate:</strong> {pct}% of MOps job postings ({mentions} of {total_jobs} roles)</p>
<p>{meta.get("description", "")}</p>
<p><strong>Pricing:</strong> {pricing}</p>
<p><strong>Strengths:</strong></p>
<ul>{pros_html}</ul>
<p><strong>Limitations:</strong></p>
<ul>{cons_html}</ul>
<p><a href="/tools/{slug}-review/">Read full {display} review</a></p>
'''

        # Related comparisons in this category
        cat_slug = roundup.get("category", "")
        related_cmps = ""
        for cmp_slug_key, cmp in COMPARISONS.items():
            if cmp["tool_a"] in roundup["tools"] or cmp["tool_b"] in roundup["tools"]:
                related_cmps += f'<li><a href="/tools/compare/{cmp_slug_key}/">{cmp["display_a"]} vs. {cmp["display_b"]}</a></li>\n'

        faq_pairs = [
            (f"What is the best {CATEGORIES.get(cat_slug, {}).get('name', 'MOps').lower()} tool in 2026?",
             f"Based on job posting frequency, {ranked[0][2].get('display', ranked[0][0]) if ranked else 'varies'} is the most in-demand option. However, the best choice depends on your company size, existing tech stack, and specific requirements."),
            (f"How do we rank these tools?",
             f"Rankings are based on mention frequency in {total_jobs} marketing operations job postings. Higher mention rates indicate stronger employer demand and larger talent pools."),
        ]

        body = f'''{bc}
<section class="page-header">
    <h1>{roundup["title"]}</h1>
    <p class="lead">{roundup["description"]}</p>
</section>

<div class="container">
{cards}

{tools_content}

{"<h2>Head-to-Head Comparisons</h2><ul>" + related_cmps + "</ul>" if related_cmps else ""}

<h2>How to Choose</h2>
<p>{CATEGORIES.get(cat_slug, {}).get("buyer_guide", "Evaluate each tool against your specific requirements, team size, and existing technology stack.")}</p>

<h2>Related Categories</h2>
<ul>
    <li><a href="/tools/">All MOps Tools</a></li>
    <li><a href="/tools/category/{cat_slug}/">{CATEGORIES.get(cat_slug, {}).get("name", "Category")} Tools</a></li>
</ul>

<p class="source-citation">Source: MOps Report analysis of {total_jobs} marketing operations job postings. Last updated April 2026.</p>
</div>
'''
        body += newsletter_cta_html("Get weekly tool intelligence for marketing operations.")
        body += faq_html(faq_pairs)

        schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
        page = get_page_wrapper(
            title=roundup["title"],
            description=roundup["description"],
            canonical_path=f"/tools/{roundup['slug']}/",
            body_content=body,
            active_path="/tools/",
            extra_head=schema,
            body_class="page-inner",
        )
        write_page(f"tools/{roundup['slug']}/index.html", page)
        print(f"  Built: tools/{roundup['slug']}/index.html")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_all_tools_pages(project_dir):
    """Entry point called from build.py."""
    data = load_tools_data(project_dir)
    tools_data = data["tools"]
    total_jobs = data["total_jobs"]

    print("\n  Building tools pages...")
    build_tools_index(tools_data, total_jobs)
    build_category_pages(tools_data, total_jobs)
    build_tool_review_pages(tools_data, total_jobs)
    build_comparison_pages(tools_data, total_jobs)
    build_roundup_pages(tools_data, total_jobs)
