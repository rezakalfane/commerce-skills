# Learnings log

Append-only-ish: add dated entries as *symptom → cause → fix*. Promote to SKILL.md
when confirmed twice; delete if disproven. Newest entries at the bottom of each section.

## Extraction (getting copy/images from the reference site)

- **2026-09-28 (Dunlop, Shopify):** Homepage background/hero images are
  `<img class="hero__image …" src="//…/cdn/shop/files/<name>_1900x.jpg?v=…">` —
  not CSS `background-image`, not `data-bgset`. Regex on `<img class="hero__image[^"]*"\s+src="…"`,
  strip `_<n>x` before the extension for the original file. Desktop vs mobile variants sit side by
  side (`small--hide` / `medium-up--hide` classes).
- **2026-09-28 (Dunlop):** Promo-grid tiles and product images use `data-src` with a `{width}` placeholder
  (`…_{width}x.jpg`) — strip `_{width}x` for the original.
- **2026-09-28 (Dunlop):** Instagram feed section is an empty `<div id="insta-feed">` in the HTML —
  images only exist after JS. Fix: crop from the user's screenshot (`scripts/crop_tiles.py`); a
  dark tile containing white text (logo) breaks the white-gap detection — pass `--count` and let
  the script infer the missing tile from the spacing.
- **2026-09-28 (Dunlop):** Two "background" files (`…1440-x-400---White.jpg`, 3–4 KB) were plain white
  fills. A tiny file size for a big banner = blank; check the contact sheet and drop them.
- **2026-09-28 (Dunlop):** Promo tiles looked pre-darkened in the file itself; a heavy extra overlay would
  make them muddy. Use ≤25% overlay and compare with the reference.
- **2026-09-28:** macOS screenshot filenames contain U+202F (narrow no-break space) before AM/PM — typing the
  name fails with "No such file"; use a glob (`*2.57.37*`).

## Builder UI (Makeswift editor)

Confirmed by the user, with screenshots (2026-09-28). Unless marked otherwise, not yet driven by an agent.

- **Editor layout:** the left sidebar has the site switcher, **Content | Design** tabs, **Pages** (search, +), and the **Elements** tree (Site Theme, Site Header, Page > Section > Box > …, Site Footer). A tool strip sits next to it, top to bottom: select, interact/preview ▶, Box, Text, Image, Button, **+** (all components). The top bar has a locale selector (`en`), the storefront URL, a **Desktop ▾** breakpoint switcher, **Share**, **Publish** (green) and a `⋯` menu. The right panel shows the selected element's properties. With nothing selected, it shows **page Metadata**: Online, Path, Title, Description, Social Image, Exclude from search engines, Canonical URL, Sitemap priority and frequency, Snippets.
- **Adding a component (user-confirmed):** click **+** in the tool strip, which opens a searchable component picker. Click a component, **then click on the page to place it**; a **blue line** shows where it will be inserted. Press **ESC** to cancel. It's two clicks, not a drag. (Box, Text, Image and Button also have their own icons in the strip.) *(img: `img/picker-01-component-catalogue.jpg`)*
- **Picker catalogue on the Catalyst "Europe Headless - B2B" site:**
  - **Basic:** Accordion, Card, Card Carousel, Carousel
  - **Catalog:** Product Card, Products Carousel, Products List
  - **Catalyst:** Customer Group Slot
  - **Layouts:** Section, Sticky sidebar
  - **Sections:** 2-Column Split, 2-Column with Image, 4-Column with Icons, Category Grid, Custom Component, Featured Card Carousel, Featured Product Carousel, Featured Product List, Large Quote, Slideshow, …
  - The prebuilt **Sections** can replace hand-built Box layouts; check them before building from scratch.
- **Site Theme** (Content → Elements → **Site Theme**): **Fonts** (Heading, Body, Accent; defaults Inter / Inter / Roboto Mono) and per-component theme settings for Accordion, Button, Card, Carousel, Footer, Header, Logo, Price label, Product card, Section and Slideshow. Set brand styling here **first**, so every component inherits it. *(img: `img/theme-01-site-theme-panel.jpg`)*
- **Design tab (design tokens):**
  - **Colors**: a swatch list with **+** to add. The edit popover has Name ("use `/` to group colors", e.g. `Dunlop/Red`), Hex, a picker, "Used in N places", delete, Cancel/Save. *(img: `img/design-01-color-edit.jpg`)*
  - **Text styles**: 2XL 24 … 8XL 96, Base 16, Label 14, Large 18, … The edit popover has Name (`/` groups), font, weight, colour and opacity, size, line height, letter spacing, underline/strike/**uppercase (TT)**, a preview, and "Used in N places". *(img: `img/design-02-text-style-edit.jpg`)*
  - Create brand tokens here, then apply them from the Text panel's **Text style** dropdown.
- **Box panel:** **Backgrounds (+)** (image and colour layers stack, so an overlay is a colour layer over an image layer; user-confirmed), Width (px/%), Height (auto vs stretch toggle), Align items (top, centre, bottom, …), Margin (4 sides, `auto` allowed, plus alignment buttons), Padding, Border, Corners, Shadows, **Row gap**, **Column gap**, Animate box in, Animate items in, Hide placeholder. *(img: `img/panel-box.jpg`)*
  - **No absolute or relative positioning** (user-confirmed), so you can't overlap elements freely. Put overlay text *inside* the Box that has the background image, and use Align items → bottom plus padding.
  - There's **no "columns" control** in the panel. Columns come from sibling elements in a shared parent, resized with drag handles per device; see "Columns and responsive grids" below.
- **Selecting a parent of a nested element (user-confirmed with a screen recording, 2026-09-28):** click selects the innermost element, e.g. an inner Box. To reach its parents:
  1. Press **ESC** to deselect (the right panel switches to page Metadata).
  2. Hover over the element on the canvas; a purple **type tag** (e.g. `Box`) appears at its **top-left**.
  3. Hover the tag. It expands into the **ancestor stack**, innermost first (e.g. `Box` / `Box` / `Page`).
  4. Click the level you want, and the right panel switches to that element.

  The Elements tree in the left sidebar is the other way in. *(img: `img/select-parent-01-tag-ancestor-stack.jpg` expanded Box / Box / Page stack → `img/select-parent-02-outer-box-selected.jpg` after clicking the outer Box: the panel switches to it and shows **Visibility** at the bottom)*
- **Columns and responsive grids (user-confirmed with 2 screen recordings, 2026-09-28).** This replaces the earlier guess about child widths.
  - **Adding siblings makes columns.** Place several Boxes (or Images, etc.) **next to each other inside the same parent**; they join one row as connected columns, with the width shared between them (e.g. Box | Box | Box | Image | Image).
  - **Resizing columns:** select the **parent** (ESC → hover → type tag → pick the parent level, or click the parent directly if part of it is exposed). Small **pill handles** appear on the dashed dividers between columns; drag one to resize the columns on either side.
  - **Responsive wrapping is set per device.** Switch devices with the **Desktop ▾** dropdown: **Desktop >1281px (1), XL 1280px (2), Large 1024px (3), Medium 768px (4), Small 640px (5)**; the numbers 1–5 are probably keyboard shortcuts. Select the parent again, then drag the handles so a column gets wider. When a row's widths pass 100%, the next columns **wrap to a new row** (the recording on Medium goes 5 in a row → 2 + 3 → 2 + 2 + …). Each device keeps its own layout, so set Desktop first, then each smaller device.
  - **Recipes:** 2×2 grid = 4 sibling Boxes, then on Desktop make the first two span the row (50/50) so the other two wrap. 4-up strip → 2×2 on Medium → 1 per row on Small. 3-up icons → 1 per row on Small.
  - *Boxes (img): `img/boxes-01-insert-box-blue-line.jpg` Box tool placed inside an existing Box (blue line at its left edge) → `img/boxes-02-second-box-beside-first.jpg` the new Box sits beside the first → `img/boxes-03-siblings-join-one-row.jpg` siblings (Box | Box | Box | Image | Image) share one row.*
  - *Responsive (img): `img/responsive-01-pill-handles-desktop.jpg` parent selected, pill handles on the dividers → `img/responsive-02-device-dropdown.jpg` switch device → `img/responsive-03-medium-before-drag.jpg` Medium still 5-up → `img/responsive-04-medium-drag-wraps.jpg` widen a column and the rest wrap → `img/responsive-05-medium-wrapped-2up.jpg` final 2-up grid.*
  - *The parent's **Visibility** bars mirror the children's layout: one bar per child, arranged in the same rows, so you can tell which bar is which.*
- **Section component (user-confirmed, screenshot 2026-09-28):** it's in the picker under **+ → Layouts → Section** (next to Sticky sidebar). A freshly placed, empty Section shows on the canvas as a **grey full-width band with a dashed outline**, and appears as `Section` in the Elements tree. Sections can be nested (the tree showed Section > Section), but prefer Section → Box → content. _To confirm: the Section panel controls (background, padding, content width)._
- **Box panel differs by nesting level:** the parent Box in the recording showed a **Visibility** setting at the bottom of its panel (below Animate items in); the inner Box showed **Hide placeholder** instead. _To confirm: does Visibility hide the element per breakpoint? If so, use it for the desktop/mobile hero swap (two carousels, one hidden per breakpoint)._
- **Text panel:** Content (textarea), **Block** (Paragraph / heading levels), **Text style** (select a saved style, or set font, weight, colour and opacity, size, line height, letter spacing, decorations), Alignment, Inline (superscript, subscript, code), On Click (Open page ▾, search pages, open in a new tab), Width (px/%), Margin. *(img: `img/panel-text.jpg`)*
- **Image panel:** Image (**Choose** opens the Files dialog), Alt text, On click (Open page ▾, page search, new tab), Width (px/%), Margin, Padding, Border, Corners, Shadows (+), Opacity, Priority. *(img: `img/panel-image.jpg`)*
- **Files dialog:** scopes Search / Site / **Workspace**. **New ▾** offers Upload files, **Upload folder**, New folder. There's also **Open Assistant** (Makeswift AI) and sort. Workspace has one folder per client. **Upload folder worked (user-confirmed 2026-09-28):** it created `Workspace files / Dunlop` with all 23 images, and the thumbnails show the prefixed names. *(img: `img/files-01-new-menu.jpg`, `img/files-02-workspace-folder-uploaded.jpg`)*

- **2026-09-28 (verified by agent): adding colours.** Design tab → Colors **+** opens the popover *anchored
  at the same spot every time* (Name field focused, Hex field to the right, Save bottom-right), so colours
  batch reliably: click Name → type `Group/Name` → click Hex → cmd+A → type `#RRGGBB` → Tab (commits and
  updates the swatch) → Save. `Dunlop/Red` etc. show as a collapsible **Dunlop** group at the bottom of the
  list, children listed by the part after the `/`. The new popover's Hex defaults to a random-ish dark
  value (#050505), so always overwrite it.

- **2026-09-28 (verified by agent): fonts.** On the Catalyst site, the text-style font list only offers
  the fonts **managed in code**: DM Serif Text (Regular), Inter (**Light/Regular/Medium only, no bold**),
  Roboto Mono. So "Inter 800" in a spec is impossible; check the available weights before writing
  the spec. The font dropdown has **Manage site fonts** → **Browse fonts** (Google Fonts, searchable, one
  checkbox per family) → Add → back on Manage, **per-weight checkboxes** (pick only the weights you need;
  a "Load time" badge goes Fast → Moderate as you add more) → Save. **Save shows a confirm dialog: "All
  font changes will be applied globally to your site, including live pages … cannot be undone."** Treat it
  like Publish: get the user's OK before Confirm. The text-style popover stays open behind the dialog.
  Clicking a style name in the Browse list does nothing; they're only previews.
- **2026-09-28 (verified by agent): text styles.** Text styles **+** opens a popover with Name pre-selected
  ("Untitled text style", so just type), font, font style, colour/opacity, size, line height, letter
  spacing, U/S/TT, a preview and **Create** (not Save).
  **The popover changes height** once a big font size is set (the preview grows), and it's anchored at the
  bottom, so every field moves **up**. Take a fresh screenshot after setting size/font before clicking the
  next field; don't reuse coordinates from before.
- **2026-09-28 (verified by agent, painful): digit keys switch devices.** When a click misses an input, typed
  digits go to the canvas and act as **device shortcuts** (1 = Desktop … 5 = Small). Typing `-0.5` into
  nothing switched the canvas to **Small**. This confirms 1–5 are breakpoint shortcuts. Fix: after clicking a
  numeric field, zoom to confirm it's focused before typing, and check the **device dropdown** (top bar)
  still says Desktop before editing layout.
- **2026-09-28 (verified by agent): reliable popover filling = element refs.** Run `find` once per popover
  ("font select, font style select, size input, line height input, letter spacing input, Create button")
  and click by `ref`. Refs stay valid while the popover moves around. Dropdown options need a second
  `find` after opening (`Barlow Condensed menuitem`, `menuitem exactly 'Bold'`). Set the **size last**
  because it resizes the popover. The U/S/TT buttons have no labels in the accessibility tree, so click TT by
  coordinate (hover shows an "Uppercase" tooltip) and zoom to confirm the preview is uppercase.

- **2026-09-28 (verified by agent): Site Theme.** Content tab → Elements → **Site Theme** → click the
  sliders icon next to **Fonts** to get a popover with Heading / Body / Accent dropdowns (added Google fonts
  appear there too). Changes apply to the canvas immediately (header nav and logo re-rendered). The user
  prefers setting **all three** to the brand font. **Button** (sliders icon) has **Font** (Body/Heading/…)
  plus colour sets for **Primary / Secondary / Tertiary / Ghost** (Background, Background hover, Text,
  Border) and Focus. There's **no corner/radius or padding setting**, so square corners must be set per
  element if the Button panel allows it. Colour swatches open a Colors list with a **search box**, so
  type `Red` / `Charcoal` to find the `Dunlop/…` tokens, click, then click outside (e.g. on the
  "Primary" label) to close. Catalyst defaults: Primary = white/black border, Secondary = #121212 fill with
  white text.

- **2026-09-28 (verified by agent): delete / duplicate.** No right-click menu in the Elements tree. Use the
  **⋯** at the top-right of the selected element's panel: Duplicate ⌘D, Copy ⌘C, Paste ⌘V, **Delete (⌫ / DEL)**.
- **2026-09-28 (user preference): static hero = Box, not Slideshow.** For a single static banner the user
  wants a full-width **Box** with a background image, not the prebuilt Slideshow. Only use Slideshow/Carousel
  when there really are rotating slides. (Slideshow panel for reference: Slides +, Autoplay, Duration, Card
  style (site-specific named styles), Height (Large…), Overlay from/colour/strength (default 80%)/fades to, Text vertical
  position, Text width, Button style (Pill button). Its default red pill "Shop all" button uses the Site Theme
  Primary button colours.)

- **2026-09-28 (verified by agent): Image file is NOT per-device.** Replacing the image while on **Small**
  replaced it on Desktop too. Width, margin and padding may be per device, but the image source isn't. For
  desktop and mobile art, use two elements and hide one per breakpoint (check Visibility), or accept one
  image. A 3.5:1 banner on Small (640px) is only about 180px tall and the baked-in text becomes tiny.
- **2026-09-28 (verified by agent): full-bleed banner recipe.** Box (top level, Width 100%, **Padding 0**, the
  default is 10) → Image (Width 100%, Padding 0). This keeps the banner's native aspect ratio at every width, so no
  cropping of baked-in text, unlike a Box background image with `cover`. **Box has no min-height/fixed height**
  (Height is only auto/stretch), so a background-image Box gets its height only from content or padding.
  Image **On click** has Open page / **Open URL** / Compose email / Call phone / Scroll to element. Use Open URL
  with a relative storefront path (`/steeplechase-bonnie-wellington/`) for BC product/category pages, which
  aren't Makeswift pages. Turn **Priority** on for above-the-fold images. The Files dialog opens straight in
  the last folder (Workspace / Dunlop), and double-clicking a thumbnail selects it.

- **2026-09-28 (verified by agent): the Site Theme Body font doesn't reach Makeswift Text.** A freshly added
  Text rendered in a plain sans (not Barlow) even with all Site Theme fonts set to Barlow Condensed. Site
  Theme fonts drive the Catalyst components (header, product cards, Slideshow). Makeswift **Text** needs a
  **Text style** (e.g. `Dunlop/H2`) applied. Choose it from the Text panel → Text style dropdown, which has a
  search box (type `H2`).
- **2026-09-28 (user tip): test styles with throwaway elements.** Drop a Text/Button on the page, apply the new
  style, check it, then delete it with ⋯ → Delete. That's quicker than guessing from the style popover preview.
- **2026-09-28 (user-confirmed, screen recording): per-device show/hide via the parent's Visibility bars.**
  Use this when a property change is **global** (e.g. the Image source) but you need a per-device result:
  1. Add the alternative element (e.g. a second Image with the mobile banner) as a **sibling** of the
     desktop one. In the recording it sat directly under Page, between the hero Box and the Section.
  2. Select the **parent** (here **Page**, via the Elements tree). Its panel shows **Visibility** with **one
     grey bar per child, in page order** (Box / Image / Section).
  3. Pick the device in the **device dropdown**, then **click a bar to toggle that child** for that
     device only. **Grey = visible, white/empty = hidden.** Hidden children are dimmed with an eye-slash
     icon in the Elements tree.
  4. Repeat per device. The final state in the demo: Desktop, XL, Large and Medium show Box (desktop banner)
     and hide the mobile Image; Small hides the Box and shows the mobile Image.
  Screenshots: `img/visibility-01-page-bars-desktop.jpg` (bars on Desktop), `img/visibility-02-small-box-hidden.jpg`,
  `img/visibility-03-medium-image-hidden.jpg` (middle bar white = mobile Image hidden on Medium).
  Remember the mobile Image needs its own On click, Alt text and Priority, because it's a separate element.
  **Verified by agent:** an element hidden on the current device can still be selected and edited from the **Elements
  tree** (it's dimmed with an eye-slash icon), so you don't need to switch device to edit it. After editing, check Small, Medium and Desktop
  from the device dropdown (not the 1–5 keys) to confirm each device shows the right element.

- **2026-09-28 (user-confirmed, then agent-verified): Text content is edited INLINE on the canvas, not in the panel.**
  The panel's **Content** box is a read-only preview; typing there does nothing. Method: **single-click the Text
  at its screen position** to select it, wait about 1 s, then **double-click at screen coordinates** on the text. The
  words highlight (edit mode) *(img: `img/text-01-inline-edit-word-selected.jpg`)*. Then use keyboard input
  (Cmd+A inside the text selects all of it; type the new copy; Escape leaves edit mode).
  - The canvas is a **cross-origin iframe**, so **element refs (`find`/`ref`) can't reach inside it. Always click
    the canvas by screen coordinates** (take a screenshot first). Browser-level clicks and keys do reach it.
  - An earlier attempt failed. The likely cause was a stale selection (the panel still showed the previous element)
    or double-clicking before the selection had settled. It worked first try after a fresh editor load: click,
    wait, double-click.
  - **Safety check before typing letters:** zoom in and confirm the blue text highlight. If there's none, don't
    type, because letters and digits can hit editor or device shortcuts (1–5 switch device).
  - The same applies to any embedded app: BigCommerce's "Edit in Makeswift" button sits in the BC app iframe, so
    `find` can't see it; click it by coordinates.

- **2026-09-28 (verified by agent): Button panel (Catalyst Button).** Margin plus alignment (left/centre/right),
  **Link** (Open URL + field), **Button text** (this *is* editable in the panel, unlike Text content), **Color**
  (Primary / Secondary / **Tertiary** = white fill, dark text, thin #DEDEDE border, i.e. the outline style / Ghost),
  **Size**, **Shape** (Pill / Rounded / **Rectangle** / Circle). Use **Rectangle** for square-cornered brand buttons.
  This answers "no corner setting in the Site Theme": set it per button with Shape.
- **2026-09-28 (verified by agent): moving an element into another parent = drag in the Elements tree.** Dragging
  `Button` onto the row just under `Text` (slightly indented) moved it *into* the Text's Box, below the heading.
  That's how to stack a heading and a button when they sit in side-by-side columns. Dragging the column divider to
  100% doesn't wrap a 2-column row: the second column just gets squeezed to a sliver.
- **2026-09-28 (verified by agent): Products Carousel hand-picked products.** **Product collection → None (static
  only)** (the other options are Best selling / Newest / Featured; there's **no category source**), then
  **Additional products +** adds a "Product" row. Click the row → popover (Title optional, **Product** search).
  Rows are 32px apart and the popover follows the row. Search is **fuzzy and slow** (the first result list can
  be stale, so wait 2–3 s and read it again) and returns near-matches (`Sport` → Junior/Kids' Sport), so always
  click the exact name. Verify the order afterwards by opening each row and reading the selected product. Rows
  have a drag handle for reordering (user tip).
- **2026-09-28 (verified by agent): margin/alignment values are per device and can carry old overrides.** The Catalyst
  "See all" button was already set to left on **Small**, so centring it on Desktop left it left-aligned on phones.
  After any alignment or spacing change on Desktop, switch to **Small** (and Medium) and check. Existing template
  elements often have per-device overrides.
- **2026-09-28 (verified by agent): prebuilt "4-Column with Icons".** Placing it makes a **shared component**: the panel says
  "Editing this component will update all instances … across your site" with **Edit component / Detach**. Click **Detach**
  to make a local copy you can edit. Structure: Section → `#Icon-grid` Box (Row gap 40, Column gap 48) → 4 × Box(Image
  24px svg, Text title, Text line). Deleting one column Box makes the rest rebalance automatically (3 equal columns). To
  place a new section *after* an existing Section, hover in that Section's **bottom padding** until the blue line spans the
  full width with a **"Page"** tag. Hovering just under the content puts it *inside* the Section.
- **2026-09-28 (verified by agent): inline edit sometimes needs a second double-click.** Click to select, then double-click; if
  there's no blue highlight, double-click again (the first one sometimes only settles the selection). Cmd+A, type,
  Escape. Always zoom in to check the highlight before typing.
- **2026-09-28 (verified by agent): canvas clicks can leave the panel stale** (the tree highlights the new element but the panel
  still shows the old one). Select via the **Elements tree** when that happens.
- **2026-09-28 (verified by agent): creating a text style from an element.** Text style dropdown → **+** → "Create new text
  style" saves the element's **current** values (including overrides). So: apply the nearest style, override size/spacing in
  the panel (overrides show purple; the shared style is **not** changed), then + → name `Dunlop/Title` → Save. It's
  applied automatically. Created `Dunlop/Title` = Barlow Condensed Bold 22 / 1 / 0.5 uppercase for icon and tile titles.
- **2026-09-28 (agent bug): Text "On Click → Open URL" drops typed letters.** Only `/` characters registered (the field
  re-renders and loses focus on each keystroke; letters go to BODY). **Fix: `form_input` on the URL field ref**, then click
  away. The value sticks. (Button → Link URL accepted typing normally.)
- **2026-09-28 (verified by agent): dragging a divider can't *un-wrap* a row.** A divider trades width between its two
  neighbours and the row stays at 100%. On Medium the 4-Column template was 50/50 + wrapped third; dragging the divider
  gave 33/67 with the third still wrapped. The Box **Width** field is the width *inside* its column cell, not the column
  width. Getting three across from a wrapped layout probably needs a different gesture (still to learn; ask the user for
  a recording). **Cmd+Z undo works** (keyboard focus on BODY is fine).
  **Second try (user-suggested right-edge handle), 2026-09-28: failed.** A selected parent Box shows no per-column
  handle on the outer right edge. Dragging from that edge changes the parent's **right padding** instead (it set 230).
  Cmd+Z only partly reverted it (padding stayed at 90), and clearing the field didn't take, so **typing 0 fixed it**.
  After any drag on a Box edge, check the Padding and Margin fields. Decision: leave Medium at 2 + 1 (the centred
  third column looks deliberate).
- **2026-09-28 (verified by agent): image-background band recipe ("We are Dunlop").** Page-level Box → Backgrounds + → Image →
  pick the file (**double-click adds TWO identical layers**, so remove one with −). Click the layer to open its popover: position
  grid, **Size** (Stretch to fill / Fit inside / Original, **no "cover"**; Stretch to fill behaves like cover here), Repeat,
  Opacity, Parallax, Priority. There's no fixed height, so **height = padding**: top padding 420 made a ~480px band. Align items →
  **Bottom** + bottom padding 0 puts the child Text on the image's lower edge. Padding field order in the panel is
  **left, top, bottom, right**, not CSS order. `form_input` on the four padding refs is the reliable way to set them.
- **2026-09-28 (user tip): Hide placeholder** on Boxes that contain no text or elements (pure image bands), so the empty
  grey placeholder doesn't show in the editor.
- **2026-09-28 (user tip): for headings that must sit tight under a band, use a Box with padding, not a Section.** A Section
  adds its own top/bottom spacing. A Page-level Box with padding L40/T0/B24/R40 put "PROTECTIVE FOOTWEAR" right under
  "WE ARE DUNLOP" with the same left edge. Move an existing Text into it by dragging it in the Elements tree.
- **2026-09-28 (agent bug): a Step 0 text style lost its values.** `Dunlop/Display` had no line height, letter spacing or
  uppercase when first used (it was created while the popover kept moving, see above). **After creating styles, reopen
  each one from Design → Text styles and check every field.** Fixed: 1 / -0.5 / TT.
- **2026-09-28 (agent bug): long inline typing can swap characters.** Typing a paragraph in one go produced "57" instead
  of "75". Always zoom in and proofread after inline typing. To fix a word: double-click it (selects only that word),
  then type the characters slowly, one per action.
- **2026-09-28 (agent quirk): picking a tool (Text/Button/+) can scroll the canvas.** Take a fresh screenshot after choosing
  the tool and *before* choosing the drop point. A blue line that starts at a child's left edge (not the full width) means
  "inside that Box". For Page level, look for the full-width line with the **Page** tag.
- **2026-09-28 (agent quirk): the agent's tab group can disappear mid-session** ("Couldn't determine which page … no tab
  group"). Recreate it with `tabs_context_mcp {createIfEmpty:true}` and navigate to the saved editor URL. Makeswift
  autosaves, so no work is lost. Keep the full editor URL written down for this.
- **2026-09-28 (verified by agent): Text font size and Box padding are PER DEVICE; text-style definitions are NOT.**
  On Small, overriding a Text's size (80 → 52) and a Box's padding (40 → 14) left Desktop and Medium untouched. The Design-tab
  text-style popover has no device switch, so change sizes per device on the element, not on the style. Visibility bars
  are also per device, with no cascade: hiding bar 6 on Desktop didn't hide it on Small. Set each device you care about.
- **2026-09-28 (verified by agent): device-specific image band = Duplicate + swap background + Page Visibility.** ⋯ →
  Duplicate the band Box (the copy lands right after it), open its background layer → Replace → Files **Search**
  `dunlop-09` → hover the result → **Choose**. Then Page → Visibility: on Desktop hide the copy's bar, on Small hide the
  original's bar. Hidden elements show dimmed with an eye-slash in the tree.
- **2026-09-28 (agent MISTAKE, near-miss): Escape deselects, and the panel falls back to page Metadata. Its top-right
  (1430,58) is the page "Online" toggle.** A blind click meant for "Backgrounds +" switched the Home page offline (in
  the draft). Caught and reverted within seconds, and nothing was published. **Rule: before any coordinate click in the right
  panel, check the panel title (top-left) is the element you expect. Don't press Escape to close file dialogs; click outside instead.**
- **2026-09-28 (agent quirk): the canvas can also scroll horizontally** (content shifted left, header clipped). Reset
  `scrollLeft`/`scrollTop` on the `bg-contrast-100 isolate` wrapper.
- **2026-09-28 (user-confirmed, recording `14-drag-boxes-into-row.mov`): making N boxes one row, then a 2×2 grid.**
  Duplicate puts the copy on a **new row**. To make them connected columns, **drag the copy by its canvas type tag onto the
  left/right edge of the other box** (a vertical blue insertion line), so it joins that row. Copy/paste (⌘C/⌘V) with the
  target selected also works. With all 4 in one row, select the **parent** and drag a divider pill wider so the row
  exceeds 100% and the last two wrap, giving 2×2. Box **Width %** does not create columns (it only shrinks the box in its cell).
  *(img: `img/row-01-drag-tile-beside.jpg`, `img/row-02-four-in-a-row.jpg`, `img/row-03-split-2x2.jpg`)*
  **Splitting a row into stacked rows (user tip, agent-verified 2026-09-28): CLICK the dashed vertical divider, don't drag
  it.** With the parent selected on the target device, hover exactly on the dashed line between two columns (not the
  pill). The cursor becomes a hand with a down/left arrow. **Single-click** it and the right-hand column wraps below at
  full width. Repeat for each row (Small: 2 clicks turned 2×2 into 4×1). Screenshots don't show the special cursor, so
  zoom in to find the line's exact x and click on it. Dragging the pill only trades width and never wraps.
- **2026-09-28 (agent MISTAKE): "click away to commit" hit the Visibility bars.** Clicking empty panel space at y≈785–800
  toggled a child's Visibility (it hid the tile body on Desktop), because child Boxes have Visibility bars at the bottom
  of the panel. Commit form values by clicking a **panel label** (e.g. "Height"), never the bottom of the panel.
- **2026-09-28: the `form_input` padding values on a freshly placed Box can be lost** if the Box was re-parented
  afterwards (the grid showed 10/10/10/10 again). Re-check padding after moving Boxes in the tree.
- **2026-09-28 (user tip, confirmed by comparing with the live site): the Dunlop tile images need no overlay.** A 22% black
  layer made them darker than dunlopboots-uk.com. Compare against the live site, not the spec's guess.
- **2026-09-28: new text elements dropped into an existing Section's placeholder go into that Section's inner Box.**
  Watch the tree after every insert.
- **2026-09-28 (agent quirk): the whole editor can scroll up by about 100px** after opening a panel dropdown near the
  bottom (top bar and device dropdown go off-screen). Fix: reset `scrollTop` on the `bg-contrast-100 isolate …`
  wrapper with JS, or scroll the panel back. Check the top bar is visible before using coordinates.

_Still to confirm by use: do other panel values (padding, font size) also vary per device like column widths do? Negative margins, Button panel, Carousel, Card Carousel and Products Carousel settings, undo shortcut, whether canvas or Elements-tree selection is easier for nested Boxes._

## Catalyst built-in components

_No entries yet._

## Workflow / collaboration

- **2026-09-28:** The user prefers uploading all images to the Makeswift library themselves in one batch
  (faster than agent-driven uploads). Provide a flat, prefixed, numbered folder **named after the client**
  (e.g. `assets/Dunlop/`) containing images only, and keep the manifest outside it. The user runs
  Files > Workspace > New > **Upload folder** to create the library folder and upload in one step.
- **2026-09-28:** **Section vs Box.** Use **Section** when content sits within the page's standard margins, and put Boxes, Text and Images inside it. Use a **Box** directly for full-page-width content (hero, full-bleed backgrounds, edge-to-edge grids) or when manual padding is needed.
- **2026-09-28 (Dunlop, build session 1):** Browser tools returned "Browser extension is not connected"
  and `list_connected_browsers` returned `[]`, even though the user had the editor open in Chrome.
  Cause: the Claude in Chrome extension wasn't connected to this Claude Code session. Fix: call
  `tabs_context_mcp` as the very first step, before any spec work. If it fails, ask the user to check the
  extension is running and signed in to the same claude.ai account (restart Chrome if newly installed),
  or to start Claude Code with `claude --chrome`, then retry. Restarting Chrome alone did **not** fix it
  this time (still `[]` afterwards).
- **2026-09-28 (Dunlop, build session 1):** The agent can only drive tabs in its own MCP tab group, so it
  can't see the tab the user already has open. Opening `app.makeswift.com` in a new tab loaded the
  *last-used* workspace/site (Commerce SE Demo → Commerce B2B - Catalyst), not the target. The site switcher
  (click the site name, top-left) only searches sites in the current workspace; **Switch workspace** at the
  bottom of that menu lists workspaces. Fix: at the start, ask the user for the full editor URL of the
  target page and navigate straight to it. What worked in practice: the user opened the BC control panel
  (channel → Overview → **Edit in Makeswift**) inside the agent's tab, which opened the right editor in a
  new tab *within the agent's group*.
- **2026-09-28: learning from the user's screen recordings.** The agent can't watch the screen live. Ask the
  user to record (Cmd+Shift+5) and give the path, then run
  `ffmpeg -i rec.mov -vf "fps=1/2,scale=900:-1,tile=2x2" sheet_%02d.jpg` into the scratchpad. Each 2×2 sheet covers
  8 s of video, so a 55 s clip gives 8 sheets. Read the sheets, then pull full-size frames for the skill with `ffmpeg -ss <t> -frames:v 1` into `references/img/`.
  Ask the user for a one-line narration, because the video shows *what* was done but not *why*.
- **2026-09-28:** The user wants built-in components only (Box, Section, Text, Carousel, Card Carousel,
  Product Carousel) — don't propose custom code components unless asked.
- **2026-09-28 (font comparison, Dunlop): the live site's DIN is closer to plain *Barlow* than to Barlow Condensed.**
  In a side-by-side test (FOOD tile title in Barlow Extra-bold vs INDUSTRY in Barlow Condensed Bold), Barlow matched DIN's
  width and letterforms. Condensed looks too narrow. Pick fonts by comparing one element with the live site before
  building every style on them. Adding a font: Site Theme → Fonts → any dropdown → **Manage fonts** → Browse fonts → search →
  tick → Add fonts → choose weights → Save → Confirm (global).
- **2026-09-28 (verified): changing a shared text style doesn't update elements that were duplicated from a styled element.**
  After switching `Dunlop/Body` from Inter 18 to Barlow Medium 16, the duplicated tile bodies stayed Inter 18. Duplicate
  seems to copy the resolved font/size as local overrides (the style still shows as "Dunlop/Body", and the style says "Used in 1
  place"). Fix: set font and size on each copy, or reapply the style. **Finalise text styles before duplicating elements.**
  Also, Button elements take their font from **Site Theme → Fonts/Button**, not from the `Dunlop/Button` text style (Used in
  0 places). Change the theme fonts to restyle buttons.
- **2026-09-28 (agent limitation): dragging a canvas type tag onto a sibling's edge doesn't work with synthetic
  drags** (`left_click_drag`). Tried twice (tiles, brand statement); the element never moved. Elements-tree drags DO
  work, but only reorder or re-parent (they can't put boxes side by side). For side-by-side columns, ask the user to do the
  one canvas drag, or build columns another way. Duplicate (⌘D works) always lands on a new row.
- **2026-09-28: Text alignment vs margin alignment.** The Text panel has two "center" controls: **Alignment** (text-align)
  and the **Margin** alignment buttons. `find` "Align center" returned the margin one. Ask for "Center Align under the
  Alignment label".
- **2026-09-28 (user-confirmed + agent-verified, recording `15-copy-paste-beside.mov`): side-by-side columns = Copy, then Paste
  placed on the target Box's LEFT EDGE.** Select the source Box → ⋯ Copy (or ⌘C). Select the target Box → ⋯ Paste (or ⌘V).
  Paste enters **placement mode**: hover the very left edge of the target Box (precise, a few px inside) until a **vertical**
  blue line with a "Box" label appears, then click. The pasted Box joins that Box's row as a 50/50 column. Delete the leftover
  original (select it, **Delete key**). **⌘Z undo** works. Cut (⌘X) is not supported. User tip: with a Box selected, **⌘D Duplicate**
  is quicker for a plain copy (lands on a new row), then use copy/paste on the left edge to make columns.

## Making columns: methods compared (verified 2026-09-28, Dunlop brand statement)
| Method | Result | Notes |
|---|---|---|
| **⌘D Duplicate on a Box that is alone in its row (100% width)** | copy lands on a **new row** | fast for making a copy you'll re-place |
| **⌘D Duplicate on a Box that is already in a multi-column row** | copy is added **beside** it; the row rebalances (2 → 3 equal columns) | quickest way to add a 3rd/4th column |
| **Copy (⌘C / ⋯ Copy) → Paste (⌘V / ⋯ Paste) → click the vertical line on the target Box's LEFT edge** | pasted Box joins the target's row (50/50) | works for the agent; the vertical-line spot is precise (a few px inside the left edge). Clicking anywhere else = new row |
| Box tool on a sibling's vertical edge | new empty Box beside | fine for empty columns |
| Drag the canvas type tag onto an edge | beside | **doesn't work with synthetic agent drags**; human only |
| Box Width 50% | only shrinks the Box inside its cell | doesn't create columns |
| ⌘X Cut | not supported | |

**Recommended agent flow for N columns:** build column A → ⌘D (new row) → Copy the copy → Paste on column A's left edge
(now 2 columns; delete the stray row) → then ⌘D inside the row for columns 3..N. **Stack on mobile:** switch to Small, select
the parent, **click** each dashed divider. Delete = select + Delete key; undo = ⌘Z.
- **2026-09-28 (verified, image strip): quickest N-in-a-row build.** Place one element in the container → Copy → Paste →
  click the vertical line at the **container cell's left edge** (the cell edge, not the image's own edge, when the image is
  narrower than its cell) → 2 in a row. Then **⌘D on one of them twice** → 4 equal columns. No leftovers to delete.
- **Split 4-up into 2×2 in one click:** on Medium, select the parent and click the **middle** divider. Everything to the right
  wraps as a new row, so the result is 2 + 2.
- **Gaps between columns:** a Section has no gap controls. Either put the items in a parent **Box** and use its **Row gap / Column
  gap** (user tip, cleaner, and the gap also applies between wrapped rows) or give each item left/right padding (8 + 8 = 16).
  Padding doesn't add a vertical gap between wrapped rows.
- **The canvas click can leave the panel stale, and "Replace" then edits the previously selected image.** For repeated per-item
  edits, select each item in the **Elements tree** (find refs) and zoom in on the panel's file name before replacing.
- **2026-09-28 (agent, unresolved): wrapping existing items in a Box for Row/Column gap.** Only Boxes have gap controls, so
  wrapping needs an intermediate Box. Adding the Box, then tree-dragging the 4 images into it, worked, but **tree drags stack items
  as separate rows** (lost the 4-across layout). Re-making the row inside the Box with Copy → Paste on the child's left edge
  failed twice. The canvas scrolls about 100px right after paste, and when the child cell and the Box share the same left edge,
  the click resolves to the Box line, so it lands as a new row. **Lesson: create the wrapper Box FIRST and build the columns
  inside it** (place one item in the Box → Copy/Paste on its left edge while it's inside a *padded* Box, or ⌘D within an
  existing row), rather than wrapping afterwards. When Box padding is 0, give it temporary padding so the child edge and Box edge
  don't overlap.
- **2026-09-28 (user-confirmed): the paste target line is on the COMPONENT's edge** (the element's own box, e.g. the Image component
  incl. its cell), not necessarily the visible image pixels. Section 7 final build: Section → **Box (padding 0, Row gap 16,
  Column gap 16)** → 4 Images (padding 0). Gaps come from the Box, so they also apply between wrapped rows (Medium 2×2 via
  the middle-divider click). This is the preferred pattern over per-item padding.
- **2026-09-28 (agent caution): in paste-placement mode the canvas drifts (scrolls ~100px) after paste and between hovers.**
  Take a fresh screenshot immediately before the placement click, and press Escape to leave placement mode when done so a stray
  click doesn't place another copy.
- **2026-09-28 (verified): Footer styling = Site Theme → Footer (sliders).** Slots: Background, Border top, Border bottom, Contact
  title, Contact text, Social icon (+hover), Section title, Footer link (+hover), Footer copyright, Focus. Fast recipe: click the
  swatch → the Colors search is auto-focused → type the token name (`Footer`, `Red`, `Charcoal`) or a hex (`FFFFFF`) → the first
  match sits ~113px (named, under a group header) or ~93px (hex) below the row → click it → click the row label to close. Near the
  bottom of the panel the popover flips upward. Dunlop: bg `Dunlop/Footer`, border top Charcoal, border bottom + focus Red,
  contact/section titles/hovers white, links and social icons #D1D1D1.
  **Gotcha:** the "Footer link" colour did NOT change the rendered links in the editor canvas (they stayed dim grey). The value is
  saved, so it may apply only on the live storefront, or the Catalyst footer links may use a different token. Check in preview.
