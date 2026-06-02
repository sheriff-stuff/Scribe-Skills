---
paths:
  - "**/*.java"
---
# Java Code Style Rules

## 1. No nested ternary operators (SonarQube S3358)
Use if-else chains instead. Simple (non-nested) ternaries are fine.

```java
// BAD
AnswerType type = !tagList.isEmpty() ? AnswerType.TAGS
        : answerText == null ? AnswerType.UNANSWERED : AnswerType.TEXT;

// GOOD
AnswerType type;
if (!tagList.isEmpty()) {
    type = AnswerType.TAGS;
} else if (answerText == null) {
    type = AnswerType.UNANSWERED;
} else {
    type = AnswerType.TEXT;
}
```
