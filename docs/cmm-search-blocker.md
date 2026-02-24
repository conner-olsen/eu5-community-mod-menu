# CMM Search/Sort Blocker Report

Date: 2026-02-24

## Goal that could not be shipped

- Case-insensitive substring search over mod display name.
- A-Z sorting of filtered result rows.
- Dynamic row labels from registered `display_name_key` metadata.

## What was implemented safely

- `cmm_register_mod` now accepts `display_name_key` and stores mod-id keyed metadata variables.
- Core and example integrations now pass `display_name_key` (and description key for future metadata use).
- Debug rows were removed from runtime UI.
- Left-list rendering moved to `dynamicgridbox` for best-effort compaction behavior.

## Probe matrix and findings

1. GUI string function discovery in vanilla files
- Searched vanilla GUI usage for candidate functions (`Contains_*`, `StartsWith_*`, `ToLower_*`, `Sort_*`, etc.).
- Found only basic operations like `EqualTo_string`, `StringIsEmpty`, `Concatenate`, and variable-system equality checks.
- No validated substring or string-sort function surfaced.

2. UI variable-system capabilities
- Vanilla usage exposes: `GetVariableSystem.Set`, `.HasValue`, `.Exists`, `.Clear`, `.Toggle`.
- No `GetVariableSystem.Get` (or equivalent string retrieval) was found in vanilla usage.

3. Direct editbox text fetch probes
- Prior runtime probes using direct editbox text fetch (`PdxGuiEditboxGetText(...)`) produced localization/data fetch failures in logs.
- Result: unsafe for shipping path in current build.

4. Mod metadata to list-row mapping
- Script variables support mod-id keyed metadata writes.
- No validated engine path was found to enumerate mod-id keyed metadata and resolve arbitrary localization keys per dynamic row in GUI script.

5. Visible-slot cache variables (`cmm_visible_slot_<index>`)
- The requested cache model requires runtime-computed variable names per visible row index.
- No validated effect-side mechanism was found to safely create/update arbitrary indexed variable names from runtime loop counters without introducing a static cap.

## Why this blocks substring/sort/name rendering

- Substring matching requires a string `contains`-style operator that is not exposed in validated GUI scripting functions.
- A-Z sorting requires a string compare/sort key pipeline for custom rows that is not exposed for this custom data model.
- Dynamic label rendering from `display_name_key` requires safe retrieval/enumeration of stored metadata keys, which is not exposed in validated GUI APIs.

## Shipping decision

- Shipped stable registry/API and non-debug UI cleanup.
- Deferred true substring/A-Z/name-key row rendering until a validated engine-safe API path is available.

## Next unblocking requirement

Any one of the following would unblock full implementation:

- A validated GUI string function for substring matching (`contains` semantics).
- A validated custom list sort/search API for scripted data (equivalent to C++ `SortSearch` contexts).
- A validated mechanism to enumerate and fetch arbitrary scripted metadata keys for dynamic rows.
