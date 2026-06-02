# URL resolution

Maps the remote URLs that appear in `proposed-tickets/` to local checkout paths, so the
`ticket-reviewer` can open a linked page or file and check whether a ticket duplicates detail
the source already owns (Body Rule **Don't duplicate spec detail from the source doc**). The
reviewer reads this file from the project root and never fetches a URL over the network.

Without a mapping for a given URL, the reviewer cannot read that source: it marks the
duplicate-spec check `UNVERIFIED` for the ticket that carries the URL and names the URL in its
batch `NOTES` line. Extend the mappings below so those checks can run.

## Format

One mapping per line, `<url-or-prefix> => <local-path>`:

- The left side is a full URL or a URL prefix. When several prefixes match, the longest wins.
- The right side is a path relative to this project root (a sibling checkout reached with `../`
  is fine).
- Lines beginning with `#` are comments.

Work-item URLs (issues, MRs, PRs) have no local equivalent — leave them unmapped; the reviewer
skips them rather than reporting them unresolved.

## Mappings

# No project-specific mappings yet. Add entries as the project's wikis and repos are checked out
# locally, for example:
#
# https://gitlab.example.com/acme/product-wiki/-/blob/main/ => ../product-wiki/
# https://gitlab.example.com/acme/backend/-/blob/main/      => ../backend/
