"""Author the Paga SDK documentation dataset.

This is a one-off authoring script: it produces the committed JSON in
paga/data/. The JSON is the source of truth from then on.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


# --------------------------------------------------------------------------- #
# The operations                                                            #
# --------------------------------------------------------------------------- #

OPERATIONS: list[dict] = []


def op(
    id: str,
    section: str,
    name: str,
    operation: str,
    endpoint: str,
    api: str,
    auth: str,
    hash_fields: list[str],
    description: str,
    notes: list[str],
    python: tuple[str, str],
    typescript: tuple[str, str],
    rust: tuple[str, str],
) -> None:
    OPERATIONS.append(
        {
            "id": id,
            "section": section,
            "name": name,
            "operation": operation,
            "endpoint": endpoint,
            "api": api,
            "auth": auth,
            "hashFields": hash_fields,
            "description": description,
            "notes": notes,
            "languages": {
                "python": {"method": python[0], "example": code(python[1])},
                "typescript": {"method": typescript[0], "example": code(typescript[1])},
                "rust": {"method": rust[0], "example": code(rust[1])},
            },
        }
    )


# --------------------------------------------------------------------------- #
# Checkout                                                                   #
# --------------------------------------------------------------------------- #

op(
    "verify-charge",
    "checkout",
    "Verify a charge",
    "Checkout - Verify a charge",
    "POST /checkout/transaction/verify",
    "collect",
    "basic",
    [],
    "Confirms a Checkout payment from your server at any time, using its "
    "`paymentReference`. Uses HTTP Basic only — it sends no `hash` header.",
    [
        "`status_code` `0` means paid, `2` means pending.",
        "A pending charge is a legitimate answer, so the response is returned rather than raised.",
    ],
    (
        "verify_charge",
        """
        verified = await client.verify_charge(
            payment_reference="PAY-2026-0311",
            public_key="YOUR_PUBLIC_KEY",
            amount=50,
        )
        if verified.status_code == 0:
            print("paid")
        """,
    ),
    (
        "verifyCharge",
        """
        const verified = await client.verifyCharge({
          paymentReference: "PAY-2026-0311",
          publicKey: "YOUR_PUBLIC_KEY",
          amount: 50,
        });
        if (verified.status_code === 0) {
          console.log("paid");
        }
        """,
    ),
    (
        "verify_charge",
        """
        let verified = client
            .verify_charge("PAY-2026-0311", "YOUR_PUBLIC_KEY", 50.0)
            .await?;
        if verified.status_code == Some(0) {
            println!("paid");
        }
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Collection                                                                 #
# --------------------------------------------------------------------------- #

op(
    "create-payment",
    "collection",
    "Create a payment request",
    "Dynamic virtual account - Create a payment request",
    "POST /paymentRequest",
    "collect",
    "basic",
    ["referenceNumber", "amount", "currency", "payer.phoneNumber", "payer.email"],
    "Creates a payment request. The customer pays via the payment methods you "
    "send, and Paga calls your callback when the payment completes.",
    [
        "The same operation serves the Bank USSD, Paga wallet and USD bank "
        "transfer flows — pick the flow with `paymentMethods`.",
        "`payer.email` takes part in the hash even when you omit it.",
    ],
    (
        "create_payment",
        """
        payment = await client.create_payment(
            reference_number="ORD-2026-0187",
            amount=50,
            payer_name="Bello Ramon",
            payer_phone_number="08064343187",
            payee_name="Your business name",
            payer_email="customer@example.com",
            call_back_url="https://yourstore.com/webhooks/paga",
            payment_methods=["BANK_TRANSFER"],
        )
        """,
    ),
    (
        "createPayment",
        """
        const payment = await client.createPayment({
          referenceNumber: "ORD-2026-0187",
          amount: 50,
          payerName: "Bello Ramon",
          payerPhoneNumber: "08064343187",
          payeeName: "Your business name",
          payerEmail: "customer@example.com",
          callBackUrl: "https://yourstore.com/webhooks/paga",
          paymentMethods: ["BANK_TRANSFER"],
        });
        """,
    ),
    (
        "create_payment",
        """
        let payment = client
            .create_payment(CreatePayment::new(
                "ORD-2026-0187",
                50.0,
                "Bello Ramon",
                "08064343187",
                "Your business name",
            ))
            .await?;
        """,
    ),
)

op(
    "get-payment-status",
    "collection",
    "Check payment status",
    "Dynamic virtual account - Check payment status",
    "POST /status",
    "collect",
    "basic",
    ["referenceNumber"],
    "Returns the status of a payment request. The outer `statusCode` only says "
    "whether the status request worked; the payment's own status is in "
    "`data.statusCode`.",
    ["`data.statusCode` of `\"0\"` means the payment was paid."],
    (
        "get_payment_status",
        """
        status = await client.get_payment_status(reference_number="ORD-2026-0187")
        if status.data and status.data.statusCode == "0":
            print("paid")
        """,
    ),
    (
        "getPaymentStatus",
        """
        const status = await client.getPaymentStatus({
          referenceNumber: "ORD-2026-0187",
        });
        if (status.data?.statusCode === "0") {
          console.log("paid");
        }
        """,
    ),
    (
        "get_payment_status",
        """
        let status = client.get_payment_status("ORD-2026-0187").await?;
        if status.data.as_ref().and_then(|d| d.status_code.as_deref()) == Some("0") {
            println!("paid");
        }
        """,
    ),
)

op(
    "get-collect-banks",
    "collection",
    "List the customer's banks",
    "Bank USSD - Get the customer's bank",
    "POST /banks",
    "collect",
    "basic",
    ["referenceNumber"],
    "Lists the banks available for a Bank USSD payment. Send a bank's `uuid` as "
    "`payer.bankId` when creating a payment request, or as "
    "`autoSweep.bankPublicId` for subsidiary accounts.",
    [],
    (
        "get_collect_banks",
        """
        banks = await client.get_collect_banks(reference_number="REF-000001")
        for bank in banks.banks or []:
            print(bank.name, bank.uuid)
        """,
    ),
    (
        "getCollectBanks",
        """
        const banks = await client.getCollectBanks({ referenceNumber: "REF-000001" });
        for (const bank of banks.banks ?? []) {
          console.log(bank.name, bank.uuid);
        }
        """,
    ),
    (
        "get_collect_banks",
        """
        let banks = client.get_collect_banks("REF-000001").await?;
        for bank in banks.banks.unwrap_or_default() {
            println!("{:?} {:?}", bank.name, bank.uuid);
        }
        """,
    ),
)

op(
    "get-usd-payment-status",
    "collection",
    "Check USD payment status",
    "Bank transfer (ACH, Wire and Swift) - Check payment status",
    "POST /status",
    "collect",
    "basic",
    ["referenceNumber", "paymentCurrency"],
    "Returns the status of a USD payment request. Unlike the other `/status` "
    "operations, this one signs the currency as well as the reference number.",
    ["`data.statusCode` of `\"1\"` means the payment is still pending."],
    (
        "get_usd_payment_status",
        """
        status = await client.get_usd_payment_status(
            reference_number="ORD-2026-0187",
            payment_currency="USD",
        )
        """,
    ),
    (
        "getUsdPaymentStatus",
        """
        const status = await client.getUsdPaymentStatus({
          referenceNumber: "ORD-2026-0187",
          paymentCurrency: "USD",
        });
        """,
    ),
    (
        "get_usd_payment_status",
        """
        let status = client
            .get_usd_payment_status("ORD-2026-0187", "USD")
            .await?;
        """,
    ),
)

op(
    "get-payment-request-history",
    "collection",
    "Payment request history",
    "Collect API - Payment request history",
    "POST /history",
    "collect",
    "basic",
    ["referenceNumber"],
    "Returns the history of your payment requests.",
    [],
    (
        "get_payment_request_history",
        """
        history = await client.get_payment_request_history(reference_number="REF-000001")
        """,
    ),
    (
        "getPaymentRequestHistory",
        """
        const history = await client.getPaymentRequestHistory({
          referenceNumber: "REF-000001",
        });
        """,
    ),
    (
        "get_payment_request_history",
        """
        let history = client.get_payment_request_history("REF-000001").await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Refunds                                                                     #
# --------------------------------------------------------------------------- #

op(
    "refund-payment",
    "refunds",
    "Refund or cancel a payment request",
    "Refunds - Refund or cancel a payment request",
    "POST /refund/v2",
    "collect",
    "basic",
    ["referenceNumber", "refundAmount"],
    "Refunds a paid payment request in full or in part, or cancels one that "
    "has not been paid.",
    [
        "Send one request per partial refund, each with its own `referenceNumber`.",
        "Reusing a `referenceNumber` returns status code `102` and never refunds twice.",
    ],
    (
        "refund_payment",
        """
        refund = await client.refund_payment(
            reference_number="RFD-2026-0031",
            payment_request_reference="ORD-2026-0187",
            refund_amount=50,
            reason="Item out of stock",
        )
        """,
    ),
    (
        "refundPayment",
        """
        const refund = await client.refundPayment({
          referenceNumber: "RFD-2026-0031",
          paymentRequestReference: "ORD-2026-0187",
          refundAmount: 50,
          reason: "Item out of stock",
        });
        """,
    ),
    (
        "refund_payment",
        """
        let refund = client
            .refund_payment(RefundPayment::new("RFD-2026-0031", "ORD-2026-0187", 50.0))
            .await?;
        """,
    ),
)

op(
    "get-refund-status",
    "refunds",
    "Check refund status",
    "Refunds - Check refund status",
    "POST /status",
    "collect",
    "basic",
    ["referenceNumber"],
    "Checks whether a payment request was refunded. Call it with the **original** "
    "payment request's `referenceNumber`, not the refund's.",
    ["`data.refundStatus` becomes `\"refunded\"` once the refund is made."],
    (
        "get_refund_status",
        """
        status = await client.get_refund_status(reference_number="ORD-2026-0187")
        if status.isRefunded:
            print("refunded")
        """,
    ),
    (
        "getRefundStatus",
        """
        const status = await client.getRefundStatus({
          referenceNumber: "ORD-2026-0187",
        });
        if (status.data?.refundStatus === "refunded") {
          console.log("refunded");
        }
        """,
    ),
    (
        "get_refund_status",
        """
        let status = client.get_refund_status("ORD-2026-0187").await?;
        if status.is_refunded() {
            println!("refunded");
        }
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Direct Debit                                                                #
# --------------------------------------------------------------------------- #

op(
    "start-direct-debit-session",
    "direct-debit",
    "Start a hosted set-up session",
    "Direct Debit - Start a hosted set-up session",
    "POST /checkout/charge-process/start",
    "collect",
    "basic",
    [],
    "Creates a hosted session and returns the `checkoutUrl` to redirect your "
    "customer to. This endpoint uses HTTP Basic only — it sends no `hash` header.",
    ["The session expiry and payment expiry are strings of seconds."],
    (
        "start_direct_debit_session",
        """
        session = await client.start_direct_debit_session(
            reference_number="DD-2026-0001",
            account_reference="CUST-000184-WALLET",
            amount_limit=50000,
            callback_url="https://yourstore.com/webhooks/mandate",
        )
        print(session.checkoutUrl)
        """,
    ),
    (
        "startDirectDebitSession",
        """
        const session = await client.startDirectDebitSession({
          referenceNumber: "DD-2026-0001",
          accountReference: "CUST-000184-WALLET",
          amountLimit: 50000,
          callbackUrl: "https://yourstore.com/webhooks/mandate",
        });
        console.log(session.data?.checkoutUrl);
        """,
    ),
    (
        "start_direct_debit_session",
        """
        let session = client
            .start_direct_debit_session(StartDirectDebitSession::new(
                "DD-2026-0001",
                "CUST-000184-WALLET",
                50_000.0,
                "https://yourstore.com/webhooks/mandate",
            ))
            .await?;
        """,
    ),
)

op(
    "create-direct-debit-mandate",
    "direct-debit",
    "Set up a mandate by API",
    "Direct Debit - Set up a mandate by API",
    "POST /paymentRequest",
    "collect",
    "basic",
    ["referenceNumber", "amount", "currency", "payer.phoneNumber", "payer.email"],
    "Creates a payment request with `paymentMethods` set to `[\"DIRECT_DEBIT\"]`, "
    "so the customer authorises you to debit their bank account.",
    [
        "The authorisation transfer must come from mobile banking, internet banking or a branch — not from POS, USSD or ATM.",
        "`payerCollectionFeeShare` and `payeeCollectionFeeShare` must sum to 1.0.",
    ],
    (
        "create_direct_debit_mandate",
        """
        mandate = await client.create_direct_debit_mandate(
            reference_number="DD-2026-0001",
            amount=5000,
            payer_name="Bello Ramon",
            payer_phone_number="08064343187",
            payee_name="Your business name",
            account_reference="CUST-000184-WALLET",
            payer_email="customer@example.com",
            call_back_url="https://yourstore.com/webhooks/mandate",
        )
        """,
    ),
    (
        "createDirectDebitMandate",
        """
        const mandate = await client.createDirectDebitMandate({
          referenceNumber: "DD-2026-0001",
          amount: 5000,
          payerName: "Bello Ramon",
          payerPhoneNumber: "08064343187",
          payeeName: "Your business name",
          accountReference: "CUST-000184-WALLET",
          payerEmail: "customer@example.com",
          callBackUrl: "https://yourstore.com/webhooks/mandate",
        });
        """,
    ),
    (
        "create_direct_debit_mandate",
        """
        let mandate = client
            .create_direct_debit_mandate(CreateDirectDebitMandate::new(
                "DD-2026-0001",
                5000.0,
                "Bello Ramon",
                "08064343187",
                "Your business name",
                "CUST-000184-WALLET",
            ))
            .await?;
        """,
    ),
)

op(
    "get-mandate-status",
    "direct-debit",
    "Check mandate status",
    "Direct Debit - Check mandate status",
    "POST /status",
    "collect",
    "basic",
    ["referenceNumber"],
    "Returns a mandate's status.",
    [
        "`data.statusCode` stays `\"1\"` / `\"pending\"` forever — it tells you nothing.",
        "Read `data.additionalData.mandate[].ProcessStatusId` instead: `PENDING`, `VERIFIED`, `APPROVED` or `REJECTED`. Charge only when it is `APPROVED`.",
    ],
    (
        "get_mandate_status",
        """
        status = await client.get_mandate_status(reference_number="DD-2026-0001")
        if status.isApproved:
            print("ready to charge")
        """,
    ),
    (
        "getMandateStatus",
        """
        const status = await client.getMandateStatus({
          referenceNumber: "DD-2026-0001",
        });
        if (status.data?.additionalData?.mandate?.[0]?.ProcessStatusId === "APPROVED") {
          console.log("ready to charge");
        }
        """,
    ),
    (
        "get_mandate_status",
        """
        let status = client.get_mandate_status("DD-2026-0001").await?;
        if status.is_approved() {
            println!("ready to charge");
        }
        """,
    ),
)

op(
    "charge-mandate",
    "direct-debit",
    "Charge the mandate",
    "Direct Debit - Charge the mandate",
    "POST /chargeDebitMandate",
    "collect",
    "basic",
    ["referenceNumber", "amount", "accountReference"],
    "Debits an approved mandate for any amount up to its limit.",
    [
        "A successful response means the charge was **accepted**, not completed — fulfil only once the charge callback confirms it.",
    ],
    (
        "charge_mandate",
        """
        charge = await client.charge_mandate(
            reference_number="DD-CHARGE-0001",
            amount=600,
            account_reference="CUST-000184-WALLET",
        )
        """,
    ),
    (
        "chargeMandate",
        """
        const charge = await client.chargeMandate({
          referenceNumber: "DD-CHARGE-0001",
          amount: 600,
          accountReference: "CUST-000184-WALLET",
        });
        """,
    ),
    (
        "charge_mandate",
        """
        let charge = client
            .charge_mandate(ChargeMandate::new(
                "DD-CHARGE-0001",
                600.0,
                "CUST-000184-WALLET",
            ))
            .await?;
        """,
    ),
)

op(
    "get-charge-mandate-status",
    "direct-debit",
    "Check charge status",
    "Direct Debit - Check charge status",
    "POST /getChargeMandateStatus",
    "collect",
    "basic",
    ["referenceNumber"],
    "Returns the status of a mandate charge, using the charge's own "
    "`referenceNumber`.",
    [
        "`data.statusCode` is `0` charged, `1` pending, `-1` invalid and `-4` unknown.",
    ],
    (
        "get_charge_mandate_status",
        """
        status = await client.get_charge_mandate_status(reference_number="DD-CHARGE-0001")
        if status.chargeStatus == 0:
            print("charged")
        """,
    ),
    (
        "getChargeMandateStatus",
        """
        const status = await client.getChargeMandateStatus({
          referenceNumber: "DD-CHARGE-0001",
        });
        if (status.data?.statusCode === 0) {
          console.log("charged");
        }
        """,
    ),
    (
        "get_charge_mandate_status",
        """
        let status = client.get_charge_mandate_status("DD-CHARGE-0001").await?;
        if status.charge_status() == Some(0) {
            println!("charged");
        }
        """,
    ),
)

op(
    "disable-mandate",
    "direct-debit",
    "Disable a mandate",
    "Direct Debit - Disable a mandate",
    "POST /disableMandate",
    "collect",
    "basic",
    ["referenceNumber", "accountReference"],
    "Stops all future charges on a mandate. Its `ProcessStatusId` then becomes "
    "`REJECTED`, and it can never be charged again.",
    [],
    (
        "disable_mandate",
        """
        await client.disable_mandate(
            reference_number="DD-DIS-0001",
            account_reference="CUST-000184-WALLET",
        )
        """,
    ),
    (
        "disableMandate",
        """
        await client.disableMandate({
          referenceNumber: "DD-DIS-0001",
          accountReference: "CUST-000184-WALLET",
        });
        """,
    ),
    (
        "disable_mandate",
        """
        client
            .disable_mandate(DisableMandate::new(
                "DD-DIS-0001",
                "CUST-000184-WALLET",
            ))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Money transfer                                                              #
# --------------------------------------------------------------------------- #

op(
    "get-banks",
    "money-transfer",
    "List institutions you can pay",
    "Money transfer - Get the bank's UUID",
    "POST /getBanks",
    "business",
    "headers",
    ["referenceNumber"],
    "Lists every institution money can be sent to, with the `uuid` you send as "
    "`destinationBankUUID`.",
    [
        "UUIDs never change, but new institutions are added every month — cache the list and refresh it weekly or monthly.",
        "To send to a Paga wallet, use Paga's UUID `AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA`.",
    ],
    (
        "get_banks",
        """
        banks = await client.get_banks(reference_number="REF-000001")
        for bank in banks.banks or []:
            print(bank.name, bank.uuid)
        """,
    ),
    (
        "getBanks",
        """
        const banks = await client.getBanks({ referenceNumber: "REF-000001" });
        for (const bank of banks.banks ?? []) {
          console.log(bank.name, bank.uuid);
        }
        """,
    ),
    (
        "get_banks",
        """
        let banks = client.get_banks("REF-000001").await?;
        for bank in banks.banks.unwrap_or_default() {
            println!("{:?} {:?}", bank.name, bank.uuid);
        }
        """,
    ),
)

op(
    "validate-deposit-to-bank",
    "money-transfer",
    "Validate the destination account",
    "Money transfer - Validate the account",
    "POST /validateDepositToBank",
    "business",
    "headers",
    ["referenceNumber", "amount", "destinationBankUUID", "destinationBankAccountNumber"],
    "Confirms the account exists and returns the account holder's name and the "
    "fee, before any money moves.",
    ["Send `amount` exactly as you will send it later: `\"5000.00\"` and `\"5000\"` sign differently."],
    (
        "validate_deposit_to_bank",
        """
        validation = await client.validate_deposit_to_bank(
            reference_number="REF-000002",
            amount="5000.00",
            destination_bank_uuid="40090E2F-7446-4217-9345-7BBAB7043C4C",
            destination_bank_account_number="0000000000",
        )
        print(validation.destinationAccountHolderNameAtBank, validation.fee)
        """,
    ),
    (
        "validateDepositToBank",
        """
        const validation = await client.validateDepositToBank({
          referenceNumber: "REF-000002",
          amount: "5000.00",
          destinationBankUUID: "40090E2F-7446-4217-9345-7BBAB7043C4C",
          destinationBankAccountNumber: "0000000000",
        });
        console.log(validation.destinationAccountHolderNameAtBank, validation.fee);
        """,
    ),
    (
        "validate_deposit_to_bank",
        """
        let validation = client
            .validate_deposit_to_bank(ValidateDepositToBank::new(
                "REF-000002",
                "5000.00",
                "40090E2F-7446-4217-9345-7BBAB7043C4C",
                "0000000000",
            ))
            .await?;
        """,
    ),
)

op(
    "send-money",
    "money-transfer",
    "Send money to a bank account",
    "Money transfer - Send the money",
    "POST /depositToBank",
    "business",
    "headers",
    ["referenceNumber", "amount", "destinationBankUUID", "destinationBankAccountNumber"],
    "Sends money from the business balance to a bank account, or to a Paga "
    "wallet using Paga's UUID.",
    [
        "Send `amount` as a string (e.g. `\"5000.00\"`) — it is signed verbatim.",
        "There is no callback for the outcome; use the transaction status endpoint.",
    ],
    (
        "send_money",
        """
        transfer = await client.send_money(
            reference_number="PAY-2026-0311",
            amount="5000.00",
            destination_bank_uuid="40090E2F-7446-4217-9345-7BBAB7043C4C",
            destination_bank_account_number="0000000000",
            remarks="Salary for June",
        )
        """,
    ),
    (
        "sendMoney",
        """
        const transfer = await client.sendMoney({
          referenceNumber: "PAY-2026-0311",
          amount: "5000.00",
          destinationBankUUID: "40090E2F-7446-4217-9345-7BBAB7043C4C",
          destinationBankAccountNumber: "0000000000",
          remarks: "Salary for June",
        });
        """,
    ),
    (
        "send_money",
        """
        let transfer = client
            .send_money(SendMoney::new(
                "PAY-2026-0311",
                "5000.00",
                "40090E2F-7446-4217-9345-7BBAB7043C4C",
                "0000000000",
            ))
            .await?;
        """,
    ),
)

op(
    "transfer-to-paga-wallet",
    "money-transfer",
    "Send money to a Paga wallet",
    "Business API - Money transfer to a Paga wallet",
    "POST /moneyTransfer",
    "business",
    "headers",
    ["referenceNumber", "amount", "destinationAccount"],
    "Sends money from the business balance to a Paga user, identified by their "
    "phone number, nickname or account number.",
    ["`referenceNumber` must be at most 50 characters."],
    (
        "transfer_to_paga_wallet",
        """
        transfer = await client.transfer_to_paga_wallet(
            reference_number="PAY-2026-0312",
            amount=5000,
            destination_account="08064343187",
        )
        """,
    ),
    (
        "transferToPagaWallet",
        """
        const transfer = await client.transferToPagaWallet({
          referenceNumber: "PAY-2026-0312",
          amount: 5000,
          destinationAccount: "08064343187",
        });
        """,
    ),
    (
        "transfer_to_paga_wallet",
        """
        let transfer = client
            .transfer_to_paga_wallet(TransferToPagaWallet::new(
                "PAY-2026-0312",
                5000.0,
                "08064343187",
            ))
            .await?;
        """,
    ),
)

op(
    "validate-money-transfer",
    "money-transfer",
    "Validate a Paga wallet transfer",
    "Business API - Validate a money transfer",
    "POST /validateMoneyTransfer",
    "business",
    "headers",
    ["referenceNumber", "amount", "destinationAccount"],
    "Confirms the recipient exists and returns their name, registration status, "
    "KYC level and the fee, before any money moves.",
    [],
    (
        "validate_money_transfer",
        """
        validation = await client.validate_money_transfer(
            reference_number="REF-000003",
            amount=5000,
            destination_account="08064343187",
        )
        print(validation.recipientAccountHolderName, validation.fee)
        """,
    ),
    (
        "validateMoneyTransfer",
        """
        const validation = await client.validateMoneyTransfer({
          referenceNumber: "REF-000003",
          amount: 5000,
          destinationAccount: "08064343187",
        });
        console.log(validation.recipientAccountHolderName, validation.fee);
        """,
    ),
    (
        "validate_money_transfer",
        """
        let validation = client
            .validate_money_transfer(ValidateMoneyTransfer::new(
                "REF-000003",
                5000.0,
                "08064343187",
            ))
            .await?;
        """,
    ),
)

op(
    "send-bulk-money-transfer",
    "money-transfer",
    "Bulk money transfer",
    "Business API - Bulk money transfer",
    "POST /moneyTransferBulk",
    "business",
    "headers",
    ["referenceNumber", "amount", "destinationAccount", "itemCount"],
    "Sends up to 300 money transfers in one call.",
    [
        "Paga hashes the **first item's** reference number, amount and destination account, followed by the total number of items — the SDK does that for you.",
        "A bulk transfer can partially succeed, so check every entry in `results`.",
    ],
    (
        "send_bulk_money_transfer",
        """
        bulk = await client.send_bulk_money_transfer(
            items=[
                {
                    "referenceNumber": "ITEM-1",
                    "amount": 100,
                    "destinationAccount": "08064343187",
                },
                {
                    "referenceNumber": "ITEM-2",
                    "amount": 200,
                    "destinationAccount": "08064343188",
                },
            ],
            bulk_reference_number="BULK-2026-0001",
        )
        """,
    ),
    (
        "sendBulkMoneyTransfer",
        """
        const bulk = await client.sendBulkMoneyTransfer({
          items: [
            { referenceNumber: "ITEM-1", amount: 100, destinationAccount: "08064343187" },
            { referenceNumber: "ITEM-2", amount: 200, destinationAccount: "08064343188" },
          ],
          bulkReferenceNumber: "BULK-2026-0001",
        });
        """,
    ),
    (
        "send_bulk_money_transfer",
        """
        let bulk = client
            .send_bulk_money_transfer(SendBulkMoneyTransfer::new(vec![
                BulkTransferItem::new("ITEM-1", 100.0, "08064343187"),
                BulkTransferItem::new("ITEM-2", 200.0, "08064343188"),
            ]))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Status                                                                      #
# --------------------------------------------------------------------------- #

op(
    "get-transaction-status",
    "status",
    "Check the transaction status",
    "Money transfer / Airtime / Bill payment - Check the transaction status",
    "POST /transactionStatus",
    "business",
    "headers",
    ["referenceNumber"],
    "Checks what happened to a transaction you already sent. It covers money "
    "transfers, airtime purchases and bill payments.",
    [
        "Only the last 48 hours are covered.",
        "After a timeout or an ambiguous response, wait at least 5 seconds before the first check.",
        "The `status` field is human-readable and may be reworded — branch on `responseCode`, not on `status`.",
    ],
    (
        "get_transaction_status",
        """
        status = await client.get_transaction_status(reference_number="PAY-2026-0311")
        if status.responseCode == 0:
            print("settled")
        """,
    ),
    (
        "getTransactionStatus",
        """
        const status = await client.getTransactionStatus({
          referenceNumber: "PAY-2026-0311",
        });
        if (status.responseCode === 0) {
          console.log("settled");
        }
        """,
    ),
    (
        "get_transaction_status",
        """
        let status = client
            .get_transaction_status(GetTransactionStatus::new("PAY-2026-0311"))
            .await?;
        if status.response_code == Some(0) {
            println!("settled");
        }
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Airtime and data                                                            #
# --------------------------------------------------------------------------- #

op(
    "get-mobile-operators",
    "airtime",
    "List mobile operators",
    "Airtime and data - Get the mobile operator",
    "POST /getMobileOperators",
    "business",
    "headers",
    ["referenceNumber"],
    "Lists the networks you can top up.",
    [
        "Send a network's `mobileOperatorCode` as `mobileOperatorPublicId` when buying, and as `operatorPublicId` when listing data bundles.",
        "Cache the list.",
    ],
    (
        "get_mobile_operators",
        """
        operators = await client.get_mobile_operators(reference_number="REF-000001")
        for operator in operators.mobileOperator or []:
            print(operator.name, operator.mobileOperatorCode)
        """,
    ),
    (
        "getMobileOperators",
        """
        const operators = await client.getMobileOperators({
          referenceNumber: "REF-000001",
        });
        for (const operator of operators.mobileOperator ?? []) {
          console.log(operator.name, operator.mobileOperatorCode);
        }
        """,
    ),
    (
        "get_mobile_operators",
        """
        let operators = client.get_mobile_operators("REF-000001", None).await?;
        for operator in operators.mobile_operator.unwrap_or_default() {
            println!("{:?} {:?}", operator.name, operator.mobile_operator_code);
        }
        """,
    ),
)

op(
    "get-data-bundles",
    "airtime",
    "List data bundles",
    "Airtime and data - For data, pick a bundle",
    "POST /getDataBundleByOperator",
    "business",
    "headers",
    ["referenceNumber", "operatorPublicId"],
    "Lists a network's data bundles.",
    [
        "Send a bundle's `serviceId` as `mobileOperatorServiceId` and **exactly** its `servicePrice` as `amount`.",
        "Bundles rarely change, so cache the list and refresh it monthly.",
    ],
    (
        "get_data_bundles",
        """
        bundles = await client.get_data_bundles(
            reference_number="REF-000001",
            operator_public_id="42419156-DD57-4737-8373-20678CD9AA29",
        )
        """,
    ),
    (
        "getDataBundles",
        """
        const bundles = await client.getDataBundles({
          referenceNumber: "REF-000001",
          operatorPublicId: "42419156-DD57-4737-8373-20678CD9AA29",
        });
        """,
    ),
    (
        "get_data_bundles",
        """
        let bundles = client
            .get_data_bundles(
                "REF-000001",
                "42419156-DD57-4737-8373-20678CD9AA29",
            )
            .await?;
        """,
    ),
)

op(
    "buy-airtime",
    "airtime",
    "Buy airtime or data",
    "Airtime and data - Buy the airtime or data",
    "POST /airtimePurchase",
    "business",
    "headers",
    ["referenceNumber", "amount", "destinationPhoneNumber"],
    "Tops up a phone with airtime or data from the business balance.",
    [
        "There is no callback: decide on `responseCode`, and check the transaction status if you need to.",
        "For a data bundle, `amount` must be exactly the bundle's `servicePrice`.",
    ],
    (
        "buy_airtime",
        """
        purchase = await client.buy_airtime(
            reference_number="AIR-2026-0042",
            amount="500",
            destination_phone_number="08063332187",
            mobile_operator_public_id="42419156-DD57-4737-8373-20678CD9AA29",
        )
        """,
    ),
    (
        "buyAirtime",
        """
        const purchase = await client.buyAirtime({
          referenceNumber: "AIR-2026-0042",
          amount: "500",
          destinationPhoneNumber: "08063332187",
          mobileOperatorPublicId: "42419156-DD57-4737-8373-20678CD9AA29",
        });
        """,
    ),
    (
        "buy_airtime",
        """
        let purchase = client
            .buy_airtime(BuyAirtime::new(
                "AIR-2026-0042",
                "500",
                "08063332187",
                "42419156-DD57-4737-8373-20678CD9AA29",
            ))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Bill payment                                                                #
# --------------------------------------------------------------------------- #

op(
    "get-merchants",
    "bill-payment",
    "List billers",
    "Bill payment - Find the biller",
    "POST /getMerchants",
    "business",
    "headers",
    ["referenceNumber"],
    "Lists every biller, with the `uuid` you send as `merchantAccount`. Cache the list.",
    [],
    (
        "get_merchants",
        """
        merchants = await client.get_merchants(reference_number="REF-000001")
        for merchant in merchants.merchants or []:
            print(merchant.displayName, merchant.uuid)
        """,
    ),
    (
        "getMerchants",
        """
        const merchants = await client.getMerchants({ referenceNumber: "REF-000001" });
        for (const merchant of merchants.merchants ?? []) {
          console.log(merchant.displayName, merchant.uuid);
        }
        """,
    ),
    (
        "get_merchants",
        """
        let merchants = client.get_merchants("REF-000001").await?;
        for merchant in merchants.merchants.unwrap_or_default() {
            println!("{:?} {:?}", merchant.display_name, merchant.uuid);
        }
        """,
    ),
)

op(
    "get-merchant-services",
    "bill-payment",
    "List a biller's services",
    "Bill payment - Pick the service",
    "POST /getMerchantServices",
    "business",
    "headers",
    ["referenceNumber", "merchantPublicId"],
    "Lists what a biller can be paid for.",
    [
        "No services means any amount is allowed.",
        "A service with `price` `0.0` means the customer chooses the amount; otherwise pay the service's `price`.",
    ],
    (
        "get_merchant_services",
        """
        services = await client.get_merchant_services(
            reference_number="REF-000001",
            merchant_public_id="A3878DC1-F07D-48E7-AA59-8276C3C26647",
        )
        """,
    ),
    (
        "getMerchantServices",
        """
        const services = await client.getMerchantServices({
          referenceNumber: "REF-000001",
          merchantPublicId: "A3878DC1-F07D-48E7-AA59-8276C3C26647",
        });
        """,
    ),
    (
        "get_merchant_services",
        """
        let services = client
            .get_merchant_services(
                "REF-000001",
                "A3878DC1-F07D-48E7-AA59-8276C3C26647",
            )
            .await?;
        """,
    ),
)

op(
    "get-merchant-account-details",
    "bill-payment",
    "Validate the customer",
    "Bill payment - Validate the customer",
    "POST /getMerchantAccountDetails",
    "business",
    "headers",
    [
        "referenceNumber",
        "merchantAccount",
        "merchantReferenceNumber",
        "merchantServiceProductCode",
    ],
    "Checks a meter, smart card or account number and returns the customer's name.",
    [
        "If the customer chose a service, always send its `code` as `merchantServiceProductCode`.",
        "Billers that don't need it still take part in the hash — send `\"\"` when there is no service.",
    ],
    (
        "get_merchant_account_details",
        """
        customer = await client.get_merchant_account_details(
            reference_number="REF-000001",
            merchant_account="A3878DC1-F07D-48E7-AA59-8276C3C26647",
            merchant_reference_number="8110411076",
        )
        print(customer.customerName)
        """,
    ),
    (
        "getMerchantAccountDetails",
        """
        const customer = await client.getMerchantAccountDetails({
          referenceNumber: "REF-000001",
          merchantAccount: "A3878DC1-F07D-48E7-AA59-8276C3C26647",
          merchantReferenceNumber: "8110411076",
        });
        console.log(customer.customerName);
        """,
    ),
    (
        "get_merchant_account_details",
        """
        let customer = client
            .get_merchant_account_details(
                "REF-000001",
                "A3878DC1-F07D-48E7-AA59-8276C3C26647",
                "8110411076",
                None,
            )
            .await?;
        """,
    ),
)

op(
    "pay-bill",
    "bill-payment",
    "Pay the bill",
    "Bill payment - Pay the bill",
    "POST /merchantPayment",
    "business",
    "headers",
    ["referenceNumber", "amount", "merchantAccount", "merchantReferenceNumber"],
    "Pays a bill from the business balance.",
    [
        "There is no callback: decide on `responseCode`.",
        "`integrationStatus` is for information only.",
    ],
    (
        "pay_bill",
        """
        bill = await client.pay_bill(
            reference_number="BILL-2026-0042",
            amount=6000,
            merchant_account="A3878DC1-F07D-48E7-AA59-8276C3C26647",
            merchant_reference_number="8110411076",
            merchant_service=["STARTERE36"],
        )
        if bill.responseCode == 0:
            print("paid")
        """,
    ),
    (
        "payBill",
        """
        const bill = await client.payBill({
          referenceNumber: "BILL-2026-0042",
          amount: 6000,
          merchantAccount: "A3878DC1-F07D-48E7-AA59-8276C3C26647",
          merchantReferenceNumber: "8110411076",
          merchantService: ["STARTERE36"],
        });
        if (bill.responseCode === 0) {
          console.log("paid");
        }
        """,
    ),
    (
        "pay_bill",
        """
        let bill = client
            .pay_bill(PayBill::new(
                "BILL-2026-0042",
                6000.0,
                "A3878DC1-F07D-48E7-AA59-8276C3C26647",
                "8110411076",
            ))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Business account                                                            #
# --------------------------------------------------------------------------- #

op(
    "get-business-balance",
    "business-account",
    "Check the business account balance",
    "Your business account - Check your balance",
    "POST /accountBalance",
    "business",
    "headers",
    ["referenceNumber"],
    "Returns the business account balance.",
    ["Check `availableBalance`, not `totalBalance`, before a payout run — it is what you can actually send."],
    (
        "get_business_balance",
        """
        balance = await client.get_business_balance(reference_number="BAL-2026-0042")
        print(balance.availableBalance)
        """,
    ),
    (
        "getBusinessBalance",
        """
        const balance = await client.getBusinessBalance({
          referenceNumber: "BAL-2026-0042",
        });
        console.log(balance.availableBalance);
        """,
    ),
    (
        "get_business_balance",
        """
        let balance = client.get_business_balance("BAL-2026-0042").await?;
        println!("{:?}", balance.available_balance);
        """,
    ),
)

op(
    "get-business-transactions",
    "business-account",
    "Get the transaction history",
    "Your business account - Get your transaction history",
    "POST /transactionHistory",
    "business",
    "headers",
    ["referenceNumber"],
    "Returns every transaction on the business account between two dates: money "
    "in, money out and fees, up to 10,000 at a time.",
    ["Use it to reconcile your records with Paga's."],
    (
        "get_business_transactions",
        """
        history = await client.get_business_transactions(
            reference_number="HIS-2026-0042",
            start_date_utc="2026-11-01T00:00:00",
            end_date_utc="2026-11-04T00:00:00",
        )
        """,
    ),
    (
        "getBusinessTransactions",
        """
        const history = await client.getBusinessTransactions({
          referenceNumber: "HIS-2026-0042",
          startDateUTC: "2026-11-01T00:00:00",
          endDateUTC: "2026-11-04T00:00:00",
        });
        """,
    ),
    (
        "get_business_transactions",
        """
        let history = client
            .get_business_transactions(GetBusinessTransactions::new(
                "HIS-2026-0042",
                "2026-11-01T00:00:00",
                "2026-11-04T00:00:00",
            ))
            .await?;
        """,
    ),
)

op(
    "get-recent-transactions",
    "business-account",
    "Get the recent transactions",
    "Your business account - Get your recent transactions",
    "POST /recentTransactionHistory",
    "business",
    "headers",
    ["referenceNumber"],
    "Returns the last five transactions on the business account, newest first, "
    "without a date range.",
    ["For anything further back, use the transaction history endpoint."],
    (
        "get_recent_transactions",
        """
        recent = await client.get_recent_transactions(reference_number="REF-000001")
        """,
    ),
    (
        "getRecentTransactions",
        """
        const recent = await client.getRecentTransactions({
          referenceNumber: "REF-000001",
        });
        """,
    ),
    (
        "get_recent_transactions",
        """
        let recent = client
            .get_recent_transactions(GetRecentTransactions::new("REF-000001"))
            .await?;
        """,
    ),
)

op(
    "get-operation-status",
    "business-account",
    "Check an operation's status",
    "Business API - Get an operation status",
    "POST /getOperationStatus",
    "business",
    "headers",
    ["referenceNumber"],
    "Returns the status of a business operation.",
    ["The status is in `transactionStatus`, not `status`."],
    (
        "get_operation_status",
        """
        status = await client.get_operation_status(reference_number="PAY-2026-0311")
        print(status.transactionStatus)
        """,
    ),
    (
        "getOperationStatus",
        """
        const status = await client.getOperationStatus({
          referenceNumber: "PAY-2026-0311",
        });
        console.log(status.transactionStatus);
        """,
    ),
    (
        "get_operation_status",
        """
        let status = client
            .get_operation_status(GetTransactionStatus::new("PAY-2026-0311"))
            .await?;
        println!("{:?}", status.transaction_status);
        """,
    ),
)

op(
    "onboard-merchant",
    "business-account",
    "Onboard a merchant",
    "Business API - Onboard a merchant",
    "POST /onboardMerchant",
    "business",
    "headers",
    ["referenceNumber", "merchantExternalId", "name", "phone", "email"],
    "Onboards a merchant and returns the credentials Paga issues for it.",
    [
        "For aggregators only.",
        "Paga names the request field `reference`, not `referenceNumber`.",
    ],
    (
        "onboard_merchant",
        """
        merchant = await client.onboard_merchant(
            reference="REF-000001",
            merchant_external_id="MERCH-1",
            legal_entity={"name": "Acme Ltd"},
            legal_entity_representative={
                "firstName": "Bello",
                "lastName": "Ramon",
                "phone": "08064343187",
                "email": "director@example.com",
                "dateOfBirth": "1989-10-02",
            },
            integration={
                "type": "EMAIL_NOTIFICATION",
                "financeAdminEmail": "finance@example.com",
            },
        )
        """,
    ),
    (
        "onboardMerchant",
        """
        const merchant = await client.onboardMerchant({
          reference: "REF-000001",
          merchantExternalId: "MERCH-1",
          legalEntity: { name: "Acme Ltd" },
          legalEntityRepresentative: {
            firstName: "Bello",
            lastName: "Ramon",
            phone: "080643643187",
            email: "director@example.com",
            dateOfBirth: "1989-10-02",
          },
          integration: {
            type: "EMAIL_NOTIFICATION",
            financeAdminEmail: "finance@example.com",
          },
        });
        """,
    ),
    (
        "onboard_merchant",
        """
        let merchant = client
            .onboard_merchant(OnboardMerchant::new(
                "REF-000001",
                "MERCH-1",
                serde_json::json!({ "name": "Acme Ltd" }),
                serde_json::json!({
                    "firstName": "Bello",
                    "lastName": "Ramon",
                    "phone": "08064343187",
                    "email": "director@example.com",
                    "dateOfBirth": "1989-10-02",
                }),
                serde_json::json!({
                    "type": "EMAIL_NOTIFICATION",
                    "financeAdminEmail": "finance@example.com",
                }),
            ))
            .await?;
        """,
    ),
)

op(
    "dispense-cash",
    "business-account",
    "Dispense cash",
    "Business API - Dispense cash",
    "POST /dispenseCash",
    "business",
    "headers",
    ["referenceNumber", "customerPhoneNumber", "amount", "withdrawalCode"],
    "Dispenses cash against a customer's withdrawal code.",
    [],
    (
        "dispense_cash",
        """
        cash = await client.dispense_cash(
            reference_number="CASH-2026-0042",
            customer_phone_number="08064343187",
            amount=5000,
            withdrawal_code="123456",
        )
        """,
    ),
    (
        "dispenseCash",
        """
        const cash = await client.dispenseCash({
          referenceNumber: "CASH-2026-0042",
          customerPhoneNumber: "08064343187",
          amount: 5000,
          withdrawalCode: "123456",
        });
        """,
    ),
    (
        "dispense_cash",
        """
        let cash = client
            .dispense_cash(DispenseCash::new(
                "CASH-2026-0042",
                "08064343187",
                5000.0,
                "123456",
            ))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Subsidiary accounts                                                         #
# --------------------------------------------------------------------------- #

op(
    "create-subsidiary-account",
    "subsidiary",
    "Create a subsidiary account",
    "Subsidiary Accounts - Create an account",
    "POST /subsidiary-accounts",
    "collect",
    "basic",
    [
        "referenceNumber",
        "accountReference",
        "iifiNumber",
        "autoSweep.bankPublicId",
        "autoSweep.destination",
        "autoSweep.accountNumber",
        "callbackUrl",
    ],
    "Creates a Paga account for one of your customers.",
    [
        "Leave out `autoSweep` for a ledger-backed account that holds funds; set `autoSweep.destination` to `VIRTUAL_ACCOUNT` or `BANK` for a virtual account that settles straight away.",
        "Reusing a `referenceNumber` or `accountReference` returns status code `102` and never creates a second account.",
    ],
    (
        "create_subsidiary_account",
        """
        account = await client.create_subsidiary_account(
            reference_number="REF-000005",
            account_reference="CUST-000184-WALLET",
            account_name="Bello Ramon",
            iifi_number="22222132329",
            callback_url="https://yourstore.com/webhooks/paga",
        )
        if account.statusCode == "102":
            print("duplicate reference")
        """,
    ),
    (
        "createSubsidiaryAccount",
        """
        const account = await client.createSubsidiaryAccount({
          referenceNumber: "REF-000005",
          accountReference: "CUST-000184-WALLET",
          accountName: "Bello Ramon",
          iifiNumber: "22222132329",
          callbackUrl: "https://yourstore.com/webhooks/paga",
        });
        if (account.statusCode === "102") {
          console.log("duplicate reference");
        }
        """,
    ),
    (
        "create_subsidiary_account",
        """
        let account = client
            .create_subsidiary_account(CreateSubsidiaryAccount::new(
                "REF-000005",
                "CUST-000184-WALLET",
                "Bello Ramon",
            ))
            .await?;
        """,
    ),
)

op(
    "charge-subsidiary-account",
    "subsidiary",
    "Charge a subsidiary account",
    "Subsidiary Accounts - Charge an account",
    "POST /subsidiary-accounts/{accountReference}/charge",
    "collect",
    "basic",
    ["referenceNumber", "amount", "currency", "narration"],
    "Debits a ledger-backed subsidiary account.",
    [
        "Not available on virtual accounts.",
        "Retrying with the same `referenceNumber` never moves money twice.",
    ],
    (
        "charge_subsidiary_account",
        """
        charge = await client.charge_subsidiary_account(
            account_reference="CUST-000184-WALLET",
            reference_number="REF-CHARGE-001",
            amount=1000,
            narration="Service fee",
        )
        print(charge.newBalance)
        """,
    ),
    (
        "chargeSubsidiaryAccount",
        """
        const charge = await client.chargeSubsidiaryAccount({
          accountReference: "CUST-000184-WALLET",
          referenceNumber: "REF-CHARGE-001",
          amount: 1000,
          narration: "Service fee",
        });
        console.log(charge.newBalance);
        """,
    ),
    (
        "charge_subsidiary_account",
        """
        let charge = client
            .charge_subsidiary_account(ChargeSubsidiaryAccount::new(
                "CUST-000184-WALLET",
                "REF-CHARGE-001",
                1000.0,
            ))
            .await?;
        """,
    ),
)

op(
    "top-up-subsidiary-account",
    "subsidiary",
    "Top up a subsidiary account",
    "Subsidiary Accounts - Top up an account",
    "POST /subsidiary-accounts/{accountReference}/topup",
    "collect",
    "basic",
    ["referenceNumber", "amount", "currency", "narration"],
    "Credits a ledger-backed subsidiary account from your business balance.",
    ["Not available on virtual accounts."],
    (
        "top_up_subsidiary_account",
        """
        top_up = await client.top_up_subsidiary_account(
            account_reference="CUST-000184-WALLET",
            reference_number="REF-TOPUP-001",
            amount=500,
            narration="Bonus credit",
        )
        print(top_up.newBalance)
        """,
    ),
    (
        "topUpSubsidiaryAccount",
        """
        const topUp = await client.topUpSubsidiaryAccount({
          accountReference: "CUST-000184-WALLET",
          referenceNumber: "REF-TOPUP-001",
          amount: 500,
          narration: "Bonus credit",
        });
        console.log(topUp.newBalance);
        """,
    ),
    (
        "top_up_subsidiary_account",
        """
        let top_up = client
            .top_up_subsidiary_account(TopUpSubsidiaryAccount::new(
                "CUST-000184-WALLET",
                "REF-TOPUP-001",
                500.0,
            ))
            .await?;
        """,
    ),
)

op(
    "transfer-between-subsidiary-accounts",
    "subsidiary",
    "Transfer between subsidiary accounts",
    "Subsidiary Accounts - Transfer between accounts",
    "POST /subsidiary-accounts/transfer",
    "collect",
    "basic",
    [
        "referenceNumber",
        "sourceAccountIdentifier",
        "destinationAccountIdentifier",
        "amount",
        "currency",
        "narration",
    ],
    "Moves money between two ledger-backed subsidiary accounts.",
    ["Paga sends one callback, for the source account only."],
    (
        "transfer_between_subsidiary_accounts",
        """
        transfer = await client.transfer_between_subsidiary_accounts(
            source_account_reference="CUST-000184-WALLET",
            destination_account_reference="CUST-000221-WALLET",
            reference_number="REF-TRANSFER-001",
            amount=1500,
            narration="Payment for goods",
        )
        """,
    ),
    (
        "transferBetweenSubsidiaryAccounts",
        """
        const transfer = await client.transferBetweenSubsidiaryAccounts({
          sourceAccountReference: "CUST-000184-WALLET",
          destinationAccountReference: "CUST-000221-WALLET",
          referenceNumber: "REF-TRANSFER-001",
          amount: 1500,
          narration: "Payment for goods",
        });
        """,
    ),
    (
        "transfer_between_subsidiary_accounts",
        """
        let transfer = client
            .transfer_between_subsidiary_accounts(
                TransferBetweenSubsidiaryAccounts::new(
                    "CUST-000184-WALLET",
                    "CUST-000221-WALLET",
                    "REF-TRANSFER-001",
                    1500.0,
                ),
            )
            .await?;
        """,
    ),
)

op(
    "retrieve-subsidiary-account",
    "subsidiary",
    "Retrieve a subsidiary account",
    "Subsidiary Accounts - Retrieve an account",
    "GET /subsidiary-accounts/{accountReference}",
    "collect",
    "basic",
    ["referenceNumber", "accountIdentifier"],
    "Returns an account's details, limits, callback URL and balance.",
    ["The `accountIdentifier` is the account's `accountReference`."],
    (
        "retrieve_subsidiary_account",
        """
        account = await client.retrieve_subsidiary_account(
            account_reference="CUST-000184-WALLET",
            reference_number="REF-GET-001",
        )
        """,
    ),
    (
        "retrieveSubsidiaryAccount",
        """
        const account = await client.retrieveSubsidiaryAccount({
          accountReference: "CUST-000184-WALLET",
          referenceNumber: "REF-GET-001",
        });
        """,
    ),
    (
        "retrieve_subsidiary_account",
        """
        let account = client
            .retrieve_subsidiary_account("CUST-000184-WALLET", "REF-GET-001")
            .await?;
        """,
    ),
)

op(
    "update-subsidiary-account",
    "subsidiary",
    "Update a subsidiary account",
    "Subsidiary Accounts - Update an account",
    "PUT /subsidiary-accounts/{accountReference}",
    "collect",
    "basic",
    [
        "referenceNumber",
        "accountIdentifier",
        "iifiNumber",
        "autoSweep.destination",
        "autoSweep.bankPublicId",
        "autoSweep.accountNumber",
        "callbackUrl",
    ],
    "Changes an account.",
    [
        "Send only what you want to change.",
        "`accountNumber` and `accountReference` cannot be changed.",
    ],
    (
        "update_subsidiary_account",
        """
        account = await client.update_subsidiary_account(
            account_reference="CUST-000184-WALLET",
            reference_number="REF-UPDATE-001",
            status="DISABLED",
        )
        """,
    ),
    (
        "updateSubsidiaryAccount",
        """
        const account = await client.updateSubsidiaryAccount({
          accountReference: "CUST-000184-WALLET",
          referenceNumber: "REF-UPDATE-001",
          status: "DISABLED",
        });
        """,
    ),
    (
        "update_subsidiary_account",
        """
        let account = client
            .update_subsidiary_account(UpdateSubsidiaryAccount::new(
                "CUST-000184-WALLET",
                "REF-UPDATE-001",
            ))
            .await?;
        """,
    ),
)

op(
    "get-subsidiary-balance",
    "subsidiary",
    "Get a subsidiary account balance",
    "Subsidiary Accounts - Get the balance",
    "GET /subsidiary-accounts/{accountReference}/balance",
    "collect",
    "basic",
    ["referenceNumber", "accountIdentifier"],
    "Returns an account's balance.",
    [],
    (
        "get_subsidiary_balance",
        """
        balance = await client.get_subsidiary_balance(
            account_reference="CUST-000184-WALLET",
            reference_number="REF-BAL-001",
        )
        print(balance.balance)
        """,
    ),
    (
        "getSubsidiaryBalance",
        """
        const balance = await client.getSubsidiaryBalance({
          accountReference: "CUST-000184-WALLET",
          referenceNumber: "REF-BAL-001",
        });
        console.log(balance.balance);
        """,
    ),
    (
        "get_subsidiary_balance",
        """
        let balance = client
            .get_subsidiary_balance("CUST-000184-WALLET", "REF-BAL-001")
            .await?;
        println!("{:?}", balance.balance);
        """,
    ),
)

op(
    "get-subsidiary-history",
    "subsidiary",
    "Get a subsidiary account history",
    "Subsidiary Accounts - Get transaction history",
    "GET /subsidiary-accounts/{accountReference}/history",
    "collect",
    "basic",
    ["accountIdentifier", "startDateTimeUTC", "endDateTimeUTC"],
    "Returns an account's transactions.",
    [
        "Up to three months at a time.",
        "Pages start at `0`.",
        "`referenceNumber` is required as a query parameter, but is not part of the hash.",
    ],
    (
        "get_subsidiary_history",
        """
        history = await client.get_subsidiary_history(
            account_reference="CUST-000184-WALLET",
            reference_number="REF-HIS-001",
            start_date_time_utc="2026-06-01T00:00:00",
            end_date_time_utc="2026-06-30T23:59:59",
            page_number=0,
            page_size=20,
        )
        """,
    ),
    (
        "getSubsidiaryHistory",
        """
        const history = await client.getSubsidiaryHistory({
          accountReference: "CUST-000184-WALLET",
          referenceNumber: "REF-HIS-001",
          startDateTimeUTC: "2026-06-01T00:00:00",
          endDateTimeUTC: "2026-06-30T23:59:59",
          pageNumber: 0,
          pageSize: 20,
        });
        """,
    ),
    (
        "get_subsidiary_history",
        """
        let history = client
            .get_subsidiary_history(GetSubsidiaryHistory::new(
                "CUST-000184-WALLET",
                "REF-HIS-001",
                "2026-06-01T00:00:00",
                "2026-06-30T23:59:59",
            ))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Persistent payment accounts                                                  #
# --------------------------------------------------------------------------- #

op(
    "register-persistent-payment-account",
    "persistent",
    "Register a persistent payment account",
    "Collect API - Register a persistent payment account",
    "POST /registerPersistentPaymentAccount",
    "collect",
    "basic",
    [
        "referenceNumber",
        "accountReference",
        "financialIdentificationNumber",
        "creditBankId",
        "creditBankAccountNumber",
        "callbackUrl",
    ],
    "Registers a standing instruction that lets a customer pay you repeatedly "
    "from the same account.",
    [
        "`accountReference` must be 11 to 30 characters.",
        "Paga calls your `callbackUrl` whenever the account is funded.",
    ],
    (
        "register_persistent_payment_account",
        """
        account = await client.register_persistent_payment_account(
            reference_number="REF-000006",
            account_reference="CUST-000184-WALLET",
            financial_identification_number="22222132329",
            credit_bank_id="40090E2F-7446-4217-9345-7BBAB7043C4C",
            credit_bank_account_number="0000000000",
            callback_url="https://yourstore.com/webhooks/paga",
        )
        """,
    ),
    (
        "registerPersistentPaymentAccount",
        """
        const account = await client.registerPersistentPaymentAccount({
          referenceNumber: "REF-000006",
          accountReference: "CUST-000184-WALLET",
          financialIdentificationNumber: "22222132329",
          creditBankId: "40090E2F-7446-4217-9345-7BBAB7043C4C",
          creditBankAccountNumber: "0000000000",
          callbackUrl: "https://yourstore.com/webhooks/paga",
        });
        """,
    ),
    (
        "register_persistent_payment_account",
        """
        let account = client
            .register_persistent_payment_account(
                RegisterPersistentPaymentAccount::new(
                    "REF-000006",
                    "CUST-000184-WALLET",
                    "22222132329",
                    "40090E2F-7446-4217-9345-7BBAB7043C4C",
                    "0000000000",
                    "https://yourstore.com/webhooks/paga",
                ),
            )
            .await?;
        """,
    ),
)

op(
    "update-persistent-payment-account",
    "persistent",
    "Update a persistent payment account",
    "Collect API - Update a persistent payment account",
    "POST /updatePersistentPaymentAccount",
    "collect",
    "basic",
    [
        "referenceNumber",
        "accountIdentifier",
        "financialIdentificationNumber",
        "creditBankId",
        "creditBankAccountNumber",
        "callbackUrl",
    ],
    "Changes a persistent payment account.",
    [
        "Every field takes part in the hash, so send the current value of the ones you are not changing.",
    ],
    (
        "update_persistent_payment_account",
        """
        account = await client.update_persistent_payment_account(
            reference_number="REF-000007",
            account_identifier="CUST-000184-WALLET",
            callback_url="https://yourstore.com/webhooks/paga-v2",
        )
        """,
    ),
    (
        "updatePersistentPaymentAccount",
        """
        const account = await client.updatePersistentPaymentAccount({
          referenceNumber: "REF-000007",
          accountIdentifier: "CUST-000184-WALLET",
          callbackUrl: "https://yourstore.com/webhooks/paga-v2",
        });
        """,
    ),
    (
        "update_persistent_payment_account",
        """
        let account = client
            .update_persistent_payment_account(
                UpdatePersistentPaymentAccount::new(
                    "REF-000007",
                    "CUST-000184-WALLET",
                ),
            )
            .await?;
        """,
    ),
)

op(
    "get-persistent-payment-account",
    "persistent",
    "Get a persistent payment account",
    "Collect API - Get a persistent payment account",
    "POST /getPersistentPaymentAccount",
    "collect",
    "basic",
    ["referenceNumber", "accountIdentifier"],
    "Returns a persistent payment account.",
    ["The `accountIdentifier` accepts a NUBAN **or** an `accountReference`."],
    (
        "get_persistent_payment_account",
        """
        account = await client.get_persistent_payment_account(
            reference_number="REF-000008",
            account_identifier="CUST-000184-WALLET",
        )
        """,
    ),
    (
        "getPersistentPaymentAccount",
        """
        const account = await client.getPersistentPaymentAccount({
          referenceNumber: "REF-000008",
          accountIdentifier: "CUST-000184-WALLET",
        });
        """,
    ),
    (
        "get_persistent_payment_account",
        """
        let account = client
            .get_persistent_payment_account("REF-000008", "CUST-000184-WALLET")
            .await?;
        """,
    ),
)

op(
    "delete-persistent-payment-account",
    "persistent",
    "Delete a persistent payment account",
    "Collect API - Delete a persistent payment account",
    "POST /deletePersistentPaymentAccount",
    "collect",
    "basic",
    ["referenceNumber", "accountIdentifier"],
    "Deletes a persistent payment account.",
    ["The `accountIdentifier` accepts a NUBAN **or** an `accountReference`."],
    (
        "delete_persistent_payment_account",
        """
        await client.delete_persistent_payment_account(
            reference_number="REF-000009",
            account_identifier="CUST-000184-WALLET",
        )
        """,
    ),
    (
        "deletePersistentPaymentAccount",
        """
        await client.deletePersistentPaymentAccount({
          referenceNumber: "REF-000009",
          accountIdentifier: "CUST-000184-WALLET",
        });
        """,
    ),
    (
        "delete_persistent_payment_account",
        """
        client
            .delete_persistent_payment_account("REF-000009", "CUST-000184-WALLET")
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Customers                                                                   #
# --------------------------------------------------------------------------- #

op(
    "register-customer",
    "customers",
    "Register a customer",
    "Business API - Register a customer",
    "POST /registerCustomer",
    "business",
    "headers",
    ["referenceNumber", "customerPhoneNumber", "customerFirstName", "customerLastName"],
    "Opens a Paga account for a customer on your business account.",
    ["The phone number must not already belong to a registered customer."],
    (
        "register_customer",
        """
        customer = await client.register_customer(
            reference_number="REF-000010",
            customer_phone_number="08064343187",
            customer_first_name="Bello",
            customer_last_name="Ramon",
            customer_email="customer@example.com",
            customer_date_of_birth="1989-10-02",
        )
        """,
    ),
    (
        "registerCustomer",
        """
        const customer = await client.registerCustomer({
          referenceNumber: "REF-000010",
          customerPhoneNumber: "08064343187",
          customerFirstName: "Bello",
          customerLastName: "Ramon",
          customerEmail: "customer@example.com",
          customerDateOfBirth: "1989-10-02",
        });
        """,
    ),
    (
        "register_customer",
        """
        let customer = client
            .register_customer(RegisterCustomer::new(
                "REF-000010",
                "08064343187",
                "Bello",
                "Ramon",
                "customer@example.com",
                "1989-10-02",
            ))
            .await?;
        """,
    ),
)

op(
    "register-customer-with-kyc",
    "customers",
    "Register a customer with KYC",
    "Business API - Register a customer with KYC",
    "POST /registerCustomerWithKYC",
    "business",
    "headers",
    ["referenceNumber", "customerPhoneNumber", "customerFirstName", "customerLastName"],
    "Opens a Paga account for a customer and uploads their identification "
    "photographs.",
    [
        "Sent as `multipart/form-data`: a `customer` JSON part, plus `customerAccountPhoto` and `customerIdPhoto` image parts.",
        "Each photograph must be a JPEG of at most 500 KB.",
    ],
    (
        "register_customer_with_kyc",
        """
        with open("account-photo.jpg", "rb") as photo:
            customer = await client.register_customer_with_kyc(
                reference_number="REF-000011",
                customer_phone_number="08064343187",
                customer_email="customer@example.com",
                customer_first_name="Bello",
                customer_last_name="Ramon",
                customer_date_of_birth="1989-10-02",
                customer_gender="MALE",
                customer_account_photo=photo.read(),
                customer_id_photo=photo.read(),
            )
        """,
    ),
    (
        "registerCustomerWithKyc",
        """
        import { readFile } from "node:fs/promises";

        const customer = await client.registerCustomerWithKyc({
          referenceNumber: "REF-000011",
          customerPhoneNumber: "08064343187",
          customerEmail: "customer@example.com",
          customerFirstName: "Bello",
          customerLastName: "Ramon",
          customerDateOfBirth: "1989-10-02",
          customerGender: "MALE",
          customerAccountPhoto: await readFile("account-photo.jpg"),
          customerIdPhoto: await readFile("id-photo.jpg"),
        });
        """,
    ),
    (
        "register_customer_with_kyc",
        """
        let photo = std::fs::read("account-photo.jpg")?;

        let customer = client
            .register_customer_with_kyc(RegisterCustomerWithKyc::new(
                "REF-000011",
                "08064343187",
                "customer@example.com",
                "Bello",
                "Ramon",
                "1989-10-02",
                "MALE",
                photo.clone(),
                photo,
            ))
            .await?;
        """,
    ),
)

op(
    "register-customer-account-photo",
    "customers",
    "Upload a customer account photo",
    "Business API - Register a customer account photo",
    "POST /registerCustomerAccountPhoto",
    "business",
    "headers",
    ["referenceNumber", "customerPhoneNumber"],
    "Uploads a customer's account photograph.",
    [
        "Sent as `multipart/form-data`: a `customer` JSON part plus a `customerAccountPhoto` image part.",
        "The photograph must be a JPEG of at most 500 KB.",
    ],
    (
        "register_customer_account_photo",
        """
        with open("account-photo.jpg", "rb") as photo:
            await client.register_customer_account_photo(
                reference_number="REF-000012",
                customer_phone_number="08064343187",
                customer_account_photo=photo.read(),
            )
        """,
    ),
    (
        "registerCustomerAccountPhoto",
        """
        import { readFile } from "node:fs/promises";

        await client.registerCustomerAccountPhoto({
          referenceNumber: "REF-000012",
          customerPhoneNumber: "08064343187",
          customerAccountPhoto: await readFile("account-photo.jpg"),
        });
        """,
    ),
    (
        "register_customer_account_photo",
        """
        let photo = std::fs::read("account-photo.jpg")?;

        client
            .register_customer_account_photo(RegisterCustomerAccountPhoto::new(
                "REF-000012",
                "08064343187",
                photo,
            ))
            .await?;
        """,
    ),
)

op(
    "register-customer-identification",
    "customers",
    "Upload a customer identification",
    "Business API - Register a customer identification",
    "POST /registerCustomerIdentification",
    "business",
    "headers",
    [
        "referenceNumber",
        "customerPhoneNumber",
        "customerIdType",
        "customerIdNumber",
        "customerIdExpirationDate",
    ],
    "Uploads a customer's identification and its photograph.",
    [
        "Sent as `multipart/form-data`: a `customer` JSON part plus a `customerIdPhoto` image part.",
        "`customerIdExpirationDate` is formatted as `YYYY-MM-DD`.",
    ],
    (
        "register_customer_identification",
        """
        with open("id-photo.jpg", "rb") as photo:
            await client.register_customer_identification(
                reference_number="REF-000013",
                customer_phone_number="08064343187",
                customer_id_type="NATIONAL_ID",
                customer_id_number="12345678901",
                customer_id_expiration_date="2030-01-01",
                customer_id_photo=photo.read(),
            )
        """,
    ),
    (
        "registerCustomerIdentification",
        """
        import { readFile } from "node:fs/promises";

        await client.registerCustomerIdentification({
          referenceNumber: "REF-000013",
          customerPhoneNumber: "08064343187",
          customerIdType: "NATIONAL_ID",
          customerIdNumber: "12345678901",
          customerIdExpirationDate: "2030-01-01",
          customerIdPhoto: await readFile("id-photo.jpg"),
        });
        """,
    ),
    (
        "register_customer_identification",
        """
        let photo = std::fs::read("id-photo.jpg")?;

        client
            .register_customer_identification(RegisterCustomerIdentification::new(
                "REF-000013",
                "08064343187",
                "NATIONAL_ID",
                "12345678901",
                "2030-01-01",
                photo,
            ))
            .await?;
        """,
    ),
)


# --------------------------------------------------------------------------- #
# Webhooks                                                                    #
# --------------------------------------------------------------------------- #

WEBHOOKS: list[dict] = [
    {
        "id": "checkout-notification",
        "name": "Checkout payment notification",
        "operation": "Checkout - Handle the payment notification",
        "signedFields": ["amount", "timeStamp", "paymentReference"],
        "delivery": "Paga sends this to your callback URL.",
        "description": "Sent to your callback URL when a Checkout payment completes. Check the hash, then fulfil.",
        "notes": ["De-duplicate on the payment reference."],
        "languages": {
            "python": {
                "method": "verify_checkout_notification",
                "example": 'ok = verify_checkout_notification(payload, received_hash, hash_key)',
            },
            "typescript": {
                "method": "verifyCheckoutNotification",
                "example": 'const ok = await verifyCheckoutNotification(payload, receivedHash, hashKey);',
            },
            "rust": {
                "method": "verify_checkout_notification",
                "example": 'let ok = webhooks::verify_checkout_notification(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "payment-callback",
        "name": "Dynamic virtual account callback",
        "operation": "Dynamic virtual account - Handle the callback",
        "signedFields": [
            "notificationId",
            "statusCode",
            "externalReferenceNumber",
            "state",
            "outstandingBalance",
        ],
        "delivery": "Paga sends this to your callback URL.",
        "description": "Sent to your `callBackUrl` when a payment request is paid, expires or is cancelled.",
        "notes": [
            "`outstandingBalance` is signed with two decimals.",
            "De-duplicate on `notificationId`.",
        ],
        "languages": {
            "python": {
                "method": "verify_payment_callback",
                "example": 'ok = verify_payment_callback(payload, received_hash, hash_key)',
            },
            "typescript": {
                "method": "verifyPaymentCallback",
                "example": 'const ok = await verifyPaymentCallback(payload, receivedHash, hashKey);',
            },
            "rust": {
                "method": "verify_payment_callback",
                "example": 'let ok = webhooks::verify_payment_callback(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "funding-notification",
        "name": "Subsidiary account funding notification",
        "operation": "Subsidiary Accounts - Handle a funding notification",
        "signedFields": [
            "transactionReference",
            "transactionDate",
            "amount",
            "accountNumber",
            "timestamp",
        ],
        "delivery": "Paga sends this to your callback URL.",
        "description": "Sent when someone pays into a subsidiary account.",
        "notes": ["The hash travels in the `x-paga-hash-v3` header, not the body."],
        "languages": {
            "python": {
                "method": "verify_funding_notification",
                "example": 'ok = verify_funding_notification(payload, received_hash, hash_key)',
            },
            "typescript": {
                "method": "verifyFundingNotification",
                "example": 'const ok = await verifyFundingNotification(payload, receivedHash, hashKey);',
            },
            "rust": {
                "method": "verify_funding_notification",
                "example": 'let ok = webhooks::verify_funding_notification(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "subsidiary-operation",
        "name": "Subsidiary charge, top-up or transfer callback",
        "operation": "Subsidiary Accounts - Handle a charge, top-up or transfer callback",
        "signedFields": [
            "externalReferenceNumber",
            "transactionDate",
            "amount",
            "accountNumber",
        ],
        "delivery": "Paga sends this to your callback URL.",
        "description": "Sent when a charge, a top-up or a transfer completes.",
        "notes": [
            "The `amount` is a formatted string with commas, such as `\"1,000.00\"`.",
            "A transfer sends one callback, for the source account only.",
        ],
        "languages": {
            "python": {
                "method": "verify_subsidiary_operation",
                "example": 'ok = verify_subsidiary_operation(payload, received_hash, hash_key)',
            },
            "typescript": {
                "method": "verifySubsidiaryOperation",
                "example": 'const ok = await verifySubsidiaryOperation(payload, receivedHash, hashKey);',
            },
            "rust": {
                "method": "verify_subsidiary_operation",
                "example": 'let ok = webhooks::verify_subsidiary_operation(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "money-transfer-notification",
        "name": "Money transfer notification",
        "operation": "Money transfer - Handle the notification",
        "signedFields": [
            "referenceNumber",
            "transactionDate",
            "transactionId",
            "amount",
            "sessionId",
        ],
        "delivery": "Paga sends this to your `statusCallbackUrl`.",
        "description": "Sent once a money transfer is processed.",
        "notes": [
            "The digest travels in the `x-paga-hash` **header**, not the body.",
            "Answer HTTP 200 with `{\"status\": \"SUCCESS\"}` once you have accepted it; Paga retries until it gets that.",
            "De-duplicate on `referenceNumber`.",
        ],
        "languages": {
            "python": {
                "method": "verify_money_transfer_notification",
                "example": 'ok = verify_money_transfer_notification(payload, request.headers["x-paga-hash"], hash_key)',
            },
            "typescript": {
                "method": "verifyMoneyTransferNotification",
                "example": 'const ok = await verifyMoneyTransferNotification(payload, request.headers["x-paga-hash"], hashKey);',
            },
            "rust": {
                "method": "verify_money_transfer_notification",
                "example": 'let ok = webhooks::verify_money_transfer_notification(Some(&payload), &received_hash, hash_key, None);',
            },
        },
    },
    {
        "id": "persistent-payment-account",
        "name": "Persistent payment account callback",
        "operation": "Collect API - Persistent Payment Account callback",
        "signedFields": [
            "statusCode",
            "accountNumber",
            "amount",
            "clearingFeeAmount",
            "transferFeeAmount",
        ],
        "delivery": "Paga sends this to your callback URL.",
        "description": "Sent when a persistent payment account is funded.",
        "notes": [
            "The body's `hash` field signs the five fields above.",
            "The `x-paga-hash` header signs `transactionReference + accountNumber + amount` instead.",
        ],
        "languages": {
            "python": {
                "method": "verify_persistent_payment_account_callback",
                "example": 'ok = verify_persistent_payment_account_callback(payload, received_hash, hash_key)',
            },
            "typescript": {
                "method": "verifyPersistentPaymentAccountCallback",
                "example": 'const ok = await verifyPersistentPaymentAccountCallback(payload, receivedHash, hashKey);',
            },
            "rust": {
                "method": "verify_persistent_payment_account_callback",
                "example": 'let ok = webhooks::verify_persistent_payment_account_callback(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "mandate-callback",
        "name": "Direct Debit mandate callback",
        "operation": "Direct Debit - Handle the mandate callback",
        "signedFields": [
            "statusCode",
            "timeStamp",
            "accountNumber",
            "bankName",
            "referenceNumber",
            "mandateStatus",
        ],
        "delivery": "Paga sends this to your mandate callback URL.",
        "description": "Sent when the authorisation transfer arrives and when the bank approves the mandate.",
        "notes": [
            "The `timeStamp` carries nanosecond precision and must be hashed exactly as received.",
            "De-duplicate on `notificationId`.",
        ],
        "languages": {
            "python": {
                "method": "verify_mandate_callback",
                "example": 'ok = verify_mandate_callback(payload, payload["hash"], hash_key)',
            },
            "typescript": {
                "method": "verifyMandateCallback",
                "example": 'const ok = await verifyMandateCallback(payload, payload.hash, hashKey);',
            },
            "rust": {
                "method": "verify_mandate_callback",
                "example": 'let ok = webhooks::verify_mandate_callback(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "charge-callback",
        "name": "Direct Debit charge callback",
        "operation": "Direct Debit - Handle the charge callback",
        "signedFields": [
            "statusCode",
            "referenceNumber",
            "accountReference",
            "amount",
        ],
        "delivery": "Paga sends this to your charge callback URL.",
        "description": "Sent when a mandate charge completes.",
        "notes": [
            "The `amount` is a string with two decimals and no commas, such as `\"600.00\"`.",
            "Decide on `statusCode`, and look up any non-zero code.",
        ],
        "languages": {
            "python": {
                "method": "verify_charge_callback",
                "example": 'ok = verify_charge_callback(payload, payload["hash"], hash_key)',
            },
            "typescript": {
                "method": "verifyChargeCallback",
                "example": 'const ok = await verifyChargeCallback(payload, payload.hash, hashKey);',
            },
            "rust": {
                "method": "verify_charge_callback",
                "example": 'let ok = webhooks::verify_charge_callback(Some(&payload), &received_hash, hash_key);',
            },
        },
    },
    {
        "id": "usd-payment-webhook",
        "name": "USD (ACH, Wire and Swift) payment webhook",
        "operation": "Bank transfer (ACH, Wire and Swift) - Handle the webhook",
        "signedFields": [],
        "delivery": "Paga sends this to your USD callback URL.",
        "description": "Sent as `CAPTURED` when a dollar payment clears, or `FUNDING_FAILED` if Paga could not fund it.",
        "notes": [
            "This webhook carries **no signature** — there is no hash to verify.",
            "De-duplicate on `referenceNumber` plus `paymentId`.",
        ],
        "languages": {
            "python": {
                "method": "parse_usd_payment_webhook",
                "example": 'webhook = parse_usd_payment_webhook(payload)\nif webhook.isCaptured:\n    ...',
            },
            "typescript": {
                "method": "parseUsdPaymentWebhook",
                "example": 'const webhook = parseUsdPaymentWebhook(payload);\nif (webhook.event === "CAPTURED") { /* fulfil */ }',
            },
            "rust": {
                "method": "parse_usd_payment_webhook",
                "example": 'let webhook = webhooks::parse_usd_payment_webhook(Some(&payload));\nif webhook.is_captured() { /* fulfil */ }',
            },
        },
    },
]


# --------------------------------------------------------------------------- #
# Sections                                                                    #
# --------------------------------------------------------------------------- #

SECTIONS: list[dict] = [
    {
        "id": "checkout",
        "title": "Checkout",
        "navTitle": "Checkout",
        "group": "accept-payments",
        "description": "Take a card or bank payment on a Paga-hosted page. The customer is redirected to Paga, pays, and Paga notifies your server.",
        "intro": "Checkout is the hosted flow: you send the customer to a Paga page and Paga handles the payment instrument. Use it when you want Paga to own the payment UI rather than building your own.",
    },
    {
        "id": "collection",
        "title": "Dynamic virtual account, Bank USSD, Paga wallet and USD bank transfer",
        "navTitle": "Collection",
        "group": "accept-payments",
        "description": "Collect money from a customer with a payment request. The same request serves the virtual account, USSD, wallet and USD flows — you pick the method.",
        "intro": "A payment request tells Paga to collect a specific amount from a specific customer. How the customer pays is up to you: a one-time virtual account number, a USSD prompt, their Paga wallet, or a USD bank transfer.",
    },
    {
        "id": "refunds",
        "title": "Refunds",
        "navTitle": "Refunds",
        "group": "accept-payments",
        "description": "Refund a payment in full or in part, or cancel one that was never paid.",
        "intro": "A refund returns money to the customer. Cancelling a payment request that has not been paid uses the same endpoint — Paga decides which it is from the request's state.",
    },
    {
        "id": "direct-debit",
        "title": "Direct Debit (Open Banking)",
        "navTitle": "Direct Debit",
        "group": "accept-payments",
        "description": "Take a standing authorisation to debit a customer's bank account, then charge against it.",
        "intro": "Direct Debit lets a customer authorise you to debit their bank account. You set the mandate up, wait for the bank to approve it, then charge it as often as the mandate allows.",
    },
    {
        "id": "money-transfer",
        "title": "Money Transfer",
        "navTitle": "Money Transfer",
        "group": "make-payments",
        "description": "Send money out of your business balance to a bank account or a Paga wallet.",
        "intro": "A money transfer moves money from your business balance to somebody else. You can validate the destination first, send in bulk, and check the status afterwards.",
    },
    {
        "id": "airtime",
        "title": "Airtime and data",
        "navTitle": "Airtime and data",
        "group": "make-payments",
        "description": "Top up a phone with airtime or a data bundle.",
        "intro": "Buy airtime or data for a phone number from your business balance. For data, pick the bundle first — the amount must match the bundle's price exactly.",
    },
    {
        "id": "bill-payment",
        "title": "Bill payment (VAS)",
        "navTitle": "Bill payment",
        "group": "make-payments",
        "description": "Pay a biller on behalf of a customer: electricity, water, TV, airtime and more.",
        "intro": "Bill payment takes a customer's account number, confirms it with the biller, and pays. Find the biller, pick the service, validate the customer, then pay.",
    },
    {
        "id": "status",
        "title": "Check the transaction status",
        "navTitle": "Transaction status",
        "group": "make-payments",
        "description": "Find out what happened to a money transfer, airtime purchase or bill payment you already sent.",
        "intro": "Some operations have no callback. The transaction status endpoint tells you where a transaction got to, and it is what you use to resolve an unknown outcome.",
    },
    {
        "id": "business-account",
        "title": "Your business account",
        "navTitle": "Business account",
        "group": "manage-accounts",
        "description": "Your own balance, transaction history, merchant onboarding and cash dispensing.",
        "intro": "The business account is your own. Read the balance before a payout run, reconcile against the transaction history, and onboard the merchants you aggregate.",
    },
    {
        "id": "subsidiary",
        "title": "Subsidiary accounts",
        "navTitle": "Subsidiary accounts",
        "group": "manage-accounts",
        "description": "Paga accounts for your customers, held on your behalf. Issue, hold and move money on their account.",
        "intro": "A subsidiary account is a Paga account for one of your customers. You can hold their money, move it between accounts, and set it up to sweep straight into a bank account.",
    },
    {
        "id": "persistent",
        "title": "Persistent payment accounts",
        "navTitle": "Persistent accounts",
        "group": "manage-accounts",
        "description": "A standing instruction that lets a customer pay you repeatedly from the same account.",
        "intro": "A persistent payment account is the customer-side equivalent of a direct debit mandate, but from the collection side: the customer authorises a debit, you keep taking it.",
    },
    {
        "id": "customers",
        "title": "Customer registration and KYC",
        "navTitle": "Customers",
        "group": "manage-accounts",
        "description": "Open a Paga account for a customer, with identity documents if you need them.",
        "intro": "Registering a customer opens a Paga account for them on your business account. The KYC variants upload photographs as well.",
    },
]


GROUPS: list[dict] = [
    {
        "id": "accept-payments",
        "title": "Accept payments",
        "description": "Collect money from a customer.",
    },
    {
        "id": "make-payments",
        "title": "Make payments",
        "description": "Send money out to a customer, a biller or a network.",
    },
    {
        "id": "manage-accounts",
        "title": "Manage accounts",
        "description": "Your own account, your customers' accounts, and the customers themselves.",
    },
]


# --------------------------------------------------------------------------- #
# Emit                                                                        #
# --------------------------------------------------------------------------- #

def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    operations_doc = {
        "$comment": "The Paga Engine SDK operation dataset. Authored in paga/data, served as paga-<lang>-docs/docs/operations.json.",
        "version": 1,
        "groups": GROUPS,
        "sections": SECTIONS,
        "operations": OPERATIONS,
        "webhooks": WEBHOOKS,
    }

    (DATA / "operations.json").write_text(
        json.dumps(operations_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(OPERATIONS)} operations and {len(WEBHOOKS)} webhooks")


if __name__ == "__main__":
    main()
