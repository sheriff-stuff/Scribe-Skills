# Frontmatter Schema

| Field       | Required | Type                | Notes                                                                           |
| ----------- | -------- | ------------------- | ------------------------------------------------------------------------------- |
| `title`     | Yes      | string              | Non-empty                                                                       |
| `type`      | No       | string              | Only accepted value is `epic`                                                   |
| `labels`    | No       | list                | Each label must already exist in the project                                    |
| `assignees` | No       | list                | GitLab usernames                                                                |
| `milestone` | No       | string              | Milestone title or ID                                                           |
| `weight`    | No       | integer             | Non-negative                                                                    |
| `due_date`  | No       | string              | `YYYY-MM-DD`                                                                    |
| `epic`      | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same MR |

List fields (`labels`, `assignees`) accept YAML inline `[a, b]` or block format.
