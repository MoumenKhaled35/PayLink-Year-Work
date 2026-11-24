# PayLink - Phase 1: Requirements Pack (Part 3)

_Architecture Lead deliverable: User Stories US-20 to US-28 (FR-20 to FR-28) and Traceability_

**Owner:** Student 3 (Architecture Lead)  
**Status:** Ready for review (pull request `docs/requirements-p3`)  
**Continues:** [`req-p2.md`](req-p2.md) (US-10 to US-19). Same conventions: MoSCoW priorities from the brief (section 3.2), acceptance criteria in Given / When / Then, all money in EGP with exact decimals.

## 1. User Stories (FR-20 to FR-28)

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