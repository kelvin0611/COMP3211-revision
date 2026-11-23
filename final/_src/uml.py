"""Tiny UML renderer: class diagrams and sequence diagrams -> inline SVG.
Specs live in diagrams.py; parts use {{UML:key}}.
"""
import math, html

INK = "#15202B"; MUT = "#566273"; LINE = "#D2D9E1"
FILL = {  # same kind of thing -> same colour
    "w": ("#FFFFFF", INK),        # ordinary class
    "b": ("#E2E6F8", "#3D4BAA"),  # superclass / abstract / interface
    "t": ("#D9EFEE", "#0B7472"),  # subclass
    "o": ("#FAE6DA", "#BF4A14"),  # highlighted (the thing being discussed)
    "y": ("#F6EBCB", "#8F6200"),  # external system / database
}
CW = 7.75   # approx char width at 12.5px monospace
FONT = 'font-family="ui-monospace,Menlo,monospace"'
HALO = 'paint-order="stroke" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"'

def esc(s): return html.escape(str(s), quote=True)

# ---------------- class diagrams ----------------
def _box(c):
    lines = [c["name"]] + c.get("attrs", []) + c.get("ops", []) + (["«" + c["stereo"] + "»"] if c.get("stereo") else [])
    w = max(len(s) for s in lines) * CW + 18
    w = max(w, c.get("minw", 0))
    h = 26 + max(1, len(c.get("attrs", []))) * 17 + 8 + max(1, len(c.get("ops", []))) * 17 + 6
    if c.get("stereo"): h += 14
    if c.get("compact"): h = 30 + (14 if c.get("stereo") else 0)
    return w, h

def _clip(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0: return cx, cy
    sx = (w / 2) / abs(dx) if dx else 1e9
    sy = (h / 2) / abs(dy) if dy else 1e9
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s

def _poly(pts, fill, stroke):
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.4"/>' % (
        " ".join("%.1f,%.1f" % p for p in pts), fill, stroke)

def _head(x, y, ux, uy, kind):
    """marker at point (x,y) where line arrives travelling in direction (ux,uy)."""
    px, py = -uy, ux
    if kind in ("gen", "real"):
        L, W = 14, 8
        b = (x - ux * L, y - uy * L)
        return _poly([(x, y), (b[0] + px * W, b[1] + py * W), (b[0] - px * W, b[1] - py * W)], "#FFFFFF", INK), L
    if kind in ("agg", "comp"):
        L, W = 22, 7
        m = (x - ux * L / 2, y - uy * L / 2)
        e = (x - ux * L, y - uy * L)
        return _poly([(x, y), (m[0] + px * W, m[1] + py * W), e, (m[0] - px * W, m[1] - py * W)],
                     INK if kind == "comp" else "#FFFFFF", INK), L
    if kind in ("nav", "dep"):
        L, W = 11, 6
        b = (x - ux * L, y - uy * L)
        return '<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.4"/>' % (
            b[0] + px * W, b[1] + py * W, x, y, b[0] - px * W, b[1] - py * W, INK), 0
    return "", 0

def class_svg(d):
    boxes = {}
    out = []
    for name, c in d["classes"].items():
        c = dict(c); c["name"] = c.get("label", name)
        w, h = _box(c)
        boxes[name] = (c["x"], c["y"], w, h, c)
    # links first (under boxes)
    for ln in d.get("links", []):
        A, B = boxes[ln["a"]], boxes[ln["b"]]
        acx, acy = A[0] + A[2] / 2, A[1] + A[3] / 2
        bcx, bcy = B[0] + B[2] / 2, B[1] + B[3] / 2
        if "ax" in ln: acx = A[0] + ln["ax"] * A[2]
        if "bx" in ln: bcx = B[0] + ln["bx"] * B[2]
        if "ay" in ln: acy = A[1] + ln["ay"] * A[3]
        if "by" in ln: bcy = B[1] + ln["by"] * B[3]
        pts = ln.get("via", [])
        first = pts[0] if pts else (bcx, bcy)
        last = pts[-1] if pts else (acx, acy)
        p0 = _clip(A[0] + A[2] / 2, A[1] + A[3] / 2, A[2], A[3], *first) if "ax" not in ln and "ay" not in ln else _edge(A, acx, acy, first)
        p1 = _clip(B[0] + B[2] / 2, B[1] + B[3] / 2, B[2], B[3], *last) if "bx" not in ln and "by" not in ln else _edge(B, bcx, bcy, last)
        allp = [p0] + list(pts) + [p1]
        kind = ln.get("kind", "assoc")
        # head at B end
        hx, hy = allp[-1]; qx, qy = allp[-2]
        L = math.hypot(hx - qx, hy - qy) or 1
        ux, uy = (hx - qx) / L, (hy - qy) / L
        mk = {"gen": "gen", "real": "real", "agg": "agg", "comp": "comp", "dep": "dep"}.get(kind, "nav" if ln.get("nav") else "")
        hs, back = _head(hx, hy, ux, uy, mk)
        lp = allp[:-1] + [(hx - ux * back, hy - uy * back)]
        dash = ' stroke-dasharray="6 4"' if kind in ("dep", "real") else ""
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.4"%s/>' % (
            " ".join("%.1f,%.1f" % p for p in lp), INK, dash))
        out.append(hs)
        # multiplicities
        def mult(text, end, nxt, side):
            if not text: return
            ex, ey = end; nx, ny = nxt
            L = math.hypot(nx - ex, ny - ey) or 1
            vx, vy = (nx - ex) / L, (ny - ey) / L
            off = ln.get("off", 1) * side
            along = 32 if (end == allp[-1] and mk in ("agg", "comp")) else 18
            tx = ex + vx * along + (-vy) * 15 * off
            ty = ey + vy * along + vx * 15 * off + 4
            out.append('<text x="%.1f" y="%.1f" font-size="12.5" text-anchor="middle" %s %s fill="#BF4A14" font-weight="700">%s</text>' % (tx, ty, FONT, HALO, esc(text)))
        mult(ln.get("ma"), allp[0], allp[1], 1)
        mult(ln.get("mb"), allp[-1], allp[-2], -1)
        if ln.get("label"):
            i = len(allp) // 2
            mx = (allp[i - 1][0] + allp[i][0]) / 2; my = (allp[i - 1][1] + allp[i][1]) / 2
            dx_, dy_ = ln.get("ldx", 0), ln.get("ldy", -6)
            out.append('<text x="%.1f" y="%.1f" font-size="12" text-anchor="middle" font-style="italic" fill="%s" %s>%s</text>' % (mx + dx_, my + dy_, MUT, HALO, esc(ln["label"])))
    for name, (x, y, w, h, c) in boxes.items():
        f, s = FILL[c.get("c", "w")]
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.4" rx="2"/>' % (x, y, w, h, f, s))
        ty = y + 18
        if c.get("stereo"):
            out.append('<text x="%.1f" y="%.1f" font-size="11.5" text-anchor="middle" %s fill="%s">«%s»</text>' % (x + w / 2, ty, FONT, MUT, esc(c["stereo"])))
            ty += 14
        style = ' font-style="italic"' if c.get("abstract") else ""
        out.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="700" text-anchor="middle" %s%s>%s</text>' % (x + w / 2, ty, FONT, style, esc(c["name"])))
        if c.get("compact"): continue
        y1 = ty + 8
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (x, y1, x + w, y1, s))
        yy = y1 + 15
        for a in c.get("attrs", []):
            out.append('<text x="%.1f" y="%.1f" font-size="12.5" %s>%s</text>' % (x + 8, yy, FONT, esc(a))); yy += 17
        if not c.get("attrs"): yy += 17
        y2 = yy - 9
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (x, y2, x + w, y2, s))
        yy = y2 + 15
        for o in c.get("ops", []):
            out.append('<text x="%.1f" y="%.1f" font-size="12.5" %s>%s</text>' % (x + 8, yy, FONT, esc(o))); yy += 17
    for t in d.get("notes", []):
        out.append('<text x="%s" y="%s" font-size="12" fill="%s">%s</text>' % (t[0], t[1], MUT, esc(t[2])))
    W, H = d["w"], d["h"]
    for name, (x, y, w, h, c) in boxes.items():
        W = max(W, x + w + 10); H = max(H, y + h + 10)
    return _wrap(out, W, H, d)

def _edge(B, px, py, toward):
    """anchor on given relative point of a box edge (px,py already absolute)."""
    return (px, py)

def _wrap(out, W, H, d):
    minw = d.get("minw", int(W) if W > 520 else 0)
    style = 'style="min-width:%dpx;max-width:%dpx"' % (minw, int(W) + 40) if minw else 'style="max-width:%dpx"' % (int(W) + 40)
    hint = '<div class="wl scrollhint">手機睇：圖可以左右捲 ⇆</div>' if minw else ''
    return '<div class="uml"><svg viewBox="0 0 %d %d" role="img" aria-label="%s" %s>%s</svg></div>%s' % (
        int(W), int(H), esc(d.get("alt", "UML diagram")), style, "".join(out), hint)

# ---------------- sequence diagrams ----------------
def seq_svg(d):
    P = d["parts"]; M = d["msgs"]
    dx = d.get("dx", 150); x0 = d.get("x0", 70); top = 14
    xs = [x0 + i * dx for i in range(len(P))]
    head_h = 34
    y = top + head_h + 50
    ys = []
    born = {}
    extra = {}
    for fr in d.get("frames", []):
        extra[fr["from"]] = extra.get(fr["from"], 0) + 18
        for el in fr.get("else", []): extra[el[0]] = extra.get(el[0], 0) + 18
    for k, m in enumerate(M):
        if m.get("gap"): y += m["gap"]
        y += extra.get(k, 0)
        ys.append(y)
        if m.get("create"): born[m["t"]] = y
        y += 44 if m["f"] == m["t"] else 34
    bottom = y + 10
    out = []
    ftxt = []
    # frames (draw first, behind)
    for fr in d.get("frames", []):
        i0, i1 = fr["from"], fr["to"]
        fx0 = xs[fr["p0"]] - fr.get("padl", 60); fx1 = xs[fr["p1"]] + fr.get("padr", 60)
        fy0 = ys[i0] - 36; fy1 = ys[i1] + (40 if M[i1]["f"] == M[i1]["t"] else 14) + fr.get("bpad", 0)
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.3"/>' % (fx0, fy0, fx1 - fx0, fy1 - fy0, "#8F6200"))
        tw = len(fr["k"]) * 8 + 14
        ftxt.append('<path d="M%d %d h%d v10 l-8 8 h-%d z" fill="#F6EBCB" stroke="#8F6200" stroke-width="1.3"/>' % (fx0, fy0, tw, tw - 8))
        ftxt.append('<text x="%d" y="%d" font-size="12" font-weight="700" %s fill="#8F6200">%s</text>' % (fx0 + 5, fy0 + 13, FONT, esc(fr["k"])))
        ftxt.append('<text x="%d" y="%d" font-size="12" %s %s fill="#8F6200">%s</text>' % (fx0 + tw + 6, fy0 + 13, FONT, HALO, esc(fr.get("g", ""))))
        for el in fr.get("else", []):
            ey = ys[el[0]] - 34
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#8F6200" stroke-width="1.2" stroke-dasharray="6 4"/>' % (fx0, ey, fx1, ey))
            ftxt.append('<text x="%d" y="%d" font-size="12" %s %s fill="#8F6200">%s</text>' % (fx0 + 6, ey + 13, FONT, HALO, esc(el[1])))
    # lifelines + heads
    for i, p in enumerate(P):
        x = xs[i]
        hy = born.get(i, None)
        y0 = (hy - 14) if hy is not None else top
        f, s = FILL[p.get("c", "y" if p.get("db") else ("o" if p.get("actor") else "w"))]
        name = p["n"]
        if p.get("actor"):
            out.append('<g stroke="%s" stroke-width="1.5" fill="none"><circle cx="%d" cy="%d" r="6" fill="%s"/><line x1="%d" y1="%d" x2="%d" y2="%d"/><line x1="%d" y1="%d" x2="%d" y2="%d"/><line x1="%d" y1="%d" x2="%d" y2="%d"/><line x1="%d" y1="%d" x2="%d" y2="%d"/></g>' % (
                s, x, y0 + 6, f, x, y0 + 12, x, y0 + 24, x - 9, y0 + 16, x + 9, y0 + 16, x, y0 + 24, x - 7, y0 + 33, x, y0 + 24, x + 7, y0 + 33))
            out.append('<text x="%d" y="%d" font-size="12.5" text-anchor="middle" font-weight="700" %s>%s</text>' % (x, y0 + 47, FONT, esc(name)))
            ly0 = y0 + 52
        else:
            w = max(len(name) * CW + 16, 70)
            out.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s" stroke="%s" stroke-width="1.4" rx="3"/>' % (x - w / 2, y0, w, head_h, f, s))
            out.append('<text x="%d" y="%d" font-size="12.5" text-anchor="middle" font-weight="700" %s text-decoration="underline">%s</text>' % (x, y0 + 22, FONT, esc(name)))
            ly0 = y0 + head_h
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2" stroke-dasharray="5 5"/>' % (x, ly0, x, bottom, MUT))
    # activations
    for a in d.get("act", []):
        i, m0, m1 = a
        ay0 = ys[m0]; ay1 = ys[m1] + (30 if M[m1]["f"] == M[m1]["t"] else 6)
        out.append('<rect x="%d" y="%d" width="10" height="%d" fill="#D9EFEE" stroke="#0B7472" stroke-width="1.1"/>' % (xs[i] - 5, ay0 - 4, ay1 - ay0 + 4))
    # messages
    for k, m in enumerate(M):
        y = ys[k]; a, b = xs[m["f"]], xs[m["t"]]
        ret = m.get("r"); dash = ' stroke-dasharray="6 4"' if ret or m.get("create") else ""
        if m["f"] == m["t"]:
            out.append('<polyline points="%d,%d %d,%d %d,%d %d,%d" fill="none" stroke="%s" stroke-width="1.4"/>' % (a + 5, y, a + 40, y, a + 40, y + 20, a + 12, y + 20, INK))
            out.append(_poly([(a + 5, y + 20), (a + 14, y + 15), (a + 14, y + 25)], INK, INK))
            out.append('<text x="%d" y="%d" font-size="12" %s %s>%s</text>' % (a + 46, y + 14, FONT, HALO, esc(m["l"])))
            continue
        dirn = 1 if b > a else -1
        sx = a + 5 * dirn; ex = b - 5 * dirn
        if m.get("create"):
            w = max(len(P[m["t"]]["n"]) * CW + 16, 70); ex = b - (w / 2) * dirn
        out.append('<line x1="%d" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"%s/>' % (sx, y, ex, y, INK, dash))
        if ret:
            out.append('<polyline points="%.1f,%d %.1f,%d %.1f,%d" fill="none" stroke="%s" stroke-width="1.4"/>' % (ex - 9 * dirn, y - 5, ex, y, ex - 9 * dirn, y + 5, INK))
        else:
            out.append(_poly([(ex, y), (ex - 10 * dirn, y - 5), (ex - 10 * dirn, y + 5)], INK, INK))
        lx = (sx + ex) / 2
        out.append('<text x="%.1f" y="%d" font-size="12" text-anchor="middle" %s %s%s>%s</text>' % (
            lx, y - 6, FONT, HALO, ' fill="%s"' % MUT if ret else "", esc(m["l"])))
    out.extend(ftxt)
    W = xs[-1] + d.get("padr", 80); H = bottom + 8
    return _wrap(out, W, H, d)

def render(d):
    return class_svg(d) if d["type"] == "class" else seq_svg(d)
