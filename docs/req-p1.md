PayLink — Phase 1: Requirements Pack (Part 1)
Requirements & Product Lead Deliverable

Owner: Student 1 — Moumen Khaled Mahmoud Abd Elatif (20242359)

Role: Requirements & Product Lead

Repository: github.com/Moumen Khaled35/PayLink-Year-Work

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

Phase 1 — Deliverable Summary
Item	Coverage
Problem Summary	Completed
Stakeholders	5 stakeholders
User Stories	US-1 to US-9
Functional Requirements	FR-1 to FR-9
Open Questions	Q1 to Q6
Use-Case Diagram	Included
AI Draft Review	Corrected

Final Status
Ready for phase-1 tag
