# Goal 4 Publication and Promotion Contract

Contract ID: `ANKOS-PROMOTION-1`

Status: Frozen by Stage 1.

## Authorized operation

Goal 4 authorizes building and, after every release gate passes, publishing a local sibling edition at `ref/A-New-Kind-of-Science-Repaired/`.

The legacy root remains `ref/A-New-Kind-of-Science/`. The sibling is an intentional additive extension to the aspirational layout in `ref/notes/context/REFACTOR_TARGET.md`; Goal 4 does not edit that target document or pretend it already specifies the repaired sibling.

## Sibling publication

- Build from frozen raw inputs plus overlays in a fresh same-filesystem staging directory.
- Resolve paths component-wise. Accept the prefix-named sibling; reject equality with the legacy root, a true descendant of it, `..` aliases, and any symlink alias into it.
- The publication target must be absent, empty, or exactly owned by a trusted prior-release manifest stored under `goal-4/releases/`.
- Never trust a target-local manifest by itself. For an owned target, every path, file type, mode, size, and hash must equal the externally trusted manifest; symlinks and unowned extras fail.
- Compute a content-addressed release ID from frozen input, overlay, tool, contract, and output-manifest digests.
- Validate disk capacity, witness audit certificate, all ledgers, two clean-build equality, inverse replay, compatibility behavior, and repository scope before publication.
- Publish by atomic same-filesystem rename. Test interruption immediately before and after the rename; the observable target must be one complete release, never a mixture.
- Preserve trusted prior release manifests/overlays under `goal-4/releases/` and retain an explicit hash-verified previous-release selection/rollback command.
- Do not overwrite or delete the last known-good release until the new release and rollback path are verified.

## Separate authorization boundary

The following are not authorized by Goal 4:

- editing, replacing, deleting, moving, or renaming any legacy corpus file;
- changing Goal 1/3 source paths, hashes, recursive exclusions, citations, or oracle expectations;
- promoting repaired files into the legacy root;
- deleting malformed legacy splits;
- committing, pushing, hosting, or externally redistributing copyrighted witness/repaired material beyond the licensing contract.

A future legacy promotion requires a new explicit user instruction and a separately reviewed migration plan with complete consumer inventory, dry-run citation/path mapping, backup hashes, atomic switch, post-switch Goal 1/3 behavior comparison, and tested rollback. No authorization token is inferred from successful sibling publication.

## Failure conditions

Publication fails on a nonempty unowned target, symlink, hash drift, unclosed authorial or review blocker, missing audit witness, incompatible license state, behavior-digest change, incomplete prior-release backup, or inability to perform an atomic switch. A failed publication leaves the validated staging tree and evidence for diagnosis but never merges it into the target.
