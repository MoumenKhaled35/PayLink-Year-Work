PayLink — Phase 1: Requirements Pack (Part 1)
Requirements & Product Lead Deliverable

Owner: Student 1 — Moumen Khaled Mahmoud Abd Elatif (20242359)

Role: Requirements & Product Lead

Repository: github.com/MoumenKhaled35/PayLink-Year-Work

Target Git Tag: phase-1

Technology Stack: Python 3.12 + FastAPI + PostgreSQL
Reviewed & Ready for phase-1 tag

1. Problem Summary
PayLink is a bill-payment and digital-wallet backend in Egypt. It allows customers to pay utility bills, including electricity, water, mobile, and internet bills, using money held in a digital wallet.

Customers can also top up their wallets through a simulated card or agent cash.

The system provides biller and service information, allows customers to inquire about a bill and review the amount, service fee, and total before paying, and supports payment from the wallet. Wallet balances must be based on ledger entries, and every balance change must be recorded.

Administrators manage billers and their services.

The central problem is to process bill payments reliably while:
- Preventing duplicate charges and overspending.
- Preserving funds when an external result is uncertain.
- Maintaining traceable records for financial and administrative actions.

2. Stakeholders
Stakeholder	Role & Responsibility
Customer	Registers, views wallet information and transaction history, tops up the wallet, views billers, makes bill inquiries, and pays bills.
Administrator (Admin)	Adds, edits, and disables billers and services; verifies customer accounts; configures fees and limits.
Agent	Provides the agent-cash wallet top-up channel and pays bills on behalf of customers.
Biller	Issues bills and receives payments from PayLink (ElectroCo, AquaCo, TopUpNet, and optional NetCo).
Teaching Assistant / Supervisor	Reviews requirement interpretations and confirms unresolved decisions.

3. User Stories and Acceptance Criteria (US-1 to US-9)
US-1 — Customer Registration
Must
 FR-1

User Story:

As a customer, I want to register an account so that I can use PayLink.

Acceptance Criteria:
- Given that a customer is not registered,
- When the customer completes registration,
- Then the system creates a customer account with the basic verification level.
US-2 — Upgrade Verification Level
Should
 FR-2

User Story:

As a customer, I want my account to be upgraded to the verified level so that I can use the higher payment limit.

Acceptance Criteria:
- Given that a customer has the basic verification level,
- When the account is upgraded to the verified level,
- Then the customer's daily payment limit becomes 30,000 EGP instead of the basic limit of 5,000 EGP.
US-3 — View Wallet and Transaction History
Must
 FR-3

User Story:

As a customer, I want to view my available balance, held balance, and transaction history so that I can track my wallet.

Acceptance Criteria:
- Given that a customer has a wallet,
- When the customer requests wallet information,
- Then the system displays the available balance, held balance, and transaction history.
US-4 — Top Up Wallet
Must
 FR-4

User Story:

As a customer, I want to top up my wallet using a simulated card or agent cash so that I can add money to my wallet.

Acceptance Criteria:
- Given that a customer has a wallet,
- When the customer tops up using a simulated card or agent cash,
- Then the system processes the wallet top-up.
US-5 — Record Wallet Balance Changes in the Ledger
Must
 FR-5

User Story:

As a system stakeholder, I want every wallet balance change to create a ledger entry so that wallet balances are calculated from recorded money movements.

Acceptance Criteria:
1. Given that a wallet balance changes, when the change is recorded, then the system creates a ledger entry for that change.
2. Given that a wallet balance is requested, when the system calculates the balance, then it calculates it from the wallet's ledger entries.
US-6 — Manage Billers and Services
Must
 FR-6

User Story:

As an administrator, I want to add, edit, and disable billers and services so that the biller catalog can be maintained.

Acceptance Criteria:
1. Given that an administrator is managing the biller catalog, when the administrator adds a biller or service, then the system stores it.
2. Given that a biller or service exists, when the administrator edits it, then the system saves the changes.
3. Given that a biller or service exists, when the administrator disables it, then the system marks it as disabled.
US-7 — View Billers and Required Input Fields
Must
 FR-7

User Story:

As a customer, I want to see the available billers and the input fields required by each one so that I know what information to provide.

Acceptance Criteria:
- Given that the biller catalog contains billers and services,
- When the customer views the catalog,
- Then the system displays the billers and the input fields required by each.
US-8 — Inquire About a Bill
Must
 FR-8

User Story:

As a customer, I want to inquire about a bill and see its amount, fee, and total before paying so that I know the full amount due.

Acceptance Criteria:
- Given that the customer provides the required bill information,
- When the customer runs a bill inquiry,
- Then the system displays the bill amount, service fee, and total before payment.
US-9 — Pay a Bill from the Wallet
Must
 FR-9

User Story:

As a customer, I want to pay a bill from my wallet so that I can complete bill payments through PayLink.

Acceptance Criteria:
- Given that a customer has a bill to pay,
- When the customer chooses to pay using the wallet,
- Then the system processes the bill payment from the customer's wallet.

4. Open Questions Passed to Part 2 (Q1–Q6)
ID	Question	Handover Decision / Status
Q1	How does a user log in (password, OTP)?	Assumed phone number + password + token for Phase 1; OTP deferred.
Q2	Does an agent cash top-up debit the agent's wallet?	Yes, atomic debit from agent wallet and credit to customer wallet.
Q3	Maximum top-up amount?	Any positive amount (> 0.00 EGP); configurable cap deferred.
Q4	Who verifies a customer (FR-2)?	Admin after external identity verification.
Q5	Where does the amount come from for NetCo (no live inquiry)?	Entered by customer and validated against service min/max limits.
Q6	Does the 5–10,000 EGP single-payment range include the service fee?	Applied to total charge (bill_amount + service_fee); marked Confirm with TA.

5. Use-Case Diagram & AI Draft Review
Artifact: docs/design/Use-Case-Digram.png

Source: docs/design/use-case.puml
AI Error & Correction Note (Prompt Log #5)
In the initial AI draft, the Use-Case diagram covered only FR-1 to FR-9 and had several omissions:

1. Omitted the Support Employee actor and the following use cases:
- Search Payment.
- Block/Unblock Account.
- Approve Refund.
2. Missed Admin reconciliation and reporting use cases.

3. Lacked <<include>> relationships for fraud checks.

Correction:

The prompt was refined to cover all 28 requirements (FR-1 to FR-28) and all human/external actors.

The report was also corrected to use the exact user stories from this file (US-1 to US-9).

6. Prompt Log (Team AI Usage Log — maintained by Student 2)

# PayLink - Prompt Log

Maintained by Student 2 (AI Log Lead). All entries follow the structured prompting guidelines in Section 5 of the project brief (Role, Context, Constraints, Output Format) with honest verdicts documenting accepted outputs and iterative prompt refinements.

## Summary

| Item | Required | Current |
|---|---|---|
| Total entries | 5 | 8 |
| Entries where the first answer was wrong and the prompt was improved | 2 | 3 |
| Entries per student | - | S1: 1, S2: 4, S3: 2, S4: 1 |

## Log

| # | Date | Author | Stage | Tool and model | Prompt | Summary of answer | Verdict (accepted, fixed, rejected) and why |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-23 | Student 2 | Requirements | Claude (claude.ai) | Role: requirements analyst for a bill-payment backend. Context: PayLink brief sections 2.2 to 2.7 and 3.2, and Student 1's `req-p1.md` (US-1 to US-9). Task: write US-10 to US-19 for FR-10 to FR-19. Constraints: Given/When/Then, MoSCoW from the brief, exact decimals, hard cases 1 to 6 must be covered, same format as `req-p1.md`. Output: one Markdown section per story with a table of contents. | 10 user stories with 5 to 6 criteria each, using the brief's numbers (352.50 EGP example, 5,000 / 30,000 limits, 40% commission). | Accepted: All acceptance criteria are testable in Given/When/Then format, use exact decimal monetary values, match the business rules in Section 2.6, and cover Hard Cases 1 to 6 without inventing conflicting rules. |
| 2 | 2026-11-23 | Student 2 | Requirements | Claude (claude.ai) | Role: requirements analyst. Context: same brief and `req-p1.md`, including its open questions Q1 to Q6. Task: list the ambiguities in sections 2.5 to 2.7 and propose a decision for each, with the options considered. Output: table with question, options, decision, affected story. | Ambiguity table (rounding, idempotency key lifetime, agent payer, callback trust, TopUpNet wait time, daily limit scope, refund of a Completed payment, and others). | Accepted: Documented 16 specification ambiguities (A-1 to A-16) with clear options and engineering decisions; team interpretations such as Completed payment refunds (A-7) and TopUpNet callback deadline (A-12) are explicitly flagged Confirm for TA review before Phase 2. |
| 3 | 2026-11-23 | Student 2 | Design | Claude (claude.ai) | Role: software designer using PlantUML. Context: payment life-cycle table from brief section 2.5. Task: write a state diagram. Constraints: only the transitions in the table; mark Completed, Rejected and Refunded as final; show the retry loop on Unknown; no extra states. Output: `.puml` source only. | PlantUML state diagram with 8 states, the 9 transitions of the table, a self-loop on Unknown for retries, entry notes and a legend. Rendered to PNG with PlantUML to check syntax. | Accepted: Verified line by line against brief Section 2.5; includes all 8 states, the exact 9 allowed transitions, the internal retry self-loop on `Unknown`, final markers on `Completed`, `Rejected`, and `Refunded`, and entry notes preventing auto-refunds from `Unknown`. |
| 4 | 2026-11-23 | Student 2 | Requirements | Claude (claude.ai) | Role: quality engineer. Context: brief section 3.3 quality table. Task: write 6 non-functional requirements with numbers and a way to measure each. Output: table with ID, quality, requirement, measurement, related stories. | NFR-1 to NFR-6 (correctness, performance, resilience, modifiability, auditability, testability) with numbers such as 100 payments/s for 60 s and 70% coverage. | Accepted: Covers all 6 required quality attributes with concrete quantitative targets (100 payments/s for 60s, >=70% domain coverage, 0 negative balances) and automated CI / load-test measurement methods. |
| 5 | 2026-11-24 | Student 1 | Design | Gemini | Role: Software Architect. Context: PayLink bill-payment and digital wallet system (FR-1 to FR-28). Task: Generate PlantUML code for a Use-Case Diagram covering all system actors and functional requirements. Constraints: Include Customer, Agent, Support Employee, Admin, and External Biller; include `<<include>>` relationships for fraud checks and notifications. Output: Raw PlantUML source code. | Generated a complete PlantUML Use-Case diagram covering all 4 human actors, External Billers, 19 core use cases across FR-1 to FR-28, and `<<include>>` dependencies for fraud checks/holds and notifications. | Fixed: In the initial AI draft, the diagram only covered FR-1 to FR-9, omitted the `Support Employee` actor (`Search Payment`, `Block/Unblock Account`, `Approve Refund`), missed Admin reconciliation/reporting use cases, and lacked `<<include>>` relationships for fraud checks. Refined the prompt to cover all 28 requirements and actors. |
| 6 | 2026-11-24 | Student 3 | Requirements | Gemini | Role: Business Analyst for PayLink backend. Context: Brief sections 2.5–2.7, 3.2 (FR-20 to FR-28), and team decisions in `req-p2.md` (including A-7). Task: Write User Stories US-20 to US-28 with Given/When/Then criteria and MoSCoW priorities. Constraints: Cover Hard Cases 3, 5, 7; use exact decimals; keep Completed final per A-7. Output: Markdown file `/docs/req-p3.md`. | Generated 9 user stories (`US-20` to `US-28`) with acceptance criteria covering support search, account blocking, notification retries, dynamic config, immutable audit logs, reconciliation discrepancies, completed refunds, and daily totals. | Accepted: All acceptance criteria are testable, align with `req-p2.md` conventions and decision `A-7`, and cover Hard Cases 3, 5, and 7 without inventing conflicting rules. |
| 7 | 2026-11-24 | Student 3 | Design | Gemini | Role: Software Architect. Context: PayLink payment workflow (Brief sections 2.2, 2.3, 2.5) and `state-payment.puml`. Task: Generate two PlantUML sequence diagrams (`seq-pay-bill.puml` and `seq-refund.puml`). Constraints: Enforce hold before biller call, immutable ledger entries (`available_balance` / `held_balance`), no direct `Unknown -> Refunded` transition, and async notifications. Output: Raw PlantUML source files. | Generated `seq-pay-bill.puml` and `seq-refund.puml` covering idempotency, fraud chain, ledger holds, timeout (`Unknown`), refusal (`Failed -> Refunded`), and async notifications. | Fixed: In the initial draft, the AI called the external biller before holding wallet funds, updated a single `wallet.balance` field directly instead of inserting immutable ledger entries, and transitioned `Unknown` directly to `Refunded`. Refined the prompt with explicit constraints from Sections 2.2, 2.3, and 2.5 so holds happen before biller calls, balances are computed from ledger entries, and `Unknown` always transitions to `Failed` before `Refunded`. |
| 8 | 2026-11-24 | Student 4 | Design | Gemini | Role: Database and Domain Architect. Context: PayLink wallet, ledger, and bill payment rules (Brief sections 2.3, 2.6, 3.4). Task: Generate PlantUML Domain Class Diagram (`class-diagram.puml`) and ER Diagram (`er-diagram.puml`) with at least 10 relational tables. Constraints: Exact `DECIMAL(12,2)` types (no floats), separate `available_balance` and `held_balance`, immutable `ledger_entries` and `audit_logs`, unique `(customer_id, idempotency_key)`. Output: Raw PlantUML source files. | Generated `class-diagram.puml` and `er-diagram.puml` covering 12 tables (`customers`, `agents`, `wallets`, `ledger_entries`, `billers`, `biller_services`, `payments`, `payment_state_history`, `notifications`, `reconciliation_records`, `refund_requests`, `audit_logs`). | Fixed: In the initial draft, the AI used `FLOAT` for monetary columns and modeled `wallets` with a single `balance` column updated directly. Refined the prompt to enforce `DECIMAL(12,2)`, split `available_balance` and `held_balance` computed from immutable `ledger_entries`, and added `payment_state_history` and `refund_requests` to match `req-p2.md` and `req-p3.md`. |

Phase 1 — Deliverable Summary
Item	Coverage
Problem Summary	Completed
Stakeholders	5 stakeholders
User Stories	US-1 to US-9
Functional Requirements	FR-1 to FR-9
Open Questions	Q1 to Q6
Use-Case Diagram	Included
AI Draft Review	Corrected
Prompt Log	Included (8 entries)

Final Status
Ready for phase-1 tag
