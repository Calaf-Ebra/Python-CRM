from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from .forms import SignUpForm
from .models import Record
from .forms import AddRecordForm


# Create your views here.
def home(request):
    records = Record.objects.all()
    #MEANS id user is trying to post something..form..let us grab their input
    if request.method == "POST":
        username = request.POST['username'] #from form input.. name = username
        password = request.POST['password']
        
        #authenticate info
        user = authenticate(request, username=username, password=password)
        if user is not None:
            ##login is imported from packages
            login(request, user)
            # meesages should be added to base file..so that any one can be shown
            messages.success(request, "You have been LOGGED IN")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, try again")
            redirect('home')
    else:   
    
        return render(request, 'web/home.html',{'records':records})

def logout_user(request):
    #imported from packages
    logout(request)
    messages.success(request, "You have been LOGGED OUT...")
    return  redirect('home')

def register_user(request):
        
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'web/register.html', {'form':form})

	return render(request, 'web/register.html', {'form':form})

def cus_record(request,pk):
    if request.user.is_authenticated:
         cus_records = Record.objects.get(id=pk)
         return render(request, 'web/record.html',{'cus_records':cus_records})
    else:
          messages.success(request, "You must be logged in to see page")
          return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated: 
        delete_it = Record.objects.get(id = pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfuly")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home')
    
def add_record(request):
     form = AddRecordForm(request.POST or None)

     if request.user.is_authenticated:
          if request.method == "POST":
            if form.is_valid:
                 add_record = form.save()
                 messages.success(request, "Record Added")
                 return redirect('home')
     
          return render(request, 'web/add_record.html',{'form':form})
     else:
        messages.success(request, "You Must Be Logged In")
        return redirect('home')
     
def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'web/update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
          
     

          

     
          
         



