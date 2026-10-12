"""Portfolio V2 — direction A prototype (gallery + one page per project).

Reads project copy and image lists from the live site (public/index.html) so the
prototype never drifts from the real content, then writes index.html and
p/<slug>.html next to this file. Images are referenced from ../../public.

    py -3.11 prototypes/v2-a/build.py
    npx http-server . -p 5242      # from the repo root, then open /prototypes/v2-a/
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LIVE = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
ASSET = "../../public/"  # from prototypes/v2-a/

# Facts the live site doesn't carry. Role lines come from the 2026 CV; the rest is
# left out rather than guessed.
EXTRA = {
    "gratis": {"category": "event", "label": "Müşteri · Yeni yorum 2026",
               "kicker": "Gratis", "title": "Harikalar Diyarı",
               "sub": "Deneyim odaklı etkinlik tasarımı · Marka dünyası",
               "idea": "Ziyaretçiyi karşılamadan keşfe, atölyelerden ana sahneye taşıyan Harikalar Diyarı temalı bir etkinlik deneyimi.",
               "ai": True},
    "wynn": {"role": "Konsept, alan tasarımı, 3D modelleme, görselleştirme ve proje sunumu."},
}
CATEGORY = {"dum": "interior"}  # everything else is event / exhibition
LABEL_DEFAULT = "Müşteri için tasarım"  # built or not is unverified per project


def tr_copy():
    block = LIVE[LIVE.find("tr: {", LIVE.find("const projectCopy")):]
    block = block[: block.find("}") + 1]
    out = {}
    for m in re.finditer(r"'project-(\w+)':\[(.*?)\]", block):
        out[m.group(1)] = re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(2))
    return out


def images():
    out = {}
    for m in re.finditer(r'<article class="case[^"]*" id="project-(\w+)"(.*?)</article>', LIVE, re.S):
        out[m.group(1)] = re.findall(r'src="((?:selected_work_final|gratis_final)/desktop/[^"]+)"', m.group(2))
    return out


def projects():
    copy, imgs, order = tr_copy(), images(), []
    for slug, files in imgs.items():
        if slug in copy:
            kicker, title, sub, idea, _ = copy[slug]
            p = {"kicker": kicker, "title": title, "sub": sub, "idea": idea}
        else:
            p = {}
        p.update(EXTRA.get(slug, {}))
        p.setdefault("category", CATEGORY.get(slug, "event"))
        p.setdefault("label", LABEL_DEFAULT)
        p["slug"], p["images"] = slug, files
        order.append(p)
    return order


def pic(path, alt, sizes, lazy=True, w=2048, h=1152):
    mobile = path.replace("/desktop/", "/mobile/").rsplit(".", 1)[0] + ".webp"
    have_mobile = (ROOT / "public" / mobile).exists()
    srcset = f' srcset="{ASSET}{mobile} 1280w, {ASSET}{path} 2048w" sizes="{sizes}"' if have_mobile else ""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return (f'<img src="{ASSET}{path}"{srcset} alt="{html.escape(alt)}" '
            f'width="{w}" height="{h}"{load}>')


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&display=swap');
:root{--ink:#0d0a08;--ink-2:#17110e;--paper:#f1e9df;--muted:#b3a698;--line:rgba(241,233,223,.14);--accent:#c7a679;
--serif:"Cormorant Garamond",Georgia,serif;--sans:Inter,system-ui,sans-serif;--edge:clamp(16px,4vw,48px)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ink);color:var(--paper);font:400 1rem/1.6 var(--sans)}
a{color:inherit}img{display:block;max-width:100%;height:auto}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.bar{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;gap:16px;
 padding:0 var(--edge);height:60px;background:rgba(13,10,8,.92);border-bottom:1px solid var(--line)}
.brand{font:600 .78rem/1 var(--sans);letter-spacing:.28em;text-decoration:none;min-height:44px;display:flex;align-items:center}
.bar nav{display:flex;gap:2px}.bar nav a{font-size:.85rem;color:var(--muted);text-decoration:none;padding:12px 10px;min-height:44px;display:inline-flex;align-items:center}
.bar nav a:hover,.bar nav a[aria-current]{color:var(--paper)}
.eyebrow{font:500 .7rem/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin:0}
h1,h2,h3{font-family:var(--serif);font-weight:400;margin:0;line-height:1.05}
.intro{padding:32px var(--edge) 24px;display:grid;gap:18px;max-width:1100px}
.intro h1{font-size:clamp(2rem,3.4vw,3.25rem);max-width:22ch}
.intro p{margin:0;color:var(--muted);max-width:56ch}
.filters{display:flex;flex-wrap:wrap;gap:8px;padding:0 var(--edge) 24px}
.filters button{min-height:44px;padding:0 16px;border:1px solid var(--line);background:none;color:var(--muted);font:500 .85rem/1 var(--sans);cursor:pointer}
.filters button[aria-pressed=true]{border-color:var(--accent);color:var(--paper)}
.grid{display:grid;grid-template-columns:1fr;gap:24px;padding:0 var(--edge) 64px}
@media (min-width:761px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1200px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card{text-decoration:none;display:grid;gap:12px}
.card .frame{overflow:hidden;background:var(--ink-2);aspect-ratio:16/10}
.card img{width:100%;height:100%;object-fit:cover;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.card:hover img{transform:scale(1.03)}
.card h2{font-size:1.4rem}
.card .meta{display:grid;gap:6px;color:var(--muted);font-size:.85rem}
.tag{font-size:.75rem;letter-spacing:.04em;color:var(--accent);white-space:normal}
.card[hidden]{display:none}
.hero{position:relative}
.hero img{width:100%;height:auto}
.back{display:inline-flex;align-items:center;min-height:44px;padding:0 var(--edge);color:var(--muted);text-decoration:none;font-size:.85rem}.back:hover{color:var(--paper)}
.head{padding:clamp(28px,5vw,64px) var(--edge);display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:24px 6vw;border-bottom:1px solid var(--line)}
.head h1{font-size:clamp(2.4rem,5.5vw,4.4rem);margin-top:10px}
.head .idea{font-family:var(--serif);font-style:italic;font-size:clamp(1.25rem,2vw,1.6rem);color:var(--paper);margin:0}
.facts{margin:0;display:grid;gap:14px;align-content:start}
.facts dt{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.facts dd{margin:4px 0 0}
.shots{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:clamp(10px,1.4vw,20px);padding:clamp(28px,5vw,64px) var(--edge)}
.shots figure{margin:0;grid-column:span 6}.shots figure:nth-child(3n+1){grid-column:1/-1}
.pager{display:flex;justify-content:space-between;gap:16px;padding:32px var(--edge) 80px;border-top:1px solid var(--line)}
.pager a{text-decoration:none;min-height:44px;display:grid;gap:4px}
.pager a span{font-family:var(--serif);font-size:1.4rem}
@media (max-width:760px){.head{grid-template-columns:1fr}.shots figure,.shots figure:nth-child(3n+1){grid-column:1/-1}.bar nav a.hide-sm{display:none}}
@media (prefers-reduced-motion:reduce){.card img{transition:none}.card:hover img{transform:none}}
"""

FILTERS = [("all", "Tümü"), ("event", "Mekân & Etkinlik"), ("interior", "İç mekân"), ("ai", "AI ile geliştirilen")]


def page(title, body, depth):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="robots" content="noindex">
<style>{CSS}</style></head><body>
<header class="bar"><a class="brand" href="{up}index.html">TEMİZ STUDIO</a>
<nav aria-label="Ana menü"><a href="{up}index.html" aria-current="page">İşler</a><a class="hide-sm" href="https://tmzstudios.com/">Giriş filmi</a><a href="mailto:suleyman@tmzstudios.com">İletişim</a></nav></header>
{body}
<script>
// Back to the index keeps the filter the visitor picked (it lives in the index URL).
(() => {{
  const r = document.referrer;
  if (!r || !/\\/index\\.html|\\/v2-a\\/(\\?|$)/.test(r)) return;
  document.querySelectorAll('a[data-index]').forEach(a => a.href = r);
}})();
</script>
</body></html>"""


def build():
    ps = projects()
    (HERE / "p").mkdir(exist_ok=True)
    cards = []
    for p in ps:
        cats = [p["category"]] + (["ai"] if p.get("ai") else [])
        cards.append(f"""<a class="card" href="p/{p['slug']}.html" data-cat="{' '.join(cats)}">
<div class="frame">{pic(p['images'][0], p['kicker'] + ' — ' + p['title'], '(min-width: 760px) 33vw, 100vw')}</div>
<div><p class="eyebrow">{html.escape(p['kicker'])}</p><h2>{html.escape(p['title'])}</h2></div>
<div class="meta"><span>{html.escape(p['sub'])}</span><span class="tag">{html.escape(p['label'])}</span></div></a>""")
    buttons = "".join(f'<button type="button" data-f="{k}" aria-pressed="{str(k == "all").lower()}">{v}</button>' for k, v in FILTERS)
    index_body = f"""<main>
<section class="intro"><p class="eyebrow">Etkinlik · Sahne · Stand</p>
<h1>Marka fikirlerini insanların içinde dolaştığı mekânlara dönüştürüyorum.</h1>
<p>Etkinlik alanları, sahneler ve fuar standları: konseptten 3D görselleştirmeye ve sunuma kadar.</p></section>
<div class="filters" role="group" aria-label="İşleri süz">{buttons}</div>
<section class="grid" aria-label="İşler">{''.join(cards)}</section></main>
<script>
(() => {{
  const btns = [...document.querySelectorAll('.filters button')], cards = [...document.querySelectorAll('.card')];
  const apply = (f) => {{
    btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.f === f)));
    cards.forEach(c => c.hidden = f !== 'all' && !c.dataset.cat.split(' ').includes(f));
  }};
  const fromUrl = () => new URLSearchParams(location.search).get('f') || 'all';
  btns.forEach(b => b.addEventListener('click', () => {{
    const u = new URL(location); u.searchParams.set('f', b.dataset.f); history.replaceState(null, '', u); apply(b.dataset.f);
  }}));
  apply(fromUrl());
}})();
</script>"""
    (HERE / "index.html").write_text(page("TEMİZ STUDIO — İşler", index_body, 0), encoding="utf-8")

    for i, p in enumerate(ps):
        prev_p, next_p = ps[i - 1], ps[(i + 1) % len(ps)]
        shots = "".join(f"<figure>{pic(f, p['title'], '(min-width: 760px) 50vw, 100vw').replace(ASSET, '../' + ASSET)}</figure>" for f in p["images"][1:])
        facts = f"<div><dt>Tür</dt><dd>{html.escape(p['sub'])}</dd></div><div><dt>Statü</dt><dd>{html.escape(p['label'])}</dd></div>"
        if p.get("role"):
            facts += f"<div><dt>Katkım</dt><dd>{html.escape(p['role'])}</dd></div>"
        body = f"""<main>
<a class="back" href="../index.html" data-index>← İşlere dön</a>
<div class="hero">{pic(p['images'][0], p['kicker'] + ' — ' + p['title'], '100vw', lazy=False).replace(ASSET, '../' + ASSET)}</div>
<section class="head"><div><p class="eyebrow">{html.escape(p['kicker'])}</p><h1>{html.escape(p['title'])}</h1></div>
<div><p class="idea">{html.escape(p['idea'])}</p></div>
<dl class="facts">{facts}</dl></section>
{f'<section class="shots" aria-label="Görseller">{shots}</section>' if shots else ''}
<nav class="pager" aria-label="Projeler arası"><a href="{prev_p['slug']}.html"><small class="eyebrow">Önceki</small><span>{html.escape(prev_p['title'])}</span></a>
<a href="../index.html" data-index><small class="eyebrow">Tüm işler</small><span>İndeks</span></a>
<a href="{next_p['slug']}.html" style="text-align:right"><small class="eyebrow">Sonraki</small><span>{html.escape(next_p['title'])}</span></a></nav></main>"""
        (HERE / "p" / f"{p['slug']}.html").write_text(page(f"{p['title']} — TEMİZ STUDIO", body, 1), encoding="utf-8")
    (HERE / "projects.json").write_text(json.dumps(ps, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(ps)} projects -> index.html + p/*.html")


if __name__ == "__main__":
    build()
