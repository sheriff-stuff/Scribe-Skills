---
paths:
  - "**/ui/**/*.java"
  - "**/dto/**/*.java"
  - "**/*Dto.java"
  - "**/*.jte"
---

# MVVM Architecture Rules

## The Layers

| Layer                | Where                | Role                                   | Example                          |
| -------------------- | -------------------- | -------------------------------------- | -------------------------------- |
| **Model**            | Java DTOs            | Pure data from backend                 | `FormQuestionAnswerDto`          |
| **Server ViewModel** | Java view components | Transform DTOs into display-ready data | `ReadPage.java` → `QuestionView` |
| **Client ViewModel** | Alpine.js components | UI state and interactivity             | `read.js` → `activeSectionIndex` |
| **View**             | JTE templates        | Structure + declarative bindings       | `ReadPage.jte`                   |

**Where does logic go?** Backend data → compute in Java. UI state (visible, selected, open) → Alpine. Templates bind to both but compute neither.

## 1. DTOs are pure data

Records have only auto-generated accessors. No display methods, no computed fields.

```java
// BAD
public record FormQuestionAnswerDto(String question, String answer) {
    public String displayLabel() { return question + ": " + answer; }
}

// GOOD
public record FormQuestionAnswerDto(String question, String answer) {}
```

## 2. Templates bind, they don't compute

JTE renders structure and binds values. Alpine directives (`x-bind`, `x-show`, `@click`) are declarative bindings, not logic. Anything that needs computation belongs in the view model.

```html
<!-- BAD: template computes -->
@if(dto.status().equals("APPROVED") && dto.reviewDate() != null)
<span>${dto.reviewDate().format(DateTimeFormatter.ofPattern("dd MMM yyyy"))}</span>
@endif

<!-- GOOD: template binds to pre-computed value -->
@if(view.isReviewed())
<span>${view.formattedReviewDate()}</span>
@endif
```

## 3. View models pre-compute display values

The Java view component (e.g. `ReadPage.java`) transforms DTOs into view models with formatting, filtering, grouping, and semantic flags already done. Controllers pass view models to templates, not raw DTOs.

**Prefer semantic properties over inline expressions.** If the template makes a decision, the view model gives it a name. "Trivially derivable" doesn't disqualify a property — `count > 0` earns `hasComments()` because the name communicates intent.

```html
<!-- BAD -->
@if(section.index() > 0)
<!-- GOOD -->
@if(section.hasPrevious())

<!-- BAD -->
@if(q.commentCount() > 0)
<!-- GOOD -->
@if(q.hasComments())
```

```java
// BAD: raw DTO passed to template
model.put("dto", formDto);

// GOOD: view model with pre-computed values
var questionViews = formDto.questions().stream()
    .map(q -> new QuestionView(q.question(), q.answer(), q.question() + ": " + q.answer()))
    .toList();
model.put("questions", questionViews);
```

## 4. View models live with the code that creates them

Co-locate view model records inside the page class that builds them. Only separate into their own file if genuinely shared across multiple pages.

```java
// GOOD
public class FormsPage {
    public ViewContext render(List<FormDto> dtos) {
        List<FormViewModel> vms = dtos.stream().map(...).toList();
        ...
    }

    public record FormViewModel(long id, String name, String state) {}
}
```

## 5. Order class members top-down

Public API before private helpers before utilities before inner types. Within private methods, domain-specific before generic.

1. Fields — constants, then instance
2. Constructor(s)
3. Public methods
4. Private instance methods
5. Private static methods — domain-specific first, generic utilities last
6. Inner types — enums, records, nested classes

```java
// GOOD
private static String getDisplayText(FormQuestionAnswerDto dto) { ... }
private static String getAnswer(FormQuestionAnswerDto dto) { ... }
private static boolean notBlank(String s) { ... }  // generic utility last

public enum AnswerType { ... }
public record QuestionView(...) {}
```

## Review Checklist

When reviewing or modifying these files, check for:

- **DTOs with logic** — any method beyond auto-generated accessors
- **Templates computing values** — string/date formatting, conditional business logic, inline comparisons like `count > 0` or `index > 0` in `.jte` files. Pre-compute as semantic properties.
- **Raw DTOs passed to templates** — controllers should build view models first
- **Logic in controllers** — display logic belongs in view models
- **View models doing backend work** — view models only transform data, never fetch or mutate
- **Wrong layer for the logic** — data formatting in Alpine (should be Java), UI state tracked in Java (should be Alpine)
- **Separated view models** — not co-located with the page class that creates them
- **Misordered members** — generic utilities above domain-specific, inner types above methods
