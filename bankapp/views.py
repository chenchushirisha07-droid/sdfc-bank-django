
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

from .models import Banking
from .forms import (
    NewAccountForm,
    BalanceForm,
    DepositForm,
    WithdrawForm,
    TransferForm,
    CloseAccountForm,
)


def home(request):
    return render(request, "home.html")


def aboutus(request):
    return render(request, "aboutus.html")


def get_account(account_no, name, password):
    """Return the account only when all credentials are valid."""
    try:
        account = Banking.objects.get(account_no=account_no)
    except Banking.DoesNotExist:
        return None

    if account.name != name:
        return None

    if not check_password(password, account.password):
        return None

    return account


def newaccount(request):
    if request.method == "POST":
        form = NewAccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)

            # Store a password hash instead of plain text.
            account.password = make_password(
                form.cleaned_data["password"]
            )

            account.save()
            messages.success(
                request,
                f"Account created successfully. Account number: "
                f"{account.account_no}"
            )
            return redirect("home")
    else:
        form = NewAccountForm()

    return render(request, "newaccount.html", {"form": form})


def balance(request):
    if request.method == "POST":
        form = BalanceForm(request.POST)

        if form.is_valid():
            account = get_account(
                form.cleaned_data["account_no"],
                form.cleaned_data["name"],
                form.cleaned_data["password"],
            )

            if account:
                return render(
                    request,
                    "balance.html",
                    {
                        "form": form,
                        "account": account,
                        "balance": account.balance,
                    },
                )

            messages.error(
                request,
                "Invalid account number, name, or password."
            )
    else:
        form = BalanceForm()

    return render(request, "balance.html", {"form": form})


def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST)

        if form.is_valid():
            account = get_account(
                form.cleaned_data["account_no"],
                form.cleaned_data["name"],
                form.cleaned_data["password"],
            )

            amount = form.cleaned_data["amount"]

            if account:
                if amount <= Decimal("0"):
                    messages.error(
                        request,
                        "Deposit amount must be greater than zero."
                    )
                else:
                    account.balance += amount
                    account.save(update_fields=["balance"])

                    messages.success(
                        request,
                        f"Deposit successful. New balance: "
                        f"{account.balance}"
                    )
                    return redirect("home")
            else:
                messages.error(
                    request,
                    "Invalid account number, name, or password."
                )
    else:
        form = DepositForm()

    return render(request, "deposit.html", {"form": form})


def withdraw(request):
    if request.method == "POST":
        form = WithdrawForm(request.POST)

        if form.is_valid():
            account = get_account(
                form.cleaned_data["account_no"],
                form.cleaned_data["name"],
                form.cleaned_data["password"],
            )

            amount = form.cleaned_data["amount"]

            if account is None:
                messages.error(
                    request,
                    "Invalid account number, name, or password."
                )
            elif amount <= Decimal("0"):
                messages.error(
                    request,
                    "Withdrawal amount must be greater than zero."
                )
            elif account.balance < amount:
                messages.error(
                    request,
                    "Insufficient balance."
                )
            else:
                account.balance -= amount
                account.save(update_fields=["balance"])

                messages.success(
                    request,
                    f"Withdrawal successful. Remaining balance: "
                    f"{account.balance}"
                )
                return redirect("home")
    else:
        form = WithdrawForm()

    return render(request, "withdraw.html", {"form": form})


def transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)

        if form.is_valid():
            sender_no = form.cleaned_data["sender_account_no"]
            sender_name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            receiver_no = form.cleaned_data["receiver_account_no"]
            amount = form.cleaned_data["amount"]

            if amount <= Decimal("0"):
                messages.error(
                    request,
                    "Transfer amount must be greater than zero."
                )
            elif sender_no == receiver_no:
                messages.error(
                    request,
                    "Sender and receiver accounts must be different."
                )
            else:
                try:
                    with transaction.atomic():
                        sender = (
                            Banking.objects.select_for_update()
                            .get(account_no=sender_no)
                        )
                        receiver = (
                            Banking.objects.select_for_update()
                            .get(account_no=receiver_no)
                        )

                        if sender.name != sender_name:
                            raise ValueError("Invalid sender details.")

                        if not check_password(password, sender.password):
                            raise ValueError("Invalid sender details.")

                        if sender.balance < amount:
                            raise ValueError("Insufficient balance.")

                        sender.balance -= amount
                        receiver.balance += amount

                        sender.save(update_fields=["balance"])
                        receiver.save(update_fields=["balance"])

                    messages.success(
                        request,
                        "Money transferred successfully."
                    )
                    return redirect("home")

                except Banking.DoesNotExist:
                    messages.error(
                        request,
                        "Sender or receiver account was not found."
                    )
                except ValueError as error:
                    messages.error(request, str(error))
    else:
        form = TransferForm()

    return render(request, "transfer.html", {"form": form})


def closeaccount(request):
    if request.method == "POST":
        form = CloseAccountForm(request.POST)

        if form.is_valid():
            account = get_account(
                form.cleaned_data["account_no"],
                form.cleaned_data["name"],
                form.cleaned_data["password"],
            )

            if account is None:
                messages.error(
                    request,
                    "Invalid account number, name, or password."
                )
            elif account.balance != Decimal("0"):
                messages.error(
                    request,
                    "Please withdraw or transfer the remaining balance "
                    "before closing the account."
                )
            else:
                account.delete()
                messages.success(
                    request,
                    "Account closed successfully."
                )
                return redirect("home")
    else:
        form = CloseAccountForm()

    return render(request, "closeaccount.html", {"form": form})
