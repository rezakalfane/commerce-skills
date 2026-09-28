# Built-in components and controls

Status legend:
- **verified (date)**: used by an agent session
- **user-confirmed (date)**: the user showed it in a screenshot or described it
- **unverified**: expected from docs or general knowledge; confirm on first use and update this file

How to select a parent: ESC → hover the element → hover its top-left type tag → pick from the ancestor stack (Box / Box / Page). *(user-confirmed 2026-09-28)*

**Columns / responsive grid:** put sibling elements side by side in one parent (they join one row) → select the parent → drag the pill handles between columns. Switch devices (Desktop >1281 / XL 1280 / Large 1024 / Medium 768 / Small 640) and widen columns to make the next ones wrap to a new row. *(user-confirmed 2026-09-28)*

**UI screenshots** (`img/`, from the Dunlop session on 2026-09-28; the Catalyst "Europe Headless - B2B" site):
| File | Shows |
|---|---|
| `picker-01-component-catalogue.jpg` | + picker: Basic / Catalog / Catalyst / Layouts / Sections |
| `theme-01-site-theme-panel.jpg` | Site Theme: Fonts + per-component theme settings |
| `design-01-color-edit.jpg`, `design-02-text-style-edit.jpg` | Design tab colour and text-style popovers |
| `panel-box.jpg`, `panel-text.jpg`, `panel-image.jpg` | Box / Text / Image property panels |
| `files-01-new-menu.jpg`, `files-02-workspace-folder-uploaded.jpg` | Files dialog: New ▾ (Upload folder), Workspace / Dunlop |
| `select-parent-01…02-*.jpg` | **Parent navigation**: expanded type-tag stack Box / Box / Page → outer Box selected |
| `boxes-01…03-*.jpg` | **Boxes**: insert a Box inside a Box (blue line) → second Box beside it → siblings share one row |
| `responsive-01…05-*.jpg` | **Responsive**: pill handles on the parent → device dropdown → Medium 5-up → drag to widen → wrapped 2-up |
| `visibility-01…03-*.jpg` | Page Visibility bars: per-device show/hide (grey = visible, white = hidden) |

How to add any component: **+** in the tool strip → pick it in the searchable picker → click on the page where the blue insertion line shows. **ESC** cancels. *(user-confirmed 2026-09-28)*

## Tool-strip components (Makeswift base)
| Component | Use for | Controls | Status |
|---|---|---|---|
| **Box** | The layout workhorse: containers, rows, grids, image-background bands, overlays | **Backgrounds (+)** with stacked image and colour layers; Width px/%; Height auto/stretch; Align items; Margin (auto ok); Padding; Border; Corners; Shadows; Row gap; Column gap; Animate box in; Animate items in; Hide placeholder (inner Box) or **Visibility** (seen on a parent Box; per-breakpoint? confirm). **No absolute/relative positioning. Columns = siblings plus drag handles on the parent** (not a panel control). | user-confirmed 2026-09-28 |
| **Text** | Headings and copy | Content; Block (Paragraph / H1…); Text style (saved style, or font, weight, colour/opacity, size, line height, letter spacing, U/S/TT); Alignment; Inline (sup, sub, code); On Click (page / new tab); Width px/%; Margin | user-confirmed 2026-09-28 |
| **Image** | Single image | Image (Choose → Files); Alt text; On click (page / new tab); Width px/%; Margin; Padding; Border; Corners; Shadows; Opacity; Priority | user-confirmed 2026-09-28 |
| **Button** | CTA | text, link, variant/colours, size (expected) | unverified |

## Picker catalogue (Catalyst site "Europe Headless - B2B", 2026-09-28)
| Group | Components |
|---|---|
| Basic | Accordion, Card, **Card Carousel**, **Carousel** |
| Catalog | Product Card, **Products Carousel**, Products List |
| Catalyst | Customer Group Slot |
| Layouts | **Section**, Sticky sidebar |

| Sections (prebuilt) | 2-Column Split, 2-Column with Image, **4-Column with Icons**, **Category Grid**, Custom Component, Featured Card Carousel, Featured Product Carousel, Featured Product List, Large Quote, **Slideshow**, … (the list scrolls) |

**Products Carousel** *(verified 2026-09-28, panel seen on the existing homepage)*: Width, Margin, **Product collection** (dropdown, e.g. *Newest*), **Max collection items** (12), **Additional products (+)** (hand-picked), Aspect ratio (5:6), Text color scheme (Light), Show scrollbar, Show buttons, Hide overflow. This answers the open question: it supports both a collection source and hand-picked products.

**Section**: + → Layouts → Section; an empty one shows as a grey dashed full-width band *(user-confirmed 2026-09-28)*; panel controls unverified.

**Section vs Box** *(user convention 2026-09-28)*: use **Section** (Layouts) for content within the standard page margins, and put Boxes, Text and Images inside it. Use a **Box** directly for full-page-width content (hero, full-bleed backgrounds, edge-to-edge grids) or when manual padding is needed.

Controls for everything in this table are **unverified**. Before hand-building a layout from Boxes, check whether a prebuilt Section already does it. Likely matches: hero → Slideshow; icon row → 4-Column with Icons; category tiles → Category Grid or Featured Card Carousel; two-column copy → 2-Column Split.

## Site-wide styling
- **Site Theme** (Content → Elements → Site Theme): Fonts (Heading, Body, Accent) plus theme settings for Accordion, Button, Card, Carousel, Footer, Header, Logo, Price label, Product card, Section, Slideshow. *(user-confirmed 2026-09-28)*
  - **Button theme** *(verified 2026-09-28)*: Font, plus Primary / Secondary / Tertiary / Ghost × (Background, Background hover, Text, Border), and Focus. No radius or padding.
  - **Fonts** *(verified 2026-09-28)*: code-managed fonts on Catalyst are DM Serif Text, Inter (300/400/500 only) and Roboto Mono; add more via Manage fonts → Browse fonts (Google Fonts). Saving fonts is global and can't be undone (confirm dialog).
- **Design tab:** Colors and Text styles, both reusable tokens with `/` grouping and "Used in N places". *(user-confirmed 2026-09-28)*
- **Page Metadata** (nothing selected): Online, Path, Title, Description, Social Image, noindex, Canonical, Sitemap, Snippets. *(user-confirmed 2026-09-28)*

## Open questions for the next UI session
- Besides column widths, which panel values are per device (padding, font size, Visibility)?
- Are negative margins allowed?
- Can Carousel or Slideshow slides use different images per breakpoint? What controls do they have (autoplay, height, link per slide)?
- Products Carousel: hand-picked products, or a category/collection source?
- Button panel controls; undo shortcut.
