from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UserprofileForm

# logowanie
def signup(request):
    # Metoda HTTP POST.Oznacza to, że formularz został przesłany przez użytkownika
    # i możemy znaleźć jej wypełnione odpowiedzi za pomocą request.POST QueryDict
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # wyświetlenie formularza
        userprofileform = UserprofileForm(request.POST)

        if form.is_valid() and userprofileform.is_valid():
            user = form.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
        userprofileform = UserprofileForm()
    
    return render(request, 'signup.html', {'form': form, 'userprofileform': userprofileform})

# uwierzytelnienie użytkownika
@login_required
def myaccount(request):
    return render(request, 'myaccount.html')