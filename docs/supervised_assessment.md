# Supervised Assessment Protocol

The app has two kinds of student interaction. Review is for learning and may include help. A supervised assessment is evidence of what the student can do independently during an in-person session.

## Instructor Workflow

1. Be present with the student and decide that the student is ready for the current week.
2. Run `python main.py --create-assessment`.
3. Share the displayed one-time code with the student.
4. Have the student run `python main.py --assessment` and enter the code.
5. Remain present while the student completes the questions and paper ledger work.
6. Review the generated file under `artifacts/assessments/`.

The code is valid for one assessment only. It is stored as a hash in `data/assessment_session.json`, which is local runtime state and should not be committed.

## Student Workflow

Review mode remains available with `python main.py`. During an assessment, use only the field materials and paper ledger allowed by the instructor. The assessment screen does not provide per-question correctness feedback or hints.

Assessment results are separate from review results. A passing assessment records the week in the game's verified progression state; a review attempt does not.

## What This Establishes

The one-time code proves that the instructor intentionally opened an assessment session and prevents accidental reuse of the same assessment. It cannot prove that no outside device or person was used. That part depends on the in-person supervision protocol.