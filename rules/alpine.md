---
paths:
  - "**/*.js"
  - "**/*.jte"
---
# Alpine.js Rules

**Core principle:** Methods update state. The template declares behaviour via bindings. Never manipulate the DOM imperatively when a directive can do it reactively.

## 1. Use Alpine directives for events, not vanilla handlers
Use `@click`, `@keydown`, `@submit`. Never `onclick`, `addEventListener`.

## 2. Use `x-bind` for reactive attributes, not imperative DOM
Attributes that change based on state use `x-bind` (`:` shorthand). Never `classList.add/remove`, `setAttribute`, or `element.style` in methods — use `x-bind:class`, `x-show`, `x-text` in the template. Use `x-ref`/`$refs` only when no declarative alternative exists.

```javascript
// GOOD: method just updates state
showSection(index) {
    this.activeSectionIndex = index;
}
```
```html
<!-- GOOD: template declares via bindings -->
<ic-section-container x-bind:class="{ 'hidden': ${section.index()} !== activeSectionIndex }">
```

## 3. Register components with `Alpine.data()`, not global functions
Use `Alpine.data()` inside an `alpine:init` listener. Global function data providers are deprecated in V3.

```js
// GOOD
document.addEventListener('alpine:init', () => {
    Alpine.data('readPage', (sectionCount) => ({
        activeSectionIndex: 0,
        showSection(index) { this.activeSectionIndex = index; }
    }));
});
```

## 4. Bridge HTMX to Alpine with `Alpine.$data()`
HTMX handlers run outside Alpine scope — `$refs` and `this` unavailable. Use a global bridge function with `Alpine.$data()`.

```html
<ic-button hx-get="/comments/1" hx-on::before-request="onBeforeLoad(event, 1)">
</ic-button>
<script>
    function onBeforeLoad(event, id) {
        var data = Alpine.$data(event.target.closest('[x-data]'));
        if (!data.openComments(id)) { event.preventDefault(); }
    }
</script>
```

## 5. Server-render default visibility alongside `x-bind:class`
Without a server-side default `class`, all elements flash visible before Alpine boots.

```html
<!-- GOOD: server renders initial state, Alpine takes over -->
<ic-section-container
    class="${section.index() == 0 ? "" : "section-hidden"}"
    x-bind:class="{ 'section-hidden': ${section.index()} !== activeSectionIndex }">
```

## 6. Guard `@click.outside` with a skip flag
When a button outside a panel opens it, `@click.outside` fires on the same click. Use `_skipClose` + `$nextTick`.

```javascript
openPanel() {
    this._skipClose = true;
    this.panelOpen = true;
    this.$nextTick(() => { this._skipClose = false; });
},
closePanel() {
    if (this._skipClose) return;
    this.panelOpen = false;
}
```
