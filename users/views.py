from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm

def register(request):
    if request.user.is_authenticated:
        messages.success(request, f'You already have an account!')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created!')
                return redirect('login')
        else:
            form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required(login_url = '/login/')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user) 
    
    context = {
        'u_form' : u_form,
    }
    return render(request, 'users/profile.html', context)





