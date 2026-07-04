from django.contrib import messages
from django.shortcuts import render

from accounts.decorators import login_required_session

from .logic.rail_fence import rail_fence_decrypt, rail_fence_encrypt
from .logic.rsa_cipher import generate_keypair, rsa_decrypt, rsa_encrypt


@login_required_session
def dashboard_view(request):
    return render(request, "ciphers/dashboard.html", {"username": request.session.get("username")})


@login_required_session
def rail_fence_view(request):
    context = {}
    if request.method == "POST":
        text = request.POST.get("text", "")
        action = request.POST.get("action")
        try:
            key = int(request.POST.get("key", 3))
            if key < 2:
                raise ValueError
        except ValueError:
            messages.error(request, "Key must be a whole number of 2 or more.")
        else:
            if action == "encrypt":
                context["result"] = rail_fence_encrypt(text, key)
                context["result_label"] = "Ciphertext"
            else:
                context["result"] = rail_fence_decrypt(text, key)
                context["result_label"] = "Plaintext"
        context["submitted_text"] = text
        context["submitted_key"] = request.POST.get("key", 3)

    return render(request, "ciphers/rail_fence.html", context)


@login_required_session
def rsa_view(request):
    context = {
        "public_key": request.session.get("rsa_public"),
        "private_key": request.session.get("rsa_private"),
        "p": request.session.get("rsa_p"),
        "q": request.session.get("rsa_q"),
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "generate":
            bits = 16
            keys = generate_keypair(bits=bits)
            request.session["rsa_public"] = list(keys["public"])
            request.session["rsa_private"] = list(keys["private"])
            request.session["rsa_p"] = keys["p"]
            request.session["rsa_q"] = keys["q"]
            context.update(
                public_key=keys["public"],
                private_key=keys["private"],
                p=keys["p"],
                q=keys["q"],
            )
            messages.success(request, "New RSA keypair generated.")

        elif action == "encrypt":
            text = request.POST.get("plain_text", "")
            public = context["public_key"]
            if not public:
                messages.error(request, "Generate a keypair first.")
            else:
                try:
                    cipher_values = rsa_encrypt(text, tuple(public))
                    context["cipher_result"] = ", ".join(str(v) for v in cipher_values)
                except ValueError as exc:
                    messages.error(request, str(exc))
            context["submitted_plain_text"] = text

        elif action == "decrypt":
            cipher_text = request.POST.get("cipher_text", "")
            private = context["private_key"]
            if not private:
                messages.error(request, "Generate a keypair first.")
            else:
                try:
                    cipher_values = [int(v.strip()) for v in cipher_text.split(",") if v.strip()]
                    context["plain_result"] = rsa_decrypt(cipher_values, tuple(private))
                except ValueError:
                    messages.error(request, "Ciphertext must be comma-separated integers.")
            context["submitted_cipher_text"] = cipher_text

    return render(request, "ciphers/rsa.html", context)
