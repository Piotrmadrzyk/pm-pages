# Probatum — Pierwszy wybór

Independently authored website concept, created from scratch on 2026-09-07.
This is a separate private Site. It does not update probatum.pl, pm-pages/main,
any Vercel project, vercel.json, or any customer subdomain.

## Editing the current studio version

- `studio.py` defines the rebuilt page bodies and the working fictional Horyzont site.
- `compose.py` owns shared assembly, metadata, existing article/form content and loads `apply_studio` before rendering.
- `dist/assets/studio.css` is the final shared art direction and responsive override layer.
- `dist/assets/studio.js` implements finite scene sequences, media playback, offer selection, prompt copying and external previews.
- `cinematic.py` / `cinematic.js` retain the tree, car and actual-project interactions.
- `brand_journey.py` / `journey.js` implement research-to-launch foundation chapters.
- `flow_scene.py`, `flow-data.js`, `flow.css` and `flow.js` implement simplified factual process maps.
- `site.js` handles navigation, filters, articles and transparent email composition.
- `python3 compose.py` generates all 16 pages; generation itself needs no installed packages.
- The optional Vite development surface serves that exact output for browser QA. Production remains static HTML/CSS/JS.
- `tests/viewport-review.html` and `/__review` are development-only responsive review tools outside the published output.
- `python3 validate.py` checks local paths, anchors, metadata, labels and assets.
- `node tests/studio-runtime.cjs` exercises current HTML with mocked browser APIs.

## Current experience

The homepage retains the full-viewport tree, a concise direction choice, a filmed
website teaser, an Agents link and a contact invitation. The navigation stays available.

Strony WWW shows a real HTML website composition assembling from separated 3D layers:
plan, image, typography and finished desktop/mobile design. The completed composition
opens `/horyzont.html`, a working one-page fictional architecture site with native links.
Marketing and Social Media reuse that identity across a poster, website and social format.
The full-screen car remains on Approach with automatic visible playback and direct chapters;
below it, research, strategy, plan and launch show a new brand taking shape.

Offer has five selectable customer intentions with corresponding scope, further reading
and prefilled contact links. Projects retain two real services and six clearly identified
demos, filters, the original/colour comparison and postcard flip. External service frames
load only after a visitor chooses to open one, and closing removes the frame. An ordinary
external link remains available because third-party framing may be blocked.

Academy has three usable prompt examples and clipboard export with manual fallback.
Knowledge sections and both articles are readable, linked and consistent with the brand.
Contact and quotation retain their functional local message composition and validation.

Motion plays once, offers pause/replay and pauses offscreen/background. Reduced-motion
and save-data preferences prevent automatic film downloads; explicit playback is available.
Sequences have selectable stages, and invisible campaign links become inert. The static
final compositions, articles and service links remain readable without JavaScript.

## Deliberate integration state

Contact and enquiry forms compose a message locally for the visitor to send using
their own email app. They do not store or send submissions to an API, and never
claim a message was delivered. Direct contact is kontakt@probatum.pl and
+48 573 569 141, taken from the existing project.

The old production lead endpoint was not attached to this private concept.
Before changing to server-side delivery, confirm the endpoint contract, permitted
origins, data-controller information, and verify delivery with synthetic data.
No payment checkout is fabricated. Custom services lead to scope and quotation;
Academy links to its existing separate platform without invented prices.

All pages are noindex/nofollow and robots.txt disallows crawling for this private
concept. Public launch requires the intended production origin and metadata.

## Actual source of the agent presentation

The following active published workflows were read through the connected n8n
integration on 2026-09-07. No workflow was run or changed.

- Recepcja Poczty v1 (PILOT): incoming email, context gathering, draft response,
  approval service, approved send or refusal. 32 nodes, active version equals draft.
- Agency Onboarding: customer record, identity, onboarding event and startup tasks.
  10 nodes, active version equals draft.
- Raport Tygodniowy Biznesowy: fetch business status, build weekly context, record
  and send report on Telegram. 7 nodes, active version equals draft.

Also inspected: the active Media branch (13 nodes) and WWW/campaign branch (16 nodes).
Their tool relationships inform the new diagrams. The public views are simplified
editorial maps, not full workflow exports. Media/WWW nodes are selectable capabilities,
not claims that every tool runs for every request.

Only their high-level process is shown publicly. No real customer messages,
workflow exports, credential labels, identifiers, tokens or contact lists are
included. Active configuration alone is not presented as proof of successful
execution. The scenarios use fictional data and are explicitly labeled examples.

The workshop's webhook explanation links to the official n8n documentation,
checked on 2026-09-07. Academy availability/pricing was not independently verified
in this build, so its changing counts, pricing and packages are not claimed.

## Portfolio and assets

Six existing demonstration projects retained; all explicitly identified as demos.
Their live websites are external links, not duplicated or modified here.
Hero diagrams are authored SVG with public semantic labels, based on inspected workflow structure.
The rejected rotating-letter assets remain removed. The accepted blooming-tree video
is copied from the original spring concept. The new ten-second car film uses matching
before/after keyframes and depicts the same classic being dismantled, restored and
reassembled. It is generated conceptual imagery, not a real workshop or service claim.
It has no sound or external media runtime. Local H.264 files have faststart metadata
and frequent keyframes for seeking; the viewport loads only one size. Car film sizes:
about 3 MB desktop / 1.3 MB mobile. Reduced-motion/data preferences avoid automatic
video downloads. No cinematic media is loaded on unrelated service/contact pages.

Live projects are kept separate from the six demos:
- https://www.edwardjanusz.pl/ — original `images/dzf-1-58a.jpg` and the site's own
  `images/dzf-1-58a-kolor.jpg`. The latter is explicitly labeled AI interpretation.
  Different framing is preserved with a whole-image transition, not a pixel-aligned slider.
- https://www.silverandglass.pl/ — actual collection scans from
  `assets/kolekcja/img_krakow/pt-3-79-a.jpg` and `pt-3-79-b.jpg` form one front/back pair;
  `pt-3-21-a.jpg` and `pt-4-3-a.jpg` are the surrounding postcards.
Images are compressed copies, without AI alterations to the historical originals.
Both sites returned HTTP 200 when their public source/materials were inspected.
Other visual examples come from the user's existing site assets.
Fonts are locally served Manrope latin/latin-ext from Google Fonts.

## Before moving to Vercel

Use a separate branch/worktree from current origin/main. Another agent writes main.
Review only authored Probatum page/asset changes. Keep p/, vercel.json and
.vercelignore intact. Do not replace the whole repository with dist. Reconcile the
new composer with the old build pipeline so a later build cannot restore old pages.
First use Vercel Preview, verify all routes and customer subdomains, then obtain
the user's decision about replacing the existing public site.

## Validation and remaining limits

All 16 generated pages pass the local-link, anchor, metadata, heading, ID and label checks.
The new event harness covers finite playback, stage selection, manual/visibility pause,
reduced-motion/data behavior, the mobile video source, errors and stale play promises,
all offer-to-contact intentions, clipboard denial, opt-in frames, and script initialization
on every page. The existing flow/car event checks were also rerun.

The source-event checks use mocked DOM APIs. An additional supported Chromium review now
uses the supervised Vite development surface serving the actual Python-generated output.
Reviewed desktop openings at a 1363 px browser viewport, 320/390 px nested viewports for
Start, Offer, Contact, Approach, Marketing and Agents, and 768 px Projects and Academy.
These are real browser layouts, not physical-device tests. Visual review found and repaired
low-contrast tree text, overlapping car links, narrow contact-address wrapping and delayed
service visuals. Verified actual tree/car/architecture playback, car stage selection,
project colour/front-back interactions, offer-to-contact selection, Academy prompt switching
and clipboard copying. The contact form prepared the expected local message with synthetic
data; its mailto link was inspected without opening or sending it. Physical Safari/Android,
virtual keyboard behavior, slow-network performance and external-frame rendering remain
untested. No Core Web Vitals or frame-rate score is claimed.

Both real project homepages returned HTTP 200 during the preceding studio rebuild; their fetched response headers
had no X-Frame-Options or Content-Security-Policy. That is not a visual iframe test.
The separate Academy platform's current program/pricing and actual message delivery are
not verified. The enquiry backend remains intentionally unconnected in this private version.

No personal author name appears in served HTML, CSS, JS, SVG or metadata. Business email
and telephone are retained. The hosting namespace is outside authored site content.
`AUDIT-2026-09-07.md` describes the earlier revision; this studio rebuild supersedes its
layout observations. Its latest addendum records the new browser review and remaining limits.

## Architecture concept media

Horyzont is expressly identified as fictional. Its two architectural images were generated
for this design; the exterior was then animated as one 10-second silent Runway shot. This is
concept imagery, not evidence of work for a real architect. No historical project image was
regenerated or retouched during this rebuild.

Optimized local files are under `dist/assets/studio/`:
- exterior image: 215,582 bytes; mobile image: 79,450 bytes;
- interior image: 198,390 bytes; mobile image: 72,464 bytes;
- desktop H.264 film, 1600×900: 4,015,750 bytes;
- mobile H.264 film, 960×540: 1,161,900 bytes.

Both films use faststart metadata, 24 fps and no audio. The viewport selects one source;
there is no video source request before its scene is visible/ready. The same cached files
are reused across the homepage teaser, website build, campaign and architecture concept.

## Review-led composition update

WWW now opens with its building scene directly below a compact heading. Marketing and
Social combine the sales message and animated campaign into one opening. Academy begins
with the usable prompt workshop. Offer and Projects have shorter introductions; all pages
share a brighter closing invitation. Stage autoplay waits for most of the scene to enter
view. Mobile offer selection moves the chosen result into view. Car video uses a multiply
blend against the page, removing the white rectangular backdrop without editing its film.

## v9 — calmer actions and visual openings

Removed decorative diagonal arrows (including dynamic templates) and repeated homepage calls to action. Mobile contact is concentrated in the bottom bar; the mobile header now contains the brand and menu.

Offer, Marketing, Social, Academy, Knowledge, Workshop, Contact and Quote use full-width finite CSS animations of three original AI-generated artworks: green glass/paper formation, magnolia resonance and an unfolding leaf/book. Projects uses unaltered original photographs and postcards. WWW opens directly in the existing architectural scene. Tree, car and agents remain. Articles share a lighter illustrated opening.

New image assets: six responsive WebP files, 510,534 bytes total (desktop/mobile variants); no new video or animation dependency. Motion respects reduced-motion and data-saving preferences and pauses offscreen. Explicit replay/pause controls are provided on the main new openings.

Verification: all 16 generated pages pass local links, fragments, assets, unique IDs, heading and input-label validation. Existing mocked runtime checks pass. Browser review covered desktop Offer and mobile WWW, Projects, Academy, Offer, Marketing and Contact; replay/pause/resume was exercised on Offer. Mobile review uses Chromium viewport sizes, not physical iOS/Safari. Existing contact remains a mailto draft, not a delivery backend.

## v10 — distinct Knowledge and Contact scenes

Knowledge now uses an original generated optical lens / leaf detail artwork with a finite focus reveal. Contact uses a separate original ceramic/glass meeting sculpture with a finite arrival movement. Academy retains its book artwork. Each of these three openings now has a different subject. New assets have responsive desktop/mobile WebP variants. Homepage tree opening no longer contains the Offer button or its empty button row. Existing navigation and bottom contact bar remain.

Validation: Python compilation, JS syntax, local routes/assets/headings validator; direct generated-markup checks for removed tree CTA and distinct hero asset references. Both new source images were visually inspected. No new browser or physical-device testing in this revision.

## v11 — copy review and cookie information

Reviewed the main content of all 16 existing pages, shared navigation/footer, form messages, dynamic offers, prompt examples and public agent phase/node descriptions. Replaced repeated abstract marketing formulas with descriptions of deliverables and client actions; retained metaphorical lead headlines and functional playback/navigation symbols. Kept AI provenance notices for concept and colorized images. Added build-time copy_review.py so reviewed copy survives regeneration, including serialized flow data.

Added cookies.html and a visible footer link on all 17 pages. It describes the inspected code: no first-party cookie, localStorage/sessionStorage, analytics or ad tracking implementation; local media/fonts; opt-in external iframes; mailto forms and clipboard behavior. External preview controls now have an adjacent disclosure and consistent open/close labels. No consent banner or storage was added for nonexistent optional first-party trackers.

Scope: this is technical cookie/data information for this private Site, not a complete GDPR privacy policy or a cookie inventory of the hosting/authentication platform. Provider cookie names and retention have not been verified and are not invented. Before production migration or introduction of tracking, reassess actual hosting/network cookies, consent requirements and legal administrator information. No personal owner name was added.

Primary reference reviewed 2026-09-08: Article 399 PKE, current consolidated text dated 2026-07-07: https://eli.gov.pl/api/acts/DU/2024/1221/text/U/D20241221Lj.pdf . Also reviewed EDPB Cookie Banner Taskforce report (2023-01-18).

Validation: all 17 pages pass local references/anchors/assets/headings/labels validation. Existing mocked runtime checks pass, including no iframe until click and removal on close. JS syntax checks pass. No new live browser/network cookie audit in this revision.
