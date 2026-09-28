# <Site> <page>: Makeswift build spec

Reference: <live URL>; screenshots in `screens/`. Target: <storefront / channel>, Makeswift site <name>, page <path>.
Components: built-in only.

## Brand styling
- Colours: primary `#…`, secondary `#…`, text `#…`, light band `#…`
- Headings: <font / weight / case / letter-spacing>; body: <…>
- Buttons: <shape, case, fill and text colours, on light vs on photo>

## Assets
Upload folder: `assets/<Client>/` (images only, prefix `<site>-`), uploaded via Files → Workspace → New → Upload folder; manifest: `assets/MAKESWIFT_MANIFEST.md`.

## Sections (top to bottom)

### N. <Name> (Screenshot X)
- **Component:** <Section / Box (cols, gap, padding) / Carousel …>
- **Layout:** <height, alignment, max width>; **mobile:** <…>
- **Copy:** exact text (quote it)
- **Images:** `<upload file name>`
- **Links:** `<target path>` (`#` means there's no target page yet)
- **Notes / differences from the reference:** <…>

## Build order and checks
1. Screenshot the current state; confirm site, page and locale, and what to remove.
2. Build one section at a time → screenshot → compare with the reference → fix.
3. Check mobile after each section.
4. Click every link in preview.
5. Don't publish without the user's OK.
