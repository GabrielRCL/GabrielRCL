"""Profile README for GabrielRCL/GabrielRCL: banner, diff status block, sections, badge stack, contact."""
import os
from urllib.parse import quote

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')


def lum(hexcolor):
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def badge(label, color, logo=None):
    text = quote(label.replace("-", "--").replace("_", "__"), safe="")
    fg = "black" if lum(color) > 0.45 else "white"
    url = f"https://img.shields.io/badge/{text}-{color}?style=for-the-badge"
    if logo:
        url += f"&logo={quote(logo, safe='')}&logoColor={fg}" if logo.startswith("data:") else f"&logo={logo}&logoColor={fg}"
    return f'<img src="{url}" alt="{label}">'


# (label, hex, simple-icons slug or None) -- same tiers and items as the site
TIERS = [
    ("Daily, in production", [
        ("Python", "3776AB", "python"), ("Odoo 19", "714B67", "odoo"), ("PostgreSQL", "4169E1", "postgresql"),
        ("FastAPI", "009688", "fastapi"), ("Django", "092E20", "django"), ("React", "61DAFB", "react"),
        ("Node.js", "5FA04E", "nodedotjs"), ("Express", "000000", "express"), ("SQLite", "003B57", "sqlite"),
        ("Linux", "FCC624", "linux"), ("Docker", "2496ED", "docker"), ("Git", "F05032", "git"),
        ("Odoo.sh", "714B67", "odoo"), ("Cloudflare", "F38020", "cloudflare"), ("Claude Code", "D97757", "claude"),
        ("Raspberry Pi", "A22846", "raspberrypi"), ("Tailscale", "242424", "tailscale"),
    ]),
    ("Integrations I have shipped", [
        ("Zabbix API", "D40000", None), ("Bitdefender GravityZone", "ED1C24", "bitdefender"),
        ("Meta Tech Provider", "0467DF", "meta"), ("WhatsApp Cloud API", "25D366", "whatsapp"),
        ("MCP", "000000", "modelcontextprotocol"), ("Claude API", "191919", "anthropic"),
        ("NFS-e Nacional · NF-e", "1B4FD8", None), ("Sicoob API", "00AE9D", None), ("Banco Inter API", "FF7A00", None),
        ("Itaú API", "EC7000", None), ("CNAB 240", "0B1530", None), ("Stripe", "635BFF", "stripe"),
        ("Telegram Bot API", "26A5E4", "telegram"), ("HighLevel API", "0B1530", None), ("WebPosto ERP", "0B1530", None),
    ]),
    ("Used in projects", [
        ("Flask", "3BABC3", "flask"), ("SQLAlchemy", "D71F00", "sqlalchemy"), ("Next.js", "000000", "nextdotjs"),
        ("Vite", "646CFF", "vite"), ("JavaScript", "F7DF1E", "javascript"), ("Tailwind", "06B6D4", "tailwindcss"),
        ("MySQL", "4479A1", "mysql"), ("MongoDB", "47A248", "mongodb"), ("Selenium", "43B02A", "selenium"),
        ("Playwright", "2EAD33", None), ("AutoHotkey", "334455", "autohotkey"), ("Lua", "000080", "lua"),
        ("Java", "000000", "openjdk"), ("XAMPP", "FB7A24", "xampp"), ("Railway", "0B0D0E", "railway"),
        ("Vercel", "000000", "vercel"), ("Hetzner", "D50C2D", "hetzner"), ("Google Cloud", "4285F4", "googlecloud"),
        ("VMware", "607078", "vmware"), ("C", "A8B9CC", "c"), ("x86 Assembly", "0B1530", None),
        ("Cheat Engine", "1B4FD8", None), ("Bitcoin Core", "F7931A", "bitcoin"), ("Umbrel", "5351FB", "umbrel"),
    ]),
    ("Studying", [
        ("Kubernetes", "326CE5", "kubernetes"), ("Argo CD", "EF7B4D", "argo"), ("Terraform", "844FBA", "terraform"),
        ("Redis", "FF4438", "redis"), ("AWS", "232F3E", None),
    ]),
]

OUTPUT = "https://raw.githubusercontent.com/GabrielRCL/GabrielRCL/output"


def main():
    stack = []
    for title, items in TIERS:
        stack.append(f"**{title}**\n\n<p>\n" + "\n".join(badge(*it) for it in items) + "\n</p>\n")
    contact = " ".join([
        f'<a href="https://gabrielrcl.dev">{badge("gabrielrcl.dev", "F87934", "googlechrome")}</a>',
        f'<a href="https://www.linkedin.com/in/gabrielrcl777/">{badge("LinkedIn", "0A66C2")}</a>',
        f'<a href="mailto:gabrielrcl@protonmail.com">{badge("gabrielrcl@protonmail.com", "6D4AFF", "protonmail")}</a>',
    ])
    readme = f"""<p align="center"><img src="assets/banner.svg" alt="Gabriel Lucas · Odoo developer" width="100%"></p>

```diff
+ Odoo developer at OutView · Vila Velha, Brazil
! Now: NexView ITSM, Meta Tech Provider, MCP, NFS-e and bank integrations
# Founder of Tibia Macros (2020–2026) · Computer Engineering at Multivix
```

### What I build now, at OutView (Odoo implementation and development, January 2025 to present)

- **[NexView ITSM](https://gonexview.com).** An ITIL-based ITSM suite for Odoo: priority matrix, problem and change management, CMDB, subscriptions and customer portal; Zabbix and Bitdefender GravityZone sync into the CMDB, Discord alerts for SLA deadlines. 379 of the suite's 513 commits are mine.
- **Meta Tech Provider, end to end.** Took OutView through Meta's accreditation: Meta app and Business Manager, business verification, App Review (approved September 2026) and the required legal pages (LGPD privacy policy, terms, data deletion request). Then built WhatsApp Embedded Signup, coexistence echoes and webhook logging on Odoo.
- **AI.** An MCP connector that gives AI assistants access to Odoo limited per model and operation, and the team's Claude Code guardrails (hooks, commit gates, skills).
- **Brazilian e-invoicing.** Co-developed a Python SDK and REST API for NFS-e Nacional and NF-e: signed XML with A1 certificates, submission to the government, XML and PDF back to Odoo.
- **Bank integration layer.** A FastAPI service between Odoo and Sicoob, Banco Inter and Itaú (mTLS, OAuth2): boletos, statements and balances. On the Odoo side: boleto issuing and reissue, CNAB 240 files.
- **Data migrations.** HighLevel to Odoo for a US retailer: about 8,500 contacts and 66,000 WhatsApp messages, with resumable extraction and rehearsals on a production copy.

That work lives in private repositories, which is why most of my contribution graph is private activity.

### Freelance

**[Mar & Minas](https://mareminas.com.br)** (Posto Colorado, Vila Velha; in daily use since July 2026): the system a 24-hour convenience store runs on, built from scratch. Point of sale, tabs, cash register, bills and reports mirroring the gas station's WebPosto ERP, plus the delivery website with SMS sign-in and order tracking. React, Vite, Node.js, Express, SQLite, Cloudflare Workers and Tunnel; the public API runs in a separate process that only opens the delivery database.

### My own product

**[tibia-macros](https://github.com/GabrielRCL/tibia-macros)** (2020 to 2026): desktop automation for the MMORPG Tibia, sold as a monthly subscription (AutoHotkey, screen pattern matching). From the start I ran all of it: the client, a license and trial API, automated Stripe billing with e-mail delivery, auto-update, the [website](https://tibiamacros.netlify.app/) and customer support. It passed 200 monthly users. After the game's publisher changed its policy on third-party software, I discontinued the service and released the source code as open source.

I have hosted and run Tibia (OpenTibia) and Minecraft servers since 2017, and I use Cheat Engine and x86 assembly for memory analysis. I learned most of this before AI assistants existed, from documentation, Stack Overflow, CS50 and the [AutoHotkey forum](https://www.autohotkey.com/boards/memberlist.php?mode=viewprofile&u=139240) (200+ posts).

### Stack

{chr(10).join(stack)}
### Contributions

<img src="{OUTPUT}/contributions.svg" alt="Contributions in the last year, updated every hour">

### Contact

Liked one of these projects? Let's talk.

{contact}

### <img src="assets/icons/coffee.svg" width="28" height="28" alt=""> Buy me a coffee

<img src="assets/icons/bitcoin.svg" width="16" height="16" alt=""> **Bitcoin on-chain**

```text
bc1qlwrptn0jgnexylsycpecpqrekl7zert5hsrxv9
```

<img src="assets/icons/lightning.svg" width="16" height="16" alt=""> **Lightning**

```text
satoshi@gabrielrcl.dev
```
"""
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    print("README.md", len(readme), "bytes,", sum(len(i) for _, i in TIERS), "badges")


if __name__ == "__main__":
    main()
