# salary/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from salary.forms import RegistrationForm, LoginForm, SalarySlipForm # Assuming you have a form for registration
from django.contrib import messages  # To show messages on form submission
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import User, SalarySlip
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas



# Function to render the homepage
class Homepage(View):
    def get(self, request):
        return render(request, 'index.html')
    
# # Class-based view to handle logout
class CreateSalarySlip(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect to login page if not authenticated
    redirect_field_name = 'redirect_to'  # Query parameter for redirect after login

    def get(self, request):
        return render(request, 'salary_form.html', {'user': request.user})

    def post(self, request):
        # Pass the user to the form constructor
        form = SalarySlipForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            salary_slip = form.save(commit=False)  # Don't save to the database yet
            salary_slip.user = request.user  # Assign the current user to the salary slip
            salary_slip.save()  # Save the form data to the database
            print(salary_slip)
            messages.success(request, 'Salary Slip submitted successfully!')
            return render(request, 'salary_form.html', {'user': request.user, 'form': form})  # Redirect to a success page or the same page
        else:
            messages.error(request, 'There was an error with your form submission.')
            print(form.errors)  # This will print the form errors to the console for debugging
            print(form.errors.as_json())
            return render(request, 'salary_form.html', {'user': request.user, 'form': form})
    
#  Class-based view to handle registration
class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
                return render(request, 'registration.html', {'form': form})

            # Proceed to save the user if no duplicate is found
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_active = True  # Set the user as active
            user.is_staff = False  # Set the user as staff
            user.role = 'user'  # Assign default role as 'user'
            print(user)  # Debug
            user.save()  # Save the user in the database

            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, "There was an error with the form. Please try again.")
            return render(request, 'registration.html', {'form': form})

# Class-based view to handle login
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Debugging: print the email and password
            print(f"Attempting to log in with email: {email} and password: {password}")

            # Authenticate with email and password
            user = authenticate(request, username=email, password=password)
            if user is not None:                
                login(request, user)  # Log the user in

                # Set session flags based on the user role
                if user.is_superuser:
                    request.session['is_admin'] = True  # Admin session flag
                    request.session['is_user'] = False  # No user session flag
                    messages.success(request, "Welcome to the Admin Panel!")
                    return redirect('/admin/')  # Redirect to Django admin panel
                else:
                    request.session['is_user'] = True  # Normal user session flag
                    request.session['is_admin'] = False  # No admin session flag
                    messages.success(request, "Welcome, User!")
                    return redirect('salary_form')  # Redirect to salary slip page
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, 'login.html', {'form': form})
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")
            return render(request, 'login.html', {'form': form})

# Class-based view to handle logout
class LogoutView(View):
    # Overriding the dispatch method to ensure the user is authenticated before proceeding
    def dispatch(self, request, *args, **kwargs):
        # Ensure that the user is logged in before processing logout
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Clear session flags
        if 'is_superuser' in request.session:
            del request.session['is_superuser']
        if 'is_admin' in request.session:
            del request.session['is_admin']
        if 'is_user' in request.session:
            del request.session['is_user']

        # Log the user out
        logout(request)
        request.session.flush()  # Clears the session data

        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
    
