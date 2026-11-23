# PayLink — Requirements & Product Lead

## 1. Problem Summary

PayLink is a bill-payment and digital-wallet backend in Egypt. It allows customers to pay utility bills, including electricity, water, mobile and internet bills, using money held in a digital wallet. Customers can also top up their wallets through a simulated card or agent cash.

The system provides biller and service information, allows customers to inquire about a bill and review the amount, service fee and total before paying, and supports payment from the wallet. Wallet balances must be based on ledger entries, and every balance change must be recorded. Administrators manage billers and their services.

## 2. Stakeholders

| Stakeholder | Role |
|---|---|
| Customer | Registers, views wallet information and transaction history, tops up the wallet, views billers, makes bill inquiries and pays bills. |
| Administrator (Admin) | Adds, edits and disables billers and services. |
| Agent | Provides the agent-cash wallet top-up channel. |
| Biller | Issues bills and receives payments from PayLink. |

## 3. User Stories and Acceptance Criteria

### US-1 — Customer Registration
**Related requirement:** FR-1  
**Priority:** Must

As a customer, I want to register an account so that I can use PayLink.

**Acceptance Criteria**
- **Given** that a customer is not registered, **when** the customer completes registration, **then** the system creates a customer account with the basic verification level.

### US-2 — Upgrade Verification Level
**Related requirement:** FR-2  
**Priority:** Should

As a customer, I want my account to be upgraded to the verified level so that I can use the higher payment limit.

**Acceptance Criteria**
- **Given** that a customer has the basic verification level, **when** the account is upgraded to the verified level, **then** the customer's daily payment limit becomes 30,000 EGP instead of the basic limit of 5,000 EGP.

### US-3 — View Wallet and Transaction History
**Related requirement:** FR-3  
**Priority:** Must

As a customer, I want to view my available balance, held balance and transaction history so that I can track my wallet.

**Acceptance Criteria**
- **Given** that a customer has a wallet, **when** the customer requests wallet information, **then** the system displays the available balance, held balance and transaction history.

### US-4 — Top Up Wallet
**Related requirement:** FR-4  
**Priority:** Must

As a customer, I want to top up my wallet using a simulated card or agent cash so that I can add money to my wallet.

**Acceptance Criteria**
- **Given** that a customer has a wallet, **when** the customer tops up using a simulated card or agent cash, **then** the system processes the wallet top-up.

### US-5 — Record Wallet Balance Changes in the Ledger
**Related requirement:** FR-5  
**Priority:** Must

As a system stakeholder, I want every wallet balance change to create a ledger entry so that wallet balances are calculated from recorded money movements.

**Acceptance Criteria**
- **Given** that a wallet balance changes, **when** the change is recorded, **then** the system creates a ledger entry for that change.
- **Given** that a wallet balance is requested, **when** the system calculates the balance, **then** it calculates it from the wallet's ledger entries.

### US-6 — Manage Billers and Services
**Related requirement:** FR-6  
**Priority:** Must

As an administrator, I want to add, edit and disable billers and services so that the biller catalog can be maintained.

**Acceptance Criteria**
- **Given** that an administrator is managing the biller catalog, **when** the administrator adds a biller or service, **then** the system stores it.
- **Given** that a biller or service exists, **when** the administrator edits it, **then** the system saves the changes.
- **Given** that a biller or service exists, **when** the administrator disables it, **then** the system marks it as disabled.

### US-7 — View Billers and Required Input Fields
**Related requirement:** FR-7  
**Priority:** Must

As a customer, I want to see the available billers and the input fields required by each one so that I know what information to provide.

**Acceptance Criteria**
- **Given** that the biller catalog contains billers and services, **when** the customer views the catalog, **then** the system displays the billers and the input fields required by each.

### US-8 — Inquire About a Bill
**Related requirement:** FR-8  
**Priority:** Must

As a customer, I want to inquire about a bill and see its amount, fee and total before paying so that I know the full amount due.

**Acceptance Criteria**
- **Given** that the customer provides the required bill information, **when** the customer runs a bill inquiry, **then** the system displays the bill amount, service fee and total before payment.

### US-9 — Pay a Bill from the Wallet
**Related requirement:** FR-9  
**Priority:** Must

As a customer, I want to pay a bill from my wallet so that I can complete bill payments through PayLink.

**Acceptance Criteria**
- **Given** that a customer has a bill to pay, **when** the customer chooses to pay using the wallet, **then** the system processes the bill payment from the customer's wallet.

## 4. Scope Note

This document covers the Student 1 scope: the problem summary, stakeholders, user stories US-1 to US-9 (FR-1 to FR-9), and the use-case diagram. It does not add requirements from FR-10 onward.
