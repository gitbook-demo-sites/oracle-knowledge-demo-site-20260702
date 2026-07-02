import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORG_ID = "2DnmWBpytIOUKeXExonU"  # Demo Org
BASE = "https://api.gitbook.com/v1"
REPO = "oracle-knowledge-demo-site-20260702"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"

SPACES = [
    {
        "key": "HOME",
        "sentinel": "XSPACE_HOME",
        "folder": "home",
        "title": "Home",
        "emoji": "1f3e0",
        "icon": "house",
        "path": "home",
        "description": "Branded front door, source mapping, editorial model, and migration story.",
    },
    {
        "key": "FOUNDATION",
        "sentinel": "XSPACE_FOUNDATION",
        "folder": "knowledge-foundation",
        "title": "Knowledge Foundation",
        "emoji": "1f4dd",
        "icon": "pen-nib",
        "path": "knowledge-foundation",
        "description": "Authoring, content reuse, lifecycle governance, versioning, and access control.",
    },
    {
        "key": "GUIDES",
        "sentinel": "XSPACE_GUIDES",
        "folder": "implementation-guides",
        "title": "Implementation Guides",
        "emoji": "1f50d",
        "icon": "magnifying-glass",
        "path": "implementation-guides",
        "description": "Installation, intelligent search, delivery channels, global knowledge, and integrations.",
    },
    {
        "key": "ANALYTICS",
        "sentinel": "XSPACE_ANALYTICS",
        "folder": "analytics-operations",
        "title": "Analytics & Operations",
        "emoji": "1f4c8",
        "icon": "chart-line",
        "path": "analytics-operations",
        "description": "Usage analytics, content health, support runbooks, and release notes.",
    },
]


def api(method: str, path: str, body=None, expected=(200, 201, 204)):
    token = os.environ["GITBOOK_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def git_commit_push(message: str):
    subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def replace_sentinels(space_ids):
    replacements = {item["sentinel"]: space_ids[item["key"]] for item in SPACES}
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def main():
    _, site = api(
        "POST",
        f"/orgs/{ORG_ID}/sites",
        {
            "type": "ultimate",
            "title": "Oracle Knowledge Experience Hub",
            "visibility": "share-link",
        },
    )
    site_id = site["id"]
    api(
        "PATCH",
        f"/orgs/{ORG_ID}/sites/{site_id}",
        {
            "title": "Oracle Knowledge Experience Hub",
            "visibility": "share-link",
            "basename": "oracle-knowledge-experience-hub",
        },
    )

    created = {"org": ORG_ID, "site": site_id, "spaces": {}, "sections": {}, "site_spaces": {}, "site_object": site}

    for item in SPACES:
        _, space = api(
            "POST",
            f"/orgs/{ORG_ID}/spaces",
            {"title": item["title"], "emoji": item["emoji"], "empty": True, "editMode": "live"},
        )
        space_id = space["id"]
        created["spaces"][item["key"]] = space_id
        _, section = api(
            "POST",
            f"/orgs/{ORG_ID}/sites/{site_id}/sections",
            {"spaceId": space_id, "title": item["title"], "icon": item["icon"], "draft": False},
        )
        section_id = section["id"]
        site_space_id = section["siteSpaces"][0]["id"]
        created["sections"][item["key"]] = section_id
        created["site_spaces"][item["key"]] = site_space_id
        api(
            "PATCH",
            f"/orgs/{ORG_ID}/sites/{site_id}/sections/{section_id}",
            {
                "path": item["path"],
                "description": item["description"],
                "draft": False,
                "defaultSiteSpace": site_space_id,
            },
        )

    api(
        "PATCH",
        f"/orgs/{ORG_ID}/sites/{site_id}",
        {
            "defaultSiteSection": created["sections"]["HOME"],
            "defaultSiteSpace": created["site_spaces"]["HOME"],
        },
    )

    replace_sentinels(created["spaces"])
    (ROOT / "gitbook-created.json").write_text(json.dumps(created, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Resolve Oracle GitBook space links")

    imports = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    (ROOT / "gitbook-import-results.json").write_text(json.dumps(imports, indent=2) + "\n", encoding="utf-8")

    customization = {
        "title": "Oracle Knowledge Experience Hub",
        "localizedTitle": {},
        "internationalization": {"locale": "en"},
        "styling": {
            "theme": "clean",
            "primaryColor": {"light": "#C74634", "dark": "#F56550"},
            "infoColor": {"light": "#312D2A", "dark": "#F8F6F3"},
            "successColor": {"light": "#5F7D4F", "dark": "#8FB879"},
            "warningColor": {"light": "#B35C1E", "dark": "#F5A45C"},
            "dangerColor": {"light": "#C74634", "dark": "#F56550"},
            "tint": {"color": {"light": "#F8F6F3", "dark": "#312D2A"}},
            "corners": "straight",
            "depth": "flat",
            "links": "accent",
            "font": "Inter",
            "monospaceFont": "IBMPlexMono",
            "icons": "regular",
            "background": "plain",
            "sidebar": {"background": "filled", "list": "line"},
            "codeTheme": {
                "default": {"light": "default-light", "dark": "default-dark"},
                "openapi": {"light": "default-light", "dark": "default-dark"},
            },
            "search": "prominent",
        },
        "favicon": {
            "icon": {
                "light": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-mark.svg",
                "dark": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-mark.svg",
            }
        },
        "header": {
            "preset": "default",
            "logo": {
                "light": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-mark.svg",
                "dark": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-mark.svg",
            },
            "links": [
                {"title": "Oracle", "to": {"kind": "url", "url": "https://www.oracle.com/"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Current docs", "to": {"kind": "url", "url": "https://www.oracle.com/technical-resources/documentation/knowledge-documentation.html"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Knowledge Management", "to": {"kind": "url", "url": "https://www.oracle.com/cx/service/knowledge-management/"}, "style": "button-secondary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {
                "light": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-mark.svg",
                "dark": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-mark.svg",
            },
            "groups": [
                {
                    "title": "Demo paths",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Knowledge Foundation", "to": {"kind": "space", "space": created["spaces"]["FOUNDATION"]}, "localizedTitle": {}},
                        {"title": "Implementation Guides", "to": {"kind": "space", "space": created["spaces"]["GUIDES"]}, "localizedTitle": {}},
                        {"title": "Analytics & Operations", "to": {"kind": "space", "space": created["spaces"]["ANALYTICS"]}, "localizedTitle": {}},
                    ],
                },
                {
                    "title": "Sources",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{REPO_OWNER}/{REPO}"}, "localizedTitle": {}},
                        {"title": "Oracle Knowledge docs", "to": {"kind": "url", "url": "https://www.oracle.com/technical-resources/documentation/knowledge-documentation.html"}, "localizedTitle": {}},
                    ],
                },
            ],
            "copyright": "Oracle Knowledge Experience Hub demo - built for review in GitBook.",
        },
        "themes": {"default": "light", "toggeable": True},
        "pdf": {"enabled": True},
        "feedback": {"enabled": True},
        "ai": {
            "mode": "assistant",
            "suggestions": [
                "How should I govern Oracle Knowledge articles?",
                "Where do I configure intelligent search?",
                "How do I deliver knowledge to agents and self-service users?",
                "Which analytics show content health?",
                "How would we migrate the Release 8.6 documentation library?",
            ],
        },
        "advancedCustomization": {"enabled": True},
        "trademark": {"enabled": True},
        "externalLinks": {"target": "self"},
        "pagination": {"enabled": True},
        "pageActions": {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]},
        "git": {"showEditLink": False},
        "privacyPolicy": {"url": "https://www.oracle.com/legal/privacy/"},
        "socialPreview": {"url": f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/oracle-knowledge-banner.svg"},
        "socialAccounts": [],
        "insights": {"trackingCookie": True},
    }
    _, customized = api("PUT", f"/orgs/{ORG_ID}/sites/{site_id}/customization", customization)
    (ROOT / "gitbook-customization-result.json").write_text(json.dumps(customized, indent=2) + "\n", encoding="utf-8")

    publish_status, publish = api("POST", f"/orgs/{ORG_ID}/sites/{site_id}/publish")
    share_status, share = api("POST", f"/orgs/{ORG_ID}/sites/{site_id}/share-links", {"name": "Oracle demo review"})
    final = {
        "publish_status": publish_status,
        "publish": publish,
        "share_status": share_status,
        "share": share,
        "published_url": share["urls"]["published"],
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
    }
    (ROOT / "gitbook-publish-share.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Add Oracle GitBook publish artifacts")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
