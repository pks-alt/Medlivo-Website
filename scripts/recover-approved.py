"""Recover preserved page versions. Does not deploy or modify remote refs."""
from pathlib import Path
import subprocess
import re
import json
import hashlib
from bs4 import BeautifulSoup

SOURCES = {
    'index.html': ('874b820c1b81d9233bb02ddda9a331734646aaf8', 'index.html', '19:58 PDT homepage V2, confirmed by FINAL_HOME_BUILD.md at 20:06'),
    'workforce-solutions.html': ('62134bf75c62a5b5b53c2c36ac6f13fc8be1b4dc', 'workforce-solutions-preview/index.html', '20:30 PDT polished Solutions, without repeated enterprise-program section'),
    'nursing-allied.html': ('794f81e033b74151d0c169185121bbcd500e8bb5', 'nursing-allied-preview/index.html', 'Approved Nursing and Allied page with openings and final spacing pass'),
    'rehabilitation.html': ('038bc2a20b8dec869574edf12ca0fd7a9446f680', 'rehabilitation-preview.html', 'Four editorial care-setting rows, combined post-acute and home-based care, openings'),
    'request-staff.html': ('780d3fc3bd125e5d1aae1960ed23f340e8c80b39', 'request-staff.html', '20:50 PDT dedicated request page aligned with final Medlivo design'),
}
BASE = '8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9'
for name in ['locum-tenens.html','search-jobs.html','about.html','leadership.html','careers.html','specialties.html']:
    SOURCES[name] = (BASE, 'v2/'+name, 'Preserved supporting page; no new design changes')

def read_version(ref, path):
    return subprocess.check_output(['git','show',ref+':'+path]).decode('utf-8')

def normalize(text):
    # Root pages resolve their own fragments and assets. A preview base tag breaks page anchors.
    text = re.sub(r'<base\b[^>]*>\s*', '', text, flags=re.I)
    text = text.replace('href="v2/', 'href="').replace("href='v2/", "href='")
    text = text.replace('action="v2/', 'action="').replace("action='v2/", "action='")
    text = text.replace('href="./"','href="index.html"')
    text = text.replace('href="https://www.medlivo.com/search-jobs','href="search-jobs.html')
    text = text.replace('href="mailto:hello@medlivo.com?subject=Healthcare%20Staffing%20Request"','href="request-staff.html"')
    # Follow the user's punctuation requirement without touching base64 image data.
    text = re.sub(r'\s*\u2014\s*', ', ', text)
    text = text.replace('Tenens,with','Tenens, with').replace('Tenens,not','Tenens, not').replace('nationwide,with','nationwide, with').replace('credentials,not','credentials, not')
    # Old cache-meta edits introduced literal backslash-n sequences in the head.
    head_end = text.find('</head>')
    text = text[:head_end].replace('>\\n<','>\n<') + text[head_end:]
    return text

manifest = {'build_id':'medlivo-recovered-20260927','source_policy':'Canonical root HTML. One native main/root GitHub Pages publisher. Preview and v2 folders are not deployment inputs.','pages':{}}
for name,(ref,path,note) in SOURCES.items():
    original = read_version(ref,path)
    text = normalize(original)
    Path(name).write_text(text,encoding='utf-8')
    manifest['pages'][name]={'commit':ref,'path':path,'selection':note,'sha256':hashlib.sha256(text.encode()).hexdigest()}

home = BeautifulSoup(Path('index.html').read_text(),'html.parser')
assert not home.select('.closing-cta'), 'Repeated closing CTA returned'
assert 'Ready When You Are' not in home.get_text(), 'Repeated Ready When You Are copy returned'
assert home.select('.workforce-v2') and home.select('.why-v2') and home.select('.heritage-v2'), 'V1 homepage selected'
classes = [' '.join(s.get('class',[])) for s in home.select('main > section')]
assert classes == ['hero home-hero-premium','specialties','careers','workforce-section workforce-v2','why-section why-v2','heritage heritage-v2'], classes
assert home.select('.workforce-v2-cta a[href="request-staff.html"]'), 'Homepage request path missing'
solutions=BeautifulSoup(Path('workforce-solutions.html').read_text(),'html.parser')
assert solutions.h1.get_text(' ',strip=True)=='Healthcare staffing built to fit the way you operate.'
assert not solutions.select('section.programs'), 'Old repeated program section returned'
nursing=BeautifulSoup(Path('nursing-allied.html').read_text(),'html.parser')
assert nursing.select_one('#open-positions')
assert nursing.h1.get_text(' ',strip=True)=='Nursing & Allied staffing built around the realities of the role.'
rehab=BeautifulSoup(Path('rehabilitation.html').read_text(),'html.parser')
settings=[x.get_text(' ',strip=True) for x in rehab.select('.care-settings .setting-card h3')]
assert settings==['Acute & Inpatient','Inpatient Rehabilitation','Post-Acute & Home-Based Care','Outpatient'],settings
assert rehab.select('.rehab-positions') and rehab.select('.therapist-proof')
request=BeautifulSoup(Path('request-staff.html').read_text(),'html.parser')
assert request.select_one('#staffingRequestForm'), 'Dedicated staffing request form missing'
for name in SOURCES:
    text=Path(name).read_text()
    assert '\u2014' not in text, name+' has em dash'
    assert 'href="v2/' not in text, name+' links to duplicate source tree'
    soup=BeautifulSoup(text,'html.parser')
    assert soup.select_one('h1') is not None, name+' lacks h1'

Path('.nojekyll').touch()
Path('BUILD.json').write_text(json.dumps(manifest,indent=2)+'\n')
rows=['# Medlivo recovered source of truth','',
      'The canonical website files are the root HTML pages on main. The native main/root GitHub Pages publisher is the only deployment mechanism.',
      'Historical previews, v2 copies, and other branches are retained for recovery only. Do not copy them to the live root without reviewing the manifest and the approved decisions.',
      '', '## Preserved evening versions','']
for name,item in manifest['pages'].items():
    rows.append('- '+name+': '+item['selection']+'. Source '+item['commit']+':'+item['path']+'.')
rows += ['', '## Homepage decision record', '',
         'FINAL_HOME_BUILD.md at commit 1e5ef83fb2de7ec506243c7c13567d45ce18c77e (20:06 PDT) identifies the homepage V2 handoff and the dedicated Request Staff page. Its order is Hero, Specialties, For Clinicians, For Healthcare Organizations with the integrated Request Staff CTA, Why Medlivo, Experience Behind Medlivo, Footer.',
         'Do not restore the 19:36 homepage as final. That predates the 19:58 lower-half V2 redesign.',
         'Do not reinsert Ready When You Are or Move forward with Medlivo.',
         '', '## Verification and integration limits', '',
         'BUILD.json records exact page hashes. A successful publish is not proof of the public page: compare live HTML with these hashes and capture the rendered pages.',
         'The staffing form and job search are frontend handoff interfaces. Do not claim live ATS data or production lead delivery without testing the developer integrations.',
         'No new photography, visual redesign, or copy changes beyond routing, preview-base cleanup and the requested punctuation cleanup are part of this recovery.']
Path('SITE_SOURCE.md').write_text('\n'.join(rows)+'\n')
print(json.dumps({'build_id':manifest['build_id'],'pages':list(SOURCES),'home_sections':classes,'rehab_settings':settings,'regressions':'passed'},indent=2))
