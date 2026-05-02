"""Canonical spec for the Cortex mock wiki.

Every page, the glossary, and the cross-link base URL live here. The
generator (generate.py) renders this into markdown.

When adding or changing content, prefer editing this file and re-running
the generator over hand-editing the rendered .md files (those will be
overwritten on the next regeneration).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


LINK_SENTINEL = "@@WIKI@@/"


@dataclass
class Page:
    path: str  # relative to wiki root, e.g. "domain/utterance.md"
    title: str
    category: str
    sections: list[tuple[str, str]]  # (heading, body) — heading "" skips the H2
    frontmatter: Mapping[str, object] = field(default_factory=dict)


def link(slug: str, label: str) -> str:
    """Wiki-internal link. The slug is the wiki-root-relative page path
    (with or without `.md`); the generator rewrites the sentinel into a
    relative path from the linking page at render time."""
    slug = slug.removesuffix(".md")
    return f"[{label}]({LINK_SENTINEL}{slug})"


# ---------------------------------------------------------------------------
# Glossary — single source of truth for vocabulary
# ---------------------------------------------------------------------------

GLOSSARY: dict[str, str] = {
    "Recording": (
        "An audio source ingested into Cortex. Wraps the original media "
        "file, the user-supplied metadata, and pointers to derived "
        "processing artifacts. The lifecycle root: Transcripts, "
        "Extractions, and Notes all hang off a Recording."
    ),
    "Transcript": (
        "A speaker-attributed record of speech in a Recording, composed "
        "of an ordered sequence of Utterances. There is exactly one "
        "Transcript per Recording."
    ),
    "Utterance": (
        "A single contiguous span of speech attributed to one Speaker "
        "Profile within a Transcript. The smallest indexable unit of "
        "transcribed speech and the anchor for citations from "
        "Extractions back into the Transcript."
    ),
    "Speaker Profile": (
        "A persistent identity that an Utterance can be attributed to. "
        "Resolved either automatically (matched against prior Recordings "
        "by voice embedding) or manually by the user assigning a name "
        "to a Speaker Tag."
    ),
    "Speaker Tag": (
        "The provisional label assigned by the Diarization Service "
        "(e.g. `Tag-1`, `Tag-2`) before resolution to a Speaker Profile. "
        "Tags are scoped to a single Transcript and are never persisted "
        "as identities."
    ),
    "Extraction": (
        "The structured output produced by the Extraction Service from "
        "a Transcript: Topics, Decisions, Action Items, and free-form "
        "summary fields. Always references the Transcript it was "
        "derived from."
    ),
    "Topic": (
        "A discussion subject extracted from a Transcript. Each Topic "
        "is bounded by a contiguous Utterance range and carries a short "
        "title, a one-line summary, and a list of citation Utterance "
        "IDs."
    ),
    "Decision": (
        "An outcome explicitly agreed during a Recording, surfaced by "
        "the Extraction Service. Decisions cite the Utterance(s) where "
        "the agreement was made."
    ),
    "Action Item": (
        "A task assigned during a Recording. Each Action Item has an "
        "optional owner (resolved to a Speaker Profile when possible), "
        "an optional due date, and a citation back to the originating "
        "Utterance."
    ),
    "Template": (
        "A versioned prompt configuration used by the Extraction "
        "Service to control what the LLM produces. Templates are "
        "selected per Recording and pinned to a Note when extraction "
        "runs, so re-running on a Note uses the same Template by "
        "default."
    ),
    "Note": (
        "The user-facing artifact that brings together a Recording, "
        "its Transcript, and its Extraction. The unit the user opens, "
        "edits, and (eventually) shares."
    ),
    "Job": (
        "A unit of work tracked by the Job Orchestrator. Each Recording "
        "produces one or more Jobs (a Transcription Job and an "
        "Extraction Job at minimum). Jobs have observable progress and "
        "a terminal status of `succeeded`, `failed`, or `cancelled`."
    ),
    "Quality Flag": (
        "An automatic annotation produced by the Audio Quality Service "
        "that warns of issues affecting transcription accuracy. "
        "Examples: low signal-to-noise ratio, sustained overlap, long "
        "silence, clipping. Quality Flags scope to Utterance ranges."
    ),
    "Pipeline": (
        "The end-to-end flow from ingested Recording to finished Note. "
        "Cortex's Pipeline is two-phase: a Transcription Phase that "
        "produces a Transcript, and an Extraction Phase that produces "
        "an Extraction. Phases are decoupled so the Transcript "
        "survives Extraction failure."
    ),
}


# ---------------------------------------------------------------------------
# Helpers for building consistent page bodies
# ---------------------------------------------------------------------------

def adr_sections(
    context: str, decision: str, consequences: str, alternatives: str = ""
) -> list[tuple[str, str]]:
    """Standard ADR template — Context / Decision / Consequences / Alternatives."""
    sections = [
        ("Context", context.strip()),
        ("Decision", decision.strip()),
        ("Consequences", consequences.strip()),
    ]
    if alternatives:
        sections.append(("Alternatives considered", alternatives.strip()))
    return sections


def standard_frontmatter(owners: str, last_updated: str = "2026-04-12") -> dict:
    return {"owners": f"[{owners}]", "last_updated": last_updated}


# ---------------------------------------------------------------------------
# Architecture pages
# ---------------------------------------------------------------------------

ARCHITECTURE_PAGES: list[Page] = [
    Page(
        path="architecture/system-overview.md",
        title="System Overview",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Cortex is a local meeting-transcription app. The user "
                "supplies a Recording (an audio or video file from a "
                "meeting), Cortex produces a Transcript and an "
                "Extraction, and assembles them into a Note that the "
                "user can read, edit, and (in future) share.",
            ),
            (
                "Shape at a glance",
                "Cortex runs entirely on the user's machine. There is "
                "a Python backend (FastAPI) that owns the Pipeline, "
                "and a React frontend served by the same backend. All "
                "long-running work happens behind the Job Orchestrator. "
                "Storage is a local relational database. Models (speech "
                "recognition and LLM) run locally by default; cloud "
                "endpoints are an opt-in fallback.",
            ),
            (
                "Top-level flow",
                "The user uploads a Recording through the web app. The "
                f"{link('services/ingest-service.md', 'Ingest Service')} "
                "validates and stores the media. The "
                f"{link('services/job-orchestrator.md', 'Job Orchestrator')} "
                "queues a Transcription Job. The "
                f"{link('services/transcription-service.md', 'Transcription Service')} "
                "produces a Transcript, then the "
                f"{link('services/diarization-service.md', 'Diarization Service')} "
                "labels Utterances with Speaker Tags. Once the Transcript "
                "is finalised the Orchestrator queues an Extraction Job, "
                "which the "
                f"{link('services/extraction-service.md', 'Extraction Service')} "
                "executes against the configured "
                f"{link('domain/template.md', 'Template')}. The result "
                f"becomes a {link('domain/note.md', 'Note')}.",
            ),
            (
                "Where to read next",
                f"- {link('architecture/service-map.md', 'Service Map')}: "
                "boundaries and dependencies between services.\n"
                f"- {link('architecture/pipeline-stages.md', 'Pipeline Stages')}: "
                "phase-by-phase walkthrough.\n"
                f"- {link('architecture/data-flow.md', 'Data Flow')}: "
                "how artifacts move between services and storage.\n"
                f"- {link('glossary.md', 'Glossary')}: canonical "
                "vocabulary used throughout.",
            ),
        ],
    ),
    Page(
        path="architecture/service-map.md",
        title="Service Map",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Names every backend service, what it owns, and what "
                "it depends on. If a responsibility doesn't fit into "
                "one of the services listed here, that is a sign the "
                "shape needs revisiting — discuss before adding a new "
                "service.",
            ),
            (
                "Services",
                f"- {link('services/ingest-service.md', 'Ingest Service')} — "
                "owns Recording intake and validation.\n"
                f"- {link('services/transcription-service.md', 'Transcription Service')} — "
                "produces a Transcript from a Recording.\n"
                f"- {link('services/diarization-service.md', 'Diarization Service')} — "
                "assigns Speaker Tags to Utterances.\n"
                f"- {link('services/extraction-service.md', 'Extraction Service')} — "
                "produces an Extraction from a Transcript.\n"
                f"- {link('services/template-service.md', 'Template Service')} — "
                "owns Template CRUD and version pinning.\n"
                f"- {link('services/notes-service.md', 'Notes Service')} — "
                "assembles, edits, and queries Notes.\n"
                f"- {link('services/job-orchestrator.md', 'Job Orchestrator')} — "
                "queues, runs, and reports Jobs.\n"
                f"- {link('services/audio-quality-service.md', 'Audio Quality Service')} — "
                "annotates Recordings with Quality Flags.",
            ),
            (
                "Dependency rules",
                "- The Job Orchestrator is the only service permitted "
                "to call Transcription, Diarization, Extraction, and "
                "Audio Quality Services directly. Other services must "
                "go through it.\n"
                "- The Notes Service is the sole writer to Note "
                "records. Other services may read, but never mutate.\n"
                "- The Ingest Service is the sole writer to Recording "
                "records.\n"
                "- The Template Service is the sole writer to Template "
                "records, and the Extraction Service is the only "
                "consumer.",
            ),
            (
                "Cross-cutting",
                "All services share a common storage layer (see "
                f"{link('architecture/storage-layer.md', 'Storage Layer')}) "
                "and emit progress events to the realtime channel "
                "described in "
                f"{link('architecture/realtime-progress.md', 'Realtime Progress')}.",
            ),
        ],
    ),
    Page(
        path="architecture/pipeline-stages.md",
        title="Pipeline Stages",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Walks through the Pipeline phase by phase, naming the "
                "service responsible for each stage and the artifact it "
                "produces.",
            ),
            (
                "Phase 1 — Transcription",
                "**Stage 1.1 Validate** — The Ingest Service confirms "
                "the uploaded file is a supported format and meets size "
                "limits. On failure the Recording is rejected before "
                "any Job is queued.\n\n"
                "**Stage 1.2 Quality scan** — The Audio Quality Service "
                "produces Quality Flags for the Recording. Flags are "
                "advisory and do not block transcription.\n\n"
                "**Stage 1.3 Transcribe** — The Transcription Service "
                "produces an ordered list of Utterances with timestamps "
                "and confidence scores.\n\n"
                "**Stage 1.4 Diarize** — The Diarization Service "
                "assigns a Speaker Tag to each Utterance. Tags can be "
                "resolved to Speaker Profiles after the fact.\n\n"
                "**Output:** a finalised Transcript.",
            ),
            (
                "Phase 2 — Extraction",
                "**Stage 2.1 Template selection** — The Extraction "
                "Service loads the Template configured for the "
                "Recording.\n\n"
                "**Stage 2.2 Chunk** — The Transcript is partitioned "
                "into chunks sized for the LLM context window with a "
                "configurable overlap (see "
                f"{link('adrs/chunked-extraction.md', 'ADR: chunked extraction')}).\n\n"
                "**Stage 2.3 Extract per chunk** — Each chunk is sent "
                "to the LLM with the Template's prompt. The result is "
                "a partial Extraction.\n\n"
                "**Stage 2.4 Merge and dedupe** — Partial Extractions "
                "are merged. Duplicate Topics, Decisions, and Action "
                "Items are collapsed using citation overlap.\n\n"
                "**Output:** a finalised Extraction.",
            ),
            (
                "Phase 3 — Note assembly",
                "**Stage 3.1** The Notes Service composes a Note from "
                "the Recording, Transcript, and Extraction.\n\n"
                "**Stage 3.2** The Note is written to storage and "
                "published on the realtime channel; the frontend "
                "displays it as soon as the event arrives.",
            ),
            (
                "Why two phases",
                "Phase 1 and Phase 2 are decoupled so a finished "
                "Transcript is preserved even if Extraction fails, "
                "fails partway, or the user re-runs Extraction with a "
                "different Template. See "
                f"{link('adrs/two-phase-pipeline.md', 'ADR: two-phase pipeline')}.",
            ),
        ],
    ),
    Page(
        path="architecture/data-flow.md",
        title="Data Flow",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Describes which service produces or mutates which "
                "artifact, and how artifacts reference each other in "
                "storage.",
            ),
            (
                "Producers",
                "- **Recording** — written by the Ingest Service. "
                "Immutable after creation; metadata edits (title, tags) "
                "happen on the associated Note rather than on the "
                "Recording itself.\n"
                "- **Transcript** — written by the Transcription "
                "Service; appended to by the Diarization Service.\n"
                "- **Extraction** — written by the Extraction Service.\n"
                "- **Note** — written and edited exclusively by the "
                "Notes Service.\n"
                "- **Template** — written by the Template Service.\n"
                "- **Job** — written by the Job Orchestrator.\n"
                "- **Quality Flag** — written by the Audio Quality "
                "Service.",
            ),
            (
                "References",
                "- Each Transcript references exactly one Recording.\n"
                "- Each Utterance references exactly one Speaker Tag "
                "and (after resolution) one Speaker Profile.\n"
                "- Each Extraction references exactly one Transcript "
                "and one Template version.\n"
                "- Each Topic, Decision, and Action Item references "
                "one or more Utterances by ID.\n"
                "- Each Note references one Recording, one Transcript, "
                "one Extraction, and (snapshotted) one Template "
                "version.",
            ),
            (
                "Citation guarantee",
                "Every Topic, Decision, and Action Item must cite at "
                "least one Utterance. The Extraction Service rejects "
                "any LLM output that fails this check; downstream UI "
                "may assume citations are always present.",
            ),
        ],
    ),
    Page(
        path="architecture/local-first-principles.md",
        title="Local-first Principles",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Cortex is local-first. This page names what that "
                "means concretely so the rule is enforceable in "
                "reviews and design discussions.",
            ),
            (
                "Principles",
                "1. **No external network call is required for the "
                "core flow.** A user with Cortex installed and the "
                "default models present must be able to take a "
                "Recording from upload to Note without internet "
                "access.\n"
                "2. **Cloud is opt-in, never default.** Any cloud "
                "endpoint (LLM API, hosted ASR) is a configurable "
                "alternative. The default configuration uses local "
                "model runtimes.\n"
                "3. **All user data lives on the user's machine.** "
                "Recordings, Transcripts, Extractions, and Notes are "
                "stored in the local database and the local media "
                "directory. Cortex must not phone home.\n"
                "4. **Telemetry is opt-in and minimal.** When enabled, "
                "telemetry is anonymised and never includes Recording "
                "content or Transcript text.",
            ),
            (
                "Why",
                f"See {link('adrs/local-first-default.md', 'ADR: local-first default')} "
                "for the reasoning behind making local the default "
                "rather than an option, and the trade-offs involved "
                "(model size, install footprint).",
            ),
        ],
    ),
    Page(
        path="architecture/model-runtime.md",
        title="Model Runtime",
        category="architecture",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "Describes how Cortex runs the speech-recognition and "
                "language models that power the Pipeline.",
            ),
            (
                "Speech recognition",
                "ASR runs locally via a bundled engine that exposes a "
                "synchronous transcribe call returning timestamped "
                "Utterances with confidence scores. The Transcription "
                "Service is the only caller; it owns model lifecycle "
                "(load, warm-up, unload) for the worker.",
            ),
            (
                "Diarization",
                "Diarization is a separate model invoked after ASR. "
                "It produces Speaker Tags but does not resolve them to "
                "Speaker Profiles — that is the Notes Service's job, "
                "via voice-embedding match against existing Profiles.",
            ),
            (
                "Language model",
                "The default LLM runtime is a local server (Ollama-"
                "compatible API). The Extraction Service speaks the "
                "OpenAI chat-completions protocol against this local "
                "endpoint. Cloud endpoints (OpenAI, Anthropic) can be "
                "configured but are not enabled by default. See "
                f"{link('adrs/llm-runtime-default.md', 'ADR: LLM runtime default')}.",
            ),
            (
                "Hardware fallback",
                "Cortex auto-detects available accelerators (CUDA on "
                "Linux/Windows, Metal on macOS) and falls back to CPU. "
                "On CPU-only systems the Transcription Service "
                "switches to a smaller model variant; the user sees a "
                "Quality Flag advising that transcription accuracy is "
                "reduced.",
            ),
        ],
    ),
    Page(
        path="architecture/storage-layer.md",
        title="Storage Layer",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Describes the database conventions used across "
                "services. Cortex uses a relational store for "
                "everything except media files.",
            ),
            (
                "Database",
                "SQLite is the default backend. Postgres is supported "
                "for users who want to run Cortex on a home server "
                "with multiple devices reading the same database. The "
                "schema is identical across both backends; service "
                "code uses the SQL builder layer rather than a full "
                "ORM (see "
                f"{link('adrs/sqlalchemy-core.md', 'ADR: SQL builder over ORM')}).",
            ),
            (
                "Media files",
                "Recordings store their original media in a local "
                "directory configured by the user. The database holds "
                "only the path and content hash. Deleting a Recording "
                "via the Notes Service deletes both the row and the "
                "underlying media file.",
            ),
            (
                "Migrations",
                "Schema migrations live in a versioned migrations "
                "directory and run automatically on startup. See "
                f"{link('ops/database-migrations.md', 'Database Migrations')} "
                "for operating procedures.",
            ),
            (
                "Identifiers",
                "All primary keys are ULIDs stored as text. ULIDs "
                "sort lexicographically by creation time, which makes "
                "the Notes Explorer's default chronological sort cheap.",
            ),
        ],
    ),
    Page(
        path="architecture/realtime-progress.md",
        title="Realtime Progress",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Describes how the frontend learns about Job progress "
                "without polling.",
            ),
            (
                "Mechanism",
                "The Job Orchestrator publishes events on a per-user "
                "Server-Sent Events channel. Each event names the Job "
                "ID, the phase it is in, a percentage estimate (where "
                "calculable), and any Quality Flags emitted so far. "
                "See "
                f"{link('adrs/sse-progress.md', 'ADR: SSE for progress')} "
                "for the reasoning behind SSE over WebSockets.",
            ),
            (
                "Event types",
                "- `job.queued` — the Job has been created.\n"
                "- `job.started` — the Job is now running.\n"
                "- `job.progress` — incremental progress, sent at most "
                "once per second per Job.\n"
                "- `job.flagged` — a Quality Flag was emitted during "
                "this Job.\n"
                "- `job.succeeded` / `job.failed` / `job.cancelled` — "
                "terminal events.",
            ),
            (
                "Reconnection",
                "Clients reconnect with the last received event ID. "
                "The Orchestrator replays missed events from a bounded "
                "buffer (last 5 minutes per channel). Older events are "
                "fetched via the Jobs REST endpoint instead.",
            ),
        ],
    ),
    Page(
        path="architecture/error-handling.md",
        title="Error Handling Strategy",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Names the categories of failure Cortex distinguishes "
                "and what each one is allowed to do.",
            ),
            (
                "Categories",
                "- **User-input errors** (invalid file, unsupported "
                "format) — surfaced synchronously at upload, never "
                "produce a Job.\n"
                "- **Transient infrastructure errors** (model worker "
                "OOM, database lock timeout) — retried with backoff "
                "by the Job Orchestrator. After three retries the Job "
                "is marked failed and the underlying error is "
                "surfaced.\n"
                "- **Model errors** (LLM returns malformed output, "
                "ASR confidence below threshold) — the Job is marked "
                "failed. The Transcript is preserved even if "
                "Extraction fails, per "
                f"{link('adrs/two-phase-pipeline.md', 'ADR: two-phase pipeline')}.\n"
                "- **Programmer errors** (assertion failure, type "
                "error) — the worker process exits, the Orchestrator "
                "marks the Job failed without retry, and the error is "
                "logged with full context for diagnosis.",
            ),
            (
                "User-facing presentation",
                "Failed Jobs surface a one-line reason in the Notes "
                "Explorer plus a longer technical detail behind a "
                "disclosure. The Notes Service never shows raw stack "
                "traces.",
            ),
            (
                "Re-run policy",
                "Any failed Extraction Job can be re-run by the user "
                "without re-running transcription. Failed Transcription "
                "Jobs require the original Recording to still be "
                "present.",
            ),
        ],
    ),
    Page(
        path="architecture/extension-points.md",
        title="Extension Points",
        category="architecture",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "Names the interfaces that are deliberately swappable. "
                "Anything not listed here is internal and may change "
                "without notice.",
            ),
            (
                "Swappable",
                "- **LLM endpoint** — the Extraction Service speaks an "
                "OpenAI-compatible API; pointing it at a different "
                "endpoint is a config change.\n"
                "- **ASR engine** — wrapped behind a minimal "
                "Transcriber interface (transcribe → list of "
                "Utterances). A user with a different ASR can supply "
                "their own implementation.\n"
                "- **Storage backend** — SQLite vs. Postgres is a "
                "config switch (see "
                f"{link('architecture/storage-layer.md', 'Storage Layer')}).\n"
                "- **Templates** — the most important extension point "
                "for users; see "
                f"{link('domain/template.md', 'Template')} and "
                f"{link('frontend/template-editor.md', 'Template Editor')}.",
            ),
            (
                "Not swappable (yet)",
                "- The diarization model — wired in at the "
                "Transcription Service boundary.\n"
                "- The Pipeline phase ordering — the two-phase "
                "structure is load-bearing for the system's failure "
                "model.",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Domain pages
# ---------------------------------------------------------------------------

DOMAIN_PAGES: list[Page] = [
    Page(
        path="domain/recording.md",
        title="Recording",
        category="domain",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "A Recording wraps an audio source ingested into "
                "Cortex along with its metadata. It is the entry point "
                "for the Pipeline.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `media_path` — absolute path to the original media "
                "file on disk.\n"
                "- `media_hash` — SHA-256 of the original media. "
                "Detects duplicates on re-upload.\n"
                "- `duration_seconds` — measured at ingest, not "
                "user-supplied.\n"
                "- `format` — container format (mp3, m4a, wav, mp4, "
                "webm).\n"
                "- `sample_rate_hz` — measured.\n"
                "- `channels` — measured.\n"
                "- `recorded_at` — user-supplied timestamp; defaults "
                "to file mtime.\n"
                "- `created_at` — ingest time.",
            ),
            (
                "Lifecycle",
                "Recordings are created by the Ingest Service and are "
                "**immutable** after creation. User-visible fields "
                "such as title and tags live on the associated Note, "
                "not on the Recording.",
            ),
            (
                "Related",
                f"- {link('services/ingest-service.md', 'Ingest Service')}\n"
                f"- {link('domain/transcript.md', 'Transcript')} — one per "
                "Recording.\n"
                f"- {link('domain/note.md', 'Note')} — one per Recording, "
                "user-facing.",
            ),
        ],
    ),
    Page(
        path="domain/transcript.md",
        title="Transcript",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "A speaker-attributed record of speech in a Recording, "
                "represented as an ordered list of Utterances.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `recording_id` — FK to Recording.\n"
                "- `language` — auto-detected ISO 639-1 code.\n"
                "- `model_version` — ASR model version used.\n"
                "- `created_at` — when transcription completed.\n"
                "- `utterances` — ordered list of Utterance rows.",
            ),
            (
                "Lifecycle",
                "Created by the Transcription Service after ASR "
                "completes. Utterances are appended (not edited) by "
                "the Diarization Service in a follow-up step. After "
                "diarization the Transcript is sealed; subsequent "
                "edits go through the Notes Service and produce a new "
                "revision rather than mutating the Transcript in "
                "place.",
            ),
            (
                "Editing model",
                "User edits to Transcript text are stored as overlays "
                "owned by the Note. The original Transcript is "
                "preserved verbatim so that re-running Extraction "
                "always sees the model's output, not the user's.",
            ),
            (
                "Related",
                f"- {link('domain/utterance.md', 'Utterance')}\n"
                f"- {link('services/transcription-service.md', 'Transcription Service')}\n"
                f"- {link('services/diarization-service.md', 'Diarization Service')}",
            ),
        ],
    ),
    Page(
        path="domain/utterance.md",
        title="Utterance",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "The smallest indexable unit of transcribed speech. "
                "All citations from an Extraction back into the "
                "Transcript reference Utterances by ID.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `transcript_id` — FK.\n"
                "- `index` — ordinal within the Transcript (0-based).\n"
                "- `start_ms` / `end_ms` — timestamps relative to the "
                "Recording start.\n"
                "- `text` — the transcribed text.\n"
                "- `speaker_tag` — provisional label assigned by "
                "diarization.\n"
                "- `speaker_profile_id` — FK to Speaker Profile, "
                "nullable until resolved.\n"
                "- `confidence` — ASR confidence score, 0.0–1.0.",
            ),
            (
                "Granularity",
                "An Utterance is roughly one continuous spoken "
                "phrase, typically 1–15 seconds. It is not a sentence "
                "and not a single word — it is whatever the ASR engine "
                "emits as a contiguous segment with a single speaker.",
            ),
            (
                "Related",
                f"- {link('domain/transcript.md', 'Transcript')}\n"
                f"- {link('domain/speaker-profile.md', 'Speaker Profile')}",
            ),
        ],
    ),
    Page(
        path="domain/speaker-profile.md",
        title="Speaker Profile",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "A persistent identity that an Utterance can be "
                "attributed to. Speaker Profiles span Recordings — "
                "naming `Tag-1` as 'Priya' once should let Cortex "
                "auto-resolve Priya's voice in subsequent Recordings.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `display_name` — user-supplied.\n"
                "- `voice_embedding` — fixed-length vector used to "
                "match new Speaker Tags to known Profiles.\n"
                "- `embedding_version` — model version that produced "
                "the embedding.\n"
                "- `created_at` / `updated_at`.",
            ),
            (
                "Resolution",
                "When a new Transcript arrives, the Notes Service "
                "compares each Speaker Tag's voice embedding to "
                "existing Speaker Profiles. Matches above the "
                "configured similarity threshold are auto-resolved; "
                "below it the Tag is left unresolved and surfaced for "
                "the user to name.",
            ),
            (
                "Related",
                f"- {link('domain/utterance.md', 'Utterance')}\n"
                f"- {link('services/diarization-service.md', 'Diarization Service')}\n"
                f"- {link('services/notes-service.md', 'Notes Service')}",
            ),
        ],
    ),
    Page(
        path="domain/extraction.md",
        title="Extraction",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "The structured output produced from a Transcript by "
                "the Extraction Service: Topics, Decisions, Action "
                "Items, plus a free-form summary.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `transcript_id` — FK.\n"
                "- `template_id` — FK to the Template version used.\n"
                "- `summary` — free-form prose, single paragraph.\n"
                "- `topics` — list of Topic rows.\n"
                "- `decisions` — list of Decision rows.\n"
                "- `action_items` — list of Action Item rows.\n"
                "- `model_version` — LLM identifier.\n"
                "- `created_at`.",
            ),
            (
                "Determinism",
                "Extractions are not deterministic — the same "
                "Transcript and Template can produce different "
                "Extractions on different runs. This is expected. "
                "Re-running Extraction is cheap and explicitly "
                "supported.",
            ),
            (
                "Related",
                f"- {link('domain/topic.md', 'Topic')}\n"
                f"- {link('domain/decision.md', 'Decision')}\n"
                f"- {link('domain/action-item.md', 'Action Item')}\n"
                f"- {link('services/extraction-service.md', 'Extraction Service')}",
            ),
        ],
    ),
    Page(
        path="domain/topic.md",
        title="Topic",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "A discussion subject extracted from a Transcript. "
                "Topics are the primary navigational unit for a Note: "
                "the user typically scans Topics first and drills into "
                "Utterances second.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `extraction_id` — FK.\n"
                "- `title` — short human-readable label.\n"
                "- `summary` — one-line.\n"
                "- `start_utterance_id` / `end_utterance_id` — "
                "bounding range within the Transcript.\n"
                "- `citation_utterance_ids` — list of additional "
                "supporting Utterance IDs.",
            ),
            (
                "Constraints",
                "Topics must be non-empty, must cite at least one "
                "Utterance, and must not overlap each other within an "
                "Extraction. Overlap is rejected at merge time (see "
                f"{link('architecture/pipeline-stages.md', 'Pipeline Stages')}).",
            ),
            (
                "Related",
                f"- {link('domain/extraction.md', 'Extraction')}\n"
                f"- {link('domain/utterance.md', 'Utterance')}",
            ),
        ],
    ),
    Page(
        path="domain/decision.md",
        title="Decision",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "An outcome explicitly agreed during a Recording. "
                "Decisions are surfaced separately from Topics because "
                "they have higher value to the user and are routinely "
                "exported to other tools (issue trackers, "
                "documents).",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `extraction_id` — FK.\n"
                "- `text` — the decision as a single sentence.\n"
                "- `citation_utterance_ids` — at least one.",
            ),
            (
                "What counts as a Decision",
                "An outcome where a participant explicitly states "
                "intent and at least one other participant agrees, or "
                "where there is no objection within the same Topic. "
                "Aspirational statements ('we should think about X') "
                "are not Decisions.",
            ),
            (
                "Related",
                f"- {link('domain/extraction.md', 'Extraction')}\n"
                f"- {link('domain/utterance.md', 'Utterance')}",
            ),
        ],
    ),
    Page(
        path="domain/action-item.md",
        title="Action Item",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "A task assigned during a Recording. Action Items are "
                "the most-exported Extraction artifact — many users "
                "open Cortex specifically to grab their Action Items "
                "from a meeting.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `extraction_id` — FK.\n"
                "- `text` — the task as a single sentence in "
                "imperative form.\n"
                "- `owner_speaker_profile_id` — nullable FK to "
                "Speaker Profile.\n"
                "- `due_date` — nullable, parsed from the Utterance "
                "text when phrased explicitly.\n"
                "- `citation_utterance_ids` — at least one.",
            ),
            (
                "Owner resolution",
                "If the Utterance contains a name that resolves to a "
                "known Speaker Profile, that Profile is the owner. If "
                "the speaker says 'I'll do X', the owner is the "
                "Speaker Profile attributed to that Utterance. "
                "Otherwise the owner is null.",
            ),
            (
                "Related",
                f"- {link('domain/extraction.md', 'Extraction')}\n"
                f"- {link('domain/utterance.md', 'Utterance')}\n"
                f"- {link('domain/speaker-profile.md', 'Speaker Profile')}",
            ),
        ],
    ),
    Page(
        path="domain/template.md",
        title="Template",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "A versioned prompt configuration used by the "
                "Extraction Service. Templates control what the LLM "
                "extracts and how the output is shaped.",
            ),
            (
                "Fields",
                "- `id` — ULID, identifies a Template.\n"
                "- `version` — monotonically increasing integer per "
                "Template id.\n"
                "- `name` — human-readable, e.g. 'Standup', '1:1', "
                "'Customer interview'.\n"
                "- `description` — single paragraph.\n"
                "- `prompt_text` — the prompt itself.\n"
                "- `is_default` — flag indicating the default "
                "Template for new Recordings.\n"
                "- `created_at`.",
            ),
            (
                "Versioning",
                "Editing a Template creates a new version rather than "
                "mutating the existing one. Each Extraction pins the "
                "exact `(template_id, version)` it ran against, so "
                "Notes remain reproducible even after Templates "
                "change.",
            ),
            (
                "Built-in Templates",
                "Cortex ships with three built-in Templates: General "
                "Meeting (the default), Standup, and Customer "
                "Interview. Built-in Templates can be cloned and "
                "customised; the originals cannot be edited or "
                "deleted.",
            ),
            (
                "Related",
                f"- {link('services/template-service.md', 'Template Service')}\n"
                f"- {link('services/extraction-service.md', 'Extraction Service')}\n"
                f"- {link('frontend/template-editor.md', 'Template Editor')}",
            ),
        ],
    ),
    Page(
        path="domain/note.md",
        title="Note",
        category="domain",
        frontmatter=standard_frontmatter("product-team"),
        sections=[
            (
                "Purpose",
                "The user-facing artifact that brings together a "
                "Recording, its Transcript, and its Extraction. The "
                "Note is what the user opens, edits, and (in future) "
                "shares.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `recording_id` — FK.\n"
                "- `transcript_id` — FK.\n"
                "- `extraction_id` — FK.\n"
                "- `template_version` — denormalised pin of the "
                "Template version used for this Note's Extraction.\n"
                "- `title` — user-editable, defaults to the "
                "Extraction's first Topic title.\n"
                "- `tags` — list of strings.\n"
                "- `transcript_overlay` — JSON document holding "
                "user-applied edits to Transcript text.\n"
                "- `created_at` / `updated_at`.",
            ),
            (
                "Editing semantics",
                "The Note is the only place where user edits land. "
                "Edits to Transcript text are stored as overlays so "
                "the original ASR output is preserved. Edits to "
                "Extraction content are first-class fields on the "
                "Note, not the Extraction (because re-running "
                "Extraction must not silently overwrite the user's "
                "manual changes).",
            ),
            (
                "Related",
                f"- {link('services/notes-service.md', 'Notes Service')}\n"
                f"- {link('frontend/notes-explorer.md', 'Notes Explorer')}\n"
                f"- {link('frontend/transcript-viewer.md', 'Transcript Viewer')}",
            ),
        ],
    ),
    Page(
        path="domain/job.md",
        title="Job",
        category="domain",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "A unit of work tracked by the Job Orchestrator. Each "
                "Recording produces one or more Jobs.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `kind` — one of `transcription`, `extraction`, "
                "`quality_scan`.\n"
                "- `recording_id` — FK.\n"
                "- `status` — `queued`, `running`, `succeeded`, "
                "`failed`, `cancelled`.\n"
                "- `progress` — 0.0–1.0.\n"
                "- `error_summary` — nullable, short user-facing "
                "string.\n"
                "- `error_detail` — nullable, full technical detail.\n"
                "- `attempt` — 1-based retry counter.\n"
                "- `started_at` / `finished_at` — nullable.",
            ),
            (
                "Status transitions",
                "Allowed transitions: `queued` → `running` → "
                "(`succeeded` | `failed` | `cancelled`). Failed Jobs "
                "are retried by the Orchestrator up to three times, "
                "each retry creating a new attempt of the same Job id.",
            ),
            (
                "Related",
                f"- {link('services/job-orchestrator.md', 'Job Orchestrator')}\n"
                f"- {link('architecture/realtime-progress.md', 'Realtime Progress')}",
            ),
        ],
    ),
    Page(
        path="domain/quality-flag.md",
        title="Quality Flag",
        category="domain",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "An automatic annotation produced by the Audio Quality "
                "Service that warns of issues affecting transcription "
                "accuracy. Flags are advisory, not blocking.",
            ),
            (
                "Fields",
                "- `id` — ULID.\n"
                "- `recording_id` — FK.\n"
                "- `kind` — one of `low_snr`, `overlap`, `silence`, "
                "`clipping`, `low_confidence`.\n"
                "- `severity` — `info`, `warning`, `error`.\n"
                "- `start_ms` / `end_ms` — bounded range within the "
                "Recording, inclusive of any later Utterance "
                "boundaries.\n"
                "- `message` — short user-facing string.",
            ),
            (
                "Where they appear",
                "Quality Flags surface in the Notes Explorer as a "
                "small badge on affected Notes, and in the Transcript "
                "Viewer as inline highlights on the affected ranges.",
            ),
            (
                "Related",
                f"- {link('services/audio-quality-service.md', 'Audio Quality Service')}",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Service pages
# ---------------------------------------------------------------------------

SERVICE_PAGES: list[Page] = [
    Page(
        path="services/ingest-service.md",
        title="Ingest Service",
        category="services",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Responsibility",
                "Owns Recording intake: validation, deduplication, "
                "and persistence of the original media file. The only "
                "writer to Recording rows.",
            ),
            (
                "Inputs",
                "An uploaded media file plus optional user-supplied "
                "metadata (title hint, recorded-at timestamp, tags).",
            ),
            (
                "Outputs",
                "A Recording row plus a media file written to the "
                "configured media directory. Emits a `recording.created` "
                "event consumed by the Job Orchestrator to queue the "
                "transcription Job.",
            ),
            (
                "Validation rules",
                "- Rejects unsupported formats.\n"
                "- Rejects files larger than the configured limit "
                "(default 1 GB).\n"
                "- Detects duplicates by content hash and returns the "
                "existing Recording instead of creating a new one. "
                "Duplicate detection is opt-out per upload.",
            ),
            (
                "Failure modes",
                "Validation failures surface synchronously as HTTP "
                "errors. Storage failures (out of disk, permission "
                "denied) surface as HTTP 500 with a user-actionable "
                "message in the body.",
            ),
            (
                "Related",
                f"- {link('domain/recording.md', 'Recording')}\n"
                f"- {link('services/job-orchestrator.md', 'Job Orchestrator')}",
            ),
        ],
    ),
    Page(
        path="services/transcription-service.md",
        title="Transcription Service",
        category="services",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Responsibility",
                "Produces a Transcript from a Recording by running "
                "ASR and emitting an ordered list of Utterances.",
            ),
            (
                "Inputs",
                "A Recording id (the service reads media path from "
                "the Recording row).",
            ),
            (
                "Outputs",
                "A Transcript with Utterances. The Transcript is "
                "written without Speaker Tags — those are added by "
                "the Diarization Service.",
            ),
            (
                "Model lifecycle",
                "The service owns model load and warm-up. The first "
                "Transcription Job after process start is slower; "
                "subsequent Jobs reuse the loaded model. Model is "
                "unloaded after a configurable idle period to free "
                "memory.",
            ),
            (
                "Concurrency",
                "Single-worker by default. Multiple workers can be "
                "configured but are gated by available accelerator "
                "memory; the Job Orchestrator never schedules more "
                "Transcription Jobs in parallel than the configured "
                "worker count.",
            ),
            (
                "Related",
                f"- {link('architecture/model-runtime.md', 'Model Runtime')}\n"
                f"- {link('services/diarization-service.md', 'Diarization Service')}\n"
                f"- {link('domain/transcript.md', 'Transcript')}",
            ),
        ],
    ),
    Page(
        path="services/diarization-service.md",
        title="Diarization Service",
        category="services",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Responsibility",
                "Assigns a Speaker Tag to each Utterance in a "
                "Transcript and produces a voice embedding per Tag "
                "for later resolution to Speaker Profiles.",
            ),
            (
                "Inputs",
                "A Transcript id and the underlying Recording's media "
                "path.",
            ),
            (
                "Outputs",
                "Updates each Utterance with a `speaker_tag` and "
                "writes a per-Tag embedding into a side table for the "
                "Notes Service to consume during Profile resolution.",
            ),
            (
                "Resolution scope",
                "Diarization does **not** resolve Tags to Speaker "
                "Profiles. Tags like `Tag-1`, `Tag-2` are scoped to a "
                "single Transcript. The Notes Service performs "
                "cross-Recording resolution by comparing embeddings.",
            ),
            (
                "Failure mode",
                "If diarization fails, the Transcript is preserved "
                "with all Utterances assigned the placeholder tag "
                "`Tag-Unknown`. The Job is marked failed; the user "
                "can re-run diarization without re-transcribing.",
            ),
            (
                "Related",
                f"- {link('domain/utterance.md', 'Utterance')}\n"
                f"- {link('domain/speaker-profile.md', 'Speaker Profile')}\n"
                f"- {link('adrs/pyannote-diarization.md', 'ADR: diarization model choice')}",
            ),
        ],
    ),
    Page(
        path="services/extraction-service.md",
        title="Extraction Service",
        category="services",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Responsibility",
                "Produces an Extraction (Topics, Decisions, Action "
                "Items, summary) from a Transcript using a Template.",
            ),
            (
                "Inputs",
                "A Transcript id and a Template version reference. "
                "If the Template reference is omitted, the default "
                "Template is used.",
            ),
            (
                "Outputs",
                "An Extraction row plus rows for its Topics, "
                "Decisions, and Action Items.",
            ),
            (
                "Chunking",
                "Long Transcripts are partitioned into chunks sized "
                "for the LLM context window with a configurable "
                "overlap (default 60 seconds of audio). Each chunk is "
                "extracted independently and the partial results are "
                "merged. See "
                f"{link('adrs/chunked-extraction.md', 'ADR: chunked extraction')} "
                "for the chunk-size rationale.",
            ),
            (
                "Citation enforcement",
                "Every Topic, Decision, and Action Item produced by "
                "the LLM must cite at least one Utterance id. The "
                "service rejects (and re-prompts once) outputs that "
                "fail this check; if the second attempt also fails "
                "the offending item is dropped.",
            ),
            (
                "Failure mode",
                "If extraction fails, the Transcript is preserved "
                "intact and the user can re-run with the same or a "
                "different Template (see "
                f"{link('adrs/two-phase-pipeline.md', 'ADR: two-phase pipeline')}).",
            ),
            (
                "Related",
                f"- {link('domain/extraction.md', 'Extraction')}\n"
                f"- {link('domain/template.md', 'Template')}\n"
                f"- {link('architecture/model-runtime.md', 'Model Runtime')}",
            ),
        ],
    ),
    Page(
        path="services/template-service.md",
        title="Template Service",
        category="services",
        frontmatter=standard_frontmatter("product-team"),
        sections=[
            (
                "Responsibility",
                "Owns Template CRUD and version pinning. The only "
                "writer to Template rows.",
            ),
            (
                "Operations",
                "- `create_template(name, description, prompt_text)` "
                "— creates a new Template at version 1.\n"
                "- `update_template(id, ...)` — creates a new version "
                "with the current value as version + 1.\n"
                "- `clone_template(id)` — copies a Template into a "
                "new id starting at version 1. Used to customise "
                "built-in Templates.\n"
                "- `set_default(id)` — flips the default flag.\n"
                "- `delete_template(id)` — soft-delete; existing "
                "Notes that pin this Template still resolve.",
            ),
            (
                "Built-in Templates",
                "The Template Service ships built-in Templates that "
                "are seeded on first startup. Built-ins cannot be "
                "deleted or directly edited; they must be cloned "
                "first. See "
                f"{link('domain/template.md', 'Template')} for the "
                "list.",
            ),
            (
                "Related",
                f"- {link('domain/template.md', 'Template')}\n"
                f"- {link('frontend/template-editor.md', 'Template Editor')}",
            ),
        ],
    ),
    Page(
        path="services/notes-service.md",
        title="Notes Service",
        category="services",
        frontmatter=standard_frontmatter("product-team"),
        sections=[
            (
                "Responsibility",
                "Assembles, edits, queries, and (eventually) shares "
                "Notes. The only writer to Note rows. Resolves Speaker "
                "Tags to Speaker Profiles.",
            ),
            (
                "Operations",
                "- `assemble(recording_id)` — composes a Note from "
                "the Recording, its latest Transcript, and its latest "
                "Extraction.\n"
                "- `update_note(id, fields...)` — partial update of "
                "user-editable fields (title, tags, transcript "
                "overlay, edited Extraction items).\n"
                "- `list_notes(query)` — paginated listing with "
                "filters (date range, tag, speaker).\n"
                "- `delete_note(id)` — deletes the Note **and** its "
                "underlying Recording, Transcript, Extraction, and "
                "media file.",
            ),
            (
                "Speaker resolution",
                "On Note assembly, the service walks each unresolved "
                "Speaker Tag and compares its embedding to all known "
                "Speaker Profiles. Matches above the configured "
                "similarity threshold (default 0.85) auto-resolve to "
                "the Profile; the Tag remains unresolved otherwise.",
            ),
            (
                "Search",
                "The Notes Service does not yet support full-text "
                "search. The current `list_notes` implementation "
                "filters by tag and date only.",
            ),
            (
                "Related",
                f"- {link('domain/note.md', 'Note')}\n"
                f"- {link('domain/speaker-profile.md', 'Speaker Profile')}",
            ),
        ],
    ),
    Page(
        path="services/job-orchestrator.md",
        title="Job Orchestrator",
        category="services",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Responsibility",
                "Queues, runs, retries, and reports on Jobs. The "
                "single point of contact between user-driven actions "
                "and long-running Pipeline work.",
            ),
            (
                "Queue model",
                "A single in-process queue per Job kind. Jobs are "
                "consumed by worker pools sized per kind: by default "
                "1 transcription worker, 2 extraction workers, 1 "
                "quality-scan worker. Workers run in-process — no "
                "external queue broker.",
            ),
            (
                "Retry policy",
                "Failed Jobs are retried up to three times with "
                "exponential backoff (1s, 5s, 30s). Programmer errors "
                "(asserted via a typed exception) are not retried. "
                "See "
                f"{link('architecture/error-handling.md', 'Error Handling Strategy')}.",
            ),
            (
                "Progress",
                "The Orchestrator publishes events on the realtime "
                "channel described in "
                f"{link('architecture/realtime-progress.md', 'Realtime Progress')}. "
                "Progress for Transcription is reported per second of "
                "audio processed; for Extraction per chunk completed.",
            ),
            (
                "Cancellation",
                "Running Jobs can be cancelled. Cancellation is "
                "cooperative — the worker checks a cancel flag at "
                "natural boundaries (after each chunk for extraction; "
                "after each utterance for transcription).",
            ),
            (
                "Related",
                f"- {link('domain/job.md', 'Job')}",
            ),
        ],
    ),
    Page(
        path="services/audio-quality-service.md",
        title="Audio Quality Service",
        category="services",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Responsibility",
                "Annotates a Recording with Quality Flags warning of "
                "audio issues that affect transcription accuracy. "
                "Runs alongside transcription; does not block it.",
            ),
            (
                "Detectors",
                "- **Low SNR** — sustained noise floor close to "
                "speech level.\n"
                "- **Overlap** — multiple simultaneous speakers "
                "longer than 500 ms.\n"
                "- **Silence** — gap longer than 30 seconds.\n"
                "- **Clipping** — peak amplitude saturation.\n"
                "- **Low confidence** — emitted post-hoc when the "
                "Transcript contains a contiguous run of low-"
                "confidence Utterances.",
            ),
            (
                "Output",
                "A list of Quality Flags written to the database. "
                "Flags are emitted incrementally during the scan and "
                "published on the realtime channel as `job.flagged` "
                "events.",
            ),
            (
                "Related",
                f"- {link('domain/quality-flag.md', 'Quality Flag')}",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Frontend pages
# ---------------------------------------------------------------------------

FRONTEND_PAGES: list[Page] = [
    Page(
        path="frontend/web-app-overview.md",
        title="Web App Overview",
        category="frontend",
        frontmatter=standard_frontmatter("frontend-team"),
        sections=[
            (
                "Purpose",
                "Describes the shape of the Cortex web app: routes, "
                "primary views, and how the frontend connects to the "
                "backend.",
            ),
            (
                "Stack",
                "React with TypeScript, built with Vite. Styling uses "
                "a utility-CSS approach with a small in-house component "
                "library (see "
                f"{link('frontend/component-library.md', 'Component Library')}). "
                "Editor surfaces use CodeMirror.",
            ),
            (
                "Routes",
                "- `/` — Notes Explorer (default landing).\n"
                "- `/notes/:id` — Note view (Transcript Viewer + "
                "Extraction sidebar).\n"
                "- `/templates` — Template list.\n"
                "- `/templates/:id` — Template Editor.\n"
                "- `/upload` — drag-and-drop upload, also accessible "
                "as a modal from any page.\n"
                "- `/settings` — configuration (model paths, storage "
                "directory, theme).",
            ),
            (
                "Backend connection",
                "All data calls go through the local FastAPI backend "
                "at `http://localhost:<port>`. Long-running progress "
                "comes over the SSE channel described in "
                f"{link('architecture/realtime-progress.md', 'Realtime Progress')}.",
            ),
            (
                "Where to read next",
                f"- {link('frontend/notes-explorer.md', 'Notes Explorer')}\n"
                f"- {link('frontend/transcript-viewer.md', 'Transcript Viewer')}\n"
                f"- {link('frontend/template-editor.md', 'Template Editor')}\n"
                f"- {link('frontend/state-management.md', 'State Management')}",
            ),
        ],
    ),
    Page(
        path="frontend/notes-explorer.md",
        title="Notes Explorer",
        category="frontend",
        frontmatter=standard_frontmatter("frontend-team"),
        sections=[
            (
                "Purpose",
                "The default landing view: a paginated list of Notes "
                "with filters and a prominent upload affordance.",
            ),
            (
                "Layout",
                "- Top bar: upload button, search input (placeholder "
                "today; full-text search is unbuilt — see "
                f"{link('services/notes-service.md', 'Notes Service')}), "
                "tag filter chips, date range filter.\n"
                "- Main: list of Note rows showing title, recorded-at, "
                "duration, primary speaker, Quality Flag badges.\n"
                "- Empty state: a single CTA encouraging upload.",
            ),
            (
                "Sort",
                "Default sort is `recorded_at` descending. Secondary "
                "sort by `created_at`. Sort order is not user-"
                "configurable in the current build.",
            ),
            (
                "Live updates",
                "Rows update in place when the SSE channel reports a "
                "Job state change for their Recording. A Note row "
                "shows a progress indicator while Jobs are in flight "
                "and transitions to fully-rendered when both phases "
                "complete.",
            ),
        ],
    ),
    Page(
        path="frontend/transcript-viewer.md",
        title="Transcript Viewer",
        category="frontend",
        frontmatter=standard_frontmatter("frontend-team"),
        sections=[
            (
                "Purpose",
                "The reading and editing surface for a Note. Shows "
                "the Transcript on the left and the Extraction "
                "(Topics, Decisions, Action Items) on the right.",
            ),
            (
                "Transcript pane",
                "Each Utterance is rendered with its speaker label, "
                "timestamp, and text. Clicking an Utterance scrubs "
                "the audio player to its start. Editing an Utterance "
                "writes to the Note's transcript_overlay; the "
                "original Transcript is never mutated.",
            ),
            (
                "Extraction pane",
                "Topics are listed with a one-line summary; "
                "expanding a Topic reveals its bounded Utterance "
                "range. Decisions and Action Items each have their "
                "own collapsible section. Every item links back into "
                "the Transcript pane via its citation Utterances; "
                "clicking the link scrolls and highlights.",
            ),
            (
                "Speaker labels",
                "Unresolved Speaker Tags (`Tag-1`) appear as buttons "
                "the user can click to assign a Speaker Profile. "
                "Resolved Profiles appear as plain names with an "
                "edit pencil for re-assignment.",
            ),
            (
                "Quality Flags",
                "Quality Flags surface as inline highlights on the "
                "affected Utterance ranges with a tooltip naming the "
                "flag kind and severity.",
            ),
        ],
    ),
    Page(
        path="frontend/template-editor.md",
        title="Template Editor",
        category="frontend",
        frontmatter=standard_frontmatter("frontend-team"),
        sections=[
            (
                "Purpose",
                "The view at `/templates/:id` for editing a Template's "
                "name, description, and prompt text.",
            ),
            (
                "Editing surface",
                "The prompt text uses CodeMirror with markdown "
                "highlighting. Saving creates a new version of the "
                "Template; the previous version remains accessible "
                "via a version selector.",
            ),
            (
                "Built-in Templates",
                "Built-in Templates are read-only. The editor "
                "surfaces a 'Clone to edit' affordance instead of a "
                "save button.",
            ),
            (
                "Preview",
                "A 'Preview against a Note' affordance lets the user "
                "select an existing Note and re-run extraction with "
                "the in-progress Template. The preview output is "
                "discarded unless the user explicitly applies it.",
            ),
            (
                "Related",
                f"- {link('domain/template.md', 'Template')}\n"
                f"- {link('services/template-service.md', 'Template Service')}",
            ),
        ],
    ),
    Page(
        path="frontend/component-library.md",
        title="Component Library",
        category="frontend",
        frontmatter=standard_frontmatter("frontend-team"),
        sections=[
            (
                "Purpose",
                "Names the in-house components the app builds on. "
                "Components live alongside the routes that consume "
                "them; nothing in this list is imported from an "
                "external design system.",
            ),
            (
                "Components",
                "- **Stack** — vertical/horizontal layout primitive.\n"
                "- **Card** — bordered container used for Note rows "
                "and Template list rows.\n"
                "- **Badge** — used for tags, severity indicators, "
                "and Speaker labels.\n"
                "- **Toolbar** — top-of-view bar with slots for "
                "search, filters, and actions.\n"
                "- **Modal** — used for upload, settings, and "
                "destructive confirmations.\n"
                "- **AudioPlayer** — wraps the native `<audio>` "
                "element with timeline scrubbing tied to Utterance "
                "boundaries.\n"
                "- **TranscriptList** — virtualised list of "
                "Utterances. Used by the Transcript Viewer.\n"
                "- **JobProgress** — small progress indicator that "
                "subscribes to the SSE channel for a given Recording.",
            ),
        ],
    ),
    Page(
        path="frontend/state-management.md",
        title="State Management",
        category="frontend",
        frontmatter=standard_frontmatter("frontend-team"),
        sections=[
            (
                "Purpose",
                "Names how data flows through the frontend. Reading "
                "this page should be enough to know where to add a "
                "new piece of state.",
            ),
            (
                "Layers",
                "- **Server cache** — a single React Query instance "
                "owns all backend reads. Mutations invalidate the "
                "relevant queries.\n"
                "- **Realtime updates** — a thin SSE subscriber feeds "
                "Job events into the React Query cache by mutating "
                "the cached Job and Note rows directly.\n"
                "- **Local UI state** — view-local state stays in "
                "components. Anything that crosses two routes lives "
                "in the URL (filters, sort) rather than a global "
                "store.",
            ),
            (
                "Anti-patterns",
                "- Don't introduce a global state store. Use the URL "
                "or React Query.\n"
                "- Don't bypass React Query for backend reads. The "
                "cache invalidation rules assume it owns all server "
                "state.",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Ops pages
# ---------------------------------------------------------------------------

OPS_PAGES: list[Page] = [
    Page(
        path="ops/local-deployment.md",
        title="Local Deployment",
        category="ops",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "How to install, run, and uninstall Cortex on a "
                "single user's machine — the supported deployment "
                "shape.",
            ),
            (
                "Install",
                "Cortex ships as a single installer per platform "
                "(macOS, Windows, Linux). The installer drops the "
                "backend, the bundled web app, and the default "
                "models into the application data directory and "
                "registers a launch agent / service.",
            ),
            (
                "Run",
                "On launch, Cortex starts the FastAPI backend on a "
                "loopback port, runs migrations, ensures the local "
                "LLM runtime is reachable (starts it if not), and "
                "opens the web app in the user's default browser.",
            ),
            (
                "Configuration",
                "User configuration lives in a single JSON file in "
                "the application data directory. Settings can be "
                "edited from the `/settings` route or by editing the "
                "file directly. See "
                f"{link('ops/troubleshooting-guide.md', 'Troubleshooting Guide')} "
                "for common issues.",
            ),
            (
                "Uninstall",
                "Uninstall removes the application binaries but "
                "leaves the user's data directory intact. The user "
                "must opt in to a clean uninstall to delete "
                "Recordings, Transcripts, and Notes.",
            ),
        ],
    ),
    Page(
        path="ops/model-management.md",
        title="Model Management",
        category="ops",
        frontmatter=standard_frontmatter("ml-team"),
        sections=[
            (
                "Purpose",
                "How to install, update, and remove the speech-"
                "recognition, diarization, and language models that "
                "Cortex runs locally.",
            ),
            (
                "Default models",
                "The installer bundles the default ASR model, the "
                "default diarization model, and a small default LLM. "
                "These are the only models needed to run Cortex out "
                "of the box.",
            ),
            (
                "Adding models",
                "Additional ASR or diarization models can be dropped "
                "into the configured models directory; Cortex picks "
                "them up on next start. Additional LLMs are pulled "
                "via the local LLM runtime's standard mechanism.",
            ),
            (
                "Updating models",
                "Updates ship with the application. When a Cortex "
                "update changes the default ASR model version, "
                "existing Transcripts are not re-processed — the "
                "Transcript's `model_version` field continues to "
                "report the version it was created with.",
            ),
            (
                "Switching models",
                "Switching the active LLM is a configuration change. "
                "Existing Notes pin the Template version they were "
                "extracted with, but not the LLM — re-running "
                "Extraction after switching LLMs may produce different "
                "output.",
            ),
        ],
    ),
    Page(
        path="ops/database-migrations.md",
        title="Database Migrations",
        category="ops",
        frontmatter=standard_frontmatter("platform-team"),
        sections=[
            (
                "Purpose",
                "How schema migrations are authored, run, and rolled "
                "back.",
            ),
            (
                "Authoring",
                "Migrations live as numbered SQL files in the "
                "migrations directory. Each migration is a single "
                "forward step; rollback is not automatic.",
            ),
            (
                "Running",
                "Migrations run automatically at startup. The backend "
                "refuses to start if a migration fails; the user is "
                "directed to the troubleshooting guide.",
            ),
            (
                "Rolling back",
                "Cortex does not support automatic rollback. To "
                "downgrade, the user restores the database from the "
                "automatic backup taken before each migration.",
            ),
            (
                "Backups",
                "A SQLite copy of the database is taken before each "
                "migration and kept in the data directory under "
                "`backups/`. The five most recent backups are "
                "retained.",
            ),
        ],
    ),
    Page(
        path="ops/troubleshooting-guide.md",
        title="Known Failure Modes",
        category="ops",
        frontmatter=standard_frontmatter("support-team"),
        sections=[
            (
                "Purpose",
                "Cortex's known failure modes and the in-app surfaces "
                "that recover from them.",
            ),
            (
                "Failure modes",
                "- **Backend startup blocked by port conflict.** The "
                "configured port is exposed in the settings file as "
                "`backend.port`.\n"
                "- **Transcription Job idle while LLM runtime is "
                "stopped.** The settings page shows runtime status "
                "and a 'Start runtime' control.\n"
                "- **Extraction Job exceeds its per-stage timeout when "
                "the configured LLM is too small for the Transcript.** "
                "The model selector in the settings page lists "
                "compatible larger models and the cloud fallback "
                "endpoint.\n"
                "- **Quality Flags emitted across the entire "
                "Recording.** The Audio Quality Service raises this "
                "pattern when the source media itself is low quality; "
                "no in-app recovery exists for the existing Recording.",
            ),
            (
                "Logs",
                "Backend logs land in `logs/cortex.log` inside the "
                "Cortex data directory. The settings page exposes a "
                "'Show logs' control that opens this file in the "
                "platform's default viewer.",
            ),
        ],
    ),
    Page(
        path="ops/oncall-runbook.md",
        title="On-call Runbook",
        category="ops",
        frontmatter=standard_frontmatter("support-team"),
        sections=[
            (
                "Purpose",
                "Cortex is local-first; there is no operations "
                "on-call rotation in the traditional sense. This "
                "runbook exists for support engineers responding to "
                "user reports.",
            ),
            (
                "First responders",
                "Support engineers triage user reports through the "
                "issue tracker. Critical-severity reports (data loss, "
                "data corruption, complete inability to start) "
                "escalate to the platform team.",
            ),
            (
                "Diagnostic bundle",
                "Users can produce a diagnostic bundle from the "
                "settings page that includes recent logs, the "
                "configuration file, and the migrations history. The "
                "bundle never contains Recording media, Transcript "
                "text, or Extraction content.",
            ),
            (
                "Escalation",
                "If a fix requires a code change, support files a "
                "ticket per "
                f"{link('process/ticket-conventions.md', 'Ticket Conventions')}. "
                "Hotfix releases follow "
                f"{link('process/release-process.md', 'Release Process')}.",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Process pages
# ---------------------------------------------------------------------------

PROCESS_PAGES: list[Page] = [
    Page(
        path="process/ticket-conventions.md",
        title="Ticket Conventions",
        category="process",
        frontmatter=standard_frontmatter("eng-leads"),
        sections=[
            (
                "Purpose",
                "Names the labels, milestones, and naming rules used "
                "when filing Cortex tickets. This page is the source "
                "of truth for any tool or skill that creates tickets "
                "on behalf of a developer.",
            ),
            (
                "Types",
                "Cortex uses four ticket types. They are not labels — "
                "they are explicit fields: Epic, Feature, Spike, Bug. "
                "Use Epic only when a body of work has multiple child "
                "tickets that belong together.",
            ),
            (
                "Labels",
                "Labels are area tags, never types. The accepted "
                "labels are:\n"
                "- `area:ingest` — work on the Ingest Service.\n"
                "- `area:transcription` — work on the Transcription "
                "or Diarization Service.\n"
                "- `area:extraction` — work on the Extraction "
                "Service or Templates.\n"
                "- `area:notes` — work on the Notes Service or "
                "Notes Explorer.\n"
                "- `area:frontend` — work on the web app outside of "
                "Notes Explorer (Template Editor, Settings, "
                "Component Library).\n"
                "- `area:platform` — Job Orchestrator, storage, "
                "realtime, deployment, infra.\n"
                "- `area:ml` — model runtime and model lifecycle.\n"
                "- `area:docs` — wiki and in-app documentation.",
            ),
            (
                "Milestones",
                "Milestone names follow `YYYY-QN` (e.g. `2026-Q2`). "
                "Quarterly milestones are advisory; tickets without a "
                "milestone are still actionable.",
            ),
            (
                "Naming",
                "Ticket titles use sentence case. They name the "
                "outcome, not the implementation. Bad: 'Add a "
                "useDebouncedSearch hook'. Good: 'Debounce notes "
                "explorer search input'.",
            ),
            (
                "Body",
                "Tickets answer **what** is being done and **how it "
                "will be verified**. The **why** lives in the wiki. "
                "If a ticket needs to justify itself, link to the "
                "wiki page that holds the justification — and if no "
                "such page exists, suggest creating one rather than "
                "inlining the rationale.",
            ),
            (
                "Acceptance criteria",
                "Acceptance criteria are falsifiable checks a "
                "reviewer can run. They are not restatements of "
                "scope, not project-wide baselines (build/lint/test "
                "expectations belong in the contributor docs), and "
                "not subjective ('feels idiomatic').",
            ),
        ],
    ),
    Page(
        path="process/release-process.md",
        title="Release Process",
        category="process",
        frontmatter=standard_frontmatter("eng-leads"),
        sections=[
            (
                "Purpose",
                "How Cortex versions are cut, signed, and shipped to "
                "users.",
            ),
            (
                "Cadence",
                "Minor releases ship monthly. Patch releases ship as "
                "needed. Major releases are reserved for changes to "
                "the data model that require user-visible migration.",
            ),
            (
                "Cut",
                "A release is cut by tagging the release commit with "
                "a semantic-version tag. CI builds installers for "
                "macOS, Windows, and Linux from the tag.",
            ),
            (
                "Signing",
                "Installers are signed with the platform's standard "
                "code-signing tool before they leave CI. Unsigned "
                "builds are not distributed.",
            ),
            (
                "Hotfixes",
                "Hotfixes branch from the most recent release tag, "
                "land the fix, and re-tag with a new patch version. "
                "Hotfixes ship installers immediately; main may not "
                "have caught up yet.",
            ),
        ],
    ),
    Page(
        path="process/documentation-style.md",
        title="Documentation Style",
        category="process",
        frontmatter=standard_frontmatter("docs-team"),
        sections=[
            (
                "Purpose",
                "The conventions wiki pages and in-app help text "
                "follow.",
            ),
            (
                "Scope",
                "The wiki is a living spec describing Cortex's current "
                "state in present tense. It carries vocabulary, "
                "structure, and reference material. Architectural "
                "decisions and the rationale behind them live in "
                "Architectural Decision Records under `adrs/`; wiki "
                "pages outside that folder describe what Cortex is, "
                "not why it got there.",
            ),
            (
                "Vocabulary",
                "Pages use the terms from "
                f"{link('glossary.md', 'Glossary')} and only those "
                "terms. New concepts are added to the glossary before "
                "they are introduced in body text.",
            ),
            (
                "Voice",
                "Pages are written in present tense, third person, "
                "indicative mood. User-facing surfaces (in-app help "
                "and the on-screen failure-mode descriptions) address "
                "the reader as 'you'.",
            ),
            (
                "Structure",
                "Every page opens with a Purpose section. Other "
                "section headings use Title Case. Cross-references "
                "are relative paths without the `.md` extension, "
                "rendered as `[Label](../folder/page)` from a "
                "subfolder or `[Label](folder/page)` from the wiki "
                "root.",
            ),
            (
                "Open questions",
                "Unresolved decisions live in an `## Open design "
                "decisions` section at the bottom of the relevant "
                "page and are removed once resolved. Tracked changes "
                "to the wiki itself live in "
                f"{link('changelog.md', 'Changelog')}.",
            ),
            (
                "Wiki vs. tickets",
                "The wiki carries vocabulary, structure, and "
                "reference content. Tickets carry the work to be "
                "done and how it is verified. Tickets link to wiki "
                "pages for context rather than restating it.",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# ADRs
# ---------------------------------------------------------------------------

ADR_PAGES: list[Page] = [
    Page(
        path="adrs/two-phase-pipeline.md",
        title="ADR: Two-phase Pipeline",
        category="adrs",
        frontmatter=standard_frontmatter("platform-team", "2025-09-04"),
        sections=adr_sections(
            context=(
                "An end-to-end Pipeline that runs transcription and "
                "extraction in a single inseparable step risks losing "
                "the Transcript when the LLM fails or when the user "
                "wants to re-run extraction with different settings. "
                "Transcripts are expensive to produce; Extractions "
                "are cheap and explicitly user-tunable."
            ),
            decision=(
                "The Pipeline is split into two phases: a Transcription "
                "Phase that ends with a sealed Transcript, and an "
                "Extraction Phase that consumes the Transcript and "
                "produces an Extraction. The phases are scheduled as "
                "separate Jobs by the Job Orchestrator and have "
                "separate failure modes."
            ),
            consequences=(
                "- A failed Extraction never costs the user their "
                "Transcript.\n"
                "- Re-running Extraction with a different Template "
                "is supported by construction.\n"
                "- The Pipeline has more moving parts; the Job "
                "Orchestrator must coordinate two Jobs per Recording "
                "rather than one."
            ),
            alternatives=(
                "A single fused Job was considered. It is simpler but "
                "fails the 'preserve Transcript on Extraction failure' "
                "requirement and would be hostile to the 'try a "
                "different Template' workflow."
            ),
        ),
    ),
    Page(
        path="adrs/local-first-default.md",
        title="ADR: Local-first by Default",
        category="adrs",
        frontmatter=standard_frontmatter("platform-team", "2025-08-21"),
        sections=adr_sections(
            context=(
                "Cortex's most-asked-for property in user research is "
                "that meeting audio never leaves the user's machine. "
                "Privacy-conscious users explicitly reject any tool "
                "that uploads recordings to a vendor."
            ),
            decision=(
                "Cortex runs entirely on the user's machine by "
                "default. All models are local; no external network "
                "call is required for the core flow. Cloud endpoints "
                "are an opt-in fallback."
            ),
            consequences=(
                "- The install footprint is large because models "
                "ship with the application.\n"
                "- Hardware requirements are higher than for a "
                "thin-client app.\n"
                "- Onboarding is simpler because the user is not "
                "asked to choose a cloud provider on first run.\n"
                "- Cortex's privacy story is enforceable, not "
                "promised."
            ),
        ),
    ),
    Page(
        path="adrs/sqlalchemy-core.md",
        title="ADR: SQL Builder over ORM",
        category="adrs",
        frontmatter=standard_frontmatter("platform-team", "2025-09-12"),
        sections=adr_sections(
            context=(
                "Cortex's query patterns are dominated by reads with "
                "specific joins and aggregations (e.g. listing Notes "
                "with their Quality Flag counts and primary speaker). "
                "ORM lazy loading is a common source of N+1 queries "
                "in shapes like this; the team also wants the same "
                "schema to work on SQLite and Postgres without "
                "diverging behaviour."
            ),
            decision=(
                "Use SQLAlchemy Core (the SQL builder layer) rather "
                "than the ORM. Service code writes explicit queries; "
                "row-to-dataclass conversion is a one-line helper."
            ),
            consequences=(
                "- Query performance is predictable; N+1 risks are "
                "visible in the code rather than hidden behind "
                "lazy loaders.\n"
                "- The same query expression runs against both "
                "SQLite and Postgres.\n"
                "- Service code is more verbose than ORM equivalents; "
                "this is accepted as a worthwhile cost."
            ),
        ),
    ),
    Page(
        path="adrs/sse-progress.md",
        title="ADR: SSE for Realtime Progress",
        category="adrs",
        frontmatter=standard_frontmatter("platform-team", "2025-10-02"),
        sections=adr_sections(
            context=(
                "The frontend needs to surface Job progress without "
                "polling. The two main candidates are Server-Sent "
                "Events and WebSockets."
            ),
            decision=(
                "Use Server-Sent Events. The frontend opens one SSE "
                "stream per user; the backend publishes Job events "
                "into it."
            ),
            consequences=(
                "- The protocol is unidirectional, which matches the "
                "use case (server pushes; client never pushes back).\n"
                "- SSE works through the FastAPI worker without a "
                "separate broker.\n"
                "- Reconnection with a `Last-Event-Id` header is "
                "trivial; the backend keeps a five-minute buffer per "
                "channel."
            ),
            alternatives=(
                "WebSockets were considered. They are a strict "
                "superset of SSE's capability but introduce "
                "complexity (custom protocol framing, keep-alives) "
                "without buying anything Cortex needs."
            ),
        ),
    ),
    Page(
        path="adrs/pyannote-diarization.md",
        title="ADR: Diarization Model Choice",
        category="adrs",
        frontmatter=standard_frontmatter("ml-team", "2025-10-15"),
        sections=adr_sections(
            context=(
                "Speaker diarization can run entirely with the ASR "
                "engine (some engines bundle a diarizer) or as a "
                "separate model invoked after ASR. The latter "
                "produces measurably better speaker boundaries on "
                "meeting audio with multiple participants."
            ),
            decision=(
                "Run diarization as a separate model after ASR. "
                "Cortex bundles a default diarization model and "
                "exposes it through the Diarization Service."
            ),
            consequences=(
                "- Diarization quality is meaningfully better on "
                "noisy meeting audio.\n"
                "- The Pipeline gains an extra stage and the model "
                "set gains an extra model; install footprint grows.\n"
                "- Future ASR engine swaps don't lose diarization "
                "quality because the diarizer is independent."
            ),
        ),
    ),
    Page(
        path="adrs/chunked-extraction.md",
        title="ADR: Chunked Extraction with Overlap",
        category="adrs",
        frontmatter=standard_frontmatter("ml-team", "2025-11-08"),
        sections=adr_sections(
            context=(
                "Long Transcripts (1+ hour meetings) exceed the "
                "context window of the default LLM. Naive truncation "
                "loses information; naive chunking at fixed "
                "boundaries loses Topics and Decisions that span the "
                "boundary."
            ),
            decision=(
                "The Extraction Service partitions long Transcripts "
                "into chunks sized for the LLM context window with a "
                "configurable overlap defaulting to 60 seconds of "
                "audio. Per-chunk Extractions are merged with "
                "duplicate detection on citation overlap."
            ),
            consequences=(
                "- No Topic or Decision is silently dropped at a "
                "chunk boundary.\n"
                "- Total LLM cost grows roughly with the number of "
                "chunks, not with audio length squared; the overlap "
                "is bounded.\n"
                "- The merge step adds complexity and introduces a "
                "well-defined failure mode (LLM produces conflicting "
                "summaries across chunks); this is handled by the "
                "Extraction Service's deduplication step."
            ),
        ),
    ),
    Page(
        path="adrs/llm-runtime-default.md",
        title="ADR: Local LLM Runtime Default",
        category="adrs",
        frontmatter=standard_frontmatter("ml-team", "2025-09-18"),
        sections=adr_sections(
            context=(
                "Cortex needs an LLM to power the Extraction Service. "
                "The choice is between bundling a self-hosted runtime "
                "(Ollama-compatible) or defaulting to a hosted "
                "provider with the option to switch."
            ),
            decision=(
                "Default to a local LLM runtime that exposes an "
                "OpenAI-compatible API. Cloud providers (OpenAI, "
                "Anthropic) are opt-in via configuration."
            ),
            consequences=(
                "- The default install includes a local LLM, "
                "increasing install footprint substantially.\n"
                "- Users with hardware that struggles to run a local "
                "LLM can opt into a cloud provider; this is "
                "documented in "
                f"{link('ops/troubleshooting-guide.md', 'Troubleshooting Guide')}.\n"
                "- The Extraction Service speaks the OpenAI chat-"
                "completions protocol; switching providers is a "
                "configuration change, not a code change."
            ),
        ),
    ),
    Page(
        path="adrs/template-versioning.md",
        title="ADR: Template Versioning Strategy",
        category="adrs",
        frontmatter=standard_frontmatter("product-team", "2025-12-03"),
        sections=adr_sections(
            context=(
                "Templates change over time as users tune their "
                "prompts. Existing Notes were extracted with the "
                "Template as it was at extraction time; later edits "
                "to the Template should not retroactively change "
                "what those Notes claim."
            ),
            decision=(
                "Templates are versioned. Each edit to a Template "
                "creates a new version with a monotonically "
                "increasing integer. Each Extraction pins the exact "
                "`(template_id, version)` it ran against; that pin "
                "is denormalised onto the Note as well."
            ),
            consequences=(
                "- Notes are reproducible: re-running Extraction on "
                "the same Note with the same pinned Template "
                "version produces structurally identical output "
                "(modulo LLM non-determinism).\n"
                "- The Template Service grows a version dimension; "
                "the Template Editor must surface version selection "
                "and a 'restore previous version' affordance.\n"
                "- Storage cost grows linearly with edit volume. "
                "Pruning old versions is deferred until a real user "
                "report identifies it as a problem."
            ),
            alternatives=(
                "A simpler 'mutate in place' model was rejected "
                "because it cannot satisfy the 'do not retroactively "
                "change a Note' invariant."
            ),
        ),
    ),
]


# ---------------------------------------------------------------------------
# Root pages
# ---------------------------------------------------------------------------

ROOT_PAGES: list[Page] = [
    Page(
        path="changelog.md",
        title="Changelog",
        category="root",
        frontmatter=standard_frontmatter("docs-team", "2026-04-15"),
        sections=[
            (
                "Purpose",
                "Record of additions, removals, and changes to the "
                "wiki. Entries describe what changed; the reasons "
                "live in commits and merge requests.",
            ),
            (
                "2026-04-15",
                "- Added: initial wiki content covering architecture, "
                "domain model, services, frontend, operations, "
                "process, and architectural decision records.\n"
                "- Added: Glossary as the canonical vocabulary for "
                "every other page.",
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

PAGES: list[Page] = (
    ROOT_PAGES
    + ARCHITECTURE_PAGES
    + DOMAIN_PAGES
    + SERVICE_PAGES
    + FRONTEND_PAGES
    + OPS_PAGES
    + PROCESS_PAGES
    + ADR_PAGES
)
