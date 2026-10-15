# Debug-first modular source rule

One feature operation per independently testable file. Keep exact asset filenames, no embedded image data in scripts. A build artifact never replaces editable source. Each module must have an indexed purpose, inputs, outputs, dependencies, dependents, tests, and related fault symptoms.

The source-of-truth files for discovery are `module_index.json` and `fault_map.json`. Do not claim old game assets migrated until they are actually extracted and path-verified. The imported V3 application is incomplete (its `index.html` is missing); the existing main branch remains unchanged.

## Debug workflow
1. Record symptom, thread ID or exact asset path.
2. Read `fault_map.json` to identify the first 1–3 likely files.
3. Run the corresponding test. Change one module.
4. Run affected tests and update maps in the same commit.

## Migration
Preserve old versions. Identify V34+ source and copy original assets as individually named files with SHA256 manifests. Extract scripts out of HTML into distinct UI/controller/data files. Keep adapter boundaries stable while replacing old logic. Do not commit secrets, logs, or personal transcript data to this public repository.
