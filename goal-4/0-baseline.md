# Goal 4 Starting Baseline

This record freezes the authoritative inputs immediately before the goal
folders were re-indexed and before the whole-book taxonomy audit began.
Goal 4 must independently reverify these facts during its guardrail and
corpus-map stages; this record is a drift detector, not inherited proof of
audit completeness.

## Repository Baseline

- Pre-reindex commit:
  `523bcd621abccaca403aa2c5b835e082b4e6fd09`
- Canonical book Git tree:
  `535d2682831132b8b520daaff611eb0b549a4406`
- Completed Goal 1 Git tree, including the then-located Goal 2 handoff:
  `83566243cd8bffd8dab687d7ff00fd2b9323674e`
- Original Goal 2 handoff Git blob:
  `45874def7baa5433b2b2933e0a0c621bee85bb44`

The handoff blob was moved without content changes from
`goal-1/goal-2-handoff.md` to `goal-2/goal-2-handoff.md` during preparation.

## Canonical Corpus

- Book documents: 29
- Navigation documents: 2 (`README.md` and `Contents.md`)
- JPEG images: 1,607
- Total files: 1,638
- Aggregate SHA-256:
  `b642dbded84170a0c3872622a19b55f6dc0ee4f5f7aff843e18eee175c85e62c`

The aggregate is reproducible from the repository root with:

```bash
(
  cd ref/A-New-Kind-of-Science
  find . -type f -print0 |
    sort -z |
    xargs -0 sha256sum |
    sha256sum
)
```

The digest binds each relative path and each file's SHA-256 digest.

## Planning and Catalog Inputs

| Input | Git blob | SHA-256 |
|---|---|---|
| `goal-2/goal-2-handoff.md` | `45874def7baa5433b2b2933e0a0c621bee85bb44` | `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192` |
| `ref/notes/CA-Types.csv` | `84a114a02baa94f6cd866ce9d3bb176d62d94778` | `26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73` |
| `api.md` | `873e43b380fc0bf77e39bdcf6121026ca206481d` | `003db8f853dd9f976c642f4a8417edd0b729bc276c4ac0f7136caeb1a97391cd` |
| `simple_programs.md` | `62dbda1ba241a057e5b51feab0fbab24b2310b71` | `0120bcd1237c774aa98bbc5b6bebab24418aae7c82bf219ccb4b9c762d74ed54` |
| `ref/notes/ca-scaffold.py` | `a04587c7f8803bf6691037841e140f2667022e2c` | `371d930d26119335647c6c693f1293cec4a76c6db91a73a75711aebe971ff202` |

During blind discovery, Goal 4 may verify these inputs and their continued
availability but must not use their taxonomy or API conclusions. They become
active comparison inputs only at the reconciliation stages defined in
`0-plan.md`.
