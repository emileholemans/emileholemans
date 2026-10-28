"""Renders the README images (hero, project cards, toolbox) in the portfolio's style.

Each image is made in a dark and a light version so the README can switch with
<picture>. Needs Google Chrome; fonts load from Google Fonts.

    python3 scripts/render.py
"""
import html
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "src"
OUT = ROOT / "assets" / "cards"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIDTH = 880

THEMES = {
    "dark": dict(bg="oklch(0.15 0.004 260)", fg="oklch(0.95 0.003 260)", muted="oklch(0.7 0.006 260)",
                 edge="oklch(0.95 0.003 260 / 0.12)", soft="oklch(0.95 0.003 260 / 0.05)",
                 btn_bg="oklch(0.95 0.003 260)", btn_fg="oklch(0.15 0.004 260)"),
    "light": dict(bg="oklch(0.985 0.002 260)", fg="oklch(0.18 0.004 260)", muted="oklch(0.45 0.006 260)",
                  edge="oklch(0.18 0.004 260 / 0.12)", soft="oklch(0.18 0.004 260 / 0.04)",
                  btn_bg="oklch(0.18 0.004 260)", btn_fg="oklch(0.985 0.002 260)"),
}

PROJECTS = [
    ("pathout", "01", "Evacuation system", "Pathout",
     ["three.js", "TypeScript", "Cloudflare Workers"],
     "Sends each person in the 35-floor IE Tower their best way out, and shows the warden who "
     "is not yet out, floor by floor. I lead core development.", True),
    ("deeptune", "02", "Music marketplace", "Deeptune",
     ["Next.js", "React", "three.js"],
     "A curated direct-to-fan marketplace with walkable 3D studio rooms. Artists keep the full "
     "listed price. Bachelor thesis, cum laude.", True),
    ("pylevels", "03", "Learning game", "PyLevels",
     ["Python", "JavaScript", "Game design", "AI tutor"],
     "Learn Python by typing real code, one level at a time, under the sea and in space, with an "
     "AI tutor that nudges without giving the answer away.", True),
    ("clipmonster", "04", "Video studio", "ClipMonster",
     ["Next.js", "TypeScript", "SQLite", "FFmpeg", "Local AI"],
     "Spots what is trending in a niche, turns it into a blueprint, produces an original video and "
     "queues it for YouTube. The heavy work stays on my laptop.", True),
    ("grainfield", "05", "Audio plugin", "Grainfield",
     ["Audio DSP", "Ableton Live", "Built with AI"],
     "A granular sampler for Ableton Live. Load a sample and watch grains rise off the waveform, "
     "in five colour themes.", True),
    ("boogi", "06", "Mobile app, internship", "Boogi",
     ["Flutter", "Mobile"],
     "Find gigs, book talent, get paid. I worked on the Flutter frontend during my internship.", False),
    ("mule", "07", "Web studio, co-founder", "Mule Digital",
     ["Web", "Brand", "SEO"],
     "Websites, brand and digital strategy for small and rural businesses. 20+ paid sites in "
     "Belgium, the Netherlands and the US.", False),
    ("experiments", "08", "Visuals and 3D", "Experiments",
     ["TouchDesigner", "Unity", "Blender", "Arduino"],
     "Particle systems, Unity worlds, a movie scene rebuilt, Arduino lamps. Questions I wanted "
     "to answer with my hands.", False),
]

# Honest on purpose: what I was trained in, what I am learning, and what I build with AI.
TOOLBOX = [
    ("Trained in", ["C#", "Unity", "Game development (KdG)"]),
    ("Learning", ["Python"]),
    ("Build with AI", ["React", "Next.js", "TypeScript", "three.js", "Flutter"]),
    ("Create", ["TouchDesigner", "Blender", "Ableton", "Arduino"]),
    ("Ship", ["Claude Code", "Cloudflare", "Vercel", "GitHub"]),
]

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=block');
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: %(w)dpx; background: %(bg)s; }
body { font-family: 'Archivo', sans-serif; color: %(fg)s; -webkit-font-smoothing: antialiased; }
.label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .16em;
         font-stretch: 112%%; color: %(muted)s; }
.display { font-stretch: 112%%; font-weight: 700; letter-spacing: -.035em; line-height: .95; }
.heading { font-stretch: 108%%; font-weight: 650; letter-spacing: -.02em; line-height: 1.08; }
.muted { color: %(muted)s; }
.pill { display: inline-flex; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 500;
        border: 1px solid %(edge)s; background: %(soft)s; margin: 0 6px 6px 0; }
.frame { border-radius: 14px; overflow: hidden; border: 1px solid %(edge)s; background: %(soft)s; padding: 6px; }
.frame img { display: block; width: 100%%; border-radius: 9px; }
"""


def page(body, theme, extra_css=""):
    css = BASE_CSS % dict(w=WIDTH, **THEMES[theme]) + extra_css % THEMES[theme]
    return f"<!doctype html><meta charset=utf-8><style>{css}</style><body>{body}</body>"


def hero(theme):
    return page(f"""
<div class="wrap">
  <div class="text">
    <p class="label">Product developer, Madrid</p>
    <h1 class="display">Emile Holemans</h1>
    <p class="muted intro">I build web, 3D and AI products, and I build them fast. Co-founder of
      Mule Digital and master's student in Computer Science and Digital Innovation at IE University.</p>
    <div class="btns"><span class="btn">See the work &rarr;</span><span class="ghost">Open to 2027 roles</span></div>
  </div>
</div>""", theme, """
.wrap { display: flex; align-items: center; padding: 44px 40px; height: 360px; }
.text { flex: 1; }
h1 { font-size: 78px; margin: 18px 0 22px; white-space: nowrap; }
.intro { font-size: 15.5px; line-height: 1.65; max-width: 62ch; }
.btns { margin-top: 26px; display: flex; gap: 10px; }
.btn, .ghost { border-radius: 999px; padding: 11px 20px; font-size: 13.5px; font-weight: 600; }
.btn { background: %(btn_bg)s; color: %(btn_fg)s; }
.ghost { border: 1px solid %(edge)s; background: %(soft)s; }
""")


def card(p, theme):
    key, num, kicker, title, tags, desc, private = p
    pills = "".join(f'<span class="pill">{html.escape(t)}</span>' for t in tags)
    lock = ('<p class="lock muted"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="4" y="11" width="16" '
            'height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Source private. Happy to walk '
            'through it.</p>') if private else ""
    return page(f"""
<div class="wrap">
  <div class="text">
    <p class="kick"><b>{num}</b><i></i><span class="muted">{html.escape(kicker)}</span></p>
    <h2 class="heading">{html.escape(title)}</h2>
    <div class="pills">{pills}</div>
    <p class="desc muted">{html.escape(desc)}</p>
    {lock}
  </div>
  <div class="frame shot"><img src="{(SRC / (key + '.jpg')).as_uri()}"></div>
</div>""", theme, """
.wrap { display: flex; gap: 36px; align-items: center; padding: 34px 40px; height: 340px;
        border-top: 1px solid %(edge)s; }
.text { width: 360px; flex: none; }
.kick { display: flex; align-items: center; gap: 12px; font-size: 14px; }
.kick b { font-weight: 600; font-stretch: 108%%; }
.kick i { width: 44px; height: 1px; background: %(edge)s; }
h2 { font-size: 40px; margin: 14px 0 16px; }
.desc { font-size: 14px; line-height: 1.6; margin-top: 8px; }
.lock { font-size: 12.5px; margin-top: 12px; display: flex; align-items: center; gap: 7px; }
.shot { flex: 1; }
.shot img { height: 250px; object-fit: cover; object-position: top; }
""")


def toolbox(theme):
    rows = "".join(
        f'<div class="row"><p class="label">{name}</p><div>'
        + "".join(f'<span class="pill">{html.escape(t)}</span>' for t in tools)
        + "</div></div>"
        for name, tools in TOOLBOX)
    return page(f'<div class="wrap"><p class="label head">Toolbox</p>{rows}</div>', theme, """
.wrap { padding: 34px 40px; height: 290px; border-top: 1px solid %(edge)s; }
.head { color: %(fg)s; margin-bottom: 22px; }
.row { display: flex; align-items: baseline; gap: 20px; margin-bottom: 10px; }
.row .label { width: 130px; flex: none; }
""")


def shoot(markup, name, height):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(markup)
    out = OUT / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={WIDTH},{height}", "--virtual-time-budget=8000",
                    "--allow-file-access-from-files", f"--screenshot={out}", f.name],
                   check=True, capture_output=True)
    pathlib.Path(f.name).unlink()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        shoot(hero(theme), f"hero-{theme}", 360)
        for p in PROJECTS:
            shoot(card(p, theme), f"{p[0]}-{theme}", 340)
        shoot(toolbox(theme), f"toolbox-{theme}", 290)


if __name__ == "__main__":
    main()
