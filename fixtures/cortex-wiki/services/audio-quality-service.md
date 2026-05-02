---
title: Audio Quality Service
category: services
owners: [ml-team]
last_updated: 2026-04-12
---

# Audio Quality Service

## Responsibility

Annotates a Recording with Quality Flags warning of audio issues that affect transcription accuracy. Runs alongside transcription; does not block it.

## Detectors

- **Low SNR** — sustained noise floor close to speech level.
- **Overlap** — multiple simultaneous speakers longer than 500 ms.
- **Silence** — gap longer than 30 seconds.
- **Clipping** — peak amplitude saturation.
- **Low confidence** — emitted post-hoc when the Transcript contains a contiguous run of low-confidence Utterances.

## Output

A list of Quality Flags written to the database. Flags are emitted incrementally during the scan and published on the realtime channel as `job.flagged` events.

## Related

- [Quality Flag](../domain/quality-flag)
