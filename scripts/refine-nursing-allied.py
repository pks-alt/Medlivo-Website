"""Apply the reviewed Nursing & Allied changes without touching other pages."""
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import re, base64, io, hashlib, json

root = Path.cwd()
source = root / '.review/preview-original.html'
s = source.read_text()
expected = 'e89c99b5cfc704124b841caf8fb37b3e15c9521d'
blob = hashlib.sha1(b'blob ' + str(len(s.encode())).encode() + b'\0' + s.encode()).hexdigest()
assert blob == expected, f'Preview changed: {blob}; reconcile before applying.'
before_dom = BeautifulSoup(s, 'html.parser')
role_names = [e.get_text() for e in before_dom.select('.role-cloud span')]
jobs = before_dom.select_one('.open-positions').get_text(' ', strip=True)
s = re.sub(r'<base\b[^>]*>\s*', '', s)
# Retain the newer opportunities section and its styles; replace only obsolete correction layers.
a = s.index('/* === Nursing & Allied final cleanup === */')
b = s.index('/* === Open Nursing & Allied Positions === */', a)
s = s[:a] + s[b:]
s = s.replace('</style>', (root / 'scripts/nursing-allied-spacing.css').read_text() + '\n</style>', 1)
s = s.replace('From bedside nursing to diagnostic, procedural, and clinical support roles, Medlivo recruits around the specialty, setting, schedule, credentials, and timing that define the opening.', 'Travel and contract staffing across bedside nursing, diagnostics, procedures, and clinical support. We recruit to your specialty, setting, schedule, and start date.')
s = re.sub(r'\s*<div class="hero-signals">.*?</div>', '', s, flags=re.S)
s = re.sub(r'\s*<div class="stack-card stack-main">.*?</div>', '', s, flags=re.S)
s = s.replace('Care delivery roles shaped by unit, specialty, and shift.', 'Nursing, from bedside to leadership.')
s = s.replace('From bedside care to coordination and leadership, the right nursing profile depends on unit experience, specialty depth, schedule alignment, and start readiness.', 'Nurses and nursing support professionals for unit coverage, care coordination, and clinical leadership.')
s = s.replace('Technical and clinical support roles shaped by modality and environment.', 'Allied health, from diagnostics to procedures.')
s = s.replace('Allied staffing depends on technical specialization, procedure exposure, care setting, and role-specific credentials, not just general clinical experience.', 'Clinical and technical professionals across imaging, respiratory care, laboratory, surgical services, and pharmacy.')
s = s.replace('The work may happen under the same roof, but the experience, credentials, and recruiting signals are not the same.', 'From bedside care to specialized clinical services, each role calls for a different mix of experience and skills.')
s = s.replace('Our team builds the search around what will actually determine whether a clinician can step into the assignment successfully.', 'Before presenting a candidate, we check clinical experience, assignment fit, travel plans, and availability.')
a = s.index('<section class="signals"'); b = s.index('</section>', a)
part = s[a:b].replace('Schedule &amp; location', 'Shift &amp; assignment fit').replace('Shift, assignment structure, geography, travel expectations, and availability.', 'Shift, call expectations, assignment length, and schedule preferences.').replace('<h3>Credentials</h3>', '<h3>Location &amp; travel</h3>').replace('Licensure, certifications, documentation, and client-specific requirements.', 'The work location and the clinician’s ability to travel for the assignment.').replace('<h3>Start readiness</h3>', '<h3>Availability</h3>').replace('Whether the clinician can complete the required steps within the target timeline.', 'The proposed start date and the clinician’s availability for the full assignment.')
s = s[:a] + part + s[b:]
s = s.replace('From selection to first shift, the details still matter.', 'Ready for the first shift.')
s = re.sub(r'\s*<div class="ready-bar">.*?</div>', '', s, flags=re.S)
s = re.sub(r'\s*<div class="engage-fields">.*?</div>', '', s, flags=re.S)
s = s.replace('      <p class="lead">Healthcare organizations can request talent directly. Clinicians can search current Nursing & Allied opportunities.</p>\n', '')
# Use the exact licensed image already embedded in the approved homepage, not a substitute.
home = BeautifulSoup((root / 'index.html').read_text(), 'html.parser')
img = home.select_one('a.spec[href="nursing-allied.html"] img')
assert img and img['src'].startswith('data:image/webp;base64,')
data = base64.b64decode(img['src'].split(',', 1)[1]); Image.open(io.BytesIO(data)).load()
asset = root / 'assets/images/nursing-allied-approved.webp'
asset.parent.mkdir(parents=True, exist_ok=True); asset.write_bytes(data)
s = s.replace('src="assets/images/home/nursing-allied.webp"', 'src="assets/images/nursing-allied-approved.webp" width="1800" height="1200" fetchpriority="high" decoding="async"')
s = s.replace('<main>', '<main id="main-content">', 1)
s = s.replace('<nav class="links">', '<nav class="links" id="primary-navigation" aria-label="Main navigation">', 1)
s = s.replace('class="menu" type="button"', 'class="menu" aria-controls="primary-navigation" type="button"')
s = s.replace("menu.setAttribute('aria-expanded',String(open));", "menu.setAttribute('aria-expanded',String(open));\n    menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');")
s = s.replace("if(e.key==='Escape'){", "if(e.key==='Escape'){\n    if(links?.classList.contains('open')){links.classList.remove('open');menu?.setAttribute('aria-expanded','false');menu?.setAttribute('aria-label','Open navigation');if(menu){menu.textContent='☰';menu.focus();}}")
s = s.replace('<head>', '<head>\n<meta name="medlivo-build" content="nursing-allied-spacing-20260928">', 1)
dom = BeautifulSoup(s, 'html.parser')
assert role_names == [e.get_text() for e in dom.select('.role-cloud span')]
assert jobs == dom.select_one('.open-positions').get_text(' ', strip=True)
assert len(dom.select('h1')) == 1 and len(dom.select('main > section')) == 6
assert not dom.select('.stack-main,.hero-signals,.ready-bar,.engage-fields')
assert 'Ready When You Are' not in s
(root / 'nursing-allied.html').write_text(s)
# Resolve preview-relative assets directly, without a base tag that hijacks same-page anchors.
def route(m):
    attr, path = m.group(1), m.group(2)
    if path.startswith(('https:', 'http:', 'tel:', 'mailto:', '#', 'data:', '/')):
        return m.group(0)
    return f'{attr}="../{path}"'
preview = re.sub(r'(href|src)="([^"]+)"', route, s)
p = root / 'nursing-allied-preview/index.html'; p.parent.mkdir(exist_ok=True); p.write_text(preview)
manifest = {'source_preview_blob': blob, 'files': {}}
for name in ['nursing-allied.html', 'nursing-allied-preview/index.html', 'assets/images/nursing-allied-approved.webp']:
    raw = (root / name).read_bytes()
    manifest['files'][name] = {'blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(), 'bytes': len(raw)}
(root / '.review/manifest.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
