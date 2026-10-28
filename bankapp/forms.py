from django import forms
from .models import Banking


class NewAccountForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=4
    )

    balance = forms.DecimalField(
        min_value=0,
        max_digits=12,
        decimal_places=2,
        initial=0
    )

    class Meta:
        model = Banking
        fields = [
            "account_no",
            "name",
            "password",
            "mobile",
            "address",
            "balance",
        ]


class AccountForm(forms.Form):
    account_no = forms.CharField(max_length=20)
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class BalanceForm(AccountForm):
    pass


class DepositForm(AccountForm):
    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=12,
        decimal_places=2
    )


class WithdrawForm(AccountForm):
    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=12,
        decimal_places=2
    )


class TransferForm(forms.Form):
    sender_account_no = forms.CharField(
        max_length=20,
        label="Sender Account Number"
    )

    name = forms.CharField(max_length=100)

    password = forms.CharField(widget=forms.PasswordInput)

    receiver_account_no = forms.CharField(
        max_length=20,
        label="Receiver Account Number"
    )

    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=12,
        decimal_places=2
    )


class CloseAccountForm(AccountForm):
    pass