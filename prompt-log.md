# PayLink - Prompt Log

Maintained by Student 2 (AI Log Lead). Every team member adds their own rows through a pull request; Student 2 merges, checks the format and keeps the summary up to date.

**Rules (brief, section 5):** structured prompts (role, context, constraints, output format, example when useful); honest verdicts (**Accepted**, **Fixed**, **Rejected**) with the reason; rejected answers earn marks when the reason is explained; never paste passwords, real personal data or other teams' code; name the AI tool in the commit message when AI wrote more than half of a change.

**Phase 1 minimum:** 5 entries, including 2 where the first AI answer was wrong and the prompt was improved.

## Summary (update before tagging `phase-1`)

| Item | Required | Current |
|---|---|---|
| Total entries | 5 | 4 (Student 2 only; teammates add theirs) |
| Entries where the first answer was wrong and the prompt was improved | 2 | to be confirmed from the verdicts below |
| Entries per student | - | S1: 0, S2: 4, S3: 0, S4: 0 |

## Log

| # | Date | Author | Stage | Tool and model | Prompt | Summary of answer | Verdict (accepted, fixed, rejected) and why |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-23 | Student 2 | Requirements | Claude (claude.ai) | **Role:** requirements analyst for a bill-payment backend. **Context:** PayLink brief sections 2.2 to 2.7 and 3.2, and Student 1's `req-p1.md` (US-1 to US-9). **Task:** write US-10 to US-19 for FR-10 to FR-19. **Constraints:** Given/When/Then, MoSCoW from the brief, exact decimals, hard cases 1 to 6 must be covered, same format as `req-p1.md`. **Output:** one Markdown section per story with a table of contents. | 10 user stories with 5 to 6 criteria each, using the brief's numbers (352.50 EGP example, 5,000 / 30,000 limits, 40% commission). | _Student 2: fill in after your review._ Review points to check: criteria are testable; numbers match the brief; no invented rules. |
| 2 | 2026-11-23 | Student 2 | Requirements | Claude (claude.ai) | **Role:** requirements analyst. **Context:** same brief and `req-p1.md`, including its open questions Q1 to Q6. **Task:** list the ambiguities in sections 2.5 to 2.7 and propose a decision for each, with the options considered. **Output:** table with question, options, decision, affected story. | Ambiguity table (rounding, idempotency key lifetime, agent payer, callback trust, TopUpNet wait time, daily limit scope, refund of a Completed payment, and others). | _Student 2: fill in._ Review points: the refund of a Completed payment versus "Completed is final" (A-7) and the TopUpNet callback deadline (A-12) are the team's own interpretations and are marked **Confirm** with the TA. |
| 3 | 2026-11-23 | Student 2 | Design | Claude (claude.ai) | **Role:** software designer using PlantUML. **Context:** payment life-cycle table from brief section 2.5. **Task:** write a state diagram. **Constraints:** only the transitions in the table; mark Completed, Rejected and Refunded as final; show the retry loop on Unknown; no extra states. **Output:** `.puml` source only. | PlantUML state diagram with 8 states, the 9 transitions of the table, a self-loop on Unknown for retries, entry notes and a legend. Rendered to PNG with PlantUML to check syntax. | _Student 2: fill in._ Review points: compare each arrow with the 9 rows of the brief table; check that Failed is not final; check that Unknown has no arrow to Refunded. |
| 4 | 2026-11-23 | Student 2 | Requirements | Claude (claude.ai) | **Role:** quality engineer. **Context:** brief section 3.3 quality table. **Task:** write 6 non-functional requirements with numbers and a way to measure each. **Output:** table with ID, quality, requirement, measurement, related stories. | NFR-1 to NFR-6 (correctness, performance, resilience, modifiability, auditability, testability) with numbers such as 100 payments/s for 60 s and 70% coverage. | _Student 2: fill in._ Review point: the 500 ms p95 and 99% success figures are the team's own targets, not numbers from the brief; keep them only if the team agrees. |
| 5 | | Student 1 | | | | | _Student 1 adds rows (requirements part 1, use-case diagram, repository setup)._ |
| 6 | 2026-11-24 | Student 3 | Requirements | Gemini | **Role:** Business Analyst for PayLink backend. **Context:** Brief sections 2.5–2.7, 3.2 (FR-20 to FR-28), and team decisions in `req-p2.md` (including A-7). **Task:** Write User Stories US-20 to US-28 with Given/When/Then criteria and MoSCoW priorities. **Constraints:** Cover Hard Cases 3, 5, 7; use exact decimals; keep Completed final per A-7. **Output:** Markdown file `/docs/req-p3.md`. | Generated 9 user stories (`US-20` to `US-28`) with acceptance criteria covering support search, account blocking, notification retries, dynamic config, immutable audit logs, reconciliation discrepancies, completed refunds, and daily totals. | **Accepted:** All acceptance criteria are testable, align with `req-p2.md` conventions and decision `A-7`, and cover Hard Cases 3, 5, and 7 without inventing conflicting rules. |
| 7 | 2026-11-24 | Student 3 | Design | Gemini | **Role:** Software Architect. **Context:** PayLink payment workflow (Brief sections 2.2, 2.3, 2.5) and `state-payment.puml`. **Task:** Generate two PlantUML sequence diagrams (`seq-pay-bill.puml` and `seq-refund.puml`). **Constraints:** Enforce hold before biller call, immutable ledger entries (`available_balance` / `held_balance`), no direct `Unknown -> Refunded` transition, and async notifications. **Output:** Raw PlantUML source files. | Generated `seq-pay-bill.puml` and `seq-refund.puml` covering idempotency, fraud chain, ledger holds, timeout (`Unknown`), refusal (`Failed -> Refunded`), and async notifications. | **Fixed:** In the initial draft, the AI called the external biller before holding wallet funds, updated a single `wallet.balance` field directly instead of inserting immutable ledger entries, and transitioned `Unknown` directly to `Refunded`. Refined the prompt with explicit constraints from Sections 2.2, 2.3, and 2.5 so holds happen before biller calls, balances are computed from ledger entries, and `Unknown` always transitions to `Failed` before `Refunded`. |
| 8 | | Student 4 | | | | | _Student 4 adds rows (ER diagram, Docker, compose, GitHub Actions)._ |

> Rows 1 to 4 describe the prompts as structured prompts. Replace the prompt text with the exact prompt you used if it was different, and write the real verdict. Do not mark an answer "wrong" unless it really was; the grader checks the log against the commits.

## Template for a new row

| # | Date | Author | Stage | Tool and model | Prompt | Summary of answer | Verdict (accepted, fixed, rejected) and why |
|---|---|---|---|---|---|---|---|
| n | YYYY-MM-DD | Student X | Requirements / Design / Code / Tests / Pipeline / ADR | tool name and model | Role: ... Context: ... Constraints: ... Output format: ... | 2 lines | Fixed: what was wrong or missing (for example "the AI missed the held balance in the wallet class") and what the improved prompt added |

## Merge checklist (Student 2, before tagging `phase-1`)

1. Collect each student's rows by pull request; keep one table, ordered by date; renumber the `#` column.
2. Check each row has a real prompt, a short summary and a verdict with a reason.
3. Count at least 5 entries and at least 2 where the first answer was wrong and the prompt was improved; update the summary table above.
4. Check that no row contains passwords, real personal data or other teams' code.
5. Check that commits with mostly AI-written content name the AI tool in the commit message.
