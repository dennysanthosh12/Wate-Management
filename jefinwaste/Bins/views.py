
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Bin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .tsp_solver import calculate_distance, TSPBranchBound
import numpy as np
from math import radians, sin, cos, sqrt, asin


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to home or any other page upon successful login
            return redirect('home_page')  # Update 'home' to the name of your home page URL pattern
        else:
            # Handle invalid login credentials here (optional)
            pass
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print("Username:", username)
        print("Password:", password)
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)

        # Check if the username is available
        if User.objects.filter(username=username).exists():
            # Handle case where username is not available
            pass
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password,first_name=first_name , last_name=last_name, email=email)
            # Optionally, log the user in after registration
            login(request, user)
            # Redirect to home or any other page upon successful registration
            return redirect('home_page')  # Update 'home' to the name of your home page URL pattern

    return render(request, 'register.html')

@login_required
def home_page(request):
    return render(request, 'showbin.html')

class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login_page')  # Redirect to 'login_page' after logout

    def get_next_page(self):
        next_page = super().get_next_page()
        return next_page or self.next_page

@login_required
def get_bin_contents(request):
    bins = Bin.objects.filter(user=request.user)
    bin_contents = [bin.bin_content for bin in bins]
    return JsonResponse({'bin_contents': bin_contents})

@csrf_exempt
def update_bin_content(request, bin_id):
    bin_obj = get_object_or_404(Bin, pk=bin_id)
    
    if request.method == 'POST':
        new_bin_content = request.POST.get('bin_content')
        print(new_bin_content)

        if new_bin_content is not None:
            try:
                new_bin_content = float(new_bin_content)
                if 0 <= new_bin_content <= 150:  # Validate bin_content range
                    bin_obj.bin_content = new_bin_content
                    bin_obj.save()
                    return JsonResponse({'message': f'Bin content updated for Bin ID {bin_id}'})
                else:
                    return JsonResponse({'error': 'bin_content value out of range'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Invalid bin_content value provided'}, status=400)
        else:
            return JsonResponse({'error': 'bin_content parameter missing or empty'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for this endpoint'}, status=405)
    

def showbin(request):
    return render(request, 'showbin.html')

def addbin(request):
    if request.method == 'POST':
        latitude_str = request.POST.get('latitude')
        longitude_str = request.POST.get('longitude')
        
        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)

            new_bin = Bin(latitude=latitude, longitude=longitude, bin_content=0.0)
            new_bin.user = request.user
            new_bin.save()  # Save the new bin object to the database
            bin_id = new_bin.Bin_Id  # Assuming 'Bin_Id' is the primary key field of your Bin model
            messages.success(request, f'Bin with Bin_ID = {bin_id} added successfully.')
            return redirect('addbin') # Redirect to home or any other appropriate page
        except Exception as e:
            messages.error(request, f'Failed to add bin: {str(e)}')
            return redirect('addbin')

    return render(request, 'addbin.html')

@login_required
def calculate(request):
    if request.method == 'POST':
        dumping_point_latitude = float(request.POST.get('latitude'))
        dumping_point_longitude = float(request.POST.get('longitude'))

        bins = Bin.objects.filter(bin_content__gte=130)
        latitudes = [bin.latitude for bin in bins]
        longitudes = [bin.longitude for bin in bins]
        latitudes.insert(0, dumping_point_latitude)
        longitudes.insert(0, dumping_point_longitude)
        bin_count = len(bins) + 1

        graph = []
        for i in range(bin_count):
            row = []
            for j in range(bin_count):
                row.append(calculate_distance(latitudes[i], longitudes[i], latitudes[j], longitudes[j]))
            graph.append(row)

        start_node = 0  # Assuming the starting node is the dumping point
        tsp_solver = TSPBranchBound(graph)
        best_path, best_cost = tsp_solver.solve(start_node)

        # Fetch bin details for each node in the best path
        bin_details = []
        for node_index in best_path:
            if node_index == 0:
                bin_details.append({'name': 'Dumping Point', 'latitude': dumping_point_latitude, 'longitude': dumping_point_longitude})
            else:
                bin = bins[node_index - 1]  # Adjust index to skip the dumping point
                bin_details.append({'name': f'Bin {bin.Bin_Id}', 'latitude': bin.latitude, 'longitude': bin.longitude})

        return render(request, 'calculate.html', {'bin_details': bin_details, 'best_cost': best_cost})

    return render(request, 'calculate.html')   # Render the form initially              
            

def deletebin(request):
    bins = Bin.objects.all()
    return render(request, 'deletebin.html', {'bins': bins})

def deleteconfirm(request, bin_id):
    bin_to_delete = get_object_or_404(Bin, Bin_Id=bin_id)

    if request.method == 'POST':
        # Confirm deletion (optional step)
        # Here, we directly proceed with deletion without confirmation

        # Delete the Bin object from the database
        bin_to_delete.delete()

        messages.success(request, f'Bin {bin_id} deleted successfully.')
        return redirect('deletebin')  # Redirect to home page after deletion

    # Render the delete confirmation template
    return render(request, 'deleteconfirm.html', {'bin': bin_to_delete})
