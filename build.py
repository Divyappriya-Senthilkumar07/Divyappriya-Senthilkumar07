#!/usr/bin/env python3
"""
Cinematic GitHub profile generator.
Edit the CONFIG block, run `python3 build.py`, commit /assets and README.md.
Every asset is a self-contained SVG (no external requests), so it renders
on GitHub exactly as designed, animations included.
"""
import math, os, random

# ───────────────────────────── CONFIG ─────────────────────────────
NAME     = "Divyappriya Senthilkumar"
NAME_LINES = ["Divyappriya", "Senthilkumar"]     # banner shows the name on two lines
TAGLINE  = "sde in progress, ai/ml curious, founder arc loading"
HANDLE   = "Divyappriya-Senthilkumar07"

ABOUT_LINES = ["I'm learning to build things", "that work today and scale", "into whatever comes next."]
ABOUT_FACTS = [("now",    "levelling up for my first SDE role"),
               ("next",   "building my own company in tech"),
               ("ask me", "about react, node, nest and supabase")]

STACK = {
    "languages": ["Python", "Java", "C", "JavaScript"],
    "web":       ["React", "Node.js", "NestJS"],
    "data":      ["SQL", "PostgreSQL", "MongoDB", "Supabase"],
    "exploring": ["AI", "Machine learning", "Entrepreneurship"],
}

G = "https://github.com/Divyappriya-Senthilkumar07/"
PROJECTS = [
    ("Pre-headline",  ["Story formation intelligence and narrative", "provenance, tracing how stories take shape."], "python",       G + "pre-headline-intelligence"),
    ("Placement",     ["A Java web app for student placements:", "profiles, readiness and skill-gap analysis."],        "java · sql",   G + "PlacementSyStem"),
    ("Decision",      ["A tracker for logging and reviewing", "the decisions that shape a project."],                   "javascript",   G + "decision-tracker"),
    ("Discovery",     ["A TypeScript project in the works,", "more details soon."],                                      "typescript",   G + "discovery"),
]

LINKS = [("github", "https://github.com/Divyappriya-Senthilkumar07"),
         ("linkedin", "https://www.linkedin.com/in/divyappriya-senthilkumar-1a1272331/")]

PHILOSOPHY = ["ship, learn, repeat", "Curious by default. Building on purpose."]
# ──────────────────────────────────────────────────────────────────

PEARL, CHAMP, EMBER, ICE = "#f4efe6", "#e6cc9a", "#ff8a3d", "#a6d8ff"
SILVER, MUTE = "#c9ccd3", "#7e828c"
SANS = "'Inter Display','Inter','SF Pro Display','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT): os.remove(os.path.join(OUT, _f))

def lerp(a, b, t): return a + (b - a) * t

def head(W, H, css=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
            '<style>@media (prefers-reduced-motion:reduce){*{animation:none!important}}'
            '.s{font-family:%s}.m{font-family:%s}%s</style>' % (W, H, W, H, SANS, MONO, css))

SHARED_DEFS = f'''
<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#ffffff"/><stop offset=".42" stop-color="#dfe1e6"/>
 <stop offset=".5" stop-color="#6f737d"/><stop offset=".62" stop-color="#cfcac2"/>
 <stop offset=".85" stop-color="#f1ede6"/><stop offset="1" stop-color="#9a9ea8"/>
</linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="{PEARL}" stop-opacity="0"/><stop offset=".5" stop-color="{PEARL}" stop-opacity=".55"/>
 <stop offset="1" stop-color="{PEARL}" stop-opacity="0"/>
</linearGradient>
<filter id="b1" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation=".9"/></filter>
<filter id="b2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="b6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b16" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/>
 <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 -.18"/>
</filter>
<filter id="tglow" x="-20%" y="-50%" width="140%" height="200%">
 <feGaussianBlur in="SourceGraphic" stdDeviation="9" result="g"/>
 <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
'''

def pixels(rng, x0, x1, y0, y1, cell, density, fill=SILVER, flick=0.08, maxop=.4):
    """Pixel-dissolve texture. density(x,y)->0..1 probability."""
    out = []
    y = y0
    while y < y1:
        x = x0
        while x < x1:
            p = density(x, y)
            if rng.random() < p:
                op = rng.uniform(.06, maxop) * (0.4 + 0.6 * p)
                size = cell - 2
                anim = ''
                if rng.random() < flick:
                    anim = ' style="animation:fl %.1fs ease-in-out %.1fs infinite"' % (rng.uniform(2.5, 6), -rng.uniform(0, 6))
                out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f"%s/>' % (x, y, size, size, fill, op, anim))
            x += cell
        y += cell
    return ''.join(out)

FLICKER = '@keyframes fl{0%,100%{opacity:.04}50%{opacity:.7}}'

def particles(rng, n, W, H, cy, spread):
    cols = [PEARL, PEARL, CHAMP, ICE, EMBER]
    out = []
    for _ in range(n):
        x = rng.uniform(0, W)
        y = min(H - 4, max(4, rng.gauss(cy, spread)))
        r = rng.choice([.5, .6, .8, 1, 1.3, 1.8]) * (1 if rng.random() > .08 else 1.8)
        c = rng.choice(cols)
        op = rng.uniform(.15, .95)
        out.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f" style="animation:tw %.1fs ease-in-out %.1fs infinite"/>'
                   % (x, y, r, c, op, rng.uniform(3, 9), -rng.uniform(0, 9)))
    return ''.join(out)

TWINKLE = '@keyframes tw{0%,100%{opacity:.08}50%{opacity:1}}'

def bundle(p0, p3, c1a, c1b, c2a, c2b, n, s0, s3, rng, wmax=1.5):
    out = []
    for i in range(n):
        u = i / (n - 1)
        y0 = p0[1] + (u - .5) * s0
        y3 = p3[1] + (u - .5) * s3
        c1 = (lerp(c1a[0], c1b[0], u), lerp(c1a[1], c1b[1], u))
        c2 = (lerp(c2a[0], c2b[0], u), lerp(c2a[1], c2b[1], u))
        d = 'M%d,%.1f C%.0f,%.1f %.0f,%.1f %d,%.1f' % (p0[0], y0, c1[0], c1[1], c2[0], c2[1], p3[0], y3)
        op = .18 + .72 * math.sin(u * math.pi) ** 1.3
        w = .45 + (wmax - .45) * rng.random() ** 2
        out.append((d, w, op))
    return out

def lg(id, W, stops):
    s = ''.join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % st for st in stops)
    return '<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%d" y2="0">%s</linearGradient>' % (id, W, s)

def trails(gid, rng, x0, x1, y, amp, n, w=.9, comet=True, comet_dur=7):
    """Small flowing-light motif used across sections. Returns (defs, body)."""
    defs = lg(gid, x1, [(0, PEARL, 0), (x0 / x1 if x1 else 0, PEARL, 0), (.35, CHAMP, .9), (.6, PEARL, 1), (.82, ICE, .7), (1, EMBER, 0)])
    paths = []
    for i in range(n):
        u = i / max(1, n - 1)
        yy = y + (u - .5) * amp * .5
        d = 'M%d,%.1f C%.0f,%.1f %.0f,%.1f %d,%.1f' % (x0, yy, lerp(x0, x1, .3), yy - amp * (.9 - u * 1.2), lerp(x0, x1, .65), yy + amp * (.8 - u * 1.4), x1 + 40, yy + (u - .5) * amp * .3)
        paths.append('<path d="%s" stroke="url(#%s)" stroke-width="%.2f" opacity="%.2f" fill="none"/>' % (d, gid, w * (.6 + rng.random() * .8), .35 + .6 * math.sin(u * math.pi)))
    body = '<g stroke-linecap="round">%s</g>' % ''.join(paths)
    body = '<g filter="url(#b6)" opacity=".8">%s</g>%s' % (body, body)
    if comet:
        mid = paths[n // 2]
        d = mid.split('d="')[1].split('"')[0]
        body += ('<path d="%s" pathLength="2000" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round" '
                 'stroke-dasharray="90 1910" style="animation:cm %ds linear infinite" filter="url(#b2)"/>' % (d, comet_dur))
    return defs, body

COMET = '@keyframes cm{from{stroke-dashoffset:2000}to{stroke-dashoffset:0}}'

def write(name, svg):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg)

# ───────────────────────────── BANNER ─────────────────────────────
import re
def bez(d):
    n = [float(x) for x in re.findall(r'-?\d+\.?\d*', d)][:8]
    return n

def dust(lines_all, rng, count):
    out = []
    for _ in range(count):
        d = rng.choice(lines_all)[0]
        x0, y0, x1, y1, x2, y2, x3, y3 = bez(d)
        t = min(1, max(0, rng.betavariate(2.2, 2.2)))
        mt = 1 - t
        x = mt**3*x0 + 3*mt*mt*t*x1 + 3*mt*t*t*x2 + t**3*x3
        y = mt**3*y0 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t**3*y3
        dx = 3*mt*mt*(x1-x0) + 6*mt*t*(x2-x1) + 3*t*t*(x3-x2)
        dy = 3*mt*mt*(y1-y0) + 6*mt*t*(y2-y1) + 3*t*t*(y3-y2)
        L = math.hypot(dx, dy) or 1
        off = rng.gauss(0, 15)
        px, py = x - dy / L * off, y + dx / L * off
        if not (0 <= px <= 1600 and 0 <= py <= 640): continue
        r = rng.choice([.4, .5, .6, .8, 1.0, 1.3])
        c = rng.choice([PEARL, PEARL, PEARL, CHAMP, ICE, '#ffd2a8'])
        an = ''
        if rng.random() < .18:
            an = ' style="animation:tw %.1fs ease-in-out %.1fs infinite"' % (rng.uniform(3, 8), -rng.uniform(0, 8))
        out.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"%s/>' % (px, py, r, c, rng.uniform(.25, .95), an))
    return ''.join(out)

def banner():
    W, H = 1600, 640
    rng = random.Random(11)
    A = bundle((-80, 540), (1680, 70), (320, 40), (560, 640), (980, 700), (1180, 110), 58, 30, 10, rng)
    B = bundle((-80, 90), (1680, 540), (350, 610), (320, 290), (1000, -70), (1160, 320), 54, 30, 12, rng)
    C = bundle((-80, 330), (1680, 250), (520, -50), (610, 520), (1100, 640), (1190, 50), 30, 12, 8, rng, wmax=1)
    D = bundle((-80, 600), (1680, 380), (500, 380), (620, 120), (1000, 200), (1100, 560), 26, 10, 30, rng, wmax=1)

    def grp(lines, g):
        return ''.join('<path d="%s" stroke="url(#%s)" stroke-width="%.2f" opacity="%.2f"/>' % (d, g, w, o) for d, w, o in lines)
    streams = ('<g id="streams" fill="none" stroke-linecap="round">%s%s%s%s</g>' % (grp(A, 'gA'), grp(B, 'gB'), grp(C, 'gC'), grp(D, 'gD')))

    # bold luminous blades: broken segments of light, like long-exposure streaks
    blade_paths = ''
    bl = [(A, 1, 4), (B, 0, 4), (C, 1, 4), (D, 0, 4)]
    for lines, off, step in bl:
        for i in range(off, len(lines), step):
            d = lines[i][0]
            u = i / (len(lines) - 1)
            w = (.9 + 2.6 * rng.random() ** 2.0) * (.55 + .8 * math.sin(u * math.pi))
            segs = [rng.randint(20, 240) if k % 2 == 0 else rng.randint(60, 420) for k in range(8)]
            S = sum(segs); dur = rng.randint(16, 30)
            blade_paths += ('<path d="%s" pathLength="2000" stroke-width="%.1f" stroke-dasharray="%s" style="--s:-%d;animation:bf %ds linear %ds infinite"/>'
                            % (d, w, ' '.join(map(str, segs)), S, dur, -rng.randint(0, dur)))
    blades = '<g id="blades" fill="none" stroke-linecap="round">%s</g>' % blade_paths

    comets = ''
    for k, (lines, idx, dur, col) in enumerate([(A, 22, 9, '#fff'), (B, 30, 11, '#fff'), (A, 40, 13, CHAMP), (B, 14, 8, ICE), (C, 12, 10, '#fff'), (D, 9, 12, CHAMP)]):
        comets += ('<path d="%s" pathLength="2000" stroke="%s" stroke-width="2" fill="none" stroke-linecap="round" '
                   'stroke-dasharray="140 1860" style="animation:cm %ds linear %ds infinite"/>' % (lines[idx][0], col, dur, -k * 2))

    svg = head(W, H, TWINKLE + COMET + FLICKER + '@keyframes bf{from{stroke-dashoffset:0}to{stroke-dashoffset:var(--s)}}@keyframes pu{0%,100%{opacity:.75}50%{opacity:1}}@keyframes rise{from{opacity:0}to{opacity:1}}.ti{animation:rise 2.6s ease-out both}')
    svg += '<defs>' + SHARED_DEFS
    svg += lg('gA', W, [(0, ICE, 0), (.1, ICE, .6), (.38, PEARL, .95), (.62, CHAMP, 1), (.86, EMBER, .85), (1, EMBER, 0)])
    svg += lg('gB', W, [(0, EMBER, 0), (.16, EMBER, .7), (.42, CHAMP, 1), (.66, PEARL, 1), (.88, ICE, .65), (1, ICE, 0)])
    svg += lg('gC', W, [(0, PEARL, 0), (.3, PEARL, .8), (.58, ICE, .95), (.84, PEARL, .9), (1, PEARL, 0)])
    svg += lg('gD', W, [(0, CHAMP, 0), (.25, CHAMP, .7), (.55, EMBER, .9), (.8, CHAMP, .8), (1, PEARL, 0)])
    svg += lg('fT', W, [(0, '#2fe8cc', 0), (.4, '#2fe8cc', 0), (.56, '#2fe8cc', 1), (.9, '#2fe8cc', .8), (1, '#2fe8cc', 0)])
    svg += lg('fV', W, [(0, '#a66bff', 0), (.4, '#a66bff', 0), (.56, '#a66bff', 1), (.9, '#a66bff', .8), (1, '#a66bff', 0)])
    svg += lg('gH', W, [(0, '#fff', 0), (.3, '#fff', 0), (.46, ICE, .55), (.58, '#fff', .95), (.72, '#ffe9cc', .9), (.86, '#ffb06a', .7), (1, EMBER, 0)])
    svg += """<radialGradient id="bg" cx=".66" cy=".5" r=".75"><stop offset="0" stop-color="#17110a"/><stop offset=".45" stop-color="#08080b"/><stop offset="1" stop-color="#010102"/></radialGradient>
<radialGradient id="flare" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".16" stop-color="%s" stop-opacity=".6"/><stop offset=".45" stop-color="%s" stop-opacity=".16"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>
<linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".86"/><stop offset=".38" stop-color="#000" stop-opacity=".55"/><stop offset=".64" stop-color="#000" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".72"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".88"/></radialGradient>
<linearGradient id="streak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>
<linearGradient id="prism" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".14" stop-color="#2fe0c4"/><stop offset=".3" stop-color="#7a5cff"/><stop offset=".47" stop-color="#fff"/><stop offset=".6" stop-color="#ffb870"/><stop offset=".8" stop-color="#ff5a5a"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="ht" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="1.9" fill="#cfe6ff"/></pattern>
<linearGradient id="hv" gradientUnits="userSpaceOnUse" x1="0" y1="%d" x2="0" y2="%d"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="hw" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="300" y2="110" spreadMethod="repeat"><stop offset="0" stop-color="#000"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="hm1"><rect width="%d" height="%d" fill="url(#hv)"/></mask><mask id="hm2"><rect width="%d" height="%d" fill="url(#hw)"/></mask>
""" % (CHAMP, EMBER, EMBER, ICE, EMBER, H - 150, H, W, H, W, H)
    svg += streams + blades + '</defs>'
    svg += '<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H)
    svg += '<use href="#streams" transform="translate(-130,-60) scale(1.12)" filter="url(#b16)" opacity=".42" style="mix-blend-mode:screen"/>'
    svg += '<use href="#streams" transform="translate(70,40) scale(.94)" filter="url(#b6)" opacity=".28" style="mix-blend-mode:screen"/>'
    svg += '<use href="#streams" filter="url(#b6)" opacity=".8" style="mix-blend-mode:screen"/>'
    svg += '<use href="#streams" style="mix-blend-mode:screen"/>'
    # blades: orange bloom, chromatic fringes (teal / violet), white-hot core
    svg += '<use href="#blades" stroke="%s" filter="url(#b16)" opacity=".45" style="mix-blend-mode:screen"/>' % EMBER
    svg += '<use href="#blades" stroke="url(#fT)" transform="translate(0,-5)" filter="url(#b1)" opacity=".38" style="mix-blend-mode:screen"/>'
    svg += '<use href="#blades" stroke="url(#fV)" transform="translate(0,5)" filter="url(#b1)" opacity=".38" style="mix-blend-mode:screen"/>'
    svg += '<use href="#blades" stroke="url(#gH)" filter="url(#b6)" opacity=".4" style="mix-blend-mode:screen"/>'
    svg += '<use href="#blades" stroke="url(#gH)" filter="url(#b1)" opacity=".7" style="mix-blend-mode:screen"/>'
    svg += '<g style="mix-blend-mode:screen">' + comets + '</g>'
    svg += '<g filter="url(#b2)" style="mix-blend-mode:screen">' + comets + '</g>'
    svg += '<ellipse cx="1040" cy="318" rx="300" ry="180" fill="url(#flare)" opacity=".8" style="animation:pu 6s ease-in-out infinite;mix-blend-mode:screen"/>'
    svg += '<rect x="380" y="315" width="1280" height="5" fill="url(#prism)" opacity=".55" filter="url(#b6)" style="mix-blend-mode:screen"/>'
    svg += '<rect x="420" y="316" width="1240" height="3" fill="url(#streak)" filter="url(#b2)" style="mix-blend-mode:screen"/>'
    svg += '<rect x="640" y="317" width="800" height="1" fill="url(#streak)" opacity=".9"/>'
    # glitter dust hugging the streams, plus ambient particles
    svg += dust(A + B + C + D, random.Random(15), 560)
    svg += particles(random.Random(3), 90, W, H, 320, 190)
    svg += '<rect width="%d" height="%d" fill="url(#shade)"/>' % (W, H)
    # halftone dot-matrix waves along the base + a few pixel cells on the right
    svg += '<g mask="url(#hm1)" opacity=".55"><rect width="%d" height="%d" fill="url(#ht)" mask="url(#hm2)"/></g>' % (W, H)
    rngp = random.Random(5)
    def dens2(x, y): return max(0, (x - 1450) / 150.0) ** 1.4 * .4 * max(0, 1 - abs(y - 330) / 320.0)
    svg += pixels(rngp, 1450, W, 20, H - 80, 10, dens2, fill=PEARL, flick=.12)
    svg += '<rect width="%d" height="%d" filter="url(#grain)" opacity=".5" style="mix-blend-mode:overlay"/>' % (W, H)
    svg += '<rect width="%d" height="%d" fill="url(#vig)"/>' % (W, H)
    l1, l2 = NAME_LINES
    svg += ('<g class="ti"><text x="116" y="276" class="s" font-size="66" font-weight="200" letter-spacing="15" fill="url(#chrome)" filter="url(#tglow)">%s</text>'
            '<text x="116" y="352" class="s" font-size="66" font-weight="200" letter-spacing="15" fill="url(#chrome)" filter="url(#tglow)">%s</text>'
            '<rect x="120" y="386" width="64" height="1" fill="%s"/>'
            '<text x="118" y="430" class="s" font-size="17" font-weight="300" letter-spacing="5" fill="%s">%s</text></g>'
            % (l1, l2, CHAMP, SILVER, TAGLINE))
    svg += '</svg>'
    write('banner.svg', svg)

# ───────────────────────────── SECTION HEADERS ─────────────────────────────
def header(fname, title, seed):
    W, H = 1600, 150
    rng = random.Random(seed)
    size, track = 46, 15
    tw = len(title) * (size * .54 + track)
    x0 = int(60 + tw + 60)
    d, body = trails('hg', rng, x0, W, 78, 52, 9, comet_dur=6 + seed % 4)
    def dens(x, y): return max(0, (x - 1360) / 240.0) ** 1.3 * .55 * max(0, 1 - abs(y - 78) / 70.0)
    pix = pixels(rng, 1360, W, 8, H - 8, 10, dens, flick=.15)
    svg = head(W, H, COMET + FLICKER)
    svg += '<defs>' + SHARED_DEFS + d + '</defs><rect width="%d" height="%d" fill="#030304"/>' % (W, H)
    svg += '<rect width="%d" height="1" fill="url(#hair)" opacity=".5"/>' % W
    svg += body + pix
    svg += '<text x="60" y="92" class="s" font-size="%d" font-weight="200" letter-spacing="%d" fill="url(#chrome)">%s</text>' % (size, track, title)
    svg += '</svg>'
    write(fname, svg)

# ───────────────────────────── ABOUT ─────────────────────────────
def about():
    W, H = 1600, 430
    rng = random.Random(21)
    d, body = trails('ag', rng, 60, W, 372, 70, 11, comet_dur=9)
    svg = head(W, H, COMET + FLICKER + TWINKLE)
    svg += '<defs>' + SHARED_DEFS + d + '<radialGradient id="ab" cx=".15" cy=".3" r=".9"><stop offset="0" stop-color="#14120f"/><stop offset="1" stop-color="#030304"/></radialGradient></defs>'
    svg += '<rect width="%d" height="%d" fill="url(#ab)"/>' % (W, H) + body
    for i, ln in enumerate(ABOUT_LINES):
        svg += '<text x="60" y="%d" class="s" font-size="58" font-weight="200" letter-spacing="1.5" fill="url(#chrome)">%s</text>' % (92 + i * 74, ln)
    for i, (k, v) in enumerate(ABOUT_FACTS):
        y = 110 + i * 70
        svg += ('<text x="1010" y="%d" class="m" font-size="14" letter-spacing="3" fill="%s">%s</text>'
                '<text x="1010" y="%d" class="s" font-size="21" font-weight="300" letter-spacing="1" fill="%s">%s</text>'
                '<rect x="1010" y="%d" width="520" height="1" fill="url(#hair)" opacity=".5"/>' % (y - 26, CHAMP, k, y + 4, SILVER, v, y + 26))
    svg += particles(random.Random(8), 60, W, H, 300, 90) + '</svg>'
    write('about.svg', svg)

# ───────────────────────────── LIQUID CHROME PANEL ─────────────────────────────
def chrome():
    W, H = 1600, 580
    rng = random.Random(33)
    svg = head(W, H, FLICKER + TWINKLE + '@keyframes drift{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}.dr{animation:drift 9s ease-in-out infinite}')
    svg += '<defs>' + SHARED_DEFS
    svg += '''<radialGradient id="cb" cx=".68" cy=".5" r=".8"><stop offset="0" stop-color="#15151a"/><stop offset=".5" stop-color="#07070a"/><stop offset="1" stop-color="#010102"/></radialGradient>
<radialGradient id="warm" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="%s" stop-opacity=".35"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>
<radialGradient id="cool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="%s" stop-opacity=".22"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>
<linearGradient id="shade2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".9"/><stop offset=".4" stop-color="#000" stop-opacity=".4"/><stop offset=".6" stop-color="#000" stop-opacity="0"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="liquid" x="-10%%" y="-30%%" width="120%%" height="160%%" color-interpolation-filters="sRGB">
 <feGaussianBlur in="SourceGraphic" stdDeviation="13" result="b"/>
 <feColorMatrix in="b" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 30 -13" result="goo"/>
 <feGaussianBlur in="goo" stdDeviation="7" result="h"/>
 <feDiffuseLighting in="h" surfaceScale="9" diffuseConstant=".85" lighting-color="#c3c7d2" result="df"><feDistantLight azimuth="215" elevation="30"/></feDiffuseLighting>
 <feSpecularLighting in="h" surfaceScale="9" specularConstant="2.2" specularExponent="34" lighting-color="#ffffff" result="s1"><fePointLight x="760" y="-60" z="260"/></feSpecularLighting>
 <feSpecularLighting in="h" surfaceScale="9" specularConstant="1.2" specularExponent="22" lighting-color="%s" result="s2"><fePointLight x="1500" y="700" z="170"/></feSpecularLighting>
 <feSpecularLighting in="h" surfaceScale="9" specularConstant="1.0" specularExponent="24" lighting-color="%s" result="s3"><fePointLight x="1480" y="-80" z="200"/></feSpecularLighting>
 <feComposite in="df" in2="s1" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="m1"/>
 <feComposite in="m1" in2="s2" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="m2"/>
 <feComposite in="m2" in2="s3" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="m3"/>
 <feComponentTransfer in="m3" result="m4"><feFuncR type="gamma" exponent="1.9" amplitude="2.0"/><feFuncG type="gamma" exponent="1.9" amplitude="2.0"/><feFuncB type="gamma" exponent="1.8" amplitude="2.1"/></feComponentTransfer>
 <feComposite in="m4" in2="goo" operator="in"/>
</filter>''' % (EMBER, EMBER, ICE, ICE, EMBER, ICE)
    shapes = ('<g fill="#fff">'
              '<ellipse cx="1030" cy="300" rx="350" ry="104" transform="rotate(-17 1030 300)" fill="none" stroke="#fff" stroke-width="58"/>'
              '<circle cx="1018" cy="298" r="66"/>'
              '<circle cx="1328" cy="190" r="30"/><circle cx="1388" cy="226" r="15"/><circle cx="1442" cy="248" r="7"/>'
              '<circle cx="560" cy="448" r="30"/><circle cx="516" cy="478" r="14"/>'
              '<circle cx="1180" cy="470" r="22"/><circle cx="1230" cy="498" r="9"/>'
              '<circle cx="860" cy="150" r="20"/></g>')
    svg += '''<pattern id="ht" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="2.2" fill="#cfe6ff"/></pattern>
<radialGradient id="rings" gradientUnits="userSpaceOnUse" cx="1250" cy="300" r="105" spreadMethod="repeat"><stop offset="0" stop-color="#000"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<linearGradient id="hf" gradientUnits="userSpaceOnUse" x1="620" y1="0" x2="1120" y2="0"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="mr"><rect width="1600" height="580" fill="url(#rings)"/></mask><mask id="mf"><rect width="1600" height="580" fill="url(#hf)"/></mask>
<linearGradient id="prism" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".14" stop-color="#2fe0c4"/><stop offset=".3" stop-color="#7a5cff"/><stop offset=".47" stop-color="#fff"/><stop offset=".6" stop-color="#ffb870"/><stop offset=".8" stop-color="#ff5a5a"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'''
    svg += '</defs><rect width="%d" height="%d" fill="url(#cb)"/>' % (W, H)
    svg += '<g mask="url(#mf)" opacity=".32"><rect width="1600" height="580" fill="url(#ht)" mask="url(#mr)"/></g>'
    svg += '<ellipse cx="1180" cy="520" rx="560" ry="60" fill="url(#warm)"/><ellipse cx="1160" cy="60" rx="520" ry="90" fill="url(#cool)"/>'
    # floor reflection
    svg += '<g transform="translate(0,1150) scale(1,-1)" opacity=".28" class="dr"><g filter="url(#liquid)">%s</g></g>' % shapes
    svg += '<rect x="0" y="548" width="%d" height="32" fill="#030304" opacity=".85"/>' % W
    svg += '<rect x="0" y="548" width="%d" height="1" fill="url(#hair)"/>' % W
    svg += '<g class="dr"><g filter="url(#liquid)">%s</g></g>' % shapes
    # prismatic lens flare on the chrome highlights
    svg += '<g style="mix-blend-mode:screen"><rect x="520" y="396" width="560" height="6" fill="url(#prism)" filter="url(#b6)" opacity=".9"/><rect x="560" y="398" width="480" height="2" fill="url(#prism)"/>'
    svg += '<rect x="1180" y="168" width="360" height="4" fill="url(#prism)" filter="url(#b6)" opacity=".7"/><rect x="1210" y="169" width="300" height="1.5" fill="url(#prism)" opacity=".9"/></g>'
    # digital dissolution: pixels echoing the form
    prng = random.Random(9)
    def dens(x, y):
        dx, dy = (x - 1030) / 520.0, (y - 300) / 200.0
        r = math.hypot(dx, dy)
        edge = max(0, 1 - abs(r - 1.0) * 2.2)
        side = max(0, (x - 1250) / 350.0)
        return edge * .16 * (0.3 + side) + (0.10 if 1400 < x < 1600 and 120 < y < 460 and prng.random() < .5 else 0) * side
    svg += pixels(prng, 520, W, 30, 540, 12, dens, fill=PEARL, flick=.12, maxop=.55)
    svg += particles(random.Random(2), 90, W, H, 300, 150)
    svg += '<rect width="%d" height="%d" fill="url(#shade2)"/>' % (W, H)
    svg += '<rect width="%d" height="%d" filter="url(#grain)" opacity=".45" style="mix-blend-mode:overlay"/>' % (W, H)
    svg += ('<text x="60" y="276" class="s" font-size="58" font-weight="200" letter-spacing="8" fill="url(#chrome)" filter="url(#tglow)">%s</text>'
            '<rect x="64" y="308" width="64" height="1" fill="%s"/>'
            '<text x="62" y="352" class="s" font-size="19" font-weight="300" letter-spacing="2.5" fill="%s">%s</text></svg>' % (PHILOSOPHY[0], CHAMP, SILVER, PHILOSOPHY[1]))
    write('signal.svg', svg)

# ───────────────────────────── STACK ─────────────────────────────
def stack():
    n = max(len(v) for v in STACK.values())
    th = 174 + n * 50
    W, H = 1600, th + 60
    svg = head(W, H, COMET + FLICKER)
    rng = random.Random(44)
    defs = ''
    body = ''
    cols = len(STACK)
    gap, mx = 40, 20
    tile_w = (W - 2 * mx - gap * (cols - 1)) // cols
    for i, (cat, items) in enumerate(STACK.items()):
        x = mx + i * (tile_w + gap)
        d, tr = trails('sg%d' % i, rng, x + 10, x + tile_w - 10, 66, 26, 5, w=.8, comet_dur=7 + i)
        defs += d
        defs += ('<linearGradient id="tb%d" gradientUnits="userSpaceOnUse" x1="%d" y1="30" x2="%d" y2="%d"><stop offset="0" stop-color="%s" stop-opacity=".7"/><stop offset=".5" stop-color="%s" stop-opacity=".12"/><stop offset="1" stop-color="%s" stop-opacity=".45"/></linearGradient>' % (i, x, x + tile_w, th + 30, [ICE, CHAMP, PEARL, EMBER][i % 4], PEARL, [CHAMP, EMBER, ICE, CHAMP][i % 4]))
        body += '<rect x="%d" y="30" width="%d" height="%d" fill="#08080b" stroke="url(#tb%d)" stroke-width="1"/>' % (x, tile_w, th, i)
        body += tr
        body += '<text x="%d" y="128" class="s" font-size="30" font-weight="200" letter-spacing="7" fill="url(#chrome)">%s</text>' % (x + 36, cat)
        body += '<rect x="%d" y="150" width="%d" height="1" fill="url(#hair)" opacity=".6"/>' % (x + 36, tile_w - 72)
        for j, it in enumerate(items):
            y = 204 + j * 50
            body += ('<rect x="%d" y="%d" width="5" height="5" fill="%s"/>'
                     '<text x="%d" y="%d" class="s" font-size="21" font-weight="300" letter-spacing="1.6" fill="%s">%s</text>' % (x + 36, y - 13, CHAMP, x + 58, y, SILVER, it))
        def dens(px, py, x=x): return max(0, (px - (x + tile_w - 70)) / 70.0) * max(0, (py - (th - 70)) / 100.0) * .8
        body += pixels(rng, x + tile_w - 80, x + tile_w - 2, th - 60, th + 28, 8, dens, flick=.2)
    svg += '<defs>' + SHARED_DEFS + defs + '</defs><rect width="%d" height="%d" fill="#030304"/>' % (W, H) + body + '</svg>'
    write('stack.svg', svg)

# ───────────────────────────── PROJECT CARDS ─────────────────────────────
def cards():
    for i, (title, desc, tags, _url) in enumerate(PROJECTS):
        W, H = 800, 300
        rng = random.Random(100 + i)
        d, tr = trails('pg', rng, 500, W, 120, 80 + i * 8, 10, w=.9, comet_dur=6 + i)
        svg = head(W, H, COMET + FLICKER + TWINKLE)
        svg += '<defs>' + SHARED_DEFS + d
        svg += '<linearGradient id="cbd" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%d" y2="%d"><stop offset="0" stop-color="%s" stop-opacity=".75"/><stop offset=".55" stop-color="%s" stop-opacity=".1"/><stop offset="1" stop-color="%s" stop-opacity=".6"/></linearGradient>' % (W, H, [ICE, CHAMP, PEARL, EMBER][i], PEARL, [CHAMP, EMBER, ICE, CHAMP][i])
        svg += '<radialGradient id="cbg" cx=".85" cy=".4" r=".9"><stop offset="0" stop-color="#17140f"/><stop offset="1" stop-color="#050507"/></radialGradient></defs>'
        svg += '<rect x="1" y="1" width="%d" height="%d" fill="url(#cbg)" stroke="url(#cbd)"/>' % (W - 2, H - 2) + tr
        svg += particles(random.Random(i), 26, W, H, 150, 60)
        svg += '<text x="44" y="112" class="s" font-size="40" font-weight="200" letter-spacing="7" fill="url(#chrome)">%s</text>' % title
        svg += '<rect x="46" y="136" width="48" height="1" fill="%s"/>' % CHAMP
        for k, ln in enumerate(desc):
            svg += '<text x="44" y="%d" class="s" font-size="16" font-weight="300" letter-spacing=".8" fill="%s">%s</text>' % (180 + k * 28, SILVER, ln)
        svg += '<text x="44" y="258" class="m" font-size="13" letter-spacing="2.5" fill="%s">%s</text>' % (CHAMP, tags)
        def dens(x, y): return max(0, (x - 700) / 100.0) * max(0, (y - 190) / 100.0) * .9
        svg += pixels(rng, 690, W - 4, 190, H - 4, 8, dens, flick=.2) + '</svg>'
        write('card-%d.svg' % (i + 1), svg)

# ───────────────────────────── CONNECT PILLS ─────────────────────────────
def pills():
    for i, (label, _u) in enumerate(LINKS):
        W, H = 420, 84
        svg = head(W, H, '@keyframes dot{0%,100%{opacity:.3}50%{opacity:1}}')
        svg += '<defs>' + SHARED_DEFS
        svg += '<linearGradient id="pb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s" stop-opacity=".8"/><stop offset=".5" stop-color="%s" stop-opacity=".15"/><stop offset="1" stop-color="%s" stop-opacity=".8"/></linearGradient>' % (ICE, PEARL, EMBER)
        svg += '<linearGradient id="pf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#101014"/><stop offset="1" stop-color="#08080a"/></linearGradient></defs>'
        svg += '<rect x="1" y="1" width="%d" height="%d" rx="42" fill="url(#pf)" stroke="url(#pb)"/>' % (W - 2, H - 2)
        svg += '<circle cx="46" cy="42" r="4" fill="%s" style="animation:dot 3s ease-in-out %ds infinite" filter="url(#tglow)"/>' % (CHAMP, -i)
        svg += '<text x="76" y="49" class="s" font-size="19" font-weight="300" letter-spacing="7" fill="url(#chrome)">%s</text></svg>' % label
        write('link-%d.svg' % (i + 1), svg)

# ───────────────────────────── FOOTER ─────────────────────────────
def footer():
    W, H = 1600, 280
    rng = random.Random(77)
    d, body = trails('fg', rng, 0, W, 100, 110, 16, comet_dur=10)
    def dens(x, y): return max(0, (y - 200) / 80.0) ** 1.4 * .55 * (0.5 + 0.5 * math.sin(x / 70.0) ** 2)
    pix = pixels(rng, 0, W, 190, H, 10, dens, flick=.1)
    svg = head(W, H, COMET + FLICKER + TWINKLE)
    svg += '<defs>' + SHARED_DEFS + d + '<radialGradient id="fv" cx=".5" cy=".5" r=".7"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient></defs>'
    svg += '<rect width="%d" height="%d" fill="#030304"/>' % (W, H) + body
    svg += particles(random.Random(6), 80, W, H, 130, 70) + pix
    svg += '<rect width="%d" height="%d" filter="url(#grain)" opacity=".4" style="mix-blend-mode:overlay"/><rect width="%d" height="%d" fill="url(#fv)"/>' % (W, H, W, H)
    svg += '<text x="800" y="212" text-anchor="middle" class="s" font-size="26" font-weight="200" letter-spacing="12" fill="url(#chrome)" filter="url(#tglow)">%s</text></svg>' % NAME
    write('footer.svg', svg)

# ───────────────────────────── README ─────────────────────────────
def readme():
    img = lambda f, alt, w='100%': '<img src="assets/%s" width="%s" alt="%s"/>' % (f, w, alt)
    cards_html = ''
    for i, (t, d, tg, u) in enumerate(PROJECTS):
        cards_html += '<a href="%s">%s</a>\n' % (u, img('card-%d.svg' % (i + 1), '%s: %s %s' % (t, ' '.join(d), tg), '49%'))
    pills_html = ''.join('<a href="%s">%s</a>\n' % (u, img('link-%d.svg' % (i + 1), l, {1:'60%',2:'42%',3:'31%'}[len(LINKS)])) for i, (l, u) in enumerate(LINKS))
    md = f'''<div align="center">

{img('banner.svg', NAME + ': ' + TAGLINE)}

{img('h-about.svg', 'about')}
{img('about.svg', ' '.join(ABOUT_LINES))}

{img('h-signal.svg', 'signal')}
{img('signal.svg', PHILOSOPHY[0] + '. ' + PHILOSOPHY[1])}

{img('h-craft.svg', 'craft')}
{img('stack.svg', 'Tech stack: ' + '; '.join('%s: %s' % (k, ', '.join(v)) for k, v in STACK.items()))}

{img('h-work.svg', 'selected work')}

{cards_html}
{img('h-connect.svg', 'connect')}

{pills_html}
{img('footer.svg', NAME)}

</div>
'''
    with open(os.path.join(os.path.dirname(OUT), 'README.md'), 'w') as f:
        f.write(md)

if __name__ == '__main__':
    banner()
    header('h-about.svg', 'about', 3)
    header('h-signal.svg', 'signal', 4)
    header('h-craft.svg', 'craft', 5)
    header('h-work.svg', 'selected work', 6)
    header('h-connect.svg', 'connect', 7)
    about(); chrome(); stack(); cards(); pills(); footer(); readme()
    print('built', len(os.listdir(OUT)), 'assets')
