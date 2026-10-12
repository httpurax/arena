# Application data format

One JSON file holds the whole pipeline. The file is **private**: real data lives in
`data/applications.json`, which the skill's `.gitignore` keeps out of the repository. The
only data file in this repository is the fictional
[`examples/applications.example.json`](../examples/applications.example.json).

```json
{
  "applications": [
    {
      "id": "nimbus-support-agent",
      "company": "Nimbus Cloudworks",
      "role": "Customer Support Agent (Remote)",
      "pay": "$22/hr",
      "source": "WeWorkRemotely listing",
      "date_applied": "2026-10-05",
      "status": "interview",
      "next_step": "30-minute video interview with the support lead",
      "next_step_deadline": "2026-10-14",
      "notes": "Recruiter said no take-home task."
    }
  ]
}
```

The top level is an object with one key, `applications`, whose value is a list of records.

## Fields

| Field | Required | Type | Rules |
|---|---|---|---|
| `id` | yes | text | Short slug, unique in the file: lowercase letters, digits and single hyphens (`nimbus-support-agent`). It is how the record is referred to in every command and in the report. |
| `company` | yes | text | Non-empty. |
| `role` | yes | text | Non-empty. Keep the posting's own wording so a follow-up can quote it. |
| `status` | yes | text | One of the eight statuses below, exactly. |
| `pay` | no | text | Free text as the posting states it (`$50/hr`, `$2,000/mo`, `not stated`). Never convert or estimate. |
| `source` | no | text | Where the opening was found and/or applied through (`job board`, `company site`, `recruiter`, `referral`). |
| `date_applied` | no | text or `null` | `YYYY-MM-DD`. `null` when the user has not applied yet (a `researching` or `watching` record). |
| `next_step` | no | text | The single next action, in the user's words. Empty when nothing is pending. |
| `next_step_deadline` | no | text or `null` | `YYYY-MM-DD`. Requires a non-empty `next_step`. |
| `notes` | no | text | Free text. **Never a password, token, code, or security answer.** |

Unknown fields are rejected rather than ignored, so a typo (`next_step_deadlin`) is reported
instead of silently dropping the deadline it was meant to carry. Every problem is listed with
its position (`applications[3].status`) so a whole file can be fixed from one report.

## Statuses

In pipeline order — the order the report prints them in:

| Status | Means | Counts as open? |
|---|---|---|
| `researching` | Looking into the company or the role; nothing sent yet. | yes |
| `applied` | Application sent, waiting on a reply. | yes |
| `assessment` | A task, test, screening, or skills assessment is in play. | yes |
| `interview` | One or more interviews are scheduled or in progress. | yes |
| `offer` | An offer exists (accepted or not). | no |
| `rejected` | Closed by the company. | no |
| `withdrawn` | Closed by the user. | no |
| `watching` | Tracking an opening that is not an active application (portal closed, awaiting re-open, considering). | yes |

`offer`, `rejected` and `withdrawn` are **closed**: the report never nudges them, even if a
stale `next_step_deadline` is still in the record.

## Deadlines and nudges

An application needs attention when **both** of these are true:

1. its `status` is not `offer`, `rejected`, or `withdrawn`; and
2. its `next_step_deadline` is in the past **or** within the next 3 days (the due-soon
   window; `--due-soon-days N` changes it).

The report labels each one `[overdue]` or `[due soon]` and sorts them by deadline, so the
most urgent is first. A record with no deadline is never flagged: the skill does not invent
urgency the user never recorded.

Dates are compared as calendar days in the user's local timezone — no time-of-day, no
timestamps. `--today YYYY-MM-DD` overrides "today" so a report is reproducible.

## Privacy rules

- `data/` is listed in this skill's `.gitignore`; `data/applications.json` must never be
  committed, attached, or pasted into a chat.
- `notes` and the other free-text fields are for logistics only: recruiter names, timezone
  requirements, rate, interview topics, next action. A portal password, an API key, a
  one-time code, or a security answer belongs in the user's password manager, not here.
- `pipeline_status.py` scans `next_step` and `notes` and prints a **privacy warning** for
  anything shaped like `password: ...`, `token = ...`, and similar. It warns; it never
  prints the value it matched.
- Anything a third party could use to impersonate the user is a credential, even if it
  looks like ordinary text.
