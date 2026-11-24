# PayLink — Requirements Pack
**Course:** Advanced Software  
**Supervisor:** D. Doskey Abd Elqawy  
**Submission date:** 24 November 2026

## 1. Problem Summary
PayLink is a digital bill-payment and wallet backend. It allows customers to maintain a wallet, browse supported billers and services, inquire about bills, review service fees, and pay securely. Agents can perform payments for customers through an agent channel. The system integrates with billers that use different protocols, handles synchronous and asynchronous payment outcomes, and protects balances through holds and an auditable ledger. Support and administrative users manage accounts, billers, configuration, refunds, reconciliation, and reporting.

The central problem is to process bill payments reliably even when networks or external billers fail. PayLink must prevent duplicate charges, prevent overspending, preserve funds while a result is uncertain, provide clear customer notifications, and retain traceable records for every financial and administrative action.

**Scope note:** The supplied repository contains `req-p2.md` and `docs/req-p3.md`, but does not contain the referenced `req-p1.md` or the original assignment brief. Therefore, US-10 to US-28 and the detailed decisions/NFRs below are carried forward from the supplied files. US-1 to US-9 are reconstructed as a clearly marked draft from references in those files and must be checked against the missing Part 1/brief before final approval.

## 2. Stakeholders
| Stakeholder | Interest / responsibility |
|---|---|
| Customer | Register/use an account, fund a wallet, inquire about bills, pay, receive receipts and notifications, request refunds |
| Agent | Accept customer cash and pay bills through an agent wallet; receive eligible commission |
| Administrator | Verify customers, manage billers and service configuration, limits, fees, and reports |
| Support employee | Investigate payments, view histories, block/unblock accounts, review refund requests |
| Finance / Operations | Reconcile settlement files, review discrepancies, monitor daily financial totals |
| Compliance / Auditor | Verify immutable ledger and audit records and trace all money movements |
| External billers (ElectroCo, AquaCo, TopUpNet; optional NetCo) | Receive payment requests and return results using different protocols |
| Notification providers | Deliver SMS, push, and email messages |
| Development / QA team | Maintain adapters, enforce business rules, automate tests, and monitor quality |
| Teaching Assistant / Supervisor | Review requirement interpretations and confirm unresolved decisions |

## 3. User Stories (28 total)

### Part 1 — Reconstructed draft (US-1 to US-9)
> These nine stories are inferred from references in the supplied Part 2/3 files (for example, US-2 verification, US-4 top-up, US-5 ledger, US-8 inquiry, and US-9 payment). They are not a substitute for the missing `req-p1.md`.

#### US-1 — Authenticate and access the system (Must)
**As** a system user, **I want** to log in using my phone number and password, **so that** I can access functions allowed for my role.
- **Given** a registered active user with valid credentials, **when** the user submits them, **then** the system authenticates the user and issues an access token associated with the user's role.
- **Given** invalid credentials, **when** the user attempts to log in, **then** access is denied and no token is issued.
- **Given** an unauthenticated request to a protected endpoint, **when** it is received, **then** the system returns `401 Unauthorized`.
- **Given** an authenticated user without the required role, **when** the user calls a restricted endpoint, **then** the system returns `403 Forbidden`.

#### US-2 — Verify a customer account (Must)
**As** an administrator, **I want** to review and verify a customer's identity, **so that** higher-trust account capabilities can be granted.
- **Given** a customer account pending verification, **when** an administrator approves it after an identity check performed outside PayLink, **then** the account status becomes `VERIFIED` and the action is recorded.
- **Given** a pending customer account, **when** an administrator rejects verification with a reason, **then** the account remains unverified and the reason is stored.
- **Given** a non-admin user, **when** they attempt to change verification status, **then** the request is rejected with `403 Forbidden`.
- **Given** a verification status change succeeds, **when** it is committed, **then** an audit record identifies the administrator, time, action, and reason.

#### US-3 — Maintain a customer wallet (Must)
**As** a customer, **I want** to have a wallet with an available balance, **so that** I can fund it and pay bills.
- **Given** a newly activated customer, **when** the wallet is created, **then** exactly one wallet is associated with that customer and its available and held balances start at `0.00 EGP`.
- **Given** a customer requests their wallet balance, **when** the request is authorized, **then** the system returns available and held balances separately.
- **Given** a customer requests another customer's wallet details, **when** the request is processed, **then** access is denied unless the caller has an authorized support/admin role.
- **Given** a wallet has ledger activity, **when** its balance is calculated, **then** the balance is consistent with the wallet's ledger entries.

#### US-4 — Top up a wallet (Must)
**As** a customer, **I want** to add money to my wallet, **so that** I can pay bills using PayLink.
- **Given** a customer submits a top-up amount greater than `0.00 EGP` through an enabled funding method, **when** the funding provider confirms the transaction, **then** the wallet is credited by a ledger entry for the confirmed amount.
- **Given** a top-up amount of `0.00 EGP` or less, **when** the request is submitted, **then** it is rejected and the wallet is unchanged.
- **Given** a funding provider declines or times out, **when** the top-up result is handled, **then** the system does not credit unconfirmed funds and records the outcome.
- **Given** an agent performs a cash top-up for a customer, **when** the operation succeeds, **then** the agent wallet is debited and the customer wallet is credited atomically using two linked ledger entries.

#### US-5 — Record wallet movements in a ledger (Must)
**As** a finance controller, **I want** every wallet movement represented by ledger entries, **so that** balances can be reconstructed and financial activity can be audited.
- **Given** a wallet is credited or debited, **when** the transaction commits, **then** corresponding ledger entries record the amount, direction, reference, timestamp, and reason.
- **Given** a ledger entry has been committed, **when** an application component attempts to edit or delete it, **then** the operation is rejected.
- **Given** concurrent debit requests exceed the available balance, **when** they are processed, **then** the system accepts only requests that can be funded and the available balance never becomes negative.
- **Given** a ledger transaction fails before commit, **when** the operation is rolled back, **then** none of its linked ledger entries are partially applied.

#### US-6 — Browse billers and services (Must)
**As** a customer, **I want** to browse available billers and their services, **so that** I can select the bill I need to pay.
- **Given** enabled billers and services exist, **when** a customer requests the catalog, **then** the system returns the enabled billers and their available service types.
- **Given** a biller or service is disabled, **when** a customer requests the catalog, **then** the disabled item is not offered for a new payment.
- **Given** a biller has multiple services, **when** the customer opens that biller, **then** each service is displayed with its required inquiry/payment input information.
- **Given** an administrator changes a biller/service availability, **when** the change is saved, **then** subsequent catalog requests reflect the new status.

#### US-7 — Manage biller and service details (Should)
**As** an administrator, **I want** to maintain biller and service metadata, **so that** customers see accurate payment options.
- **Given** an administrator adds a biller with a unique identifier and required connection configuration, **when** the record is saved, **then** the biller becomes available according to its enabled status.
- **Given** a duplicate biller identifier is submitted, **when** the administrator saves it, **then** the system rejects the duplicate.
- **Given** a biller or service is edited, **when** the update is valid, **then** the new metadata is used for future catalog and inquiry requests.
- **Given** a biller is disabled, **when** a new payment is initiated, **then** the system rejects it before funds are held.

#### US-8 — Inquire about a bill and show the fee (Must)
**As** a customer, **I want** to inquire about a bill and see the bill amount, service fee, and total, **so that** I can decide whether to pay.
- **Given** a customer provides the required bill identifier for a supported live-inquiry service, **when** the inquiry succeeds, **then** the system displays the biller, service, bill amount, service fee, and total charge.
- **Given** the inquiry identifier is invalid or the biller reports no bill, **when** the inquiry is processed, **then** the system returns a clear error and no payment or hold is created.
- **Given** a service uses the NetCo batch/no-live-inquiry flow, **when** the customer enters an amount, **then** the amount is validated against the service minimum and maximum.
- **Given** a fee is calculated during inquiry, **when** the customer later confirms the payment, **then** the fee value from that inquiry is retained for the payment.

#### US-9 — Confirm and pay a bill (Must)
**As** a customer, **I want** to confirm a bill payment after reviewing its details, **so that** the bill is paid from my wallet.
- **Given** a valid inquiry and sufficient available wallet funds for the total charge, **when** the customer confirms the payment, **then** PayLink creates a payment reference and begins the payment lifecycle.
- **Given** the customer has insufficient available funds, **when** the payment is confirmed, **then** the payment is rejected with an `insufficient funds` reason and no biller payment is sent.
- **Given** the customer cancels before confirmation, **when** the cancellation is received, **then** no payment is submitted and no funds are held.
- **Given** a payment is confirmed, **when** the result is available, **then** the customer can retrieve the payment reference and final/current status.

### Part 2 — Payment processing and risk controls (US-10 to US-19)
| Story | Requirement | Title | Priority | Module |
|---|---|---|---|---|
| US-10 | FR-10 | Idempotent payment requests | Must | Payment Processing |
| US-11 | FR-11 | Enforce the payment life cycle | Must | Payment Processing |
| US-12 | FR-12 | Hold funds before calling the biller | Must | Accounts & Wallet / Payment Processing |
| US-13 | FR-13 | Handle biller timeout and retries | Must | Biller Integration |
| US-14 | FR-14 | Accept asynchronous callbacks and ignore duplicates | Must | Biller Integration |
| US-15 | FR-15 | Support billers with different formats | Must | Biller Integration |
| US-16 | FR-16 | Calculate service fees | Must | Fees & Commissions |
| US-17 | FR-17 | Agent pays on behalf of a customer | Should | Payment Processing / Fees & Commissions |
| US-18 | FR-18 | Reject payments above single or daily limits | Must | Fraud Checks |
| US-19 | FR-19 | Block an account after too many payments | Should | Fraud Checks |

### US-10 - Idempotent payment requests (FR-10, Must)

**As** a customer on a slow network, **I want** a repeated payment request to return the first result, **so that** I am never charged twice.

**Acceptance criteria**

1. **Given** a payment request with idempotency key K that was processed and ended Completed, **when** the same customer sends the same request with key K again, **then** the system returns the original result (same payment reference and state), creates no new payment, no new hold, no new ledger entry and makes no new biller call.
2. **Given** a payment request with key K that is still being processed, **when** the same request arrives again at the same moment, **then** only one payment is created and the second request returns the same payment reference with its current state.
3. **Given** a key K already used for a payment of 350.00 EGP, **when** a request with key K arrives with different content (another amount or another bill), **then** it is rejected with the reason "idempotency key reused with different request" and nothing is changed.
4. **Given** a payment request without an idempotency key, **when** it is submitted, **then** it is rejected with a validation error naming the missing key and no payment is created.
5. **Given** two different customers who send the same key value, **when** both submit, **then** each gets their own payment (keys are scoped per customer).

_Note:_ Covers hard case 1. Key retention time and scope are decided in the ambiguities list (A-8).

### US-11 - Enforce the payment life cycle (FR-11, Must)

**As** the business, **I want** every payment to be in exactly one state and to follow only the allowed transitions, **so that** a payment can never reach an impossible or unsafe state.

**Acceptance criteria**

1. **Given** a new payment, **when** it is created, **then** its state is Initiated and the creation is recorded in the payment history with time and reason.
2. **Given** each allowed transition in section 2.5 of the brief (Initiated to FundsHeld or Rejected; FundsHeld to SentToBiller; SentToBiller to Completed, Failed or Unknown; Unknown to Completed or Failed; Failed to Refunded), **when** its event happens, **then** the state changes to the target state and the history records the old state, the new state, the event and the time.
3. **Given** any pair of states that is not in the allowed table (for example Initiated to Completed, or Completed to Failed), **when** the system tries to apply it, **then** the change is refused, the state stays the same and the attempt is logged.
4. **Given** a payment in a final state (Completed, Rejected or Refunded), **when** any event arrives (late callback, retry result, settlement file line), **then** the state does not change.
5. **Given** a payment in Unknown, **when** the system evaluates it, **then** it is never moved to Refunded directly and is never refunded automatically; it must first become Failed.

_Note:_ Source for [`design/state-payment.puml`](design/state-payment.puml). Test idea: a table-driven test that tries all 8 x 8 state pairs and expects only the 9 allowed ones to pass.

### US-12 - Hold funds before calling the biller (FR-12, Must)

**As** a customer, **I want** my money to be held before the biller is called and released if the payment fails, **so that** I am not charged for a payment that did not happen and cannot overspend.

**Acceptance criteria**

1. **Given** Sara has 1,000.00 EGP available and a payment total of 352.50 EGP, **when** the fraud checks pass, **then** two ledger entries move 352.50 EGP from Available to Held (available 647.50, held 352.50), the payment becomes FundsHeld, and only then is the biller called.
2. **Given** a payment in state Failed with 352.50 EGP held, **when** the failure is confirmed, **then** the hold is released to the wallet by a new ledger entry (available back to 1,000.00, held 0.00) and the payment becomes Refunded.
3. **Given** a payment in state Unknown, **when** time passes, **then** the hold stays in place and is not released until the payment is Completed or Failed.
4. **Given** a wallet with 400.00 EGP available and two payments of 352.50 EGP arriving at the same moment, **when** both are processed, **then** exactly one becomes FundsHeld and the other is Rejected with the reason "insufficient funds"; the available balance never goes below 0.00.
5. **Given** a payment that completes, **when** the biller confirms, **then** the hold becomes a final charge: Held decreases by 352.50, bill amount 350.00 is recorded as paid to the biller, and fee 2.50 as PayLink fee income.

_Note:_ Covers hard case 4. Depends on US-5 (ledger). Concurrency control technique (row lock or optimistic version) is a design decision in the ADR, not a requirement.

### US-13 - Handle biller timeout and retries (FR-13, Must)

**As** a customer, **I want** a payment that does not get an answer to be handled safely and retried, **so that** I am neither charged without payment nor refunded wrongly.

**Acceptance criteria**

1. **Given** ElectroCo takes 12 seconds to answer while the timeout is 10 seconds, **when** the payment is sent, **then** after 10 seconds the payment becomes Unknown, the money stays held and the customer is told "your payment is being processed".
2. **Given** a payment in Unknown, **when** 1, 5 and 15 minutes have passed since it became Unknown, **then** the system re-queries the biller at each of these times, at most 3 times in total.
3. **Given** a re-query in which the biller says the payment was received, **when** the answer arrives, **then** the payment becomes Completed (charge, fee and notification as in US-12 criterion 5).
4. **Given** a re-query in which the biller says it refused, **when** the answer arrives, **then** the payment becomes Failed, then Refunded when the hold is released.
5. **Given** three re-queries that all got no answer, **when** the last one ends, **then** the payment stays Unknown with the money held and waits for reconciliation (FR-26); no automatic refund happens.
6. **Given** a retry or re-query, **when** it is sent, **then** it uses the original payment reference so the biller cannot receive the same payment twice.

_Note:_ Covers hard case 2. Timeout and retry delays come from configuration. Not applied to NetCo (batch).

### US-14 - Accept asynchronous callbacks and ignore duplicates (FR-14, Must)

**As** the system, **I want** to accept the final result that TopUpNet sends later by callback and to ignore repeated callbacks, **so that** a payment completes exactly once.

**Acceptance criteria**

1. **Given** a TopUpNet payment in state SentToBiller (the biller answered "accepted"), **when** TopUpNet calls the callback URL with "success" and the payment reference, **then** the payment becomes Completed.
2. **Given** a TopUpNet payment in state SentToBiller, **when** the callback says "failed", **then** the payment becomes Failed and then Refunded as in US-12 criterion 2, and the customer gets an SMS with the reason.
3. **Given** a payment that is already Completed, **when** TopUpNet calls the callback with "success" a second time, **then** the payment is not changed, no second charge, fee, commission or notification is created, and the duplicate is written to the log.
4. **Given** a payment in Unknown, **when** a valid callback "success" arrives, **then** the payment becomes Completed.
5. **Given** a callback for a payment reference that does not exist or has an invalid signature or secret, **when** it arrives, **then** it is rejected, nothing changes and the attempt is logged.
6. **Given** a callback whose result conflicts with a final state (for example "success" for a payment that is Refunded), **when** it arrives, **then** the payment is not changed and the conflict is flagged for support in the reconciliation report.

_Note:_ Covers hard case 6. Callback authentication method is decided in A-10.

### US-15 - Support billers with different formats (FR-15, Must)

**As** PayLink management, **I want** at least ElectroCo, AquaCo and TopUpNet supported through one adapter each, **so that** the rest of the system does not depend on any biller's protocol and billers can fail independently.

**Acceptance criteria**

1. **Given** ElectroCo (REST/JSON), AquaCo (SOAP-style XML) and TopUpNet (REST/JSON, asynchronous), **when** a payment is made to each, **then** the Payment Processing module uses the same internal request and result model for all three and never sees the biller's field names or error codes.
2. **Given** AquaCo refuses a payment with a biller-specific error code, **when** the adapter receives it, **then** the code is translated to a standard reason, the payment becomes Failed, the hold is released (Refunded) and the customer gets an SMS with a clear reason.
3. **Given** AquaCo rejects any payment above the bill amount, **when** a customer pays more than the inquiry amount, **then** the payment is stopped before the biller call with the reason "amount above bill" or, if it reaches the biller, handled as in criterion 2.
4. **Given** ElectroCo is down, **when** customers pay AquaCo and TopUpNet bills, **then** those payments are processed normally; only ElectroCo payments end Unknown or Failed.
5. **Given** a new biller, **when** it is added, **then** only a new adapter and its configuration are added and no existing module changes. NetCo (daily batch file) is optional.

_Note:_ Covers hard cases 3 and 8. Related: FR-6 (catalog), resilience target in section 2.

### US-16 - Calculate service fees (FR-16, Must)

**As** PayLink management, **I want** the service fee to follow the business rules, **so that** the company earns the right fee and the customer sees the right total.

**Acceptance criteria**

1. **Given** an electricity or water bill of any valid amount, **when** the fee is calculated, **then** it is the fixed value 2.50 EGP.
2. **Given** a mobile top-up, **when** the fee is calculated, **then** it is 1.5% of the amount with a minimum of 1.00 EGP: 100.00 gives 1.50; 20.00 gives 1.00 (minimum applies); 123.45 gives 1.85 (rounded to 2 decimals, see A-6).
3. **Given** an internet bill, **when** the fee is calculated, **then** it is 2.00 EGP for an amount up to and including 200.00 EGP and 4.00 EGP for an amount above 200.00 EGP.
4. **Given** a promotion configured for one biller with a start and an end date, **when** a payment is made to that biller inside the period (both dates included), **then** the fee is 0.00 EGP; outside the period or for another biller the normal fee applies.
5. **Given** any fee calculation, **when** it is done, **then** all values come from configuration (no fee value in code) and all arithmetic uses exact decimals.
6. **Given** a payment where the fee was calculated at inquiry time, **when** the payment is confirmed, **then** the same fee is used even if the configuration changed in between.

_Note:_ Related: FR-24 (edit fees without redeploying), US-8 (shows the fee), US-17 (commission is 40% of this fee).

### US-17 - Agent pays on behalf of a customer (FR-17, Should)

**As** an agent at a PayLink terminal, **I want** to pay a bill for a customer and earn commission, **so that** customers without the app can pay and I am rewarded.

**Acceptance criteria**

1. **Given** an agent wallet with at least 352.50 EGP and a customer who gives the agent 352.50 EGP in cash, **when** the agent pays the ElectroCo bill of 350.00 EGP (fee 2.50) and ElectroCo confirms, **then** the payment is Completed, it is marked with the agent as the channel, and the receipt is issued to the customer.
2. **Given** a completed agent payment with fee 2.50 EGP, **when** the payment completes, **then** a commission of 1.00 EGP (40% of the fee) is credited to the agent wallet by a ledger entry and PayLink fee income is reduced accordingly in the report (net 1.50 EGP).
3. **Given** an agent payment that ends Failed, Rejected or Unknown, **when** the state changes, **then** no commission is credited; for Unknown it is credited only if the payment later becomes Completed.
4. **Given** an agent wallet with less than the total, **when** the agent pays, **then** the payment is Rejected with the reason "insufficient funds".
5. **Given** an agent payment with a promotion fee of 0.00 EGP, **when** it completes, **then** the commission is 0.00 EGP and no commission entry is created.
6. **Given** a user who is not an agent, **when** they try to pay on behalf of a customer, **then** the request is rejected as forbidden.

_Note:_ Whose wallet pays is decided in A-9. The commission percentage comes from configuration.

### US-18 - Reject payments above single or daily limits (FR-18, Must)

**As** the business and the regulator, **I want** payments above the single-payment limit or the daily limit to be rejected with a clear reason, **so that** exposure to fraud and losses is limited.

**Acceptance criteria**

1. **Given** a total charge of 10,000.01 EGP or 4.99 EGP, **when** the customer confirms the payment, **then** it is Rejected with the reason "total amount outside allowed range (5.00 - 10,000.00 EGP)" and nothing is held.
2. **Given** a BASIC account with 4,800.00 EGP already counted today and a new payment of 300.00 EGP, **when** it is confirmed, **then** it is Rejected with the reason "daily limit exceeded (5,000.00 EGP)" and nothing is held.
3. **Given** a VERIFIED account with 29,000.00 EGP counted today, **when** it pays 1,000.00 EGP, **then** the payment is accepted because the total is exactly 30,000.00 EGP; a payment of 1,000.01 EGP is Rejected.
4. **Given** an earlier payment that ended Failed, Rejected or Refunded, **when** the daily total is computed, **then** that payment is not counted; Completed payments and payments in FundsHeld, SentToBiller and Unknown are counted.
5. **Given** the daily limit values in configuration, **when** an admin changes them (FR-24), **then** the new values are used for the next payment without redeploying.
6. **Given** a payment at 00:00 Cairo time of the next day, **when** the daily total is computed, **then** the new day starts with 0.00 EGP.

_Note:_ Part of the fraud chain. Interpretation of the range (with or without fee) follows Q6 / A-5.

### US-19 - Block an account after too many payments (FR-19, Should)

**As** the business, **I want** an account that makes more than 5 payments in 60 seconds to be blocked for 10 minutes, **so that** automated attacks and runaway clients are stopped.

**Acceptance criteria**

1. **Given** an account that has made 5 payments in the last 60 seconds, **when** it submits a 6th payment within the same 60 seconds, **then** the 6th is Rejected with the reason "too many payments, account blocked for 10 minutes" and the account is blocked.
2. **Given** an account that is blocked by this rule, **when** it submits any payment during the next 10 minutes, **then** the payment is Rejected with the reason "account blocked" and nothing is held.
3. **Given** a block that started 10 minutes ago, **when** the account submits a payment after the block time ended, **then** the block is removed automatically and the payment is processed normally.
4. **Given** exactly 5 payments in 60 seconds, **when** the account submits a payment 61 seconds after the first one, **then** it is not blocked (sliding 60-second window).
5. **Given** a repeated request with an already used idempotency key (US-10), **when** it arrives, **then** it does not count as a new payment for this rule.
6. **Given** an account blocked by this rule, **when** a support employee unblocks it (FR-21), **then** the block ends immediately and the action is written to the audit log.

_Note:_ Window length, count and block time come from configuration. Payments already in progress when the block starts are not cancelled.

## 2. Non-Functional Requirements (6, measurable)

Each requirement has a number and a way to measure it, so a test or a CI report can show it. Targets follow the brief (section 3.3).

| ID | Quality | Requirement (with number) | How it is measured | Related stories |
|---|---|---|---|---|
| NFR-1 | Correctness (money) | Zero double charges and zero negative balances. In a test with 100 parallel payments on one wallet that can pay only 1 of them, and in a test that sends the same idempotency key 50 times in parallel, exactly 1 charge is made and the final balance is >= 0.00 EGP. All money uses exact decimal types. | Automated concurrency and duplicate tests (hard cases 1 and 4) in CI; ledger sum check after each test | US-5, US-10, US-12 |
| NFR-2 | Performance | The system sustains 100 payments per second for 60 seconds (6,000 payments) against the mock billers, with an error rate below 1% and a 95th percentile response time of 500 ms or less for the PayLink part of a payment (biller time excluded). | Load-test script (for example k6 or Locust) run against docker compose; result stored in the report | US-9, US-15 |
| NFR-3 | Resilience | If one biller is down or slow, payments to the other billers continue: with ElectroCo stopped for 5 minutes, at least 99% of AquaCo and TopUpNet payments in the same period still reach a final state or SentToBiller, and a payment to the failed biller returns an answer within 10 seconds (timeout) instead of hanging. | Chaos test with a mock biller set to "fail on purpose" or "delay 12 s" (hard case 2) | US-13, US-15 |
| NFR-4 | Modifiability | Adding a new biller, or the ElectroCo API v2 change, touches only the Biller Integration module and configuration: 0 files changed in the other modules (checked with the list of changed paths of the commit). A new biller takes no more than 1 new adapter class, 1 configuration entry and its tests. | `git diff --name-only` review and the hard-case 8 test; reported in the Phase 2 change-request section | US-15, US-16 |
| NFR-5 | Auditability | 100% of money movements and admin actions have an audit record with who, when and why. Ledger and audit entries cannot be updated or deleted by the application (0 successful update or delete attempts in tests). | Test that counts ledger entries versus audit records per scenario and must be equal; coverage report of audited operations | US-2, US-5, US-6 |
| NFR-6 | Testability | At least 70% line coverage on domain logic, measured by the CI pipeline on every push; every one of the 8 hard cases has at least 1 automated test. | Coverage report in GitHub Actions; the build fails if coverage is below 70% | All stories |

_Optional extra (not counted in the 6):_ Notification delivery - a failed SMS or email is retried 3 times and then marked undelivered, and a notification failure never changes the payment result (hard case 5, FR-23).

## 3. Ambiguities, Questions and Decisions

The brief and the first AI drafts left several points open. Each one is listed with the question, the options, the decision the team made for Phase 1 and the story it affects. "Team decision" means the requirements leads decided it; items marked **Confirm** should be confirmed with the TA before Phase 2 coding starts.

### 3.1 Questions passed from Student 1 (Q1 to Q6)

| # | Question | Decision | Affects |
|---|---|---|---|
| Q1 / A-1 | How does a user log in (password, OTP)? | Out of scope for the payment rules. Phase 1 design assumes login by phone number and password with a token; OTP is a later improvement. Every protected endpoint needs a logged-in user with a role (Customer, Agent, Admin, Support). | US-1, all |
| Q2 / A-2 | Does an agent cash top-up debit the agent's wallet? | Yes. The agent wallet is debited and the customer wallet credited in one atomic operation (two ledger entries, one reference). | US-4, US-17 |
| Q3 / A-3 | Maximum top-up amount? | No maximum in the brief. Only an amount greater than 0 is accepted; a configurable maximum can be added later. | US-4 |
| Q4 / A-4 | Who verifies a customer (FR-2)? | An admin, after an identity check done outside the system. | US-2 |
| Q5 / A-11 | Where does the amount come from for NetCo (no live inquiry)? | The customer enters it, checked against the service minimum and maximum. | US-8, US-15 |
| Q6 / A-5 | Does the 5 - 10,000 EGP range include the service fee? | **Decision:** the range applies to the total charge (bill amount plus fee), as written in US-9 and US-18. The daily limit also counts the total charge. **Confirm** with the TA, because the brief says "single payment". | US-9, US-18 |

### 3.2 New ambiguities found in this part

| # | Question / ambiguity | Options considered | Decision | Affects |
|---|---|---|---|---|
| A-6 | Rounding rule for a percentage fee (1.5% of 123.45 = 1.85175) | Round half up; round half even (banker's); truncate | Round half up to 2 decimals, using exact decimals only. The rule is configurable in one place. | US-16 |
| A-7 | Refund of a **Completed** payment (FR-27, Could) conflicts with section 2.5: Completed is final and only Failed leads to Refunded | (a) allow Completed to Refunded; (b) keep Completed final and create a separate Refund record with its own compensating ledger entries | (b). The payment stays Completed; a Refund record (Requested, Approved, Done) moves the money back. The state diagram therefore keeps the brief's 9 transitions. FR-27 is Could and is designed in Phase 1 (sequence diagram) only. **Confirm** with the TA. | US-11, FR-27 |
| A-8 | How long and for whom does an idempotency key count? | Forever; 24 hours; per payment only | Scoped per customer and kept for 24 hours (configurable). Same key plus different request content is rejected. | US-10 |
| A-9 | Who pays when an agent pays on behalf of a customer? | Agent wallet; customer wallet (needs the customer's consent) | Agent wallet (customer gives cash). Limits and fraud rules apply to the paying account, which is the agent. **Confirm** the agent's daily limit with the TA. | US-17, US-18 |
| A-10 | How do we trust a TopUpNet callback? | No check; shared secret header; signed body | Shared secret in a header, kept in configuration (not in code). Invalid secret means rejected and logged. | US-14 |
| A-12 | TopUpNet answers "accepted" quickly, then calls back minutes later. The brief gives a 10 s timeout only for live billers and no wait time for callbacks | Wait forever; use the retry rule; add a configurable callback deadline | The payment stays SentToBiller after "accepted". If the 10 s timeout is exceeded before "accepted", it becomes Unknown. If no callback arrives within a configurable deadline (proposed 30 minutes) it becomes Unknown and follows the retry and reconciliation rules. **Confirm** the 30 minutes. | US-13, US-14 |
| A-13 | What happens to the third retry when Unknown is still unresolved (brief: "waits for reconciliation")? | Auto-refund after reconciliation; keep Unknown until the settlement file or support decides | Keep Unknown with money held. Only a callback, a retry answer or the settlement file moves it (to Completed or Failed). If the settlement file has no such payment, it becomes Failed and then Refunded. | US-11, US-13 |
| A-14 | Which payments count towards the daily limit | All attempts; only money actually spent or held | Completed, FundsHeld, SentToBiller and Unknown are counted; Failed, Rejected and Refunded are not. The day is a calendar day in Cairo time (Africa/Cairo). | US-18 |
| A-15 | Does the velocity rule count rejected attempts and which payment is blocked? | Count only accepted; count all submissions | Count all new payment submissions (not idempotent repeats). The 6th submission in a 60-second sliding window is rejected and starts the 10-minute block. | US-19 |
| A-16 | AquaCo "rejects payments above the bill amount": who prevents this? | Only the biller; check before sending | PayLink checks the amount against the inquiry result before sending, and also maps AquaCo's refusal code if it still happens. | US-15 |
| A-17 | Who writes FR-18 and FR-19: the brief split names Student 2 for FR-10 to FR-19, while the note in `req-p1.md` mentions Student 3 for FR-18 and FR-19 | Student 2 writes them; Student 3 reviews | Student 2 wrote US-18 and US-19 in this file (as in the assignment table). Student 3 should review the fraud-chain rules, not duplicate them. | US-18, US-19 |

### 3.3 Questions the AI asked while drafting

These are the clarifying questions the AI assistant raised during the drafting sessions. Each is answered by one of the decisions above.

| AI question | Answered by |
|---|---|
| Is the fee part of the amount checked against the limits? | A-5 |
| How should the system treat a callback that arrives after the payment is already final? | US-14 (criteria 3 and 6) |
| Should retried biller calls reuse the payment reference? | US-13 (criterion 6) |
| Which time zone defines "a day" for the daily limit? | A-14 |
| Is a Refund of a Completed payment a new state or a separate record? | A-7 |

## 4. Traceability (FR to story to design)

| FR | Story | Priority | Use case in diagram | Other design artifact |
|---|---|---|---|---|
| FR-10 | US-10 | Must | Pay a bill (FR-9..FR-12) | Sequence diagram "pay a bill" |
| FR-11 | US-11 | Must | Pay a bill (FR-9..FR-12) | [`state-payment.puml`](design/state-payment.puml) |
| FR-12 | US-12 | Must | Hold funds | State and sequence diagrams; ER (ledger, holds) |
| FR-13 | US-13 | Must | Handle timeout, retry and callback | State diagram (Unknown) |
| FR-14 | US-14 | Must | Handle timeout, retry and callback | State diagram; sequence diagram |
| FR-15 | US-15 | Must | Send payment to biller | Class diagram (adapters) |
| FR-16 | US-16 | Must | Calculate fee | Class diagram (fee strategies) |
| FR-17 | US-17 | Should | Pay on behalf of customer | Class diagram (commission) |
| FR-18 | US-18 | Must | Run fraud checks | Class diagram (fraud chain) |
| FR-19 | US-19 | Should | Run fraud checks | Class diagram (fraud chain) |

## 5. Payment State Diagram

Source: [`/docs/design/state-payment.puml`](design/state-payment.puml). The PNG is a preview of the same diagram. It contains the 9 transitions of section 2.5 of the brief, the three final states (Completed, Rejected, Refunded), and the retry loop on Unknown (up to 3 re-queries). Failed is not final because the hold still has to be released to reach Refunded.

![Payment state diagram](design/state-payment.png)

| From | Event | To |
|---|---|---|
| Initiated | Fraud checks pass and wallet has enough funds | FundsHeld |
| Initiated | Fraud check fails or funds insufficient | Rejected |
| FundsHeld | Request sent to biller | SentToBiller |
| SentToBiller | Biller confirms | Completed |
| SentToBiller | Biller refuses | Failed |
| SentToBiller | No answer within timeout | Unknown |
| Unknown | Biller later confirms (callback, retry or settlement file) | Completed |
| Unknown | Biller later refuses, or reconciliation finds no payment | Failed |
| Failed | Hold released to the wallet | Refunded |

_Check:_ the brief's table has 9 transition rows; the diagram has the same 9 plus the self-loop on Unknown for the re-query (an internal action that does not change the state).

### Part 3 — Support, notifications, administration and reconciliation (US-20 to US-28)

### User Stories (US-20 to US-28)

| Story | Requirement | Title | Priority | Module |
|---|---|---|---|---|
| US-20 | FR-20 | Search payment by reference and view full history | Must | Payment Processing |
| US-21 | FR-21 | Block and unblock a customer or agent account | Should | Accounts & Wallet / Fraud Checks |
| US-22 | FR-22 | Send SMS and push notifications on payment completion and failure | Must | Notifications |
| US-23 | FR-23 | Retry failed notifications up to 3 times | Should | Notifications |
| US-24 | FR-24 | Edit fee and limit configuration without redeploying | Should | Biller Catalog / Fees & Commissions |
| US-25 | FR-25 | Record every money movement and admin action in an immutable audit log | Must | Accounts & Wallet / Audit |
| US-26 | FR-26 | Generate daily reconciliation report from settlement files | Should | Reconciliation |
| US-27 | FR-27 | Request and approve refund for a completed payment | Could | Payment Processing / Accounts & Wallet |
| US-28 | FR-28 | View daily financial and failure totals per biller | Could | Reconciliation / Reporting |

### US-20 - Search payment by reference and view full history (FR-20, Must)

**As** a support employee, **I want** to search for a payment by its unique reference and view its full life-cycle history, **so that** I can investigate customer inquiries and resolve disputes accurately.

**Acceptance criteria**

1. **Given** an existing payment with reference `PAY-2026-00123`, **when** a support employee searches by `PAY-2026-00123`, **then** the system returns the payment details (customer/agent ID, biller, service, bill amount, service fee, agent commission, current state) and the chronological list of all state transitions (old state, new state, triggering event, timestamp, and reason).
2. **Given** a payment that has associated ledger entries and notification attempts, **when** a support employee views that payment by reference, **then** the response also displays the linked ledger entry IDs and notification delivery statuses (`delivered`, `retrying`, or `undelivered`).
3. **Given** a payment reference that does not exist in the system, **when** a support employee searches for it, **then** the system returns a `404 Not Found` error with a clear message.
4. **Given** a user whose role is `Customer` or `Agent`, **when** they attempt to access the support payment-search endpoint for another user's payment, **then** the request is rejected with `403 Forbidden`.

_Note:_ Supports customer service investigations and Hard Case 7 reviews.

### US-21 - Block and unblock an account (FR-21, Should)

**As** a support employee, **I want** to manually block and unblock a customer or agent account, **so that** suspicious accounts can be frozen immediately and legitimate users restored after review.

**Acceptance criteria**

1. **Given** an active account, **when** a support employee blocks the account with a mandatory reason, **then** the account status becomes `Blocked`, any subsequent payment or top-up attempt from that account is rejected with the reason `"account blocked"`, and an audit log entry is recorded (US-25).
2. **Given** an account that was blocked either manually by support or automatically by the velocity rule (US-19), **when** a support employee unblocks the account with a reason, **then** the account status immediately returns to `Active`, new payments are allowed again, and the unblock action is written to the audit log.
3. **Given** a support employee attempts to block or unblock an account without providing a reason, **when** the request is submitted, **then** it is rejected with a validation error and the account state does not change.
4. **Given** an account that is currently `Blocked` while an earlier payment is already in `SentToBiller` or `Unknown`, **when** the biller later confirms or refuses that in-flight payment, **then** the in-flight payment still completes its life cycle (either `Completed` or `Failed` -> `Refunded`) without losing funds.

_Note:_ Complements US-19 (automated 10-minute velocity block).

### US-22 - Send SMS and push notifications on completion and failure (FR-22, Must)

**As** a customer, **I want** to receive an SMS and a push notification when my payment completes or fails, **so that** I have immediate confirmation of my bill status and wallet balance.

**Acceptance criteria**

1. **Given** a payment of 350.00 EGP (fee 2.50 EGP, total 352.50 EGP) transitions to `Completed`, **when** the completion event is processed, **then** the system queues and sends both an SMS and a push notification to the customer containing the payment reference, biller name, amount paid, fee, and new available balance.
2. **Given** AquaCo refuses a payment with an error code and the payment transitions to `Failed` and then `Refunded`, **when** the failure is processed, **then** the customer receives both an SMS and a push notification stating that the payment failed, the clear translated reason, and that the held amount (352.50 EGP) has been released back to the wallet.
3. **Given** a payment transitions to `Unknown` after a 10-second timeout, **when** the timeout occurs, **then** the customer is notified that the payment is still being processed and the funds remain held (no false completion or failure message is sent).
4. **Given** the external SMS provider is down at the exact moment a payment completes, **when** the notification dispatch fails, **then** the payment remains `Completed` (never rolled back or delayed) and the notification enters the retry workflow (US-23).

_Note:_ Covers Hard Cases 3 and 5.

### US-23 - Retry failed notifications up to 3 times (FR-23, Should)

**As** PayLink operations, **I want** failed SMS or email notifications to be retried up to 3 times before being marked undelivered, **so that** temporary gateway glitches do not cause missed customer alerts.

**Acceptance criteria**

1. **Given** an SMS or email notification fails on its initial send attempt, **when** the retry worker processes it, **then** the system retries sending up to 3 additional times, incrementing `retry_count` on each attempt.
2. **Given** a failed notification succeeds on the 2nd retry attempt, **when** the gateway confirms delivery, **then** the notification status becomes `delivered`, `delivered_at` is recorded, and no further retries occur.
3. **Given** a notification fails on the initial attempt and all 3 retry attempts, **when** the 3rd retry fails, **then** its final status is set to `undelivered` with the last gateway error reason, and no 4th retry is attempted.
4. **Given** a notification that is already marked `delivered`, **when** any duplicate event or worker run occurs, **then** the notification is not sent again.

_Note:_ Covers Hard Case 5. Maximum retry count (3) is stored in configuration.

### US-24 - Edit fee and limit values without redeploying (FR-24, Should)

**As** an admin, **I want** to update service fees, promotion periods, and transaction limits dynamically through configuration, **so that** business rule changes take effect immediately without downtime or code deployment.

**Acceptance criteria**

1. **Given** an admin updates the daily limit for `Basic` accounts from `5,000.00` EGP to `7,500.00` EGP or updates a biller's fixed fee, **when** the configuration update is saved, **then** the very next bill inquiry or payment uses the updated value without restarting or redeploying the application.
2. **Given** an admin configures a promotion period (`start_date` and `end_date`) for a single chosen biller, **when** payments occur within that date range (inclusive), **then** the fee evaluates to `0.00` EGP; if another biller already had an active promotion, only one biller promotion is active per rule configuration.
3. **Given** an admin updates a fee rule while a customer has already run a bill inquiry (US-8) and is confirming payment, **when** the payment is processed, **then** the fee locked at inquiry time is honored (consistent with US-16 criterion 6).
4. **Given** an admin submits an invalid configuration value (such as a negative fee, `min_amount > max_amount`, or `start_date > end_date`), **when** saved, **then** the system rejects the change with a validation error and keeps the previous valid configuration.
5. **Given** any valid configuration change by an admin, **when** committed, **then** an audit log entry is recorded with the admin ID, timestamp, parameter key, old value, new value, and reason (US-25).

### US-25 - Record every money movement and admin action in an immutable audit log (FR-25, Must)

**As** a compliance officer and auditor, **I want** every money movement and administrative action recorded in an immutable audit log, **so that** the system maintains 100% financial traceability and accountability.

**Acceptance criteria**

1. **Given** any money movement occurs (wallet top-up, fund hold, hold capture/final charge, fee income credit, agent commission credit, hold release/refund, or approved completed-payment refund), **when** the ledger entry is created, **then** an audit record is created in the same transaction containing `actor_id`, `actor_role`, `timestamp`, `action_type`, `entity_id`, `amount`, and `reason`.
2. **Given** any administrative or support action occurs (upgrading customer verification, adding/editing/disabling a biller, editing fees or limits, blocking/unblocking an account, or approving a refund), **when** the action succeeds, **then** an audit record is written with who performed it, when, what changed, and why.
3. **Given** existing rows in `audit_logs` or `ledger_entries`, **when** any application service attempts an `UPDATE` or `DELETE` operation on them, **then** the operation is rejected (enforced at both domain and database levels).

_Note:_ Directly satisfies NFR-5 (Auditability: 100% coverage).

### US-26 - Produce a daily reconciliation report from a settlement file (FR-26, Should)

**As** a finance and operations specialist, **I want** the system to compare PayLink's daily payment records against each biller's nightly settlement file and generate a discrepancy report, **so that** stuck payments are resolved and financial mismatches are caught.

**Acceptance criteria**

1. **Given** a payment is in `Unknown` state in PayLink and the nightly settlement file from ElectroCo lists that payment reference as paid with matching amount, **when** reconciliation runs, **then** the payment transitions from `Unknown` to `Completed`, the held funds are captured as a final charge, fee/commission are recorded, and the customer is notified.
2. **Given** a payment is in `Unknown` state in PayLink and is absent from (or marked failed in) the biller's nightly settlement file after the settlement cutoff, **when** reconciliation runs, **then** the payment transitions from `Unknown` to `Failed` and immediately to `Refunded` (releasing the hold to the customer's available balance).
3. **Given** a payment is marked `Failed` or `Refunded` in PayLink, **when** the nightly settlement file lists that same payment reference as received/paid by the biller, **then** PayLink does NOT automatically alter the final state, and flags the record as a `CRITICAL_DISCREPANCY` in the reconciliation report for support review (Hard Case 7).
4. **Given** a settlement file contains a payment reference unknown to PayLink or an amount that differs from PayLink's recorded bill amount, **when** reconciliation runs, **then** the line is flagged in the reconciliation report with the exact variance details.
5. **Given** reconciliation finishes processing a settlement file, **when** the report is generated, **then** it summarizes total matched payments, total resolved `Unknown` payments, total discrepancies, and net settlement amount per biller.

_Note:_ Covers Hard Case 7 and the `Unknown` resolution rules in section 2.5.

### US-27 - Request and approve refund of a completed payment (FR-27, Could)

**As** a customer, **I want** to request a refund for a completed payment when a billing dispute occurs, and have a support employee review and approve it, **so that** valid disputes are refunded safely with full audit control.

**Acceptance criteria**

1. **Given** a payment in state `Completed`, **when** the owning customer submits a refund request with a reason, **then** a separate `RefundRequest` record is created with status `Requested` while the original payment remains in state `Completed` (consistent with decision A-7).
2. **Given** a `RefundRequest` in status `Requested`, **when** a support employee approves it with an approval note, **then** the refund status becomes `Approved` -> `Done`, compensating ledger entries credit the customer's available balance, and an audit log entry records the support employee's approval.
3. **Given** a `RefundRequest` in status `Requested`, **when** a support employee rejects it with a reason, **then** the refund status becomes `Rejected`, no ledger movement occurs, and the customer is notified of the rejection reason.
4. **Given** a payment that is NOT `Completed` (such as `Initiated`, `Unknown`, `Failed`, or `Rejected`), or a `Completed` payment that already has an active/approved `RefundRequest`, **when** a customer requests a refund, **then** the request is rejected with a clear validation error.

_Note:_ Designed in Phase 1 (sequence diagram [`design/seq-refund.puml`](design/seq-refund.puml)) per decision A-7.

### US-28 - View daily totals report (FR-28, Could)

**As** an admin, **I want** to view daily aggregated totals for payments, fees earned, commissions paid, and failures per biller, **so that** I can monitor daily revenue and biller reliability.

**Acceptance criteria**

1. **Given** an admin queries the daily totals report for a specific date (evaluated in `Africa/Cairo` calendar day), **when** the report is generated, **then** it displays for each biller and overall: total count and EGP volume of `Completed` payments, gross service fees earned, total agent commissions paid (40% of agent-channel fees), net PayLink fee revenue, and count of `Failed` / `Rejected` payments.
2. **Given** a day with zero transactions for a specific biller, **when** the daily totals report is requested, **then** that biller appears with `0` counts and `0.00` EGP totals rather than failing or omitting the biller.
3. **Given** a non-admin user attempts to access the daily totals endpoint, **when** requested, **then** the system returns `403 Forbidden`.

## 2. Traceability (FR-20 to FR-28)

| FR | Story | Priority | Use case in diagram | Other design artifact |
|---|---|---|---|---|
| FR-20 | US-20 | Must | Search Payment by Reference | Class diagram (`Payment`, `PaymentHistory`) |
| FR-21 | US-21 | Should | Block / Unblock Account | Class diagram (`Customer`, `AuditLog`) |
| FR-22 | US-22 | Must | Send SMS / Push Notifications | Sequence diagram "pay a bill" & "refund" |
| FR-23 | US-23 | Should | Handle Notification Retries | Class diagram (`Notification`) |
| FR-24 | US-24 | Should | Configure Fees & Limits | ER diagram (`config_settings` / `biller_services`) |
| FR-25 | US-25 | Must | Record Audit Log | ER diagram (`audit_logs`) |
| FR-26 | US-26 | Should | Process Daily Settlement & Reconciliation Report | ER diagram (`reconciliation_records`) |
| FR-27 | US-27 | Could | Request & Approve Refund | Sequence diagram "refund" ([`design/seq-refund.puml`](design/seq-refund.puml)) |
| FR-28 | US-28 | Could | View Daily Totals Report | Class diagram (`ReportingService`) |

## 4. Non-Functional Requirements
The six measurable NFRs are retained from the supplied Part 2 file:
- **NFR-1 Correctness:** zero double charges and zero negative balances; concurrency tests with 100 simultaneous payment attempts and 50 parallel repeats of one idempotency key must result in exactly one charge where appropriate.
- **NFR-2 Performance:** sustain 100 payments/second for 60 seconds (6,000 payments), error rate below 1%, and PayLink-side p95 response time at or below 500 ms excluding biller time.
- **NFR-3 Resilience:** with ElectroCo unavailable for 5 minutes, at least 99% of AquaCo and TopUpNet payments still reach a final state or `SentToBiller`; failed-biller requests return within the 10-second timeout.
- **NFR-4 Modifiability:** adding a biller/API version change affects only the Biller Integration module and configuration; no other module files change; a new biller requires at most one adapter class and one configuration entry, plus tests.
- **NFR-5 Auditability:** 100% of money movements and admin actions have who/when/why records; application update/delete attempts against ledger/audit records have zero successful outcomes.
- **NFR-6 Testability:** at least 70% line coverage for domain logic on every CI push, and at least one automated test for each of the eight hard cases.

## 5. AI Questions, Ambiguities and Decisions
The following questions were raised while drafting or reviewing the requirements. Decisions are recorded as the team's current Phase 1 interpretation; items marked **Confirm** require supervisor/TA confirmation.

| Question / ambiguity | Decision made | Status |
|---|---|---|
| Login method (Q1/A-1) | Assume phone number + password + token; OTP is a later improvement and outside current payment rules. | Assumption |
| Does agent cash top-up debit the agent wallet? (Q2/A-2) | Yes; debit agent and credit customer atomically with linked ledger entries. | Decision |
| Maximum top-up amount? (Q3/A-3) | No maximum is specified; accept amounts greater than zero. | Decision; configurable cap may be added later |
| Who verifies a customer? (Q4/A-4) | Admin verifies after an identity check performed outside PayLink. | Decision |
| Does the single-payment range include the fee? (Q6/A-5) | Apply the `5.00–10,000.00 EGP` range to bill amount plus fee; daily limit also counts total charge. | **Confirm** |
| Percentage-fee rounding? (A-6) | Round half up to two decimals using exact decimal arithmetic. | Decision |
| Refund of a Completed payment? (A-7) | Keep payment state `Completed`; create a separate RefundRequest and compensating ledger entries. | **Confirm** |
| Idempotency key lifetime/scope? (A-8) | Per customer, retained for 24 hours (configurable); same key with different content is rejected. | Decision |
| Which wallet pays for agent transactions? (A-9) | Agent wallet pays; customer provides cash; fraud limits apply to the paying agent account. | **Confirm** |
| How are TopUpNet callbacks authenticated? (A-10) | Shared secret in a header, stored in configuration and never hard-coded. | Decision |
| Amount for NetCo without live inquiry? (A-11) | Customer enters amount, validated against service minimum/maximum. | Decision |
| How long does TopUpNet wait for a callback? (A-12) | Proposed configurable 30-minute deadline; if no callback arrives, payment becomes Unknown and follows retry/reconciliation rules. | **Confirm** |
| What happens after all Unknown re-queries fail? (A-13) | Keep funds held and state Unknown until callback, retry answer, or settlement reconciliation resolves it; no automatic refund. | Decision |
| What timezone defines a daily limit? (A-14) | Cairo calendar day (`Africa/Cairo`). Count Completed, FundsHeld, SentToBiller and Unknown; exclude Failed, Rejected and Refunded. | Decision |
| Which submissions count for velocity blocking? (A-15) | Count all new submissions, not idempotent repeats; sixth submission in 60 seconds is rejected and starts a 10-minute block. | Decision |
| Who prevents AquaCo overpayment? (A-16) | PayLink checks against inquiry amount before calling AquaCo and also maps any biller refusal code. | Decision |
| Ownership of FR-18/FR-19? (A-17) | Student 2 authors US-18/US-19; Student 3 reviews the fraud-chain rules. | Decision |
| Missing Part 1 source | `req-p1.md` is referenced by the supplied files but absent from the uploaded repository. US-1 to US-9 were reconstructed from cross-references and must be compared with the original before sign-off. | **Open** |
| Missing original assignment brief | The repository references brief sections and hard cases, but the original brief was not included. Numeric targets and rules are carried forward from team files, not independently verified against the brief. | **Open** |
| 500 ms p95 / 99% resilience targets | These are team-defined measurable targets in the supplied NFR table, not independently confirmed brief values. | **Confirm** |
| US-23 channel mismatch | Story title/criteria mention SMS/email while US-22 specifies SMS/push. Confirm whether email is also required or whether retry scope should be SMS/push only. | **Open** |
| US-25 audit atomicity | Audit record is required in the same transaction as the ledger movement; confirm implementation/database enforcement strategy in design. | Design follow-up |

## 6. Prioritization (MoSCoW)
- **Must:** US-1 to US-16, US-18, US-20, US-22, US-25.
- **Should:** US-17, US-19, US-21, US-23, US-24, US-26.
- **Could:** US-27, US-28.

**Priority note:** Priorities for US-1 to US-9 are provisional because Part 1 was missing. The supplied Part 2/3 priorities for US-10 to US-28 are preserved.

## 7. Decisions and implementation notes
1. Money must use exact decimal values; never binary floating-point arithmetic for EGP amounts.
2. Wallet movements are represented by immutable ledger entries; available and held amounts are kept distinct.
3. A payment must hold funds before a biller call; Unknown keeps the hold until resolved.
4. Only the lifecycle transitions documented in the state table are allowed. Completed, Rejected and Refunded are final payment states.
5. A refund of a completed payment is a separate refund workflow and does not rewrite the original payment state.
6. Biller-specific protocols/errors are isolated behind adapters.
7. Configuration-driven values (fees, limits, retries, callback deadline and commission) must not be hard-coded.
8. Cairo time is used for daily aggregation and daily limits.
9. The current repository's `app/main.py` exposes only a FastAPI health endpoint; the requirements describe the intended product scope and are not evidence that all business features are implemented.

## 8. Source files reviewed
- `req-p2.md` — US-10 to US-19, six NFRs, ambiguity/decision log, traceability and payment lifecycle.
- `docs/req-p3.md` — US-20 to US-28 and traceability.
- `prompt-log.md` — AI prompt history and review notes.
- `app/main.py` — current API skeleton (health endpoint only).
- `pyproject.toml`, tests and Docker configuration — repository setup context.

