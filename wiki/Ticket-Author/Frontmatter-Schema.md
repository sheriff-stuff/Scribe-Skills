# Frontmatter Schema

| Field    | Required | Type                | Notes                                                                               |
| -------- | -------- | ------------------- | ----------------------------------------------------------------------------------- |
| `title`  | Yes      | string              | Non-empty                                                                           |
| `type`   | No       | string              | Only accepted value is `epic`                                                       |
| `labels` | No       | list                |                                                                                     |
| `weight` | No       | integer             |                                                                                     |
| `epic`   | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same branch |

List fields (`labels`) accept YAML inline `[a, b]` or block format.
