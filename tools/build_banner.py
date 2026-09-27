"""Profile banner for GabrielRCL/GabrielRCL: name, a self-made typing line and a mini integrations wire.

SMIL only (GitHub renders README SVGs as <img>: no scripts, no web fonts, CSS keyframes are fine but
SMIL keeps the typing steps exact). Monospace width is forced with textLength so the cursor lands
right after the last character on any system font.
"""
import os
import html

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'banner.svg')
W, H = 1280, 320
PHRASES = [
    "Odoo developer · ERP integrations",
    "ITSM · WhatsApp · MCP · NFS-e · banks",
    "Founder of Tibia Macros (2020–2026)",
    "Computer Engineering at Multivix",
]
CYCLE, SLOT = 16.0, 4.0            # seconds: whole loop, one phrase
TYPE, HOLD_END, DEL = 1.3, 3.2, 0.45  # typing time, hold until, deleting time (inside a slot)
CW, X0, Y0 = 15.0, 104, 236        # char width, typing line origin


def timeline(i):
    """(time, chars shown) pairs for phrase i over the whole cycle."""
    n, s = len(PHRASES[i]), i * SLOT
    pts = [(0.0, 0)]
    for k in range(1, n + 1):
        pts.append((s + TYPE * k / n, k))
    pts.append((s + HOLD_END, n))
    for k in range(1, n + 1):
        pts.append((s + HOLD_END + DEL * k / n, n - k))
    return pts


def discrete(points, fmt):
    pts = sorted(dict(points).items())
    if pts[0][0] != 0:
        pts.insert(0, (0.0, pts[0][1]))
    times = ";".join(f"{t / CYCLE:.5f}" for t, _ in pts)
    vals = ";".join(fmt(v) for _, v in pts)
    return times, vals


def main():
    clips, texts = [], []
    cursor_pts = {}
    for i, p in enumerate(PHRASES):
        tl = timeline(i)
        kt, vals = discrete(tl, lambda c: f"{c * CW:.1f}")
        clips.append(
            f'<clipPath id="c{i}"><rect x="{X0}" y="{Y0 - 30}" height="40" width="0">'
            f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>'
            f'</rect></clipPath>')
        texts.append(f'<text x="{X0}" y="{Y0}" class="mono" textLength="{len(p) * CW:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})">{html.escape(p)}</text>')
        s = i * SLOT
        for t, c in tl:
            if s <= t < s + SLOT:
                cursor_pts[t] = c
    kt, vals = discrete(cursor_pts.items(), lambda c: f"{X0 + c * CW + 2:.1f}")

    nodes = ["Zabbix → CMDB", "WhatsApp", "MCP", "NFS-e", "Banks"]
    wire_x, top, gap = 968, 92, 42
    node_svg = []
    for k, label in enumerate(nodes):
        y = top + 34 + k * gap
        node_svg.append(
            f'<line x1="{wire_x}" y1="{y}" x2="{wire_x + 26}" y2="{y}" stroke="#1B4FD8" stroke-width="3"/>'
            f'<rect x="{wire_x + 26}" y="{y - 15}" width="190" height="30" rx="8" fill="#0C1633" stroke="#1C2A4F"/>'
            f'<text x="{wire_x + 42}" y="{y + 5}" class="node">{html.escape(label)}</text>')
    wire_end = top + 34 + (len(nodes) - 1) * gap

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
    .head {{ font: 500 13px ui-monospace, 'SF Mono', Consolas, monospace; letter-spacing: 2px; fill: #E2E8F0; }}
  </style>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>
  <rect width="{W}" height="{H}" fill="url(#glowBlue)"/>
  <rect width="{W}" height="{H}" fill="url(#glowSun)"/>
  <text x="{X0 - 30}" y="92" class="eyebrow">ODOO DEVELOPER · ERP INTEGRATIONS · FOUNDER</text>
  <text x="{X0 - 34}" y="178" class="name"><tspan fill="#F8FAFC">Gabriel </tspan><tspan fill="url(#sun)">Lucas</tspan></text>
  <text x="{X0 - 30}" y="{Y0}" class="prompt">&gt;</text>
  {''.join(texts)}
  <rect y="{Y0 - 22}" width="12" height="26" fill="#F87934" x="{X0}">
    <animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>
    <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;0.55" values="1;0"/>
  </rect>
  <circle cx="{wire_x}" cy="{top}" r="9" fill="#050A1C" stroke="#1B4FD8" stroke-width="3"/>
  <text x="{wire_x + 20}" y="{top + 5}" class="head">ODOO 19</text>
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
