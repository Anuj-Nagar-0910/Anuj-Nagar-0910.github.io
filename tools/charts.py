"""Tiny inline-SVG chart helpers. Every chart is a <figure> with a text alternative; colours come from CSS classes."""
import html

esc = html.escape
W = 720


def fig(svg, alt, caption):
    return f'<figure class="chart"><div role="img" aria-label="{esc(alt)}">{svg}</div><figcaption>{caption}</figcaption></figure>'


def _svg(h, body):
    return f'<svg viewBox="0 0 {W} {h}" aria-hidden="true" focusable="false">{body}</svg>'


def diverging(rows, lo, hi, unit=" ms", label_w=150):
    """rows: (label, value, css_class, tag). Bars grow left/right from zero."""
    x0, x1 = label_w, W - 20
    sx = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    zero = sx(0)
    h = 40 + len(rows) * 34
    out = [f'<line class="axis" x1="{zero:.1f}" x2="{zero:.1f}" y1="12" y2="{h - 22}" stroke-width="2"/>']
    for t in range(int(lo), int(hi) + 1, 2):
        out.append(f'<text x="{sx(t):.1f}" y="{h - 6}" text-anchor="middle" opacity=".7">{t:+d}</text>' if t else f'<text x="{zero:.1f}" y="{h - 6}" text-anchor="middle" opacity=".7">0</text>')
    for i, (lab, v, cls, tag) in enumerate(rows):
        y = 18 + i * 34
        xa, xb = sorted((zero, sx(v)))
        out.append(f'<text x="0" y="{y + 15}">{esc(lab)}</text>')
        out.append(f'<rect class="{cls}" x="{xa:.1f}" y="{y}" width="{max(xb - xa, 2):.1f}" height="22" rx="3"/>')
        vx = sx(v) + (8 if v >= 0 else -8)
        out.append(f'<text x="{vx:.1f}" y="{y + 15}" text-anchor="{"start" if v >= 0 else "end"}">{v:+.1f}{unit}{(" " + tag) if tag else ""}</text>')
    return _svg(h, "".join(out))


def pairs(rows, vmax, names, label_w=150, unit="%"):
    """rows: (label, v1, v2). Two bars per row, first accent, second ink."""
    x0, x1 = label_w, W - 70
    sx = lambda v: x0 + v / vmax * (x1 - x0)
    h = 44 + len(rows) * 46
    out = [f'<rect class="bar-b" x="0" y="4" width="12" height="12" rx="2"/><text x="18" y="14">{esc(names[0])}</text><rect class="bar-a" x="260" y="4" width="12" height="12" rx="2"/><text x="278" y="14">{esc(names[1])}</text>']
    for i, (lab, a, b) in enumerate(rows):
        y = 34 + i * 46
        out.append(f'<text x="0" y="{y + 18}">{esc(lab)}</text>')
        out.append(f'<rect class="bar-b" x="{x0}" y="{y}" width="{max(sx(a) - x0, 2):.1f}" height="16" rx="3"/><text x="{sx(a) + 6:.1f}" y="{y + 12}">{a:g}{unit}</text>')
        out.append(f'<rect class="bar-a" x="{x0}" y="{y + 20}" width="{max(sx(b) - x0, 2):.1f}" height="16" rx="3"/><text x="{sx(b) + 6:.1f}" y="{y + 32}">{b:g}{unit}</text>')
    return _svg(h, "".join(out))


def stack(parts, total=None, unit="%"):
    """parts: (label, value, css_class). A single stacked bar with a legend row."""
    total = total or sum(v for _, v, _ in parts)
    x = 0.0
    out = []
    for lab, v, cls in parts:
        w = v / total * (W - 4)
        out.append(f'<rect class="{cls}" x="{x + 2:.1f}" y="30" width="{max(w - 3, 2):.1f}" height="46" rx="4"/>')
        x += w
    lx = 0
    for lab, v, cls in parts:
        out.append(f'<rect class="{cls}" x="{lx}" y="102" width="12" height="12" rx="2"/><text x="{lx + 18}" y="112">{esc(lab)} {v:g}{unit}</text>')
        lx += 18 + len(lab) * 8 + 90
    return _svg(130, "".join(out))


def columns(items, vmax, fmt=lambda v: f"{v:g}", base=34, h=250):
    """items: (label, value, css_class). Vertical bars from zero."""
    n = len(items)
    gap = 24
    bw = (W - gap * (n + 1)) / n
    out = [f'<line class="axis" x1="0" x2="{W}" y1="{h - base}" y2="{h - base}" stroke-width="2"/>']
    for i, (lab, v, cls) in enumerate(items):
        bh = v / vmax * (h - base - 30)
        x = gap + i * (bw + gap)
        y = h - base - bh
        out.append(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4"/>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" style="font-weight:700">{fmt(v)}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{h - 12}" text-anchor="middle">{esc(lab)}</text>')
    return _svg(h, "".join(out))


def line(vals, labels, vmax, fmt=lambda v: f"{v:g}", h=250, ticks=(0, .5, 1.0), tick_fmt=lambda v: f"${v:g}M", mark=()):
    """Month-style line chart; mark = indexes to annotate."""
    left, right, top, bottom = 52, 16, 20, 34
    pw, ph = W - left - right, h - top - bottom
    sx = lambda i: left + i / (len(vals) - 1) * pw
    sy = lambda v: top + ph - v / vmax * ph
    out = []
    for t in ticks:
        y = sy(t * 1e6 if vmax > 1000 else t)
        out.append(f'<line class="axis" x1="{left}" x2="{W - right}" y1="{y:.1f}" y2="{y:.1f}" stroke-dasharray="3 4"/><text x="0" y="{y + 4:.1f}">{tick_fmt(t)}</text>')
    pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
    out.append(f'<polyline points="{pts}" fill="none" stroke="var(--accent)" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, v in enumerate(vals):
        out.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="{5.5 if i in mark else 3.5}" fill="{"var(--accent)" if i in mark else "var(--bg)"}" stroke="var(--fg)" stroke-width="2"/>')
        out.append(f'<text x="{sx(i):.1f}" y="{h - 12}" text-anchor="middle">{labels[i]}</text>')
    for i in mark:
        anchor = "end" if i == len(vals) - 1 else "middle"
        out.append(f'<text x="{sx(i) + (4 if anchor == "end" else 0):.1f}" y="{sy(vals[i]) - 12:.1f}" text-anchor="{anchor}" style="font-weight:700">{fmt(vals[i])}</text>')
    return _svg(h, "".join(out))


def flow(boxes, h=130):
    """boxes: (title, subtitle). A left-to-right flow with arrows."""
    n = len(boxes)
    gap = 26
    bw = (W - gap * (n - 1)) / n
    out = ['<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="currentColor"/></marker></defs>']
    for i, (a, b) in enumerate(boxes):
        x = i * (bw + gap)
        out.append(f'<rect x="{x:.1f}" y="18" width="{bw:.1f}" height="86" rx="12" fill="none" stroke="var(--fg)" stroke-width="2"/>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="56" text-anchor="middle" style="font-weight:700;font-size:13px">{esc(a)}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="76" text-anchor="middle" opacity=".75">{esc(b)}</text>')
        if i < n - 1:
            out.append(f'<line x1="{x + bw + 3:.1f}" x2="{x + bw + gap - 4:.1f}" y1="61" y2="61" stroke="var(--fg)" stroke-width="2" marker-end="url(#ar)" style="color:var(--fg)"/>')
    return _svg(h, "".join(out))
