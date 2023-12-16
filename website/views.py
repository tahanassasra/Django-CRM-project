from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.contrib.auth.decorators import login_required



def home(request):
    records = Record.objects.all()

    #check to see if the user is logged in
    if request.method =='POST':
        #get names as they appear in the name attribute inside the form
        username = request.POST['username']
        password = request.POST['password']
        
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in. Please try again...")
            return redirect('home')

    return render(request, 'home.html', {'records' : records})


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully Registerred! Welcome")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, "register.html", {'form':form})   
    return render(request, "register.html", {'form':form})



def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')


def delete_record(request, pk):
    item = Record.objects.get(id=pk)
    if request.user.is_authenticated:
        item.delete()
        messages.success(request, message = f"Record of {item} has been successfully deleted.")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')


@login_required
def add_record(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            add_record = form.save()
            messages.success(request, "Record saved")
            return redirect('home')
    else:
        form = AddRecordForm()
        return render(request, "add_record.html", {'form':form})
    return render(request, "add_record.html", {'form':form})
  

@login_required
def update_record(request, pk):
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Record has been updated!")
        return redirect('home')
    else:
        return render(request, "update_record.html", {'form': form})

 