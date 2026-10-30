"""Build only public site content. No network calls or filesystem deletion."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse, html, json, os, re, shutil
import markdown

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--output",default="dist",help="New or empty output directory; default relative to repository root")
args=parser.parse_args()
OUT=Path(args.output)
if not OUT.is_absolute(): OUT=ROOT/OUT
OUT=OUT.resolve()
if OUT==ROOT or ROOT in OUT.parents and OUT.parts[len(ROOT.parts):][0] in ("docs","updates","technical-baseline","scripts","evidence"):
    raise SystemExit("Refusing an output path over source content")
if OUT.exists() and any(OUT.iterdir()): raise SystemExit("Output must be new or empty; preserve prior build")
OUT.mkdir(parents=True,exist_ok=True)
def write(rel,content):
    target=OUT/rel
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(content,encoding="utf-8")
def rewrite_links(content):
    return re.sub(r'(href=["\'])([^"\']+?)(["\'])',lambda m:m[1]+re.sub(r"\.md(?=$|#)",".html",m[2])+m[3],content)
def page(title,body,relpath):
    prefix="../"*len(Path(relpath).parent.parts)
    escaped=html.escape(title)
    return f'''<!doctype html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escaped} · SMR Safety Thailand</title>
<meta name="description" content="ความรู้ SMR safety ภาษาไทย พร้อมที่มาและข้อจำกัดของหลักฐาน">
<link rel="stylesheet" href="{prefix}styles.css"><link rel="stylesheet" href="{prefix}article.css"></head>
<body><a class="skip" href="#article">ข้ามไปเนื้อหา</a>
<header class="site-header"><a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>SMR Safety<span class="brand-small">THAILAND · เล่าเรื่องนิวเคลียร์ให้เข้าใจ</span></span></a>
<nav aria-label="เมนูหลัก"><a href="{prefix}index.html#explain">เริ่มเข้าใจ</a><a href="{prefix}index.html#designs">รู้จักแบบเตา</a><a href="{prefix}docs/iaea-infrastructure.html">IAEA &amp; ไทย</a><a href="{prefix}updates/index.html">ตามข่าว</a></nav></header>
<main id="article" class="article-shell"><a class="article-back" href="{prefix}index.html">← กลับหน้าแรก</a>
<article class="article-content">{body}</article>
<div class="article-end"><p>อ่านแล้วมีคำถามต่อ เป็นเรื่องปกติ กลับไปดูแหล่งอ้างอิงและเงื่อนไขของข้อมูลได้</p><a href="{prefix}evidence/index.html">ดูแหล่งอ้างอิงทั้งหมด →</a></div></main>
<footer class="wrap page-footer"><span>SMR SAFETY THAILAND</span><span>ดูแลส่วนบุคคล · ไม่ใช่ช่องทางทางการของ สทน.</span></footer></body></html>'''
source_registers=[ROOT/"evidence/public-sources.json",ROOT/"technical-baseline/evidence/sources.json"]
sources=[]
for registry in source_registers: sources.extend(json.loads(registry.read_text(encoding="utf-8"))["sources"])
source_ids={s["id"] for s in sources}
def refs(body,prefix):
    return re.sub(r"\[([PS]\d{2})\]",lambda m:f'<a class="source-ref" href="{prefix}evidence/index.html#{m[1]}">[{m[1]}]</a>' if m[1] in source_ids else m[0],body)

assets=["styles.css","article.css","measurement.js","app.js"]
for asset in assets:
    text=(ROOT/asset).read_text(encoding="utf-8")
    if asset=="app.js": text=re.sub(r"\.md(?=[\"'])",".html",text)
    write(asset,text)
home=(ROOT/"index.html").read_text(encoding="utf-8")
home=rewrite_links(home)
home=home.replace('href="evidence/public-sources.json"','href="evidence/index.html"')
write("index.html",home)
md_files=[ROOT/"README.md",ROOT/"CONTRIBUTING.md",ROOT/"STYLE_GUIDE.md"]
for folder in ("docs","updates","templates","technical-baseline"):
    md_files.extend(sorted((ROOT/folder).rglob("*.md")))
for source in md_files:
    raw=source.read_text(encoding="utf-8")
    title_match=re.search(r"(?m)^#\s+(.+)",raw)
    title=title_match[1] if title_match else source.stem
    body=markdown.markdown(raw,extensions=["tables","fenced_code","sane_lists","toc"],output_format="html5")
    rel=source.relative_to(ROOT).with_suffix(".html")
    prefix="../"*len(rel.parent.parts)
    body=refs(rewrite_links(body),prefix)
    write(rel,page(title,body,rel))
for folder in ("evidence","technical-baseline/evidence"):
    for source in (ROOT/folder).glob("*.json"):
        target=OUT/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
source_body='<h1>แหล่งข้อมูลที่ใช้</h1><p>แหล่งอ้างอิงพร้อมวันที่ ขอบเขตการอ่าน และข้อจำกัด แยกข้ออ้างผู้พัฒนาออกจากผลประเมินของเรา</p>'
for source in sources:
    identifier=source["id"]; title=html.escape(source["title"])
    org=html.escape(source.get("organization",source.get("author","")))
    date=html.escape(str(source.get("publication_date",source.get("date")) or "ไม่ระบุวันที่"))
    url=html.escape(source["url"],quote=True)
    locator=html.escape(source.get("locator",""))
    access=html.escape(source.get("access",""))
    limit=html.escape(source.get("limits",""))
    source_body+=f'<section class="source-entry" id="{identifier}"><span class="source-id">{identifier}</span><h2>{title}</h2><p>{org} · {date}</p><p>{locator}</p><p>{access}</p><p class="small">{limit}</p><a href="{url}" target="_blank" rel="noopener">เปิดแหล่งต้นทาง ↗</a></section>'
write("evidence/index.html",page("แหล่งข้อมูลที่ใช้",source_body,Path("evidence/index.html")))
write("404.html",page("ยังไม่พบหน้านี้",'<h1>หน้านี้อาจเปลี่ยนที่อยู่</h1><p>ลองกลับหน้าแรกแล้วเลือกเรื่องที่อยากอ่านอีกครั้ง</p>',Path("404.html")))
write("robots.txt","User-agent: *\nAllow: /\n")
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.append(a["id"])
        if tag=="a" and a.get("href"):self.links.append(a["href"])
        if tag in ("script","link","img"):
            url=a.get("src") or a.get("href")
            if url:self.links.append(url)
parsers={}
for built in OUT.rglob("*.html"):
    doc=Links();doc.feed(built.read_text(encoding="utf-8"));parsers[built.resolve()]=doc
    if len(doc.ids)!=len(set(doc.ids)):raise SystemExit(f"Duplicate ids in {built.relative_to(OUT)}")
broken=[]
for built,doc in parsers.items():
    for url in doc.links:
        parts=urlsplit(url)
        if parts.scheme or parts.netloc:continue
        path=unquote(parts.path)
        target=(OUT/path.lstrip("/")) if path.startswith("/") else (built.parent/path if path else built)
        target=target.resolve()
        if target.is_dir():target=target/"index.html"
        if not target.is_file():broken.append(f"{built.relative_to(OUT)} -> {url}")
        elif parts.fragment and target in parsers and parts.fragment not in parsers[target].ids:broken.append(f"Missing anchor: {url}")
if broken:raise SystemExit("\n".join(broken))
# JS-created profile links are checked separately, since not present in static home markup.
for profile in re.findall(r'profile:"([^"]+)"',(OUT/"app.js").read_text(encoding="utf-8")):
    if not (OUT/profile).is_file():raise SystemExit(f"Missing design profile {profile}")
receipt={"result":"Pass","markdown_pages":len(md_files),"html_pages":len(parsers),"sources":len(sources),"broken_links":0,"design_profiles":5,"network_calls_in_builder":0}
write("build-manifest.json",json.dumps(receipt,ensure_ascii=False,indent=2))
print(json.dumps(receipt))

