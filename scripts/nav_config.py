# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "MOps Report"
SITE_URL = "https://mopsreport.com"
SITE_TAGLINE = "Career intelligence for marketing operations professionals"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "1"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Brief"

SIGNUP_WORKER_URL = "https://mops-newsletter-signup.rome-workers.workers.dev/subscribe"

GA_MEASUREMENT_ID = ""
GOOGLE_SITE_VERIFICATION = ""  # Set to verification filename (e.g., "google1234abcd.html") to generate file
GOOGLE_SITE_VERIFICATION_META = ""  # Set to verification code for meta tag method (alternative to HTML file)

NAV_ITEMS = [
    {
        "href": "/salary/",
        "label": "Salary Data",
        "children": [
            {"href": "/salary/", "label": "Salary Index"},
            {"href": "/salary/entry/", "label": "Entry-Level"},
            {"href": "/salary/senior/", "label": "Senior"},
            {"href": "/salary/director/", "label": "Director"},
            {"href": "/salary/vp/", "label": "VP"},
            {"href": "/salary/remote/", "label": "Remote vs. Onsite"},
            {"href": "/salary/calculator/", "label": "Calculator"},
            {"href": "/salary/vs-revops/", "label": "MOps vs. RevOps"},
        ],
    },
    {
        "href": "/tools/",
        "label": "Tools",
        "children": [
            {"href": "/tools/", "label": "Tools Index"},
            {"href": "/tools/category/marketing-automation/", "label": "Marketing Automation"},
            {"href": "/tools/category/crm/", "label": "CRM"},
            {"href": "/tools/category/analytics/", "label": "Analytics"},
            {"href": "/tools/category/integration/", "label": "Integration"},
            {"href": "/tools/compare/marketo-vs-hubspot/", "label": "Marketo vs. HubSpot"},
        ],
    },
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-break-into-mops/", "label": "How to Break Into MOps"},
            {"href": "/careers/job-growth/", "label": "Job Market Growth"},
        ],
    },
    {"href": "/glossary/", "label": "Glossary"},
    {
        "href": "/insights/",
        "label": "Resources",
        "children": [
            {"href": "/insights/", "label": "Insights"},
            {"href": "/blog/", "label": "Blog"},
            {"href": "/jobs/", "label": "Job Board"},
        ],
    },
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/entry/", "label": "Entry-Level"},
        {"href": "/salary/senior/", "label": "Senior"},
        {"href": "/salary/director/", "label": "Director"},
        {"href": "/salary/remote/", "label": "Remote vs. Onsite"},
        {"href": "/salary/calculator/", "label": "Calculator"},
        {"href": "/salary/vs-revops/", "label": "MOps vs. RevOps"},
    ],
    "Resources": [
        {"href": "/tools/", "label": "MOps Tools"},
        {"href": "/tools/category/marketing-automation/", "label": "Marketing Automation"},
        {"href": "/tools/category/crm/", "label": "CRM Tools"},
        {"href": "/tools/category/analytics/", "label": "Analytics Tools"},
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/careers/how-to-break-into-mops/", "label": "How to Break Into MOps"},
        {"href": "/glossary/", "label": "Glossary"},
        {"href": "/jobs/", "label": "Job Board"},
        {"href": "/blog/", "label": "Blog"},
        {"href": "/insights/", "label": "Insights"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
    "MOps Tools & Resources": [
        {"href": "https://therevopsreport.com", "label": "RevOps Report", "external": True},
        {"href": "https://gtmepulse.com", "label": "GTME Pulse", "external": True},
        {"href": "https://b2bsalestools.com", "label": "B2B Sales Tools", "external": True},
        {"href": "https://datastackguide.com", "label": "DataStack Guide", "external": True},
    ],
}
