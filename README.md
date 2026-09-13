# Herp & Rodent Haven

A text-based business simulation that turns advanced math (Precalculus/Algebra II) and practical
financial literacy into a hands-on, paper-ledger-and-terminal game. The player runs a virtual
exotic pet shop; every business decision is really a math problem in disguise.

This repo is the actual engine and content used for a one-on-one home study program — not a
generic template. It's shared here so the student can play from their own machine and so the
whole thing is transparent and versioned.

---

## Who this is for

| If you're the... | Start here |
| --- | --- |
| **Student** | [Playing as the student](#playing-as-the-student) |
| **Parent** | [What this actually is](#what-this-actually-is) |
| **Instructor** | [Running instructor mode](#running-instructor-mode) |

---

## What this actually is

Each week, the student gets a dashboard (cash, debt, reputation, unlocked modules) and a small set
of tasks spanning operations math, compound interest, population growth modeling, and pricing
optimization — plus a short written reflection. Answers are worked out by hand on paper first, then
entered into the program for validation.

- **Review Mode** — practice, retries, and outside help (including AI) are fine. It's for learning.
- **Supervised Assessment Mode** — a one-time instructor code, no hints, no feedback, done in person.
  This is the only mode that can unlock official progression.
- **Instructor Console** — preview any week's content, adjust difficulty, and review artifacts,
  without ever touching the student's real save file.

Nothing here grades homework silently in the background. The math engine and answer keys are kept
out of plain sight in the source (see [Source privacy](#source-privacy-note)), and every reflection
or assessment result is saved as a plain JSON artifact so a parent or instructor can always see
exactly what was recorded and when.

---

## Playing as the student

You need Python 3.11+ and (optionally) `git` if you want to pull weekly updates and back up your
work — ask your instructor for the repo link.

```bash
python3 main.py
```

That runs your current week: a dashboard, a handful of ledger tasks, and a reflection question.
Your progress is saved automatically to `data/game_state.json` after each turn — that file is
yours; it never gets uploaded anywhere.

If you're working from a cloned copy of this repo:

```bash
python3 main.py --sync     # pull the latest unlocked modules/difficulty from your instructor
python3 main.py --submit   # push your saved artifacts/ (reflections) back to the shared repo
```

`--sync` only ever updates difficulty settings and unlocked modules — it will never touch your
cash, debt, reputation, or week progress. `--submit` only ever commits the `artifacts/` folder.

When your instructor gives you a one-time assessment code in person:

```bash
python3 main.py --assessment
```

---

## Running instructor mode

```bash
python3 main.py --admin              # preview lesson content and current difficulty
python3 main.py --demo               # same, using a demo profile (won't touch the real save)
python3 main.py --create-assessment  # generate a one-time supervised assessment code
```

To freely explore any week's content — play through it, try `--admin`, generate assessment
codes — without any risk to the student's real save or artifacts, use the sandbox script:

```bash
./scripts/demo_week.sh
```

This swaps in a demo save (all modules unlocked, difficulty bumped) for the duration of an
interactive shell session, and automatically restores the real `data/game_state.json` and
`artifacts/` the moment you exit (normal exit, Ctrl+C, or a crash all trigger the rollback).

Adjust week-to-week difficulty and module unlocks in `data/weekly_config.json` — commit and push
that file, and the student picks it up with `--sync`.

---

## Source privacy note

Per the design goals, answer keys and validation logic live in `engine/math_engine.py` as SHA-256
hashes, not plaintext — so a curious student browsing the repo (which they're welcome to clone)
can't just read the answers off the page. It's a deterrent appropriate for a home-study context,
not a cryptographic guarantee.

---

## Project layout

```
main.py                    # CLI entry point (student play, --admin, --sync, --submit, --assessment)
data/
  game_state.json           # per-machine save file (gitignored, never shared)
  weekly_config.json         # instructor-controlled difficulty/unlocks (tracked, synced via git)
docs/                       # markdown field guides, one per week
artifacts/                  # saved reflections and assessment records (JSON)
engine/
  state.py                  # GameState persistence + weekly-config merging
  math_engine.py             # hashed answer validation + growth/interest formulas
  events.py                  # market event generator
  assessment.py               # one-time supervised assessment codes
  admin.py                    # instructor preview helpers
  git_sync.py                  # conservative git pull/push wrappers for --sync/--submit
  ui.py                         # small ANSI terminal UI helpers
scripts/
  demo_week.sh                  # sandboxed instructor preview with automatic rollback
tests/                       # unit tests (run with: python -m unittest discover -s tests -v)
```

## Running tests

```bash
python -m unittest discover -s tests -v
```
