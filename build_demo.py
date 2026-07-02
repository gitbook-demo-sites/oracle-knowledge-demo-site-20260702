from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/gitbook-demo-sites/oracle-knowledge-demo-site-20260702/main"


SPACES = {
    "home": "Home",
    "knowledge-foundation": "Knowledge Foundation",
    "implementation-guides": "Implementation Guides",
    "analytics-operations": "Analytics & Operations",
}


def write(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def yaml(space: str) -> None:
    write(
        f"{space}/.gitbook.yaml",
        """
        root: ./
        structure:
          readme: README.md
          summary: SUMMARY.md
        """,
    )


def vars_file(space: str) -> None:
    write(
        f"{space}/.gitbook/vars.yaml",
        """
        product_name: Oracle Knowledge
        demo_name: Oracle Knowledge Experience Hub
        support_channel: Oracle Support
        review_stage: First-draft demo
        """,
    )


def summary(space: str, lines: list[str]) -> None:
    write(space + "/SUMMARY.md", "# Table of contents\n\n" + "\n".join(lines))


def card(icon: str, title: str, desc: str, href: str) -> str:
    return f'<tr><td><i class="fa-{icon}"></i></td><td><strong>{title}</strong></td><td>{desc}</td><td><a href="{href}">{title}</a></td></tr>'


for slug in SPACES:
    yaml(slug)
    vars_file(slug)

write(
    "README.md",
    """
    # Oracle Knowledge demo site

    First-draft GitBook demo content for Oracle Knowledge. Each top-level folder is a GitBook space imported into the demo site.
    """,
)

write(".gitignore", ".DS_Store\nThumbs.db\n*.swp\n*.swo\n.idea/\n.vscode/\n")

write(
    "assets/oracle-knowledge-banner.svg",
    """
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520" role="img" aria-label="Oracle Knowledge demo banner">
      <rect width="1600" height="520" fill="#F8F6F3"/>
      <rect x="0" y="0" width="1600" height="18" fill="#C74634"/>
      <circle cx="1240" cy="190" r="210" fill="#312D2A" opacity=".08"/>
      <circle cx="1370" cy="275" r="180" fill="#C74634" opacity=".10"/>
      <path d="M1060 130h260c58 0 105 47 105 105s-47 105-105 105h-260c-58 0-105-47-105-105s47-105 105-105zm0 52c-29 0-53 24-53 53s24 53 53 53h260c29 0 53-24 53-53s-24-53-53-53h-260z" fill="#C74634"/>
      <text x="96" y="190" font-family="Arial, Helvetica, sans-serif" font-size="86" font-weight="700" fill="#312D2A" letter-spacing="0">Oracle Knowledge</text>
      <text x="100" y="255" font-family="Arial, Helvetica, sans-serif" font-size="30" fill="#5F5753">Experience hub demo for governed knowledge, search, analytics, and service delivery</text>
      <rect x="100" y="324" width="205" height="42" rx="3" fill="#C74634"/>
      <text x="124" y="352" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">GitBook first draft</text>
    </svg>
    """,
)

write(
    "assets/oracle-mark.svg",
    """
    <svg xmlns="http://www.w3.org/2000/svg" width="420" height="120" viewBox="0 0 420 120" role="img" aria-label="Oracle Knowledge">
      <rect width="420" height="120" fill="#F8F6F3"/>
      <path d="M54 29h210c17 0 31 14 31 31s-14 31-31 31H54c-17 0-31-14-31-31s14-31 31-31zm0 17c-8 0-14 6-14 14s6 14 14 14h210c8 0 14-6 14-14s-6-14-14-14H54z" fill="#C74634"/>
      <text x="314" y="66" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#312D2A">Knowledge</text>
    </svg>
    """,
)

write(
    "home/README.md",
    f"""
    ---
    description: A branded front door for Oracle Knowledge documentation, authoring, search, analytics, and service delivery.
    icon: house
    cover: "{RAW}/assets/oracle-knowledge-banner.svg"
    coverY: 0
    layout:
      width: wide
      cover:
        visible: true
        size: hero
      title:
        visible: true
      description:
        visible: true
      tableOfContents:
        visible: false
      outline:
        visible: false
      pagination:
        visible: true
    ---

    # Oracle Knowledge Experience Hub

    One governed knowledge system for authoring, search, delivery, analytics, and continuous improvement.

    This first-draft demo turns the public Oracle Knowledge documentation library into a modern GitBook experience. It keeps the major source areas from the Release 8.6 library, then reframes them as task-based paths for knowledge authors, administrators, service teams, implementers, and operations leaders.

    {{% hint style="info" %}}
    Demo assumption: this is a curated first draft, not a literal migration. It uses Oracle's public product and documentation themes to show what a cleaner knowledge documentation hub could feel like in GitBook.
    {{% endhint %}}

    ## Choose your path

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    {card("pen-nib", "Author and govern knowledge", "Templates, lifecycle states, reuse, approval, access, and version control.", "https://app.gitbook.com/s/XSPACE_FOUNDATION/")}
    {card("magnifying-glass", "Implement search and delivery", "Intelligent search, agent workspace delivery, self-service, global knowledge, and integrations.", "https://app.gitbook.com/s/XSPACE_GUIDES/")}
    {card("chart-line", "Measure and improve", "Knowledge effectiveness, search analysis, content health, support runbooks, and release notes.", "https://app.gitbook.com/s/XSPACE_ANALYTICS/")}
    {card("route", "Map the source docs", "Understand how the old Oracle Knowledge library maps to the new GitBook structure.", "source-map.md")}
    </tbody></table>

    ## Demo story

    {{% columns %}}
    {{% column %}}
    **Before:** readers start from release packages and PDF libraries such as installation, intelligent search, information manager, analytics, CRM/integration, and general platform documentation.

    **After:** readers start from the job they need to complete, then GitBook search and AI Assistant pull across every space.
    {{% endcolumn %}}
    {{% column %}}
    **For Oracle teams:** product, docs, support, services, and regional teams get a single reviewable source.

    **For customers:** administrators, agents, and self-service teams can find the right article, configuration, or operational guidance faster.
    {{% endcolumn %}}
    {{% endcolumns %}}

    ## What GitBook adds

    * Share-link review for a staged documentation experience.
    * Git-backed authoring and review workflows for technical writers and product owners.
    * AI answers across authoring, administration, search, delivery, and analytics topics.
    * Cleaner navigation than a release-by-release documentation table.
    """,
)

summary(
    "home",
    [
        "* [Home](README.md)",
        "* [Source map](source-map.md)",
        "* [Editorial model](editorial-model.md)",
        "* [Migration story](migration-story.md)",
    ],
)

write(
    "home/source-map.md",
    """
    ---
    description: Map the public Oracle Knowledge documentation library into the demo GitBook structure.
    icon: route
    ---

    # Source Map

    The source page groups Oracle Knowledge Release 8.6 into installation and release documentation, intelligent search, information manager, analytics, CRM and integration, and general platform documentation. The demo keeps those areas but presents them as reader jobs.

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><i class="fa-box-open"></i></td><td><strong>Installation and release</strong></td><td>Install, configure, upgrade, and understand supported environments.</td><td><a href="https://app.gitbook.com/s/XSPACE_GUIDES/installation-and-upgrade.md">Installation and upgrade</a></td></tr>
    <tr><td><i class="fa-magnifying-glass"></i></td><td><strong>Intelligent Search</strong></td><td>Search configuration, relevance, recommendations, and tuning.</td><td><a href="https://app.gitbook.com/s/XSPACE_GUIDES/intelligent-search.md">Intelligent search</a></td></tr>
    <tr><td><i class="fa-file-pen"></i></td><td><strong>Information Manager</strong></td><td>Article creation, categorization, workflows, and governance.</td><td><a href="https://app.gitbook.com/s/XSPACE_FOUNDATION/create-and-govern-articles.md">Create and govern articles</a></td></tr>
    <tr><td><i class="fa-chart-simple"></i></td><td><strong>Analytics</strong></td><td>Usage, answer quality, search terms, and content health.</td><td><a href="https://app.gitbook.com/s/XSPACE_ANALYTICS/analytics-reporting.md">Analytics and reporting</a></td></tr>
    </tbody></table>

    ## What changed

    * Release libraries become a persistent documentation hub with space-level ownership.
    * PDF-style topic sets become task-based pages with stepper blocks, cards, hints, and status updates.
    * Cross-functional areas such as analytics, search, and access control become easier to discover from any entry point.
    """,
)

write(
    "home/editorial-model.md",
    """
    ---
    description: A practical operating model for maintaining Oracle Knowledge documentation in GitBook.
    icon: users-gear
    ---

    # Editorial Model

    A knowledge documentation hub needs a governance model as much as it needs a nicer front end. The strongest demo story is an Oracle-style documentation workflow that lets writers, product owners, support leaders, and regional teams collaborate without weakening control.

    {% stepper %}
    {% step %}
    ### Draft in the right space

    Writers update authoring, implementation, or analytics pages in the space that owns the topic.
    {% endstep %}

    {% step %}
    ### Review with product and support

    Product owners check feature accuracy, while support teams validate whether the page answers real service questions.
    {% endstep %}

    {% step %}
    ### Stage through a share link

    A share-link site lets sales, success, services, and leadership test the experience before publishing.
    {% endstep %}

    {% step %}
    ### Improve from feedback and analytics

    Page feedback, search analytics, and AI answer gaps turn documentation quality into a measurable workflow.
    {% endstep %}
    {% endstepper %}
    """,
)

write(
    "home/migration-story.md",
    """
    ---
    description: The recommended first migration path from release libraries to a GitBook documentation hub.
    icon: arrows-rotate
    ---

    # Migration Story

    This demo does not assume Oracle would migrate every historical release library on day one. A cleaner path is to separate evergreen product knowledge from archival release material.

    {% tabs %}
    {% tab title="First demo" %}
    Show the Release 8.6 areas as a polished experience with authored landing pages, high-signal representative guides, and AI Assistant enabled.
    {% endtab %}

    {% tab title="Pilot" %}
    Import one complete library, wire Git Sync, add owner review, and measure search terms and feedback.
    {% endtab %}

    {% tab title="Scale" %}
    Add versioned spaces or archive spaces for older releases, then route current users to the most relevant version automatically.
    {% endtab %}
    {% endtabs %}

    {% hint style="success" %}
    Demo talk track: GitBook can make a large documentation estate feel more usable without forcing a risky all-at-once migration.
    {% endhint %}
    """,
)

write(
    "knowledge-foundation/README.md",
    """
    ---
    description: Build, govern, reuse, and secure Oracle Knowledge content.
    icon: pen-nib
    ---

    # Knowledge Foundation

    The foundation of Oracle Knowledge is a repeatable way to create accurate articles, route them through review, reuse content across experiences, and control who can see what.

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><i class="fa-file-pen"></i></td><td><strong>Create articles</strong></td><td>Turn policies, procedures, and troubleshooting knowledge into reusable content.</td><td><a href="create-and-govern-articles.md">Create articles</a></td></tr>
    <tr><td><i class="fa-layer-group"></i></td><td><strong>Reuse content</strong></td><td>Share trusted knowledge across self-service, agent, field service, and internal help.</td><td><a href="reusable-content.md">Reuse content</a></td></tr>
    <tr><td><i class="fa-code-branch"></i></td><td><strong>Control lifecycle</strong></td><td>Manage draft, review, approval, versioning, expiration, and rollback.</td><td><a href="lifecycle-versioning.md">Control lifecycle</a></td></tr>
    <tr><td><i class="fa-lock"></i></td><td><strong>Restrict access</strong></td><td>Separate public, agent-only, partner, and internal knowledge experiences.</td><td><a href="access-control.md">Restrict access</a></td></tr>
    </tbody></table>
    """,
)

summary(
    "knowledge-foundation",
    [
        "* [Overview](README.md)",
        "* [Create and govern articles](create-and-govern-articles.md)",
        "* [Reusable content](reusable-content.md)",
        "* [Lifecycle and versioning](lifecycle-versioning.md)",
        "* [Access control](access-control.md)",
    ],
)

write(
    "knowledge-foundation/create-and-govern-articles.md",
    """
    ---
    description: Use templates, review states, categories, and ownership to keep knowledge useful.
    icon: file-pen
    ---

    # Create and Govern Articles

    Knowledge authoring should help subject-matter experts capture answers without making readers understand the internal release library.

    {% stepper %}
    {% step %}
    ### Pick the article pattern

    Use templates for FAQs, troubleshooting procedures, how-to guides, policy explanations, and technical support documents.
    {% endstep %}

    {% step %}
    ### Assign ownership

    Give each article a clear product owner, support reviewer, and expiration review date.
    {% endstep %}

    {% step %}
    ### Classify for discovery

    Add product, audience, region, language, service workflow, and access-level metadata.
    {% endstep %}

    {% step %}
    ### Publish through review

    Route sensitive content through approval before it reaches agents, self-service users, or partners.
    {% endstep %}
    {% endstepper %}

    {% hint style="info" %}
    In GitBook, this article pattern can be modeled with templates, change requests, page metadata, and reusable content blocks.
    {% endhint %}
    """,
)

write(
    "knowledge-foundation/reusable-content.md",
    """
    ---
    description: Reuse trusted knowledge across articles, channels, and audiences without copy-paste drift.
    icon: layer-group
    ---

    # Reusable Content

    Oracle Knowledge includes the idea of placing reusable articles into multiple knowledge assets. In a GitBook demo, the same idea can be shown with reusable snippets, variables, and cross-space references.

    {% columns %}
    {% column %}
    **Reusable snippets**

    Use includes for repeated disclaimers, support escalation paths, prerequisite blocks, and compliance notes.
    {% endcolumn %}
    {% column %}
    **Shared variables**

    Use variables for product names, support channels, version labels, and regional service names.
    {% endcolumn %}
    {% endcolumns %}

    ```mermaid
    flowchart LR
      Source[Canonical answer] --> Public[Self-service article]
      Source --> Agent[Agent workspace note]
      Source --> Field[Field service guidance]
      Source --> Internal[Internal help desk page]
    ```
    """,
)

write(
    "knowledge-foundation/lifecycle-versioning.md",
    """
    ---
    description: Keep article revisions current, reviewed, and recoverable.
    icon: code-branch
    ---

    # Lifecycle and Versioning

    A mature knowledge base needs lifecycle controls that are visible to owners and understandable to readers.

    <table>
    <thead><tr><th>State</th><th>Owner action</th><th>Reader impact</th></tr></thead>
    <tbody>
    <tr><td>Draft</td><td>Capture or revise the answer.</td><td>Not visible unless explicitly shared.</td></tr>
    <tr><td>Review</td><td>Product, support, or compliance validates the content.</td><td>Preview through staging.</td></tr>
    <tr><td>Published</td><td>Content is available in the correct channel.</td><td>Searchable and answerable by AI.</td></tr>
    <tr><td>Expired</td><td>Owner must reapprove, update, or archive.</td><td>Can be hidden or flagged as stale.</td></tr>
    </tbody>
    </table>

    {% hint style="warning" %}
    Old release documentation should not disappear, but it should be clearly separated from current customer-facing guidance.
    {% endhint %}
    """,
)

write(
    "knowledge-foundation/access-control.md",
    """
    ---
    description: Model public, agent-only, partner, and internal knowledge access.
    icon: lock
    ---

    # Access Control

    Knowledge delivery often changes by audience. Public self-service users, agents, field service teams, partners, and employees may need different levels of detail.

    <details>
    <summary>Example access levels</summary>

    * Public: customer-facing troubleshooting and setup guidance.
    * Agent-only: internal decision trees, escalation paths, and service scripts.
    * Partner: integration checklists, deployment guidance, and account-specific steps.
    * Internal: policies, HR, IT, and operational procedures.

    </details>

    {% hint style="success" %}
    GitBook can demo this with site visibility, space permissions, visitor claims, and adaptive content.
    {% endhint %}
    """,
)

write(
    "implementation-guides/README.md",
    """
    ---
    description: Implement, configure, search, deliver, translate, and integrate Oracle Knowledge.
    icon: magnifying-glass
    ---

    # Implementation Guides

    This space turns the implementation side of Oracle Knowledge into task-based guidance for admins and services teams.

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><i class="fa-screwdriver-wrench"></i></td><td><strong>Install and upgrade</strong></td><td>Plan environments, prerequisites, configuration, and release upgrades.</td><td><a href="installation-and-upgrade.md">Install and upgrade</a></td></tr>
    <tr><td><i class="fa-magnifying-glass"></i></td><td><strong>Tune intelligent search</strong></td><td>Improve relevance, recommendations, filters, excerpts, and answer precision.</td><td><a href="intelligent-search.md">Tune search</a></td></tr>
    <tr><td><i class="fa-headset"></i></td><td><strong>Deliver knowledge</strong></td><td>Embed answers in agent workspaces, self-service, field service, and internal help.</td><td><a href="agent-self-service.md">Deliver knowledge</a></td></tr>
    <tr><td><i class="fa-plug"></i></td><td><strong>Integrate systems</strong></td><td>Connect CRM, support, search, and external knowledge sources.</td><td><a href="integration-patterns.md">Integrate systems</a></td></tr>
    </tbody></table>
    """,
)

summary(
    "implementation-guides",
    [
        "* [Overview](README.md)",
        "## Plan and configure",
        "* [Installation and upgrade](installation-and-upgrade.md)",
        "* [Intelligent search](intelligent-search.md)",
        "## Deliver answers",
        "* [Agent and self-service delivery](agent-self-service.md)",
        "* [Global knowledge](global-knowledge.md)",
        "* [Integration patterns](integration-patterns.md)",
    ],
)

write(
    "implementation-guides/installation-and-upgrade.md",
    """
    ---
    description: Plan the installation, configuration, upgrade, and supported environment story.
    icon: screwdriver-wrench
    ---

    # Installation and Upgrade

    The original library separates installation, release notes, upgrading, supported environments, and third-party acknowledgments. A GitBook pilot can keep those topics connected through a single implementation checklist.

    {% stepper %}
    {% step %}
    ### Confirm supported environments

    Validate product version, infrastructure, browser, integration, and third-party requirements.
    {% endstep %}

    {% step %}
    ### Configure the knowledge stack

    Prepare authoring, search, delivery channels, access rules, and analytics.
    {% endstep %}

    {% step %}
    ### Run the upgrade plan

    Review release notes, known issues, rollback steps, and post-upgrade verification.
    {% endstep %}

    {% step %}
    ### Publish operational status

    Give administrators one page for current release state, support contacts, and next actions.
    {% endstep %}
    {% endstepper %}
    """,
)

write(
    "implementation-guides/intelligent-search.md",
    """
    ---
    description: Configure and tune search so agents and customers find useful answers quickly.
    icon: magnifying-glass
    ---

    # Intelligent Search

    Intelligent search is the bridge between a large knowledge repository and a fast answer experience.

    {% tabs %}
    {% tab title="Relevance" %}
    Use product, audience, language, article type, and freshness signals to prioritize the best answer.
    {% endtab %}

    {% tab title="Recommendations" %}
    Surface suggested articles in agent workflows based on service request context and customer intent.
    {% endtab %}

    {% tab title="Analysis" %}
    Review search terms, no-result queries, clicked answers, and deflection outcomes to tune the repository.
    {% endtab %}
    {% endtabs %}

    ```mermaid
    flowchart LR
      Query[Customer or agent question] --> Index[Knowledge index]
      Index --> Rank[Relevance and filters]
      Rank --> Answer[Article, excerpt, or recommendation]
      Answer --> Analytics[Search and answer analysis]
      Analytics --> Rank
    ```
    """,
)

write(
    "implementation-guides/agent-self-service.md",
    """
    ---
    description: Deliver the right answer in agent workspace, customer self-service, field service, and internal help.
    icon: headset
    ---

    # Agent and Self-Service Delivery

    Knowledge has the most impact when it appears inside the workflow where the question starts.

    <table>
    <thead><tr><th>Channel</th><th>What readers need</th><th>Demo page pattern</th></tr></thead>
    <tbody>
    <tr><td>Agent workspace</td><td>Recommended articles and service scripts.</td><td>Role-based troubleshooting guide.</td></tr>
    <tr><td>Self-service portal</td><td>Searchable FAQs and how-to content.</td><td>Public customer help page.</td></tr>
    <tr><td>Field service</td><td>Onsite instructions and media-rich guidance.</td><td>Mobile-friendly procedures.</td></tr>
    <tr><td>Internal help desk</td><td>Employee policies and IT answers.</td><td>Private knowledge space.</td></tr>
    </tbody>
    </table>

    {% hint style="info" %}
    In a live GitBook demo, each channel can become either a space, a section, or an adaptive page view depending on how Oracle wants to govern ownership.
    {% endhint %}
    """,
)

write(
    "implementation-guides/global-knowledge.md",
    """
    ---
    description: Support multilingual and regional knowledge experiences.
    icon: globe
    ---

    # Global Knowledge

    Global organizations need the same answer to be trustworthy across regions, languages, and channels.

    {% columns %}
    {% column %}
    **Language operations**

    Track translation state, compare language versions, and localize examples without losing source ownership.
    {% endcolumn %}
    {% column %}
    **Regional delivery**

    Route readers to the content that matches product availability, geography, and support policy.
    {% endcolumn %}
    {% endcolumns %}

    <details>
    <summary>Demo extension</summary>

    Add localized site variants for two high-priority languages, then use a shared source space to show what stays canonical across translations.

    </details>
    """,
)

write(
    "implementation-guides/integration-patterns.md",
    """
    ---
    description: Connect knowledge to CRM, service portals, external repositories, and support workflows.
    icon: plug
    ---

    # Integration Patterns

    Oracle Knowledge documentation references CRM and integration material. In a modern hub, those integrations should be visible as implementation patterns rather than hidden in a PDF library.

    ```mermaid
    flowchart TB
      Knowledge[Knowledge repository] --> CRM[CRM and service requests]
      Knowledge --> Portal[Self-service portal]
      Knowledge --> Search[Search and AI answer layer]
      External[External knowledge sources] --> Search
      Analytics[Analytics] --> Knowledge
    ```

    ## Integration checklist

    * Decide which system owns article source content.
    * Define metadata that must travel with each article.
    * Test search relevance across internal and external sources.
    * Add analytics for no-result searches and low-confidence answer paths.
    * Document escalation paths when an article does not solve the issue.
    """,
)

write(
    "analytics-operations/.gitbook/tags.yaml",
    """
    releases:
      label: Releases
      color: "#C74634"
    analytics:
      label: Analytics
      color: "#312D2A"
    operations:
      label: Operations
      color: "#6F625C"
    """,
)

write(
    "analytics-operations/README.md",
    """
    ---
    description: Use analytics, runbooks, release notes, and feedback loops to keep knowledge useful.
    icon: chart-line
    ---

    # Analytics & Operations

    Knowledge management becomes strategic when teams can see what content works, what readers cannot find, and what needs review.

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><i class="fa-chart-simple"></i></td><td><strong>Measure usage</strong></td><td>Track article usage, search terms, deflection, and answer effectiveness.</td><td><a href="analytics-reporting.md">Measure usage</a></td></tr>
    <tr><td><i class="fa-stethoscope"></i></td><td><strong>Inspect health</strong></td><td>Find stale, low-value, duplicate, and missing knowledge assets.</td><td><a href="content-health.md">Inspect health</a></td></tr>
    <tr><td><i class="fa-life-ring"></i></td><td><strong>Operate support</strong></td><td>Use runbooks for escalation, content gaps, and critical answer incidents.</td><td><a href="support-runbook.md">Operate support</a></td></tr>
    <tr><td><i class="fa-clock-rotate-left"></i></td><td><strong>Communicate releases</strong></td><td>Publish versioned updates, known issues, and documentation changes.</td><td><a href="release-notes.md">Communicate releases</a></td></tr>
    </tbody></table>
    """,
)

summary(
    "analytics-operations",
    [
        "* [Overview](README.md)",
        "* [Analytics and reporting](analytics-reporting.md)",
        "* [Content health](content-health.md)",
        "* [Support runbook](support-runbook.md)",
        "* [Release notes](release-notes.md)",
    ],
)

write(
    "analytics-operations/analytics-reporting.md",
    """
    ---
    description: Turn knowledge usage and search behavior into operational insight.
    icon: chart-simple
    ---

    # Analytics and Reporting

    Analytics should answer whether the knowledge base is reducing effort for customers, agents, and employees.

    <table>
    <thead><tr><th>Report</th><th>Question it answers</th><th>Owner</th></tr></thead>
    <tbody>
    <tr><td>Knowledgebase effectiveness</td><td>Which articles resolve incidents or deflect cases?</td><td>Support operations</td></tr>
    <tr><td>Search analysis</td><td>What terms lead to no result or weak answers?</td><td>Search owner</td></tr>
    <tr><td>Answer analysis</td><td>Which answers are stale, popular, or confusing?</td><td>Documentation lead</td></tr>
    <tr><td>Revision control</td><td>Where are review bottlenecks or outdated approvals?</td><td>Knowledge governance</td></tr>
    </tbody>
    </table>
    """,
)

write(
    "analytics-operations/content-health.md",
    """
    ---
    description: Detect outdated, duplicated, missing, and low-performing knowledge content.
    icon: stethoscope
    ---

    # Content Health

    A large knowledge estate needs a visible health loop. Otherwise the same stale article can appear in self-service, agent workspace, and internal help.

    {% stepper %}
    {% step %}
    ### Find signals

    Use searches with no click, repeated escalations, low ratings, high bounce, and expired review dates.
    {% endstep %}

    {% step %}
    ### Triage the gap

    Decide whether the issue is missing content, confusing wording, weak metadata, or product behavior.
    {% endstep %}

    {% step %}
    ### Assign ownership

    Route the update to documentation, support, product, regional operations, or compliance.
    {% endstep %}

    {% step %}
    ### Verify improvement

    Watch whether no-result searches, escalations, or article dislikes decrease after publication.
    {% endstep %}
    {% endstepper %}
    """,
)

write(
    "analytics-operations/support-runbook.md",
    """
    ---
    description: Operational runbooks for answer gaps, broken search, stale articles, and escalations.
    icon: life-ring
    ---

    # Support Runbook

    Use this page in the demo to show how GitBook can hold operational knowledge, not just product reference pages.

    <details>
    <summary>No-result search spike</summary>

    1. Review the top failed terms.
    2. Check whether articles exist but lack metadata.
    3. Add redirects, synonyms, or new article stubs.
    4. Assign article owners for full remediation.

    </details>

    <details>
    <summary>Critical article is stale</summary>

    1. Mark the article as needing review.
    2. Add a temporary warning note if readers may be affected.
    3. Route the page to the product owner.
    4. Publish the corrected version and document the change.

    </details>
    """,
)

write(
    "analytics-operations/release-notes.md",
    """
    ---
    description: Versioned release and documentation updates for the demo site.
    icon: clock-rotate-left
    layout:
      width: wide
    ---

    # Release Notes

    {% updates %}
    {% update date="2026-07-02" tags="releases,analytics" %}
    ### First Oracle Knowledge demo draft

    Created the first GitBook demo structure with home, knowledge foundation, implementation guides, and analytics operations spaces.
    {% endupdate %}

    {% update date="2026-07-02" tags="operations" %}
    ### Source map added

    Added a source map from Oracle Knowledge Release 8.6 documentation areas into task-based GitBook spaces.
    {% endupdate %}
    {% endupdates %}
    """,
)


print(f"Built {len(SPACES)} spaces in {ROOT}")
