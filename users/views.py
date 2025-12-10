from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #email = form.cleaned_data.get('email')
            messages.success(request,f"Cuenta generada para {username}.")

            #Redirigimos al usuario a la home para que no se cargue de nuevo el formulario
            return redirect('login')
        #if form.errors:
            #print(form.errors.as_data())
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form': form})

#Decorator
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid()  and p_form.is_valid():
            username = request.user.username
            u_form.save()
            p_form.save()
            messages.success(request, f"Se ha modificado el perfil de {username}.")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form
        }


    return render(request,'users/profile.html',context)

