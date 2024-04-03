from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records


def home(request):

    records = Records.objects.all()

    # Check to see if loggin in:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.success(request, "The username or password is incorrect. Please try again")
            return redirect('home')
    else:
        return render(request, 'home.html', { 'records': records    })


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    return(request, 'register.html', {})


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})



def customer_record(request, pk):
    if request.user.is_authenticated:

        customer_record = Records.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "Please login to view this page")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Records.objects.get(id=pk) # Get the record
        record.delete()
        messages.success(request, "Record has been deleted")
        return redirect('home')
    else:
        messages.success(request, "Please login to view this page")
        return redirect('home')

def update_record(request, pk):
    record = Records.objects.get(id=pk)
    form = RecordForm(instance=record)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')
    return render(request, 'update_record.html', {'form': form})


def add_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been added")
                return redirect('home')
        else:
            form = AddRecordForm()
            return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "Please login to view this page")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "Please login to view this page")
        return redirect('home')