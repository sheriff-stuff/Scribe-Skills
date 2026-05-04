# Versioning Strategy

The repo follows SemVer with a release-branch workflow.

## Version identity

Each release has a tag `vX.Y.Z` on the commit that ships it.

## Branch model

- `master`: the current released version.
- `vX.Y`: the release branch for the upcoming release. Feature work for that release lands on this branch.
- Feature branches branch off the relevant release branch and merge back into it.
- Cutting a release merges the release branch into `master` and creates a matching `vX.Y.Z` tag.

## Feature flow

- A feature branch is created off the relevant release branch.
- Wiki pages describing the feature are written on the feature branch.
- Tickets are created from those wiki page changes.
- Implementation lands on the feature branch and merges into the release branch.
- When the release branch ships, it merges into `master` and is tagged.

## Generic versioning concerns

Hotfixes, forward-ports, long-lived release branches, and breaking changes are handled with the standard release-branch workflow.
