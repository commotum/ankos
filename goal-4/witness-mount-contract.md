# Goal 4 Witness Mount Contract

Contract ID: `ANKOS-WITNESS-MOUNT-1`

Status: schema frozen; no authorized witness is mounted.

## Purpose

The Goal 4 build remains reproducible from the immutable local OCR and repair overlays. A separate audit mode may verify those overlays against an edition-identical primary witness, but witness bytes never become build inputs and never enter the repaired release.

## Required authorization

Before an automated audit opens a witness, its permission record must explicitly cover private local storage or access, automated or AI-assisted comparison, retention, permitted derivatives, and redistribution boundaries. Public reachability, personal-use language, robots permission, or a downloadable chapter link is not enough.

The current official NKS Online candidate is `REMOTE_INTERACTIVE_ONLY` for planning and `USE_NOT_AUTHORIZED` for bulk or AI-assisted acquisition under the terms observed on 2026-07-14. No bulk download or site mirror is part of Goal 4.

## Mount interface

An authorized witness is supplied at runtime through a caller-owned absolute path. The path, credentials, cookies, tokens, DRM material, and machine-specific identifiers are never written to repository artifacts, logs, repair records, release manifests, or error messages.

Audit mode must require all of the following:

- the mount exists and is a read-only directory or read-only device;
- no component of the path is a symbolic link;
- the permission/license record ID matches the witness manifest;
- the whole-object and per-unit hashes match the manifest before review begins;
- the edition and printing fingerprints match `ANKOS-WITNESS-1` or an explicitly approved alternate witness record;
- the unit manifest and region manifest cover the mounted object without missing, duplicate, reordered, or silently substituted units;
- the audit process cannot write into the mount;
- the build remains bit-for-bit reproducible when the mount is absent.

## Stored metadata

The repository may store public source URLs, edition facts, permission record IDs, hashes, byte counts, page labels, dimensions, page-box metadata, coverage results, review decisions, and blockers. It may not store the primary witness, page rasters, full-page OCR, bounded crops, or before/witness/after composites unless the exact artifact class is separately marked `COMMIT_ALLOWED` in the licensing contract.

## Failure behavior

Missing permission, mount drift, hash drift, terms drift, an unknown edition, an incomplete unit census, inadequate formula/figure/Index legibility, or any attempted write causes audit mode to fail closed. Offline build mode may continue, but its result remains `UNCERTIFIED` and cannot support an unqualified full-repair claim.

## Current unblock path

Obtain written permission from `ip@wolframscience.com` for a complete official born-digital witness or authorized bulk access, including private storage, automated or AI-assisted review, retention, and derivative limits. If that is unavailable, a legitimately acquired matching physical edition can support human visual adjudication, but it does not by itself authorize an automated site mirror or public redistribution.
