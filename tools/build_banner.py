"""Profile banner for GabrielRCL/GabrielRCL: name, a self-made typing line and a mini integrations wire.

Each typed phrase, once complete, gets an underline sweep and its logos pop in after the cursor.
SMIL only: GitHub renders README SVGs as <img> (no scripts, no web fonts, no external files), so the
logos are embedded as data URIs from assets/icons. Monospace width is forced with textLength so the
cursor and the logos land right after the last character on any system font.
"""
import base64
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "banner.svg")
ICONS = os.path.join(ROOT, "assets", "icons")
W, H = 1280, 320

# (phrase, [(icon file, width, height)])
PHRASES = [
    ("Odoo developer · ERP integrations", [("odoo.png", 30, 30)]),
    ("ITSM · WhatsApp · MCP · NFS-e · banks", [("nexview.png", 44, 21), ("whatsapp.svg", 28, 28), ("claude.svg", 28, 28), ("nfse.png", 52, 20), ("banks.png", 30, 30)]),
    ("Founder of Tibia Macros (2020–2026)", [("tibiamacros.png", 38, 32)]),
    ("Computer Engineering at Multivix", [("multivix.png", 30, 30)]),
]
# Logos that need a white plate: the NFS-e wordmark is dark green and blue on the navy banner.
PLATED = {"nfse.png"}
SLOT = 4.6                          # seconds per phrase
CYCLE = SLOT * len(PHRASES)
TYPE, HOLD_END, DEL = 1.3, 3.8, 0.45  # typing time, hold until, deleting time (inside a slot)
CW, X0, Y0 = 15.0, 104, 236         # char width, typing line origin


def data_uri(name):
    mime = "image/svg+xml" if name.endswith(".svg") else "image/png"
    with open(os.path.join(ICONS, name), "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def kt(*times):
    return ";".join(f"{min(max(t, 0), CYCLE) / CYCLE:.5f}" for t in times)


def timeline(i):
    """(time, chars shown) pairs for phrase i over the whole cycle."""
    n, s = len(PHRASES[i][0]), i * SLOT
    pts = [(0.0, 0)]
    pts += [(s + TYPE * k / n, k) for k in range(1, n + 1)]
    pts.append((s + HOLD_END, n))
    pts += [(s + HOLD_END + DEL * k / n, n - k) for k in range(1, n + 1)]
    return pts


def discrete(points, fmt):
    pts = sorted(dict(points).items())
    if pts[0][0] != 0:
        pts.insert(0, (0.0, pts[0][1]))
    return ";".join(f"{t / CYCLE:.5f}" for t, _ in pts), ";".join(fmt(v) for _, v in pts)


def main():
    uri = {}
    clips, texts, effects = [], [], []
    cursor_pts = {}
    for i, (phrase, logos) in enumerate(PHRASES):
        n, s = len(phrase), i * SLOT
        width = n * CW
        tl = timeline(i)
        k, v = discrete(tl, lambda c: f"{c * CW:.1f}")
        clips.append(
            f'<clipPath id="c{i}"><rect x="{X0}" y="{Y0 - 30}" height="40" width="0">'
            f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{k}" values="{v}"/>'
            f'</rect></clipPath>')
        texts.append(f'<text x="{X0}" y="{Y0}" class="mono" textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})">{html.escape(phrase)}</text>')
        for t, c in tl:
            if s <= t < s + SLOT:
                cursor_pts[t] = c

        done, hold = s + TYPE, s + HOLD_END
        # underline sweep under the finished phrase
        effects.append(
            f'<rect x="{X0}" y="{Y0 + 12}" height="3" rx="1.5" width="0" fill="url(#sun)">'
            f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{kt(0, done, done + 0.35, hold, hold + 0.2, CYCLE)}" values="0;0;{width:.1f};{width:.1f};0;0"/>'
            f'</rect>')
        # logos pop in after the cursor, one after another
        x = X0 + width + 30
        for j, (icon, w, h) in enumerate(logos):
            uri.setdefault(icon, data_uri(icon))
            a = done + 0.1 + 0.09 * j
            y = Y0 - 8 - h / 2
            fade = f'<animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{kt(0, a, a + 0.3, hold, hold + 0.15, CYCLE)}" values="0;0;1;1;0;0"/>'

            def rise(top):
                return (f'<animate attributeName="y" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{kt(0, a, a + 0.3, CYCLE)}" '
                        f'values="{top + 8:.1f};{top + 8:.1f};{top:.1f};{top:.1f}"/>')
            if icon in PLATED:
                effects.append(f'<rect x="{x - 4:.1f}" y="{y - 4:.1f}" width="{w + 8}" height="{h + 8}" rx="4" fill="#FFFFFF" opacity="0">{fade}{rise(y - 4)}</rect>')
            effects.append(f'<image href="{uri[icon]}" x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" opacity="0">{fade}{rise(y)}</image>')
            x += w + (16 if icon in PLATED else 8)
    ck, cv = discrete(cursor_pts.items(), lambda c: f"{X0 + c * CW + 2:.1f}")

    nodes = [("NexView ITSM", "nexview.png", 26, 12.9), ("Zabbix → CMDB", "zabbix.png", 18, 18),
             ("WhatsApp", "whatsapp.svg", 18, 18), ("Claude · MCP", "claude.svg", 20, 20),
             ("NFS-e", "nfse.png", 26, 10), ("Banks", "banks.png", 22, 22)]
    wire_x, top, gap = 968, 62, 40
    first = top + 36
    wire_end = first + (len(nodes) - 1) * gap
    node_svg = []
    for k, (label, icon, iw, ih) in enumerate(nodes):
        plate = icon in PLATED
        uri.setdefault(icon, data_uri(icon))
        y = first + k * gap
        ix = wire_x + 38 + (26 - iw) / 2
        node_svg.append(
            f'<line x1="{wire_x}" y1="{y}" x2="{wire_x + 26}" y2="{y}" stroke="#1B4FD8" stroke-width="3"/>'
            f'<rect x="{wire_x + 26}" y="{y - 15}" width="206" height="30" rx="8" fill="#0C1633" stroke="#1C2A4F"/>'
            + (f'<rect x="{ix - 3:.1f}" y="{y - ih / 2 - 3:.1f}" width="{iw + 6}" height="{ih + 6}" rx="3" fill="#FFFFFF"/>' if plate else '')
            + f'<image href="{uri[icon]}" x="{ix:.1f}" y="{y - ih / 2:.1f}" width="{iw}" height="{ih}"/>'
            f'<text x="{wire_x + 72}" y="{y + 5}" class="node">{html.escape(label)}</text>')
    uri.setdefault("odoo.png", data_uri("odoo.png"))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Gabriel Lucas, Odoo developer">
  <title>Gabriel Lucas · Odoo developer</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050A1C"/><stop offset="1" stop-color="#0C1633"/></linearGradient>
    <radialGradient id="glowBlue" cx="0.82" cy="0.25" r="0.55"><stop offset="0" stop-color="#00B8FF" stop-opacity="0.20"/><stop offset="1" stop-color="#00B8FF" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowSun" cx="0.06" cy="1" r="0.5"><stop offset="0" stop-color="#F87934" stop-opacity="0.22"/><stop offset="1" stop-color="#F87934" stop-opacity="0"/></radialGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F15C48"/><stop offset="0.5" stop-color="#F87934"/><stop offset="1" stop-color="#F9B233"/></linearGradient>
    <linearGradient id="wire" gradientUnits="userSpaceOnUse" x1="{wire_x}" y1="{top}" x2="{wire_x}" y2="{wire_end}"><stop offset="0" stop-color="#1B4FD8"/><stop offset="1" stop-color="#00B8FF"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#94A3B8" stroke-opacity="0.07"/></pattern>
    <radialGradient id="fade" cx="0.7" cy="0.4" r="0.7"><stop offset="0.3" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
    {''.join(clips)}
  </defs>
  <style>
    .eyebrow {{ font: 700 15px 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; letter-spacing: 3px; fill: #38C6F4; }}
    .name {{ font: 900 76px 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; letter-spacing: -2px; }}
    .mono {{ font: 400 25px ui-monospace, 'SF Mono', Consolas, 'Liberation Mono', monospace; fill: #CBD5E1; }}
    .prompt {{ font: 700 25px ui-monospace, 'SF Mono', Consolas, 'Liberation Mono', monospace; fill: #F87934; }}
    .node {{ font: 600 14px 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; fill: #E2E8F0; }}
    .head {{ font: 600 13px ui-monospace, 'SF Mono', Consolas, monospace; letter-spacing: 2px; fill: #E2E8F0; }}
  </style>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>
  <rect width="{W}" height="{H}" fill="url(#glowBlue)"/>
  <rect width="{W}" height="{H}" fill="url(#glowSun)"/>
  <text x="{X0 - 30}" y="92" class="eyebrow">ODOO DEVELOPER · ITSM · ERP INTEGRATIONS · FOUNDER</text>
  <text x="{X0 - 34}" y="178" class="name"><tspan fill="#F8FAFC">Gabriel </tspan><tspan fill="url(#sun)">Lucas</tspan></text>
  <text x="{X0 - 30}" y="{Y0}" class="prompt">&gt;</text>
  {''.join(texts)}
  {''.join(effects)}
  <rect y="{Y0 - 22}" width="12" height="26" fill="#F87934" x="{X0}">
    <animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{ck}" values="{cv}"/>
    <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;0.55" values="1;0"/>
  </rect>
  <circle cx="{wire_x}" cy="{top}" r="9" fill="#050A1C" stroke="#1B4FD8" stroke-width="3"/>
  <image href="{uri['odoo.png']}" x="{wire_x + 18}" y="{top - 11}" width="22" height="22"/>
  <text x="{wire_x + 48}" y="{top + 5}" class="head">ODOO 19</text>
  <line x1="{wire_x}" y1="{top + 9}" x2="{wire_x}" y2="{wire_end}" stroke="url(#wire)" stroke-width="3" stroke-linecap="round"/>
  {''.join(node_svg)}
  <circle cx="{wire_x}" cy="{top + 12}" r="5" fill="#F87934">
    <animate attributeName="cy" dur="4.5s" repeatCount="indefinite" values="{top + 12};{wire_end};{top + 12}" keyTimes="0;0.85;1" calcMode="spline" keySplines="0.45 0 0.55 1;0 0 1 1"/>
    <animate attributeName="opacity" dur="4.5s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;0.08;0.78;0.86;1"/>
  </circle>
</svg>
'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("banner.svg", len(svg), "bytes")


if __name__ == "__main__":
    main()
