from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username", "autofocus": True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Choose a password"}),
    )
    algorithm = forms.ChoiceField(
        choices=[("sha256", "SHA-256"), ("md5", "MD5")],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Hash algorithm",
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username", "autofocus": True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
