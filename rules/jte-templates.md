---
paths:
  - "**/*.jte"
---
# JTE Template Rules

## 1. Extract all context fields at the top of the template
Extract fields from the context parameter into local variables before the HTML body.

```html
@param ReadPageContext readContext

!{var formName = readContext.formName();}
!{var sections = readContext.sections();}

<ic-typography variant="h1">${formName}</ic-typography>
```

## 2. Extract self-contained sections into components
Sidebars, modals, panels → separate `.jte` templates. Pages compose via `@template.` calls. A ViewComponent class is only needed if the component transforms data.

## 3. No vanilla JavaScript — use HTMX and Alpine.js
- Server interactions → HTMX (`hx-get`, `hx-post`, `hx-target`, `hx-swap`)
- Client-side interactivity → Alpine.js (`x-data`, `@click`, `x-ref`)
- Vanilla JS → only for HTMX-Alpine bridge functions

Never write custom `fetch`/`XHR`, `document.getElementById`, `addEventListener`, or `onclick`.

## 4. No inline styles
Use CSS classes in `<style>` blocks, not `style=""` attributes.

## 5. Prefer ICDS components over plain HTML elements
See `.claude/rules/icds-usage.md`. Common replacements: `<button>` → `<ic-button>`, `<span>` → `<ic-typography>`, `<a>` → `<ic-link>`. Plain `<div>` for layout is fine.

## 6. No hardcoded colours, font sizes, dimensions, or fallbacks
Use ICDS tokens: `var(--ic-color-*)`, `var(--ic-space-*)`, `ic-typography` variants. No hex values, no `font-size` in CSS, no pixel fallbacks in `var()`.

Available `ic-typography` variants: `h1`–`h4`, `subtitle-large`, `subtitle-small`, `body`, `label`, `label-uppercase`, `caption`, `caption-uppercase`.

## 7. Use class selectors in CSS, not element names
`ic-data-row { }` is unclear and affects every instance. Use `.qa-row { }`.

## 8. Page scripts in external files, not inline `<script>` blocks
Alpine components and HTMX bridges go in `/static/{page}.js`. CSS stays in the template `<style>` block.

## Alpine.js rules
See `.claude/rules/alpine.md` for Alpine-specific rules (directives, reactive bindings, components, HTMX bridging).
