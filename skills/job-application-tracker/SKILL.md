---
name: job-application-tracker
description: Track job applications, next steps, and deadlines.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: productivity
---

# Job Application Tracker

Keep one structured pipeline for a remote job hunt: every application, its current status,
the next step, and that step's deadline — plus a nudge when something is overdue or due
soon.

The hunt usually lives scattered across chats with recruiters, assessment portals, and an
inbox. This skill puts it in a single file the user owns, and answers three questions fast:
*where does everything stand*, *what is about to expire*, and *what do I do next*.

## When to Use

- The user mentions a new application, a reply, an assessment, an interview, an offer, or
  a rejection and expects it to be remembered.
- The user asks "where do my applications stand?", "what's next?", "anything overdue?".
- A weekly check-in is due, or the user asks for a pipeline digest.
- A deadline is approaching on an assessment, a take-home task, a follow-up, or a form the
  employer is waiting on.

## When Not to Use

- The user wants a résumé, cover letter, or application answers written — that is a
  different job; do it, then record the outcome here.
- The user wants a job *search*: this skill tracks applications already found or sent, it
  does not scrape boards or apply anywhere.
- The user only wants to vent about a rejection. Listen first; record the status change
  only once they want it recorded.

## Setup — first run only

Real data lives in `data/applications.json`, which is **never committed**: the skill ships
a `.gitignore` that excludes `data/`, and everything committed is fictional. Create the
private file by copying the shipped example, then replace the sample records with the
user's real ones.

```bash
mkdir -p data && cp examples/applications.example.json data/applications.json
```

```powershell
New-Item -ItemType Directory -Force data | Out-Null
Copy-Item examples/applications.example.json data/applications.json
```

Run these from the skill directory (`<skills root>/productivity/job-application-tracker/`).
`pipeline_status.py` is stdlib-only Python 3.8+ and needs no third-party packages; the
interpreter is `python3` on Linux and macOS, `python` (or `py -3`) on Windows.

## Data Model

One JSON file, `{"applications": [...]}`, one object per application:

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Short slug, unique, e.g. `nimbus-support-agent`. Used to refer to the record. |
| `company` | yes | e.g. `Nimbus Cloudworks`. |
| `role` | yes | As the posting words it, e.g. `Support Team Lead (Remote)`. |
| `status` | yes | `researching`, `applied`, `assessment`, `interview`, `offer`, `rejected`, `withdrawn`, `watching`. |
| `pay` | no | As stated, e.g. `$50/hr`. Never converted, never guessed. |
| `source` | no | Where it was found or applied through. |
| `date_applied` | no | `YYYY-MM-DD`, or `null` if nothing was sent yet. |
| `next_step` | no | The single next action, in the user's words, e.g. `Finish the language screening assessment`. |
| `next_step_deadline` | no | `YYYY-MM-DD` or `null`; needs a non-empty `next_step`. |
| `notes` | no | Free text. **Never a password, token, code, or security answer.** |

[`references/data-format.md`](references/data-format.md) has the full rules: what each
status means, which ones close an application, and how deadlines are compared.

Write the file by hand (or with a JSON edit) and let the script validate it: any unknown
field, bad date, bad status, or duplicate `id` is reported with its position, and nothing is
changed on disk. Records are stored in the order they were added; the report sorts them.

## Behaviors

### 1. Add or update an application

- **Never invent data.** Record only what the user states, or what a source they pointed at
  actually shows. If a date, a rate, or a status is unknown, leave `date_applied` / `pay`
  as `null` or omit the field — do not default to today, do not guess a pay band, do not
  assume a status from silence.
- On a new application: derive a slug `id` from company plus role (`harbourview-inbox-lead`),
  check it is not already used, then add the record with the status that is true right now.
- On an update: edit the existing record — status, `next_step`, `next_step_deadline`,
  `notes` — and keep `date_applied` as it was. Never re-add a record that already exists.
- Status moves the way a hunt moves: sent → `applied`; a task, test, or screening → `assessment`;
  a scheduled call or panel → `interview`; an offer → `offer`; closed by them → `rejected`;
  closed by the user → `withdrawn`. `researching` is before anything is sent, `watching` is
  for an opening being tracked without an active application.
- When an update lands, also set the *next* step and its deadline, or clear both (`""` and
  `null`) if nothing is pending. A stale next step is worse than none.
- After every change, run the script (below) to confirm the file still parses and to show
  the user the new pipeline state.
- Quote the user's own wording for `next_step` when they give it; keep `notes` to facts
  (recruiter name, timezone requirement, what the interview covers, what was promised).
- Some steps are the user's alone: an AI-proctored assessment, a video interview, an
  identity check, a signature. Record them, chase them, and say plainly that the user has
  to do that one. Never offer to sit it for them.

### 2. Pipeline view — group by status

Groups print in pipeline order (`researching` → `watching`), each with a count, so a glance
answers "how many live interviews do I have?":

```bash
python3 scripts/pipeline_status.py
```

```powershell
python scripts/pipeline_status.py
```

```
job application pipeline
data:  <skill>/data/applications.json
today: 2026-10-12

5 applications tracked: 1 applied, 1 assessment, 1 interview, 1 rejected, 1 watching

applied (1)
  - harbourview-inbox-lead: Harbourview Logistics - Inbox Support Team Lead (Remote) ($31/hr)
      applied 2026-09-28 | via referral | next: Follow up if there is no reply by Friday (deadline 2026-10-16, due in 4 days)

assessment (1)
  - lumen-data-annotator: Lumen Data Co - Data Annotator - Arabic (Contract) ($18/hr)
      applied 2026-10-02 | next: Finish the language screening assessment (deadline 2026-10-11, overdue by 1 day)

interview (1)
  - nimbus-support-agent: Nimbus Cloudworks - Customer Support Agent (Remote) ($22/hr)
      applied 2026-10-05 | next: 30-minute video interview with the support lead (deadline 2026-10-14, due in 2 days)
```

*(Output from the fictional example file; a real pipeline has the user's own records.)*

Options: `--data PATH` for another file, `--today YYYY-MM-DD` for a reproducible report,
`--due-soon-days N` to widen or narrow the nudge window (default 3).

### 3. Nudges for overdue and due-soon next steps

The same command ends with a **needs attention** section. An application is surfaced when
its status is *not* `offer`, `rejected`, or `withdrawn` **and** its `next_step_deadline` is
past or within 3 days:

```
needs attention (2)
  - [overdue] lumen-data-annotator: Lumen Data Co - Data Annotator - Arabic (Contract) ($18/hr)
      applied 2026-10-02 | next: Finish the language screening assessment (deadline 2026-10-11, overdue by 1 day)
  - [due soon] nimbus-support-agent: Nimbus Cloudworks - Customer Support Agent (Remote) ($22/hr)
      applied 2026-10-05 | next: 30-minute video interview with the support lead (deadline 2026-10-14, due in 2 days)

privacy warnings (0)
  none: no free-text field looks like a password, token or code
```

- Overdue first, sorted by deadline. `[overdue]` and `[due soon]` are the two labels.
- Report the section as it stands; do not soften an overdue item, and do not add one that
  the file does not contain.
- A record with no deadline is never flagged, and closed applications are never nudged —
  an offer is a decision, and a rejection cannot be chased.
- For each flagged item, say what the step is, what the deadline was, and who has to do it
  (the user, the employer, or nobody — waiting is fine). Then offer the obvious help:
  draft the follow-up, block the time, or clear the step if it is done.
- The report ends with a **privacy warnings** count for free text that looks like a pasted
  credential. If it is non-zero, tell the user which record and which field, and move the
  value to their password manager — never echo the value itself.

### 4. Weekly review

Once a week — or whenever the user asks for a digest — run the script and add a short
narrative. Keep it under about a dozen lines:

1. **Where things stand**: totals per status, and how many are open at all.
2. **Moved this week**: applications whose status changed since the last digest.
3. **Stuck**: open applications with no deadline and no movement for a while, if the user
   has dates on them.
4. **Needs attention**: the overdue / due-soon list, verbatim.
5. **Next three actions**, in priority order, each with a date or an explicit "no date".
6. **Decisions only the user can make**: accept or decline, chase a silent recruiter, drop
   a dead one, withdraw from one that no longer fits.

Then ask whether anything happened that the file does not know about, and update what the
user reports. Do not add speculative entries.

## Privacy Rules

This repository is public and the data file is not part of it.

- Real data goes in `data/applications.json` only. `data/` is ignored by this skill's
  `.gitignore`; if it is ever staged, stop and say so.
- Committed examples are fictional. Never copy a real company, recruiter, rate, or note
  into `examples/`, a test fixture, `SKILL.md`, or a commit message.
- `notes` and `next_step` hold logistics, not secrets. Passwords, API keys, one-time codes,
  and security answers belong in the user's password manager; the script warns when free
  text looks like one — and it never prints the matched value.
- Never put personal data in a filename, a branch name, or a PR title, and never paste the
  content of `data/applications.json` into a chat with anyone else.

## Completion Checklist

Before saying the pipeline is up to date, confirm:

- Every new or changed application reflects what the user actually said or a source they
  pointed at — no invented statuses, dates, rates, or next steps.
- Each open record has either a next step with a deadline, or an explicit no-deadline next
  step; nothing was quietly dropped.
- `pipeline_status.py` exits 0, and the printed pipeline matches the record the user just
  described.
- Overdue and due-soon items were surfaced without softening, and each says who must act.
- Closed applications (`offer`, `rejected`, `withdrawn`) were not nudged.
- No credential-like text was added to any field, and the privacy warning count is zero.
- `data/applications.json` is still untracked by git.
