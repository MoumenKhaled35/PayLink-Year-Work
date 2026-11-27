# PayLink — Consolidated Requirements Pack (Phase 1)

**Course:** Advanced Software Engineering  
**Supervisor:** D. Doskey Abd Elqawy  
**Repository:** `github.com/MoumenKhaled35/PayLink-Year-Work`  
**Target Git Tag:** `phase-1`  
**Technology Stack:** Python 3.12 + FastAPI + PostgreSQL  

---

## 1. Problem Summary

PayLink is a bill-payment and digital-wallet backend in Egypt. It allows customers to pay utility bills—including electricity, water, mobile, and internet bills—using money held in a digital wallet. Customers can also top up their wallets through a simulated card or agent cash, browse supported billers and services, inquire about bills, and review the bill amount, service fee, and total charge before paying. Wallet balances are calculated strictly from immutable ledger entries, and every balance change is recorded.

Agents can perform bill payments and cash top-ups on behalf of customers, while support employees and administrators manage accounts, billers, service configurations, refunds, daily reconciliation, and financial reporting.

The central problem is to process bill payments reliably even when networks or external billers fail. PayLink must:
- Prevent duplicate charges and wallet overspending.
- Preserve held funds safely when an external biller outcome is uncertain.
- Isolate biller-specific protocols behind clean adapters.
- Maintain complete, immutable audit trails for every financial and administrative action.

---

## 2. Stakeholders

| Stakeholder | Role & Responsibility |
|---|---|
| Customer | Registers an account, views wallet balances and transaction history, tops up wallet, browses billers, inquires about bills, pays bills, receives notifications, and requests refunds. |
| Agent | Provides the agent-cash wallet top-up channel and pays bills on behalf of customers in exchange for a 40% fee commission. |
| Administrator (Admin) | Adds, edits, and disables billers and services; verifies customer accounts; configures fees, promotions, and limits; views daily financial totals. |
| Support Employee | Searches payments by reference, inspects full life-cycle histories, blocks/unblocks accounts, and reviews/approves refund requests. |
| Finance / Operations | Runs nightly settlement reconciliation, resolves `Unknown` payments, and investigates discrepancies. |
| Compliance / Auditor | Audits immutable ledger entries and system audit logs to trace all financial and administrative operations. |
| External Billers | Receive payment requests and return outcomes across distinct protocols (`ElectroCo`, `AquaCo`, `TopUpNet`, and optional `NetCo`). |
| Notification Providers | Deliver SMS, push, and email alerts with retry support. |
| Teaching Assistant / Supervisor | Reviews requirement interpretations and confirms unresolved domain decisions. |

---

## 3. User Stories and Acceptance Criteria (US-1 to US-28)

### Part 1 — Core Accounts, Wallet, Catalog & Bill Payment (`docs/req-p1.md`, US-1 to US-9)

#### US-1 — Customer Registration (`FR-1`, Must)
**As** a customer, **I want** to register an account **so that** I can use PayLink.

**Acceptance Criteria:**
- **Given** that a customer is not registered, **when** the customer completes registration, **then** the system creates a customer account with the basic verification level.

#### US-2 — Upgrade Verification Level (`FR-2`, Should)
**As** a customer, **I want** my account to be upgraded to the verified level **so that** I can use the higher payment limit.

**Acceptance Criteria:**
- **Given** that a customer has the basic verification level, **when** the account is upgraded to the verified level, **then** the customer's daily payment limit becomes `30,000.00 EGP` instead of the basic limit of `5,000.00 EGP`.

#### US-3 — View Wallet and Transaction History (`FR-3`, Must)
**As** a customer, **I want** to view my available balance, held balance, and transaction history **so that** I can track my wallet.

**Acceptance Criteria:**
- **Given** that a customer has a wallet, **when** the customer requests wallet information, **then** the system displays the available balance, held balance, and transaction history.

#### US-4 — Top Up Wallet (`FR-4`, Must)
**As** a customer, **I want** to top up my wallet using a simulated card or agent cash **so that** I can add money to my wallet.

**Acceptance Criteria:**
- **Given** that a customer has a wallet, **when** the customer tops up using a simulated card or agent cash, **then** the system processes the wallet top-up.

#### US-5 — Record Wallet Balance Changes in the Ledger (`FR-5`, Must)
**As** a system stakeholder, **I want** every wallet balance change to create a ledger entry **so that** wallet balances are calculated from recorded money movements.

**Acceptance Criteria:**
1. **Given** that a wallet balance changes, **when** the change is recorded, **then** the system creates a ledger entry for that change.
2. **Given** that a wallet balance is requested, **when** the system calculates the balance, **then** it calculates it from the wallet's ledger entries.

#### US-6 — Manage Billers and Services (`FR-6`, Must)
**As** an administrator, **I want** to add, edit, and disable billers and services **so that** the biller catalog can be maintained.

**Acceptance Criteria:**
1. **Given** that an administrator is managing the biller catalog, **when** the administrator adds a biller or service, **then** the system stores it.
2. **Given** that a biller or service exists, **when** the administrator edits it, **then** the system saves the changes.
3. **Given** that a biller or service exists, **when** the administrator disables it, **then** the system marks it as disabled.

#### US-7 — View Billers and Required Input Fields (`FR-7`, Must)
**As** a customer, **I want** to see the available billers and the input fields required by each one **so that** I know what information to provide.

**Acceptance Criteria:**
- **Given** that the biller catalog contains billers and services, **when** the customer views the catalog, **then** the system displays the billers and the input fields required by each.

#### US-8 — Inquire About a Bill (`FR-8`, Must)
**As** a customer, **I want** to inquire about a bill and see its amount, fee, and total before paying **so that** I know the full amount due.

**Acceptance Criteria:**
- **Given** that the customer provides the required bill information, **when** the customer runs a bill inquiry, **then** the system displays the bill amount, service fee, and total before payment.

#### US-9 — Pay a Bill from the Wallet (`FR-9`, Must)
**As** a customer, **I want** to pay a bill from my wallet **so that** I can complete bill payments through PayLink.

**Acceptance Criteria:**
- **Given** that a customer has a bill to pay, **when** the customer chooses to pay using the wallet, **then** the system processes the bill payment from the customer's wallet.

---

### Part 2 — Payment Processing, Integrations, Fees & Fraud Controls (`docs/req-p2.md`, US-10 to US-19)

#### US-10 — Idempotent Payment Requests (`FR-10`, Must)
**As** a customer on a slow network, **I want** a repeated payment request to return the first result, **so that** I am never charged twice.

**Acceptance Criteria:**
1. **Given** a payment request with idempotency key `K` that was processed and ended `Completed`, **when** the same customer sends the same request with key `K` again, **then** the system returns the original result (same payment reference and state), creates no new payment, no new hold, no new ledger entry, and makes no new biller call.
2. **Given** a payment request with key `K` that is still being processed, **when** the same request arrives again at the same moment, **then** only one payment is created and the second request returns the same payment reference with its current state.
3. **Given** a key `K` already used for a payment of `350.00 EGP`, **when** a request with key `K` arrives with different content (another amount or another bill), **then** it is rejected with the reason `"idempotency key reused with different request"` and nothing is changed.
4. **Given** a payment request without an idempotency key, **when** it is submitted, **then** it is rejected with a validation error naming the missing key and no payment is created.
5. **Given** two different customers who send the same key value, **when** both submit, **then** each gets their own payment (keys are scoped per customer).

_Note:_ Covers Hard Case 1. Key retention time and scope are decided in `A-8`.

#### US-11 — Enforce the Payment Life Cycle (`FR-11`, Must)
**As** the business, **I want** every payment to be in exactly one state and to follow only the allowed transitions, **so that** a payment can never reach an impossible or unsafe state.

**Acceptance Criteria:**
1. **Given** a new payment, **when** it is created, **then** its state is `Initiated` and the creation is recorded in the payment history with time and reason.
2. **Given** each allowed transition (`Initiated -> FundsHeld` or `Rejected`; `FundsHeld -> SentToBiller`; `SentToBiller -> Completed`, `Failed`, or `Unknown`; `Unknown -> Completed` or `Failed`; `Failed -> Refunded`), **when** its event happens, **then** the state changes to the target state and the history records the old state, the new state, the event, and the time.
3. **Given** any pair of states that is not in the allowed table (for example `Initiated -> Completed`, or `Completed -> Failed`), **when** the system tries to apply it, **then** the change is refused, the state stays the same, and the attempt is logged.
4. **Given** a payment in a final state (`Completed`, `Rejected`, or `Refunded`), **when** any event arrives (late callback, retry result, settlement file line), **then** the state does not change.
5. **Given** a payment in `Unknown`, **when** the system evaluates it, **then** it is never moved to `Refunded` directly and is never refunded automatically; it must first become `Failed`.

_Note:_ Source for `docs/design/state-payment.puml`.

#### US-12 — Hold Funds Before Calling the Biller (`FR-12`, Must)
**As** a customer, **I want** my money to be held before the biller is called and released if the payment fails, **so that** I am not charged for a payment that did not happen and cannot overspend.

**Acceptance Criteria:**
1. **Given** a customer has `1,000.00 EGP` available and a payment total of `352.50 EGP`, **when** the fraud checks pass, **then** two ledger entries move `352.50 EGP` from `Available` to `Held` (`available = 647.50`, `held = 352.50`), the payment becomes `FundsHeld`, and only then is the biller called.
2. **Given** a payment in state `Failed` with `352.50 EGP` held, **when** the failure is confirmed, **then** the hold is released to the wallet by a new ledger entry (`available` back to `1,000.00`, `held = 0.00`) and the payment becomes `Refunded`.
3. **Given** a payment in state `Unknown`, **when** time passes, **then** the hold stays in place and is not released until the payment is `Completed` or `Failed`.
4. **Given** a wallet with `400.00 EGP` available and two payments of `352.50 EGP` arriving at the same moment, **when** both are processed, **then** exactly one becomes `FundsHeld` and the other is `Rejected` with the reason `"insufficient funds"`; the available balance never goes below `0.00`.
5. **Given** a payment that completes, **when** the biller confirms, **then** the hold becomes a final charge: `Held` decreases by `352.50`, bill amount `350.00` is recorded as paid to the biller, and fee `2.50` as PayLink fee income.

_Note:_ Covers Hard Case 4. Depends on `US-5`.

#### US-13 — Handle Biller Timeout and Retries (`FR-13`, Must)
**As** a customer, **I want** a payment that does not get an answer to be handled safely and retried, **so that** I am neither charged without payment nor refunded wrongly.

**Acceptance Criteria:**
1. **Given** ElectroCo takes 12 seconds to answer while the timeout is 10 seconds, **when** the payment is sent, **then** after 10 seconds the payment becomes `Unknown`, the money stays held, and the customer is told `"your payment is being processed"`.
2. **Given** a payment in `Unknown`, **when** 1, 5, and 15 minutes have passed since it became `Unknown`, **then** the system re-queries the biller at each of these times, at most 3 times in total.
3. **Given** a re-query in which the biller says the payment was received, **when** the answer arrives, **then** the payment becomes `Completed` (charge, fee, and notification as in `US-12` criterion 5).
4. **Given** a re-query in which the biller says it refused, **when** the answer arrives, **then** the payment becomes `Failed`, then `Refunded` when the hold is released.
5. **Given** three re-queries that all got no answer, **when** the last one ends, **then** the payment stays `Unknown` with the money held and waits for reconciliation (`FR-26`); no automatic refund happens.
6. **Given** a retry or re-query, **when** it is sent, **then** it uses the original payment reference so the biller cannot receive the same payment twice.

_Note:_ Covers Hard Case 2. Timeout and retry delays come from configuration. Not applied to `NetCo` (batch).

#### US-14 — Accept Asynchronous Callbacks and Ignore Duplicates (`FR-14`, Must)
**As** the system, **I want** to accept the final result that TopUpNet sends later by callback and to ignore repeated callbacks, **so that** a payment completes exactly once.

**Acceptance Criteria:**
1. **Given** a TopUpNet payment in state `SentToBiller` (the biller answered `"accepted"`), **when** TopUpNet calls the callback URL with `"success"` and the payment reference, **then** the payment becomes `Completed`.
2. **Given** a TopUpNet payment in state `SentToBiller`, **when** the callback says `"failed"`, **then** the payment becomes `Failed` and then `Refunded` as in `US-12` criterion 2, and the customer gets an SMS with the reason.
3. **Given** a payment that is already `Completed`, **when** TopUpNet calls the callback with `"success"` a second time, **then** the payment is not changed, no second charge, fee, commission, or notification is created, and the duplicate is written to the log.
4. **Given** a payment in `Unknown`, **when** a valid callback `"success"` arrives, **then** the payment becomes `Completed`.
5. **Given** a callback for a payment reference that does not exist or has an invalid signature or secret, **when** it arrives, **then** it is rejected, nothing changes, and the attempt is logged.
6. **Given** a callback whose result conflicts with a final state (for example `"success"` for a payment that is `Refunded`), **when** it arrives, **then** the payment is not changed and the conflict is flagged for support in the reconciliation report.

_Note:_ Covers Hard Case 6. Callback authentication method is decided in `A-10`.

#### US-15 — Support Billers with Different Formats (`FR-15`, Must)
**As** PayLink management, **I want** at least ElectroCo, AquaCo, and TopUpNet supported through one adapter each, **so that** the rest of the system does not depend on any biller's protocol and billers can fail independently.

**Acceptance Criteria:**
1. **Given** ElectroCo (REST/JSON), AquaCo (SOAP-style XML), and TopUpNet (REST/JSON, asynchronous), **when** a payment is made to each, **then** the Payment Processing module uses the same internal request and result model for all three and never sees the biller's field names or error codes.
2. **Given** AquaCo refuses a payment with a biller-specific error code, **when** the adapter receives it, **then** the code is translated to a standard reason, the payment becomes `Failed`, the hold is released (`Refunded`), and the customer gets an SMS with a clear reason.
3. **Given** AquaCo rejects any payment above the bill amount, **when** a customer pays more than the inquiry amount, **then** the payment is stopped before the biller call with the reason `"amount above bill"` or, if it reaches the biller, handled as in criterion 2.
4. **Given** ElectroCo is down, **when** customers pay AquaCo and TopUpNet bills, **then** those payments are processed normally; only ElectroCo payments end `Unknown` or `Failed`.
5. **Given** a new biller, **when** it is added, **then** only a new adapter and its configuration are added and no existing module changes. `NetCo` (daily batch file) is optional.

_Note:_ Covers Hard Cases 3 and 8.

#### US-16 — Calculate Service Fees (`FR-16`, Must)
**As** PayLink management, **I want** the service fee to follow the business rules, **so that** the company earns the right fee and the customer sees the right total.

**Acceptance Criteria:**
1. **Given** an electricity or water bill of any valid amount, **when** the fee is calculated, **then** it is the fixed value `2.50 EGP`.
2. **Given** a mobile top-up, **when** the fee is calculated, **then** it is `1.5%` of the amount with a minimum of `1.00 EGP`: `100.00` gives `1.50`; `20.00` gives `1.00` (minimum applies); `123.45` gives `1.85` (rounded to 2 decimals per `A-6`).
3. **Given** an internet bill, **when** the fee is calculated, **then** it is `2.00 EGP` for an amount up to and including `200.00 EGP` and `4.00 EGP` for an amount above `200.00 EGP`.
4. **Given** a promotion configured for one biller with a start and an end date, **when** a payment is made to that biller inside the period (both dates included), **then** the fee is `0.00 EGP`; outside the period or for another biller the normal fee applies.
5. **Given** any fee calculation, **when** it is done, **then** all values come from configuration (no fee value in code) and all arithmetic uses exact decimals.
6. **Given** a payment where the fee was calculated at inquiry time, **when** the payment is confirmed, **then** the same fee is used even if the configuration changed in between.

#### US-17 — Agent Pays on Behalf of a Customer (`FR-17`, Should)
**As** an agent at a PayLink terminal, **I want** to pay a bill for a customer and earn commission, **so that** customers without the app can pay and I am rewarded.

**Acceptance Criteria:**
1. **Given** an agent wallet with at least `352.50 EGP` and a customer who gives the agent `352.50 EGP` in cash, **when** the agent pays the ElectroCo bill of `350.00 EGP` (fee `2.50`) and ElectroCo confirms, **then** the payment is `Completed`, it is marked with the agent as the channel, and the receipt is issued to the customer.
2. **Given** a completed agent payment with fee `2.50 EGP`, **when** the payment completes, **then** a commission of `1.00 EGP` (`40%` of the fee) is credited to the agent wallet by a ledger entry and PayLink fee income is reduced accordingly in the report (net `1.50 EGP`).
3. **Given** an agent payment that ends `Failed`, `Rejected`, or `Unknown`, **when** the state changes, **then** no commission is credited; for `Unknown` it is credited only if the payment later becomes `Completed`.
4. **Given** an agent wallet with less than the total, **when** the agent pays, **then** the payment is `Rejected` with the reason `"insufficient funds"`.
5. **Given** an agent payment with a promotion fee of `0.00 EGP`, **when** it completes, **then** the commission is `0.00 EGP` and no commission entry is created.
6. **Given** a user who is not an agent, **when** they try to pay on behalf of a customer, **then** the request is rejected as forbidden.

#### US-18 — Reject Payments Above Single or Daily Limits (`FR-18`, Must)
**As** the business and the regulator, **I want** payments above the single-payment limit or the daily limit to be rejected with a clear reason, **so that** exposure to fraud and losses is limited.

**Acceptance Criteria:**
1. **Given** a total charge of `10,000.01 EGP` or `4.99 EGP`, **when** the customer confirms the payment, **then** it is `Rejected` with the reason `"total amount outside allowed range (5.00 - 10,000.00 EGP)"` and nothing is held.
2. **Given** a `BASIC` account with `4,800.00 EGP` already counted today and a new payment of `300.00 EGP`, **when** it is confirmed, **then** it is `Rejected` with the reason `"daily limit exceeded (5,000.00 EGP)"` and nothing is held.
3. **Given** a `VERIFIED` account with `29,000.00 EGP` counted today, **when** it pays `1,000.00 EGP`, **then** the payment is accepted because the total is exactly `30,000.00 EGP`; a payment of `1,000.01 EGP` is `Rejected`.
4. **Given** an earlier payment that ended `Failed`, `Rejected`, or `Refunded`, **when** the daily total is computed, **then** that payment is not counted; `Completed` payments and payments in `FundsHeld`, `SentToBiller`, and `Unknown` are counted.
5. **Given** the daily limit values in configuration, **when** an admin changes them (`FR-24`), **then** the new values are used for the next payment without redeploying.
6. **Given** a payment at `00:00` Cairo time (`Africa/Cairo`) of the next day, **when** the daily total is computed, **then** the new day starts with `0.00 EGP`.

#### US-19 — Block an Account After Too Many Payments (`FR-19`, Should)
**As** the business, **I want** an account that makes more than 5 payments in 60 seconds to be blocked for 10 minutes, **so that** automated attacks and runaway clients are stopped.

**Acceptance Criteria:**
1. **Given** an account that has made 5 payments in the last 60 seconds, **when** it submits a 6th payment within the same 60 seconds, **then** the 6th is `Rejected` with the reason `"too many payments, account blocked for 10 minutes"` and the account is blocked.
2. **Given** an account that is blocked by this rule, **when** it submits any payment during the next 10 minutes, **then** the payment is `Rejected` with the reason `"account blocked"` and nothing is held.
3. **Given** a block that started 10 minutes ago, **when** the account submits a payment after the block time ended, **then** the block is removed automatically and the payment is processed normally.
4. **Given** exactly 5 payments in 60 seconds, **when** the account submits a payment 61 seconds after the first one, **then** it is not blocked (sliding 60-second window).
5. **Given** a repeated request with an already used idempotency key (`US-10`), **when** it arrives, **then** it does not count as a new payment for this rule.
6. **Given** an account blocked by this rule, **when** a support employee unblocks it (`FR-21`), **then** the block ends immediately and the action is written to the audit log.

---

### Part 3 — Support, Notifications, Administration & Reconciliation (`docs/req-p3.md`, US-20 to US-28)

#### US-20 — Search Payment by Reference and View Full History (`FR-20`, Must)
**As** a support employee, **I want** to search for a payment by its unique reference and view its full life-cycle history, **so that** I can investigate customer inquiries and resolve disputes accurately.

**Acceptance Criteria:**
1. **Given** an existing payment with reference `PAY-2026-00123`, **when** a support employee searches by `PAY-2026-00123`, **then** the system returns the payment details (customer/agent ID, biller, service, bill amount, service fee, agent commission, current state) and the chronological list of all state transitions (old state, new state, triggering event, timestamp, and reason).
2. **Given** a payment that has associated ledger entries and notification attempts, **when** a support employee views that payment by reference, **then** the response also displays the linked ledger entry IDs and notification delivery statuses (`delivered`, `retrying`, or `undelivered`).
3. **Given** a payment reference that does not exist in the system, **when** a support employee searches for it, **then** the system returns a `404 Not Found` error with a clear message.
4. **Given** a user whose role is `Customer` or `Agent`, **when** they attempt to access the support payment-search endpoint for another user's payment, **then** the request is rejected with `403 Forbidden`.

#### US-21 — Block and Unblock an Account (`FR-21`, Should)
**As** a support employee, **I want** to manually block and unblock a customer or agent account, **so that** suspicious accounts can be frozen immediately and legitimate users restored after review.

**Acceptance Criteria:**
1. **Given** an active account, **when** a support employee blocks the account with a mandatory reason, **then** the account status becomes `Blocked`, any subsequent payment or top-up attempt from that account is rejected with the reason `"account blocked"`, and an audit log entry is recorded (`US-25`).
2. **Given** an account that was blocked either manually by support or automatically by the velocity rule (`US-19`), **when** a support employee unblocks the account with a reason, **then** the account status immediately returns to `Active`, new payments are allowed again, and the unblock action is written to the audit log.
3. **Given** a support employee attempts to block or unblock an account without providing a reason, **when** the request is submitted, **then** it is rejected with a validation error and the account state does not change.
4. **Given** an account that is currently `Blocked` while an earlier payment is already in `SentToBiller` or `Unknown`, **when** the biller later confirms or refuses that in-flight payment, **then** the in-flight payment still completes its life cycle (either `Completed` or `Failed -> Refunded`) without losing funds.

#### US-22 — Send SMS and Push Notifications on Completion and Failure (`FR-22`, Must)
**As** a customer, **I want** to receive an SMS and a push notification when my payment completes or fails, **so that** I have immediate confirmation of my bill status and wallet balance.

**Acceptance Criteria:**
1. **Given** a payment of `350.00 EGP` (fee `2.50 EGP`, total `352.50 EGP`) transitions to `Completed`, **when** the completion event is processed, **then** the system queues and sends both an SMS and a push notification to the customer containing the payment reference, biller name, amount paid, fee, and new available balance.
2. **Given** AquaCo refuses a payment with an error code and the payment transitions to `Failed` and then `Refunded`, **when** the failure is processed, **then** the customer receives both an SMS and a push notification stating that the payment failed, the clear translated reason, and that the held amount (`352.50 EGP`) has been released back to the wallet.
3. **Given** a payment transitions to `Unknown` after a 10-second timeout, **when** the timeout occurs, **then** the customer is notified that the payment is still being processed and the funds remain held (no false completion or failure message is sent).
4. **Given** the external SMS provider is down at the exact moment a payment completes, **when** the notification dispatch fails, **then** the payment remains `Completed` (never rolled back or delayed) and the notification enters the retry workflow (`US-23`).

_Note:_ Covers Hard Cases 3 and 5.

#### US-23 — Retry Failed Notifications Up to 3 Times (`FR-23`, Should)
**As** PayLink operations, **I want** failed SMS or email notifications to be retried up to 3 times before being marked undelivered, **so that** temporary gateway glitches do not cause missed customer alerts.

**Acceptance Criteria:**
1. **Given** an SMS or email notification fails on its initial send attempt, **when** the retry worker processes it, **then** the system retries sending up to 3 additional times, incrementing `retry_count` on each attempt.
2. **Given** a failed notification succeeds on the 2nd retry attempt, **when** the gateway confirms delivery, **then** the notification status becomes `delivered`, `delivered_at` is recorded, and no further retries occur.
3. **Given** a notification fails on the initial attempt and all 3 retry attempts, **when** the 3rd retry fails, **then** its final status is set to `undelivered` with the last gateway error reason, and no 4th retry is attempted.
4. **Given** a notification that is already marked `delivered`, **when** any duplicate event or worker run occurs, **then** the notification is not sent again.

_Note:_ Covers Hard Case 5.

#### US-24 — Edit Fee and Limit Values Without Redeploying (`FR-24`, Should)
**As** an admin, **I want** to update service fees, promotion periods, and transaction limits dynamically through configuration, **so that** business rule changes take effect immediately without downtime or code deployment.

**Acceptance Criteria:**
1. **Given** an admin updates the daily limit for `Basic` accounts from `5,000.00 EGP` to `7,500.00 EGP` or updates a biller's fixed fee, **when** the configuration update is saved, **then** the very next bill inquiry or payment uses the updated value without restarting or redeploying the application.
2. **Given** an admin configures a promotion period (`start_date` and `end_date`) for a single chosen biller, **when** payments occur within that date range (inclusive), **then** the fee evaluates to `0.00 EGP`; if another biller already had an active promotion, only one biller promotion is active per rule configuration.
3. **Given** an admin updates a fee rule while a customer has already run a bill inquiry (`US-8`) and is confirming payment, **when** the payment is processed, **then** the fee locked at inquiry time is honored (consistent with `US-16` criterion 6).
4. **Given** an admin submits an invalid configuration value (such as a negative fee, `min_amount > max_amount`, or `start_date > end_date`), **when** saved, **then** the system rejects the change with a validation error and keeps the previous valid configuration.
5. **Given** any valid configuration change by an admin, **when** committed, **then** an audit log entry is recorded with the admin ID, timestamp, parameter key, old value, new value, and reason (`US-25`).

#### US-25 — Record Every Money Movement and Admin Action in an Immutable Audit Log (`FR-25`, Must)
**As** a compliance officer and auditor, **I want** every money movement and administrative action recorded in an immutable audit log, **so that** the system maintains 100% financial traceability and accountability.

**Acceptance Criteria:**
1. **Given** any money movement occurs (wallet top-up, fund hold, hold capture/final charge, fee income credit, agent commission credit, hold release/refund, or approved completed-payment refund), **when** the ledger entry is created, **then** an audit record is created in the same transaction containing `actor_id`, `actor_role`, `timestamp`, `action_type`, `entity_id`, `amount`, and `reason`.
2. **Given** any administrative or support action occurs (upgrading customer verification, adding/editing/disabling a biller, editing fees or limits, blocking/unblocking an account, or approving a refund), **when** the action succeeds, **then** an audit record is written with who performed it, when, what changed, and why.
3. **Given** existing rows in `audit_logs` or `ledger_entries`, **when** any application service attempts an `UPDATE` or `DELETE` operation on them, **then** the operation is rejected (enforced at both domain and database levels).

_Note:_ Directly satisfies `NFR-5` (Auditability).

#### US-26 — Produce a Daily Reconciliation Report from a Settlement File (`FR-26`, Should)
**As** a finance and operations specialist, **I want** the system to compare PayLink's daily payment records against each biller's nightly settlement file and generate a discrepancy report, **so that** stuck payments are resolved and financial mismatches are caught.

**Acceptance Criteria:**
1. **Given** a payment is in `Unknown` state in PayLink and the nightly settlement file from ElectroCo lists that payment reference as paid with matching amount, **when** reconciliation runs, **then** the payment transitions from `Unknown` to `Completed`, the held funds are captured as a final charge, fee/commission are recorded, and the customer is notified.
2. **Given** a payment is in `Unknown` state in PayLink and is absent from (or marked failed in) the biller's nightly settlement file after the settlement cutoff, **when** reconciliation runs, **then** the payment transitions from `Unknown` to `Failed` and immediately to `Refunded` (releasing the hold to the customer's available balance).
3. **Given** a payment is marked `Failed` or `Refunded` in PayLink, **when** the nightly settlement file lists that same payment reference as received/paid by the biller, **then** PayLink does NOT automatically alter the final state, and flags the record as a `CRITICAL_DISCREPANCY` in the reconciliation report for support review (Hard Case 7).
4. **Given** a settlement file contains a payment reference unknown to PayLink or an amount that differs from PayLink's recorded bill amount, **when** reconciliation runs, **then** the line is flagged in the reconciliation report with the exact variance details.
5. **Given** reconciliation finishes processing a settlement file, **when** the report is generated, **then** it summarizes total matched payments, total resolved `Unknown` payments, total discrepancies, and net settlement amount per biller.

_Note:_ Covers Hard Case 7.

#### US-27 — Request and Approve Refund of a Completed Payment (`FR-27`, Could)
**As** a customer, **I want** to request a refund for a completed payment when a billing dispute occurs, and have a support employee review and approve it, **so that** valid disputes are refunded safely with full audit control.

**Acceptance Criteria:**
1. **Given** a payment in state `Completed`, **when** the owning customer submits a refund request with a reason, **then** a separate `RefundRequest` record is created with status `Requested` while the original payment remains in state `Completed` (consistent with decision `A-7`).
2. **Given** a `RefundRequest` in status `Requested`, **when** a support employee approves it with an approval note, **then** the refund status becomes `Approved -> Done`, compensating ledger entries credit the customer's available balance, and an audit log entry records the support employee's approval.
3. **Given** a `RefundRequest` in status `Requested`, **when** a support employee rejects it with a reason, **then** the refund status becomes `Rejected`, no ledger movement occurs, and the customer is notified of the rejection reason.
4. **Given** a payment that is NOT `Completed` (such as `Initiated`, `Unknown`, `Failed`, or `Rejected`), or a `Completed` payment that already has an active/approved `RefundRequest`, **when** a customer requests a refund, **then** the request is rejected with a clear validation error.

_Note:_ Designed in Phase 1 (`docs/design/seq-refund.puml`) per decision `A-7`.

#### US-28 — View Daily Totals Report (`FR-28`, Could)
**As** an admin, **I want** to view daily aggregated totals for payments, fees earned, commissions paid, and failures per biller, **so that** I can monitor daily revenue and biller reliability.

**Acceptance Criteria:**
1. **Given** an admin queries the daily totals report for a specific date (evaluated in `Africa/Cairo` calendar day), **when** the report is generated, **then** it displays for each biller and overall: total count and EGP volume of `Completed` payments, gross service fees earned, total agent commissions paid (`40%` of agent-channel fees), net PayLink fee revenue, and count of `Failed` / `Rejected` payments.
2. **Given** a day with zero transactions for a specific biller, **when** the daily totals report is requested, **then** that biller appears with `0` counts and `0.00 EGP` totals rather than failing or omitting the biller.
3. **Given** a non-admin user attempts to access the daily totals endpoint, **when** requested, **then** the system returns `403 Forbidden`.

---

## 4. Non-Functional Requirements (6 Measurable)

| ID | Quality | Requirement (with Target) | How It Is Measured | Related Stories |
|---|---|---|---|---|
| NFR-1 | Correctness (Money) | Zero double charges and zero negative balances. In a test with 100 parallel payments on one wallet that can pay only 1 of them, and in a test that sends the same idempotency key 50 times in parallel, exactly 1 charge is made and the final balance is `>= 0.00 EGP`. All money uses exact decimal types. | Automated concurrency and duplicate tests (Hard Cases 1 and 4) in CI; ledger sum check after each test. | US-5, US-10, US-12 |
| NFR-2 | Performance | The system sustains `100 payments/second` for `60 seconds` (`6,000` payments) against mock billers, with an error rate below `1%` and a 95th percentile (`p95`) response time of `500 ms` or less for PayLink's processing (excluding biller latency). | Load-test script (`k6` or `Locust`) run against `docker compose`; results archived in report. | US-9, US-15 |
| NFR-3 | Resilience | If one biller is down or slow, payments to other billers continue: with ElectroCo stopped for 5 minutes, at least `99%` of AquaCo and TopUpNet payments still reach a final state or `SentToBiller`, and requests to the failed biller return within the `10-second` timeout instead of hanging. | Chaos test with a mock biller configured to fail or delay 12s (Hard Case 2). | US-13, US-15 |
| NFR-4 | Modifiability | Adding a new biller or adapting to ElectroCo API v2 touches only the Biller Integration module and configuration (`0` files changed in other modules). A new biller requires at most `1` new adapter class, `1` configuration entry, and its tests. | `git diff --name-only` inspection and Hard Case 8 test. | US-15, US-16 |
| NFR-5 | Auditability | `100%` of money movements and admin actions have an audit record with who, when, and why. Ledger and audit entries cannot be updated or deleted by the application (`0` successful `UPDATE`/`DELETE` attempts). | Automated test asserting equality between ledger movements and audit records, plus immutability constraints. | US-2, US-5, US-6, US-25 |
| NFR-6 | Testability | At least `70%` line coverage on domain logic measured by CI on every push; every one of the 8 hard cases has at least `1` automated test. | Coverage report in GitHub Actions; pipeline fails if coverage drops below `70%`. | All stories |

---

## 5. Ambiguities, Open Questions & Decisions

Items marked **Confirm** represent team interpretations scheduled for supervisor/TA confirmation before Phase 2 implementation.

| ID | Question / Ambiguity | Options Considered | Decision Made | Status | Affects |
|---|---|---|---|---|---|
| Q1 / A-1 | How does a user log in (password, OTP)? | Password + token; SMS OTP | Assume phone number + password + token for Phase 1; OTP is deferred. Protected endpoints enforce role-based access (`Customer`, `Agent`, `Admin`, `Support`). | Assumption | US-1, all |
| Q2 / A-2 | Does an agent cash top-up debit the agent's wallet? | Debit agent wallet; external cash tracking only | Yes. Agent wallet is debited and customer wallet is credited atomically via two linked ledger entries. | Decision | US-4, US-17 |
| Q3 / A-3 | Maximum top-up amount? | Fixed cap; no upper cap | Accept any amount `> 0.00 EGP`; a configurable cap may be added later. | Decision | US-4 |
| Q4 / A-4 | Who verifies a customer (`FR-2`)? | Automated KYC; Admin approval | Admin verifies after an external identity check. | Decision | US-2 |
| Q6 / A-5 | Does the `5.00–10,000.00 EGP` single-payment range include the service fee? | Base bill amount only; total charge (`bill + fee`) | Applies to total charge (`bill_amount + service_fee`); daily limit also counts total charge. | **Confirm** | US-9, US-18 |
| A-6 | Rounding rule for percentage fees (`1.5%` of `123.45 = 1.85175`)? | Round half up; banker's rounding; truncate | Round half up (`ROUND_HALF_UP`) to 2 decimal places using exact `Decimal` arithmetic. | Decision | US-16 |
| A-7 | Refund of a `Completed` payment (`FR-27`, Could) vs. `Completed` being a final state? | Allow `Completed -> Refunded`; keep `Completed` final with separate `RefundRequest` | Keep `Completed` final; create a separate `RefundRequest` (`Requested -> Approved -> Done`) with compensating ledger entries. | **Confirm** | US-11, US-27 |
| A-8 | How long and for whom does an idempotency key count? | Forever; 24 hours; single request | Scoped per customer and retained for 24 hours (configurable); same key with different payload is rejected. | Decision | US-10 |
| A-9 | Which wallet pays when an agent pays on behalf of a customer? | Agent wallet; customer wallet | Agent wallet pays (customer pays cash to agent); fraud limits apply to the paying agent account. | **Confirm** | US-17, US-18 |
| A-10 | How are TopUpNet callbacks authenticated? | Unauthenticated; shared secret header; HMAC body signature | Shared secret header stored in configuration (never hard-coded). Invalid secrets are rejected and logged. | Decision | US-14 |
| Q5 / A-11 | Where does the amount come from for NetCo (no live inquiry)? | Biller lookup; customer input | Customer enters the amount, validated against service `min_amount` and `max_amount`. | Decision | US-8, US-15 |
| A-12 | How long does PayLink wait for an asynchronous TopUpNet callback? | Indefinitely; configurable callback deadline | Configurable 30-minute callback deadline after `"accepted"`. If exceeded, payment moves to `Unknown` and enters retry/reconciliation. | **Confirm** | US-13, US-14 |
| A-13 | What happens after all 3 `Unknown` re-queries fail? | Auto-refund; keep `Unknown` until reconciliation | Keep `Unknown` with funds held until callback, retry answer, or nightly settlement file resolves it (`Completed` or `Failed -> Refunded`). | Decision | US-11, US-13 |
| A-14 | Which payments and time zone define the daily limit? | UTC vs. Cairo time; all attempts vs. active/completed | Calendar day in `Africa/Cairo`. Counts `Completed`, `FundsHeld`, `SentToBiller`, and `Unknown`; excludes `Failed`, `Rejected`, and `Refunded`. | Decision | US-18 |
| A-15 | Which submissions count toward velocity blocking (`FR-19`)? | Accepted attempts only; all new submissions | Count all new submissions (excluding idempotent duplicates); 6th submission in a 60-second sliding window triggers a 10-minute block. | Decision | US-19 |
| A-16 | Who prevents AquaCo overpayment? | Biller only; PayLink pre-check + adapter mapping | PayLink validates against inquiry amount before calling AquaCo and maps any biller refusal code. | Decision | US-15 |

---

## 6. Consolidated Traceability Matrix (FR-1 to FR-28)

| FR | User Story | Priority | Use-Case Diagram | Design Artifacts |
|---|---|---|---|---|
| FR-1 | US-1 | Must | Register Account | `class-diagram.puml` (`Customer`), `er-diagram.puml` (`customers`) |
| FR-2 | US-2 | Should | Upgrade Verification | `class-diagram.puml` (`VerificationLevel`), `er-diagram.puml` (`customers`, `audit_logs`) |
| FR-3 | US-3 | Must | View Balance & History | `class-diagram.puml` (`Wallet`, `LedgerEntry`), `er-diagram.puml` (`wallets`, `ledger_entries`) |
| FR-4 | US-4 | Must | Top Up Wallet | `class-diagram.puml` (`WalletService`), `er-diagram.puml` (`wallets`, `ledger_entries`) |
| FR-5 | US-5 | Must | Ledger & Balances | `class-diagram.puml` (`LedgerEntry`), `er-diagram.puml` (`ledger_entries`) |
| FR-6 | US-6 | Must | Manage Billers & Services | `class-diagram.puml` (`Biller`, `BillerService`), `er-diagram.puml` (`billers`, `biller_services`) |
| FR-7 | US-7 | Must | View Billers & Input Fields | `class-diagram.puml` (`Biller`, `BillerService`), `er-diagram.puml` (`billers`, `biller_services`) |
| FR-8 | US-8 | Must | Bill Inquiry | `seq-pay-bill.puml`, `class-diagram.puml` (`BillerAdapter`) |
| FR-9 | US-9 | Must | Pay a Bill | `seq-pay-bill.puml`, `state-payment.puml`, `er-diagram.puml` (`payments`) |
| FR-10 | US-10 | Must | Idempotency | `seq-pay-bill.puml`, `er-diagram.puml` (`payments.idempotency_key`) |
| FR-11 | US-11 | Must | Payment Lifecycle | `state-payment.puml`, `er-diagram.puml` (`payment_state_history`) |
| FR-12 | US-12 | Must | Hold / Release Funds | `seq-pay-bill.puml`, `seq-refund.puml`, `state-payment.puml`, `er-diagram.puml` (`wallets`, `ledger_entries`) |
| FR-13 | US-13 | Must | Timeout & Retry | `state-payment.puml` (`Unknown`), `seq-pay-bill.puml` |
| FR-14 | US-14 | Must | Async Callbacks | `state-payment.puml`, `seq-pay-bill.puml` |
| FR-15 | US-15 | Must | Biller Integration | `seq-pay-bill.puml`, `class-diagram.puml` (`BillerAdapter` subclasses) |
| FR-16 | US-16 | Must | Fees & Promotions | `seq-pay-bill.puml`, `class-diagram.puml` (`FeeService`) |
| FR-17 | US-17 | Should | Pay on Behalf | `seq-pay-bill.puml`, `class-diagram.puml` (`Agent`), `er-diagram.puml` (`agents`) |
| FR-18 | US-18 | Must | Payment & Daily Limits | `seq-pay-bill.puml`, `class-diagram.puml` (`FraudCheckChain`) |
| FR-19 | US-19 | Should | Excessive Attempts Blocking | `seq-pay-bill.puml`, `class-diagram.puml` (`FraudCheckChain`) |
| FR-20 | US-20 | Must | Search Payment & History | `class-diagram.puml` (`Payment`, `PaymentStateHistory`), `er-diagram.puml` |
| FR-21 | US-21 | Should | Block / Unblock Account | `class-diagram.puml` (`Customer`, `AccountStatus`), `er-diagram.puml` (`audit_logs`) |
| FR-22 | US-22 | Must | SMS & Push Notifications | `seq-pay-bill.puml`, `seq-refund.puml`, `class-diagram.puml` (`NotificationService`) |
| FR-23 | US-23 | Should | Retry Notifications | `seq-refund.puml`, `class-diagram.puml` (`Notification`), `er-diagram.puml` (`notifications`) |
| FR-24 | US-24 | Should | Configure Fees & Limits | `class-diagram.puml` (`FeeService`), `er-diagram.puml` (`biller_services`, `audit_logs`) |
| FR-25 | US-25 | Must | Audit Log | `seq-pay-bill.puml`, `seq-refund.puml`, `er-diagram.puml` (`audit_logs`) |
| FR-26 | US-26 | Should | Settlement & Reconciliation | `class-diagram.puml` (`ReconciliationRecord`), `er-diagram.puml` (`reconciliation_records`) |
| FR-27 | US-27 | Could | Request & Approve Refund | `seq-refund.puml`, `class-diagram.puml` (`RefundRequest`), `er-diagram.puml` (`refund_requests`) |
| FR-28 | US-28 | Could | Daily Financial Totals | `class-diagram.puml` (`Payment`, `Biller`), `er-diagram.puml` (`payments`, `billers`) |

---

## 7. Payment State Diagram & Transitions

Source: [`docs/design/state-payment.puml`](design/state-payment.puml) (`docs/design/state-payment.png`).  
Includes all 8 states, the 9 allowed transitions from Section 2.5, final markers on `Completed`, `Rejected`, and `Refunded`, and the internal retry loop on `Unknown` (up to 3 re-queries at 1, 5, and 15 minutes).

| From State | Triggering Event | To State |
|---|---|---|
| `Initiated` | Fraud checks pass and wallet has sufficient funds | `FundsHeld` |
| `Initiated` | Fraud check fails or funds insufficient | `Rejected` |
| `FundsHeld` | Payment request sent to biller | `SentToBiller` |
| `SentToBiller` | Biller confirms payment | `Completed` |
| `SentToBiller` | Biller refuses payment | `Failed` |
| `SentToBiller` | No answer within 10s timeout | `Unknown` |
| `Unknown` | Biller later confirms (callback, retry, or settlement file) | `Completed` |
| `Unknown` | Biller later refuses, or reconciliation finds no payment | `Failed` |
| `Failed` | Held funds released back to wallet | `Refunded` |

---

## 8. Prioritization Summary (MoSCoW) & Implementation Notes

- **Must (20 stories):** `US-1`, `US-3`, `US-4`, `US-5`, `US-6`, `US-7`, `US-8`, `US-9`, `US-10`, `US-11`, `US-12`, `US-13`, `US-14`, `US-15`, `US-16`, `US-18`, `US-20`, `US-22`, `US-25`.
- **Should (7 stories):** `US-2`, `US-17`, `US-19`, `US-21`, `US-23`, `US-24`, `US-26`.
- **Could (2 stories):** `US-27`, `US-28`.

### Key Architectural & Implementation Rules
1. All monetary amounts use exact `Decimal` / `DECIMAL(12,2)` arithmetic—never binary floating-point types.
2. Wallet `available_balance` and `held_balance` are maintained distinctly and derived from immutable `ledger_entries`.
3. Funds are held (`FundsHeld`) prior to any external biller call and remain held while `Unknown`.
4. Only the 9 state transitions in Section 7 are permitted; `Completed`, `Rejected`, and `Refunded` are terminal states.
5. Refunds of `Completed` payments (`FR-27`) are modeled as separate `RefundRequest` workflows with compensating ledger entries.
6. External billers are isolated behind protocol-specific adapters.
7. All fees, limits, retry schedules, callback deadlines, and commission percentages are configuration-driven.
8. Daily limits and financial aggregations are evaluated on the `Africa/Cairo` calendar day.

### Source Documents
- `docs/req-p1.md` — Part 1 User Stories (`US-1` to `US-9`), Stakeholders, Open Questions (`Q1`–`Q6`), and Use-Case Diagram review.
- `docs/req-p2.md` — Part 2 User Stories (`US-10` to `US-19`), Non-Functional Requirements (`NFR-1` to `NFR-6`), Ambiguities (`A-1` to `A-17`), and State Diagram.
- `docs/req-p3.md` — Part 3 User Stories (`US-20` to `US-28`) and Traceability Matrix.
- `docs/prompt-log.md` — Team AI Prompt Log (8 structured entries across Requirements and Design).