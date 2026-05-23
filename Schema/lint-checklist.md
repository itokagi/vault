# Lint Checklist

Run before every commit. All items must pass.

## Wiki Notes

- [ ] Each note uses exactly one allowed tag: `topic`, `concept`, `entity`, `project`, or `log`
- [ ] `source_count` equals the number of entries in `sources`
- [ ] Every path in `sources` points to an existing file under `Raw/Sources/`
- [ ] `status` is one of: `seed`, `growing`, `evergreen`
- [ ] `created` and `updated` are valid dates in `YYYY-MM-DD` format
- [ ] Note is filed in the correct folder for its tag

## Raw Sources

- [ ] Frontmatter includes `Title`, `Author`, `Reference`, `Created`, `Processed`, and `tags`
- [ ] `tags` includes `source`
- [ ] If `Processed: true`, at least one Wiki note exists with this source in its `sources` field

## Catalog

- [ ] `Wiki/catalog.jsonl` exists
- [ ] Every compiled Wiki note has an entry in the catalog
- [ ] Each catalog entry includes `path`, `title`, `tag`, `topics`, `sources`, and `updated`

## Source Manifest

- [ ] `Schema/source-manifest.jsonl` exists
- [ ] Every file in `Raw/Sources/` has an entry
- [ ] Processed sources show `covered_by` pointing to existing Wiki notes

## Audit

- [ ] `audit_public.py` passes with no secrets, private paths, or plugin/cache state
