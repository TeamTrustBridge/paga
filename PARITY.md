# Paga Engine SDK parity

The operation matrix for the three SDKs. Every row is implemented in all
three; the `Method` column names the method as it appears in each SDK.

- `paga-python` — <https://github.com/TeamTrustBridge/paga-python>
- `paga-ts` — <https://github.com/TeamTrustBridge/paga-ts>
- `paga-rs` — <https://github.com/TeamTrustBridge/paga-rs> (crates.io package `paga-rs`, Rust path `paga`)

## How the three SDKs are organised

The operations are grouped the same way in all three — one module (or mixin)
per section of Paga's documentation:

| Section | Python | TypeScript | Rust |
|---|---|---|---|
| Checkout | `paga.checkout` | `checkout.ts` | `operations::checkout` |
| Dynamic virtual account, Bank USSD, Paga wallet, USD bank transfer | `paga.collection` | `collection.ts` | `operations::collection` |
| Refunds | `paga.refunds` | `refunds.ts` | `operations::refunds` |
| Direct Debit (Open Banking) | `paga.direct_debit` | `directDebit.ts` | `operations::direct_debit` |
| Money Transfer | `paga.money_transfer` | `moneyTransfer.ts` | `operations::money_transfer` |
| Airtime and data | `paga.airtime` | `airtime.ts` | `operations::airtime` |
| Bill payment (VAS) | `paga.bill_payment` | `billPayment.ts` | `operations::bill_payment` |
| Check the transaction status | `paga.status` | `status.ts` | `operations::status` |
| Your business account | `paga.business` | `business.ts` | `operations::business` |
| Subsidiary accounts | `paga.subsidiary` | `subsidiary.ts` | `operations::subsidiary` |
| Persistent payment accounts | `paga.persistent` | `persistent.ts` | `operations::persistent` |
| Customer registration and KYC | `paga.customer` | `customer.ts` | `operations::customer` |

## Operations

| Section | Operation | Endpoint | Auth | Hash fields | Python | TypeScript | Rust |
|---|---|---|---|---|---|---|---|
| Checkout | Verify a charge | `POST /checkout/transaction/verify` | Basic | — | `verify_charge` | `verifyCharge` | `verify_charge` |
| Collection | Create a payment request | `POST /paymentRequest` | Basic | `referenceNumber, amount, currency, payer.phoneNumber, payer.email` | `create_payment` | `createPayment` | `create_payment` |
| Collection | Check payment status | `POST /status` | Basic | `referenceNumber` | `get_payment_status` | `getPaymentStatus` | `get_payment_status` |
| Collection | List the customer's banks | `POST /banks` | Basic | `referenceNumber` | `get_collect_banks` | `getCollectBanks` | `get_collect_banks` |
| Collection | Check USD payment status | `POST /status` | Basic | `referenceNumber, paymentCurrency` | `get_usd_payment_status` | `getUsdPaymentStatus` | `get_usd_payment_status` |
| Collection | Payment request history | `POST /history` | Basic | `referenceNumber` | `get_payment_request_history` | `getPaymentRequestHistory` | `get_payment_request_history` |
| Refunds | Refund or cancel | `POST /refund/v2` | Basic | `referenceNumber, refundAmount` | `refund_payment` | `refundPayment` | `refund_payment` |
| Refunds | Check refund status | `POST /status` | Basic | `referenceNumber` | `get_refund_status` | `getRefundStatus` | `get_refund_status` |
| Direct Debit | Start hosted set-up session | `POST /checkout/charge-process/start` | Basic, no hash | — | `start_direct_debit_session` | `startDirectDebitSession` | `start_direct_debit_session` |
| Direct Debit | Set up a mandate by API | `POST /paymentRequest` | Basic | `referenceNumber, amount, currency, payer.phoneNumber, payer.email` | `create_direct_debit_mandate` | `createDirectDebitMandate` | `create_direct_debit_mandate` |
| Direct Debit | Check mandate status | `POST /status` | Basic | `referenceNumber` | `get_mandate_status` | `getMandateStatus` | `get_mandate_status` |
| Direct Debit | Charge the mandate | `POST /chargeDebitMandate` | Basic | `referenceNumber, amount, accountReference` | `charge_mandate` | `chargeMandate` | `charge_mandate` |
| Direct Debit | Check charge status | `POST /getChargeMandateStatus` | Basic | `referenceNumber` | `get_charge_mandate_status` | `getChargeMandateStatus` | `get_charge_mandate_status` |
| Direct Debit | Disable a mandate | `POST /disableMandate` | Basic | `referenceNumber, accountReference` | `disable_mandate` | `disableMandate` | `disable_mandate` |
| Money Transfer | List institutions | `POST /getBanks` | Headers | `referenceNumber` | `get_banks` | `getBanks` | `get_banks` |
| Money Transfer | Validate the account | `POST /validateDepositToBank` | Headers | `referenceNumber, amount, destinationBankUUID, destinationBankAccountNumber` | `validate_deposit_to_bank` | `validateDepositToBank` | `validate_deposit_to_bank` |
| Money Transfer | Send money to a bank account | `POST /depositToBank` | Headers | `referenceNumber, amount, destinationBankUUID, destinationBankAccountNumber` | `send_money` | `sendMoney` | `send_money` |
| Money Transfer | Send money to a Paga wallet | `POST /moneyTransfer` | Headers | `referenceNumber, amount, destinationAccount` | `transfer_to_paga_wallet` | `transferToPagaWallet` | `transfer_to_paga_wallet` |
| Money Transfer | Validate a Paga wallet transfer | `POST /validateMoneyTransfer` | Headers | `referenceNumber, amount, destinationAccount` | `validate_money_transfer` | `validateMoneyTransfer` | `validate_money_transfer` |
| Money Transfer | Bulk money transfer | `POST /moneyTransferBulk` | Headers | `referenceNumber, amount, destinationAccount, itemCount` | `send_bulk_money_transfer` | `sendBulkMoneyTransfer` | `send_bulk_money_transfer` |
| Status | Check the transaction status | `POST /transactionStatus` | Headers | `referenceNumber` | `get_transaction_status` | `getTransactionStatus` | `get_transaction_status` |
| Airtime | List operators | `POST /getMobileOperators` | Headers | `referenceNumber` | `get_mobile_operators` | `getMobileOperators` | `get_mobile_operators` |
| Airtime | List data bundles | `POST /getDataBundleByOperator` | Headers | `referenceNumber, operatorPublicId` | `get_data_bundles` | `getDataBundles` | `get_data_bundles` |
| Airtime | Buy airtime or data | `POST /airtimePurchase` | Headers | `referenceNumber, amount, destinationPhoneNumber` | `buy_airtime` | `buyAirtime` | `buy_airtime` |
| Bill payment | List billers | `POST /getMerchants` | Headers | `referenceNumber` | `get_merchants` | `getMerchants` | `get_merchants` |
| Bill payment | List a biller's services | `POST /getMerchantServices` | Headers | `referenceNumber, merchantPublicId` | `get_merchant_services` | `getMerchantServices` | `get_merchant_services` |
| Bill payment | Validate the customer | `POST /getMerchantAccountDetails` | Headers | `referenceNumber, merchantAccount, merchantReferenceNumber, merchantServiceProductCode` | `get_merchant_account_details` | `getMerchantAccountDetails` | `get_merchant_account_details` |
| Bill payment | Pay the bill | `POST /merchantPayment` | Headers | `referenceNumber, amount, merchantAccount, merchantReferenceNumber` | `pay_bill` | `payBill` | `pay_bill` |
| Business account | Check balance | `POST /accountBalance` | Headers | `referenceNumber` | `get_business_balance` | `getBusinessBalance` | `get_business_balance` |
| Business account | Transaction history | `POST /transactionHistory` | Headers | `referenceNumber` | `get_business_transactions` | `getBusinessTransactions` | `get_business_transactions` |
| Business account | Recent transactions | `POST /recentTransactionHistory` | Headers | `referenceNumber` | `get_recent_transactions` | `getRecentTransactions` | `get_recent_transactions` |
| Business account | Operation status | `POST /getOperationStatus` | Headers | `referenceNumber` | `get_operation_status` | `getOperationStatus` | `get_operation_status` |
| Business account | Onboard a merchant | `POST /onboardMerchant` | Headers | `referenceNumber, merchantExternalId, name, phone, email` | `onboard_merchant` | `onboardMerchant` | `onboard_merchant` |
| Business account | Dispense cash | `POST /dispenseCash` | Headers | `referenceNumber, customerPhoneNumber, amount, withdrawalCode` | `dispense_cash` | `dispenseCash` | `dispense_cash` |
| Subsidiary accounts | Create an account | `POST /subsidiary-accounts` | Basic | `referenceNumber, accountReference, iifiNumber, autoSweep.bankPublicId, autoSweep.destination, autoSweep.accountNumber, callbackUrl` | `create_subsidiary_account` | `createSubsidiaryAccount` | `create_subsidiary_account` |
| Subsidiary accounts | Charge an account | `POST /subsidiary-accounts/{accountReference}/charge` | Basic | `referenceNumber, amount, currency, narration` | `charge_subsidiary_account` | `chargeSubsidiaryAccount` | `charge_subsidiary_account` |
| Subsidiary accounts | Top up an account | `POST /subsidiary-accounts/{accountReference}/topup` | Basic | `referenceNumber, amount, currency, narration` | `top_up_subsidiary_account` | `topUpSubsidiaryAccount` | `top_up_subsidiary_account` |
| Subsidiary accounts | Transfer between accounts | `POST /subsidiary-accounts/transfer` | Basic | `referenceNumber, sourceAccountIdentifier, destinationAccountIdentifier, amount, currency, narration` | `transfer_between_subsidiary_accounts` | `transferBetweenSubsidiaryAccounts` | `transfer_between_subsidiary_accounts` |
| Subsidiary accounts | Retrieve an account | `GET /subsidiary-accounts/{accountReference}` | Basic | `referenceNumber, accountIdentifier` | `retrieve_subsidiary_account` | `retrieveSubsidiaryAccount` | `retrieve_subsidiary_account` |
| Subsidiary accounts | Update an account | `PUT /subsidiary-accounts/{accountReference}` | Basic | `referenceNumber, accountIdentifier, iifiNumber, autoSweep.destination, autoSweep.bankPublicId, autoSweep.accountNumber, callbackUrl` | `update_subsidiary_account` | `updateSubsidiaryAccount` | `update_subsidiary_account` |
| Subsidiary accounts | Get the balance | `GET /subsidiary-accounts/{accountReference}/balance` | Basic | `referenceNumber, accountIdentifier` | `get_subsidiary_balance` | `getSubsidiaryBalance` | `get_subsidiary_balance` |
| Subsidiary accounts | Get transaction history | `GET /subsidiary-accounts/{accountReference}/history` | Basic | `accountIdentifier, startDateTimeUTC, endDateTimeUTC` | `get_subsidiary_history` | `getSubsidiaryHistory` | `get_subsidiary_history` |
| Persistent accounts | Register | `POST /registerPersistentPaymentAccount` | Basic | `referenceNumber, accountReference, financialIdentificationNumber, creditBankId, creditBankAccountNumber, callbackUrl` | `register_persistent_payment_account` | `registerPersistentPaymentAccount` | `register_persistent_payment_account` |
| Persistent accounts | Update | `POST /updatePersistentPaymentAccount` | Basic | `referenceNumber, accountIdentifier, financialIdentificationNumber, creditBankId, creditBankAccountNumber, callbackUrl` | `update_persistent_payment_account` | `updatePersistentPaymentAccount` | `update_persistent_payment_account` |
| Persistent accounts | Get | `POST /getPersistentPaymentAccount` | Basic | `referenceNumber, accountIdentifier` | `get_persistent_payment_account` | `getPersistentPaymentAccount` | `get_persistent_payment_account` |
| Persistent accounts | Delete | `POST /deletePersistentPaymentAccount` | Basic | `referenceNumber, accountIdentifier` | `delete_persistent_payment_account` | `deletePersistentPaymentAccount` | `delete_persistent_payment_account` |
| Customers | Register | `POST /registerCustomer` | Headers | `referenceNumber, customerPhoneNumber, customerFirstName, customerLastName` | `register_customer` | `registerCustomer` | `register_customer` |
| Customers | Register with KYC | `POST /registerCustomerWithKYC` | Headers, multipart | `referenceNumber, customerPhoneNumber, customerFirstName, customerLastName` | `register_customer_with_kyc` | `registerCustomerWithKyc` | `register_customer_with_kyc` |
| Customers | Upload account photo | `POST /registerCustomerAccountPhoto` | Headers, multipart | `referenceNumber, customerPhoneNumber` | `register_customer_account_photo` | `registerCustomerAccountPhoto` | `register_customer_account_photo` |
| Customers | Upload identification | `POST /registerCustomerIdentification` | Headers, multipart | `referenceNumber, customerPhoneNumber, customerIdType, customerIdNumber, customerIdExpirationDate` | `register_customer_identification` | `registerCustomerIdentification` | `register_customer_identification` |

**Auth** is `Basic` for the Collect API (HTTP Basic plus a `hash` header) and
`Headers` for the Business API (`principal` and `credentials` headers plus a
`hash` header).

## Webhooks

| Callback | Signed fields | Python | TypeScript | Rust |
|---|---|---|---|---|
| Checkout payment notification | `amount, timeStamp, paymentReference` | `verify_checkout_notification` | `verifyCheckoutNotification` | `verify_checkout_notification` |
| Dynamic virtual account callback | `notificationId, statusCode, externalReferenceNumber, state, outstandingBalance` | `verify_payment_callback` | `verifyPaymentCallback` | `verify_payment_callback` |
| Subsidiary funding notification | `transactionReference, transactionDate, amount, accountNumber, timestamp` | `verify_funding_notification` | `verifyFundingNotification` | `verify_funding_notification` |
| Subsidiary charge / top-up / transfer callback | `externalReferenceNumber, transactionDate, amount, accountNumber` | `verify_subsidiary_operation` | `verifySubsidiaryOperation` | `verify_subsidiary_operation` |
| Money transfer notification | `referenceNumber, transactionDate, transactionId, amount, sessionId` | `verify_money_transfer_notification` | `verifyMoneyTransferNotification` | `verify_money_transfer_notification` |
| Persistent payment account callback | `statusCode, accountNumber, amount, clearingFeeAmount, transferFeeAmount` | `verify_persistent_payment_account_callback` | `verifyPersistentPaymentAccountCallback` | `verify_persistent_payment_account_callback` |
| Direct Debit mandate callback | `statusCode, timeStamp, accountNumber, bankName, referenceNumber, mandateStatus` | `verify_mandate_callback` | `verifyMandateCallback` | `verify_mandate_callback` |
| Direct Debit charge callback | `statusCode, referenceNumber, accountReference, amount` | `verify_charge_callback` | `verifyChargeCallback` | `verify_charge_callback` |
| USD (ACH, Wire, Swift) payment | *(no signature)* | `parse_usd_payment_webhook` | `parseUsdPaymentWebhook` | `parse_usd_payment_webhook` |

## Shared test fixtures

`fixtures/hash_vectors.json` holds the hash vectors all three SDKs are tested
against. The digests are generated outside the SDKs
(`printf '%s' "$message" | sha512sum`), so they pin byte-level behaviour
rather than merely confirming each SDK agrees with itself.

Each SDK repository carries a copy under `tests/fixtures/`; this file is the
canonical one. When it changes, copy it to all three:

```bash
for sdk in paga-python paga-ts paga-rs; do
  cp fixtures/hash_vectors.json "$sdk/tests/fixtures/hash_vectors.json"
done
```

## Not yet implemented

These are documented by Paga but not wrapped yet:

- The business transaction **file download** (the CSV export). The operation
  is referenced from the transaction history page, but its endpoint and auth
  are not published.
- **Become a biller** — the merchant onboarding flow beyond
  `POST /onboardMerchant`.
