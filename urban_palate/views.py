from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from django.shortcuts import render, redirect

def home_view(request):
    # 1. Check if the user is authenticated (logged in)
    if request.user.is_authenticated:

        # 2. Check if the user is a staff/admin user
        if request.user.is_staff:
            # If they are staff, redirect them to the namespaced dashboard home
            return redirect('dashboard:home')

        # 3. If they are authenticated but NOT staff (i.e., a normal customer)
        else:
            # Redirect them to the main authenticated normal users view (index.html)

            return render (request,'index.html')

    # 4. If the user is NOT authenticated (anonymous visitor)
    else:
        # Redirect them to the custom landing page (landing.html)

        return render(request,'landing.html')

