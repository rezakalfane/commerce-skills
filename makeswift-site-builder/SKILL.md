---
name: makeswift-site-builder
description: >-
  Build or restyle pages in the Makeswift visual builder (BigCommerce Catalyst
  storefronts) by driving the builder UI in the user's browser (Claude in
  Chrome / `claude --chrome`), using the built-in components (Box, Section,
  Text, Button, Image, Carousel, Card Carousel, Product Carousel...) rather
  than code. Use when the user wants to recreate a reference site's homepage
  or landing page in Makeswift, lay out sections from screenshots, prepare
  images for the Makeswift file library, or says "build it in Makeswift",
  "use the page builder", or "recreate this page". For writing or registering
  *custom* Makeswift components in code, use `makeswift-components` instead.
---

# Makeswift Site Builder (UI-driven)

This skill turns reference material (a live site plus screenshots) into a Makeswift page built only from built-in components, by clicking through the builder in the user's own logged-in browser.

**It is a living skill.** Every session that uses it must record what it learned in `references/learnings.md` (see "Self-improvement protocol"). Read that file **before starting**, because it has UI quirks and fixes that earlier sessions paid for.

## Prerequisites
- A browser-control tool (Claude in Chrome; start Claude Code with `claude --chrome`). If no browser tool is available, don't pretend: produce the spec and assets (phases 1–2) and hand off.
- The user is logged in to Makeswift with the target site and page open.
- The storefront's catalog already exists (category paths and product ids are known), e.g. from `site-to-catalog`.

## Workflow

### Phase 1: Spec (no browser needed)
1. Collect the references: the live URL plus the user's screenshots. Save the screenshots into the project (e.g. `screens/`). macOS screenshot names contain U+202F before AM/PM, so match them with a glob.
2. Pull the real copy, links and images from the live page. **Don't guess at the text.** See `references/learnings.md` → "Extraction" for per-platform recipes (e.g. Shopify `hero__image`).
3. Write `<PAGE>_SPEC.md` from `references/spec-template.md`: one block per section with component, layout, sizes, copy, links, images, and desktop and mobile notes. Map every link to a path that exists on the **target** storefront. Mark links with no target as `#` and list them for the user.

### Phase 2: Assets
1. Download the originals and strip Shopify-style size suffixes (`_1900x`, `_{width}x`) to get full resolution.
2. For anything rendered by JavaScript (Instagram feeds, lazy widgets), crop it from the reference screenshot: `scripts/crop_tiles.py`.
3. View a contact sheet of every asset before calling it done. File size and name tell you nothing: "background" files can be blank white fills, and tiles can come pre-darkened.
4. `scripts/prepare_upload.py` builds one images-only folder named after the client (`assets/Dunlop/`), with prefixed, ordered names (`dunlop-01-hero-...`); the manifest is written next to the folder, not inside it. The user uploads it with **Files → Workspace → New → Upload folder**, which creates the client folder and uploads everything in one step. That's faster than the agent uploading one file at a time. Images are then picked by searching the prefix.

### Phase 3: Build in the builder (browser)
1. **Screenshot the current page first.** Confirm with the user which site, page and locale are open, and whether existing sections should be removed or kept.
2. **Set up brand styling before building any sections:**
   - **Design tab → Colors**: add the brand palette, named with `/` groups, e.g. `Dunlop/Red`.
   - **Design tab → Text styles**: add heading and body styles (font, weight, size, line height, letter spacing, uppercase).
   - **Content → Elements → Site Theme**: set the Heading, Body and Accent fonts, plus the Button, Header and Section theme settings.

   Sections then pick up these saved styles instead of per-element overrides.
3. **To add a component:** click **+** in the tool strip, pick it (the picker is searchable), then click on the page where the **blue line** marks the insertion point. **ESC** cancels.
   **To select the parent of a nested element** (Box in Box): press **ESC** to deselect, hover the element, then hover the purple type tag at its top-left. It expands into the ancestor stack (e.g. `Box` / `Box` / `Page`); click the level you want. The Elements tree also works. *(see `references/img/select-parent-*.jpg`)*
4. Build **top to bottom, one section at a time**: add the component, set its properties, take a screenshot, compare with the reference, fix. Don't batch several sections before checking.
5. **Section vs Box (user convention):** use **Section** (+ → Layouts → Section) for content that sits inside the page's standard margins, then put Boxes, Text and Images inside it. Use a **Box** directly for **full-width** bands (hero, full-bleed image background, edge-to-edge grids), or when you need to set the padding yourself.
6. **Check the prebuilt Sections first** (Slideshow, 4-Column with Icons, Category Grid, 2-Column Split, …). Hand-build from Section → Box → leaf components (Text, Button, Image, carousels) only when no prebuilt one fits. See `references/components.md`.
7. **Columns and responsive layout:** place sibling elements side by side in one parent Box (they join one row). Select the **parent**, then drag the pill handles between columns to size them. For responsive behaviour, switch device (**Desktop ▾**: Desktop >1281 / XL 1280 / Large 1024 / Medium 768 / Small 640), select the parent again, and widen columns until the next ones wrap to a new row. Each device keeps its own layout. To stack columns into rows on a device, **click** (don't drag) the dashed divider between them with the parent selected. To create columns: ⌘D inside an existing row adds a column; to start a row, Copy then Paste on the target Box's left-edge vertical line (see the methods table in `references/learnings.md`). *(see `references/img/boxes-*.jpg`, `responsive-*.jpg`)*
8. **Box has no absolute or relative positioning.** Overlapping effects mean putting the text *inside* the Box that has the background image (Align items, padding). Overlays are stacked Backgrounds layers (an image, then a semi-transparent colour).
9. After each section, set and check **Medium** and **Small** too (see step 7). Some properties are **global, not per device** (e.g. the Image source). For a different element per device, add both as siblings, select the **parent** (e.g. Page), and in its **Visibility** control (one grey bar per child, in order) click a bar to hide that child **on the current device**. Grey = visible, white = hidden. See `references/learnings.md` and `references/img/visibility-*.jpg`.
10. Use preview or interact mode (▶ in the tool strip) to click every link.
11. **Never click Publish without the user's explicit OK.** Publishing changes the live storefront.

### Phase 4: Close out
- Give the user a per-section summary: what matches the reference, what differs, and why.
- Update `references/learnings.md` (required), and update `references/components.md` if you confirmed or disproved anything there.

## Self-improvement protocol
- **During the session**, whenever something in the builder surprised you (a control in a different place, a drag that failed, a workaround), append a dated entry to `references/learnings.md` under the right heading: *symptom → cause → fix*. Write it at the moment it happens, not at the end, so it survives if the session is cut short.
- **Component facts** (which control holds padding, whether Image accepts a URL, per-breakpoint settings, and so on) go into `references/components.md`. Mark a fact **verified (date)** only once you've seen it in the UI yourself.
- **Promote** a learning into this `SKILL.md` (Workflow or Gotchas) once it has held true in two sessions, or if it prevented a real mistake. Delete learnings that turn out to be wrong rather than letting them pile up.
- Keep this file short. Detail belongs in `references/`.

## Gotchas (confirmed so far)
- JavaScript-rendered sections (Instagram feeds) have no image URLs in the HTML. Crop them from the screenshot.
- Hero banners often have their headline and CTA **baked into the image**. Don't lay Text or Button over them; make the whole slide the link.
- Desktop and mobile hero art are usually separate files with different layouts. The Image source is **global, not per device**, so use two sibling elements and hide one per device with the parent's Visibility bars (workflow step 9).
- The source's CSS overlay is not in the image file, but some images come pre-darkened anyway. Look before adding an overlay.

- **The canvas is a cross-origin iframe.** Element refs from `find`/`read_page` only reach the editor chrome (panels, tree). **Click on the page by screen coordinates.** Text copy is edited **inline**: click the Text, wait, then double-click it at its coordinates. Confirm the highlight before typing (see `references/learnings.md`).

## Files
- `references/learnings.md`: running log of UI quirks, extraction recipes and fixes. **Read first, append always.**
- `references/img/`: annotated UI screenshots and recording frames that back up learnings (e.g. `visibility-*.jpg`). Add frames when a text description isn't enough.
- `references/components.md`: built-in component and control reference, with verified/unverified flags.
- `references/spec-template.md`: page spec skeleton.
- `scripts/prepare_upload.py`: flattens and prefixes assets into an upload folder, and writes a manifest.
- `scripts/crop_tiles.py`: detects and crops image tiles out of a screenshot.
