---
paths:
  - "**/*.jte"
---
# ICDS Component Usage Rules

## 1. Use the most specific ICDS component for the job
Don't approximate with generic components. Reference: `.docs/icds/components/`.

| Situation | Wrong | Right |
|-----------|-------|-------|
| Empty content | `<ic-typography>No items</ic-typography>` | `<ic-empty-state heading="No items">` |
| Loading | Custom spinner CSS | `<ic-loading-indicator>` or `<ic-skeleton>` |
| Inline feedback | `<ic-typography>Error</ic-typography>` | `<ic-alert variant="error">` |
| Transient notification | `window.alert()` | `<ic-toast>` |

## 2. Badge: always set `accessible-label` and `max-number`

```html
<ic-badge slot="badge" label="${count}" max-number="99"
    variant="info" accessible-label="${count} comments on this question">
</ic-badge>
```

## 3. Badge size must match parent component size

## 4. Data list: always include a `heading` attribute

## 5. Use ICDS slots correctly
Key slots: `ic-data-row` → `value`, `end-component`; `ic-empty-state` → `actions`, `image`; `ic-badge`/`ic-button` → `badge`.

## 6. Style through CSS custom properties, not raw CSS
Shadow DOM components need their exposed custom properties (e.g., `--ic-typography-color`), not raw `color` or `font-size`.

## Quick reference: commonly missed components
- Empty states → `ic-empty-state`
- Status → `ic-status-tag`
- Badges → `ic-badge`
- Chips → `ic-chip`
- Loading → `ic-loading-indicator`, `ic-skeleton`
- Messages → `ic-alert`
- Notifications → `ic-toast`
- Menus → `ic-popover-menu`
- Expandable → `ic-accordion`
