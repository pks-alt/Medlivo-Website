# Medlivo recovered source of truth

The canonical website files are the root HTML pages on main. The native main/root GitHub Pages publisher is the only deployment mechanism.
Historical previews, v2 copies, and other branches are retained for recovery only. Do not copy them to the live root without reviewing the manifest and the approved decisions.

## Preserved evening versions

- index.html: 19:58 PDT homepage V2, confirmed by FINAL_HOME_BUILD.md at 20:06. Source 874b820c1b81d9233bb02ddda9a331734646aaf8:index.html.
- workforce-solutions.html: 20:30 PDT polished Solutions, without repeated enterprise-program section. Source 62134bf75c62a5b5b53c2c36ac6f13fc8be1b4dc:workforce-solutions-preview/index.html.
- nursing-allied.html: Approved Nursing and Allied page with openings and final spacing pass. Source 794f81e033b74151d0c169185121bbcd500e8bb5:nursing-allied-preview/index.html.
- rehabilitation.html: Four editorial care-setting rows, combined post-acute and home-based care, openings. Source 038bc2a20b8dec869574edf12ca0fd7a9446f680:rehabilitation-preview.html.
- request-staff.html: 20:50 PDT dedicated request page aligned with final Medlivo design. Source 780d3fc3bd125e5d1aae1960ed23f340e8c80b39:request-staff.html.
- locum-tenens.html: Preserved supporting page; no new design changes. Source 8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9:v2/locum-tenens.html.
- search-jobs.html: Preserved supporting page; no new design changes. Source 8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9:v2/search-jobs.html.
- about.html: Preserved supporting page; no new design changes. Source 8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9:v2/about.html.
- leadership.html: Preserved supporting page; no new design changes. Source 8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9:v2/leadership.html.
- careers.html: Preserved supporting page; no new design changes. Source 8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9:v2/careers.html.
- specialties.html: Preserved supporting page; no new design changes. Source 8ad7bb331a03c987d0bcced4b2161dc90fd8f6f9:v2/specialties.html.

## Homepage decision record

FINAL_HOME_BUILD.md at commit 1e5ef83fb2de7ec506243c7c13567d45ce18c77e (20:06 PDT) identifies the homepage V2 handoff and the dedicated Request Staff page. Its order is Hero, Specialties, For Clinicians, For Healthcare Organizations with the integrated Request Staff CTA, Why Medlivo, Experience Behind Medlivo, Footer.
Do not restore the 19:36 homepage as final. That predates the 19:58 lower-half V2 redesign.
Do not reinsert Ready When You Are or Move forward with Medlivo.

## Verification and integration limits

BUILD.json records exact page hashes. A successful publish is not proof of the public page: compare live HTML with these hashes and capture the rendered pages.
The staffing form and job search are frontend handoff interfaces. Do not claim live ATS data or production lead delivery without testing the developer integrations.
No new photography, visual redesign, or copy changes beyond routing, preview-base cleanup and the requested punctuation cleanup are part of this recovery.
