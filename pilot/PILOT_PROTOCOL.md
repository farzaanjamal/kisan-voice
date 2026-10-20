# Kisaan Voice — Pilot Protocol (v1)

**Student project. No institutional sponsor. Voluntary, free, low-risk.**
Duration: 7 days. Target: 15–30 farmers, one crop, one area.

> Run **Version A** only if ≥1 agronomist has reviewed the messages you'll send
> and every sent entry has `status: approved`. Otherwise run **Version B**
> (comprehension test) — it needs no approved advice and still produces real data.

## Who can join
Adults (18+) who farm the target crop and own a phone. Participation is optional
and can stop any time by replying **STOP** or telling you.

## What participants receive
- **Version A:** 1–2 approved advisories per day, matched to the current crop stage, for 7 days.
- **Version B:** a one-time set of 8 sample messages, and you ask what each means. No live advice.

## Data collected (the minimum)
`farmer_id`, region, crop, language preference, consent flag/date. **Phone numbers
live only in `farmers.csv`, which is git-ignored and never committed or published.**
No names in public outputs unless the farmer explicitly consents to a quote/photo.

## Storage, retention, deletion
- `farmers.csv` (with numbers) stays on one device, not in the repo.
- Logs used for analysis (`sent_log.csv`, `feedback_log.csv`) contain `farmer_id` only — no numbers.
- Delete the phone-number file within 30 days of the pilot ending, or on request.

## How to stop
Reply **STOP** (auto-marked inactive if the gateway exposes inbound SMS), or tell
the organiser. A stopped farmer receives nothing further.

## Measurement (honest)
Primary: % of farmers who can **explain a message in their own words** (understood/
partly/not) — this beats a yes/no "did you understand". Secondary: delivery rate,
self-reported action taken, text-vs-voice preference. Small samples are reported as
counts ("17 of 22"), never generalised and never with significance claims.

## Ethics guardrails
- No message with `status != approved` is ever sent in Version A.
- No yield or income promises, ever.
- Any dose/chemical/timing must trace to an official source and expert sign-off.
