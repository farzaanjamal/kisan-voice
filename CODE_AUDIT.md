# Code audit — original upload vs v2

Formal list of what was wrong or missing in the **originally uploaded** code
(`encoder.py`, `decoder.py`, `regional_selector.py`, the three v1 dictionaries,
README) and what v2 does about it. Severity: critical / major / minor.

| # | Issue | Sev | Status in v2 |
|---|---|---|---|
| 1 | **Dictionary metadata inflated.** `kpk_wheat` claimed 16 problems / 14 actions but defined 8 / 3; `sindh_rice` claimed 18 / 15 but defined 11 / 5 (punjab was consistent). | major | **Fixed** — v2 drops hand-written counts; counts are derived from content, and `D2_COVERAGE.md` states gaps honestly. |
| 2 | **District selection silently broken for Punjab.** `regional_selector.select_by_district` reads `region_info.districts`, but `punjab_cotton_v1.json` has no `region_info`, so Punjab districts never matched and it fell back to default without warning. | major | **Addressed** — v2 selects by region+crop (`select_dictionary`); district lookup to be re-added once district lists exist. |
| 3 | **No structural validation.** Original only checked that 5 top-level keys existed; malformed entries, duplicate ids, or missing languages passed silently. | critical | **Fixed** — JSON Schema + semantic checks; every error names the entry id. |
| 4 | **Encoding was string concat only.** No binary/BLE form, no SMS segment counting, no templates — so the compression and offline-relay claims were unverifiable. | major | **Fixed** — SMS form + binary form + GSM-7/UCS-2 segment counting + typed slots, all tested. |
| 5 | **No safety on version/unknown codes.** A wrong or stale code could resolve to the wrong message. | critical | **Fixed** — unknown codes and dictionary-version mismatches raise; they never render a wrong message. |
| 6 | **README overclaimed shipped features.** Audio playback, SMS sending, mesh, dashboards described as built; the mp3s and mesh did not exist. | major | **Addressed** — `CAPABILITIES.md` splits built vs planned; audio is a generator you run, mesh is a simulator clearly labelled. |
| 7 | **Two parallel codebases.** An early `kisan_voice` mesh package and the `kisaan_voice` v2 package diverged. | minor | **Merged** — mesh now lives in `kisaan_voice/mesh_sim.py` and uses the real `encode_binary` packet size; the early package is superseded. |
| 8 | **CLI example wouldn't validate.** `encoder.py`'s help hardcodes `C P01 A03 !2 U`, which fails against `kpk_wheat` (no `C` crop). | minor | **Fixed** — CLI `demo` reads a real dictionary and only shows valid codes. |
| 9 | **No tests.** README referenced a `tests/` dir that wasn't present. | major | **Fixed** — 14 passing tests; core modules 81–100% covered. |
| 10 | **Dictionary cache never invalidated** (`_dictionary_cache` keyed by path). | minor | Acceptable for now; note for a future reload flag. |

## Honest coverage note
Core logic coverage: `segments.py` 100%, `encoding.py` 92%, `dictionary.py` 81%,
`templates.py` 72%. The simulator, benchmark and CLI are exercised by their run
scripts (`run_s1.py`, `benchmark.py`, `demo`) rather than unit tests, which is why
the whole-repo number is lower — worth adding unit tests for those next.
