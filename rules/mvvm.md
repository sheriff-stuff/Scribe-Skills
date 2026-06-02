---
paths:
  - "**/*.java"
  - "**/*.jte"
---
# MVVM Architecture Rules

Full reference with examples: `.docs/principles/mvvm.md`

## The Layers

| Layer | Where | Role |
|-------|-------|------|
| **Model** | Java DTOs | Pure data from backend |
| **Server ViewModel** | Java view components | Transform DTOs → display-ready data |
| **Client ViewModel** | Alpine.js components | UI state and interactivity |
| **View** | JTE templates | Structure + declarative bindings |

**Where does logic go?** Backend data → compute in Java. UI state (visible, selected, open) → Alpine. Templates bind to both but compute neither.

## 1. DTOs = pure data
No logic methods. Records have only auto-generated accessors.

## 2. Templates = structure and bindings
JTE templates render and bind — they don't compute values. Alpine directives are declarative bindings, not logic.

```html
<!-- BAD: template computes -->
@if(dto.status().equals("APPROVED") && dto.reviewDate() != null)
    <span>${dto.reviewDate().format(DateTimeFormatter.ofPattern("dd MMM yyyy"))}</span>

<!-- GOOD: template binds to pre-computed value -->
@if(view.isReviewed())
    <span>${view.formattedReviewDate()}</span>
```

## 3. Server view models = data transformation
Transform DTOs into view models with pre-computed display values. **Prefer semantic properties over inline expressions.** If the template makes a decision, pre-compute it with a meaningful name.

```html
<!-- BAD --> @if(section.index() > 0)
<!-- GOOD --> @if(section.hasPrevious())

<!-- BAD --> @if(q.commentCount() > 0)
<!-- GOOD --> @if(q.hasComments())
```

## 4. View models live with the code that creates them
Co-locate view model records inside the page class that builds them. Only separate if genuinely shared across multiple pages.

## 5. Order class members top-down
1. Fields (constants, then instance)
2. Constructor(s)
3. Public methods
4. Private instance methods
5. Private static methods (domain-specific first, generic utilities last)
6. Inner types (enums, records)
