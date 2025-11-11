from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('accounts:login')
        else:
            if form.errors:
                messages.error(
                    request,
                    "Registration failed. Please check your inputs and ensure the username/email is not already in use."
                )
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'page_title': 'Register',
    }
    return render(request, 'accounts/register.html', context)


def mask_email(email):
    """Masks the email to show only the first two characters and the domain (e.g., ru****@domain.com)."""
    if not email or '@' not in email:
        return "N/A"

    username, domain = email.split('@', 1)

    # Determine how many characters to show (max 2)
    chars_to_show = min(2, len(username))

    # Get the visible part
    visible_part = username[:chars_to_show]

    # Use **** for the masked part
    masked_part = '****'

    return f"{visible_part}{masked_part}@{domain}"


@login_required
def profile(request):
    """
    Displays the user profile page, including the securely masked email address.
    """
    # --- Masking Implementation ---
    masked_email = mask_email(request.user.email)

    # Pass the masked email to the context
    context = {
        'page_title': 'User Profile',
        'masked_email': masked_email,  # This variable is used in the template
    }

    return render(request, 'accounts/profile.html', context)