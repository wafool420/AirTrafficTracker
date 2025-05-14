from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm, ItemForm
from .models import Items, ArchiveGroup
import logging

logger = logging.getLogger(__name__)

def register_view(request):
    logger.error("Register View Accessed")
    if request.method == "POST":
        logger.error("Register Form Submitted")
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            logger.error(f"Registering user: {username} {first_name} {last_name}")
            try:
                user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name
                )
                logger.error("User created successfully")
                return redirect('login')
            except Exception as e:
                logger.error(f"Error creating user: {e}")
        else:
            logger.error(f"Form Errors: {form.errors}")
    else:
        logger.error("Register View Accessed - GET Request")
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    logger.error("Login View Accessed")
    error_message = ""
    if request.method == "POST":
        logger.error("Login Form Submitted")
        username = request.POST.get("username")
        password = request.POST.get("password")
        logger.error(f"Attempting login for user: {username}")
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logger.error(f"User {username} authenticated successfully")
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next') or 'home'
                return redirect(next_url)
            else:
                logger.error("Invalid credentials provided")
                error_message = "Invalid Credentials"
        except Exception as e:
            logger.error(f"Login Error: {e}")
    return render(request, 'accounts/login.html', {'error': error_message})


def logout_view(request):
    logger.error("Logout View Accessed")
    if request.method == "POST":
        logger.error("User logged out via POST")
        logout(request)
        return redirect('login')
    elif request.method == "GET":
        return render(request, 'accounts/logout.html')
    else:
        return redirect('home')


@login_required
def home_view(request):
    logger.error("Home View Accessed")
    users = User.objects.all()
    return render(request, 'main_site/home.html', {'users': users})

@login_required
def create_item_view(request):
    logger.error("Create Item View Accessed")
    if request.method == 'POST':
        logger.error("Create Item Form Submitted")
        form = ItemForm(request.POST)
        if form.is_valid():
            logger.error("Item Form Valid")
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            logger.error("Item created successfully")
            return redirect('items')
        else:
            logger.error(f"Item Form Errors: {form.errors}")
    else:
        form = ItemForm()
    return render(request, 'main_site/create_form.html', {'form': form})


@login_required
def item_list_view(request):
    logger.error("Item List View Accessed")
    items = Items.objects.filter(archive_group__isnull=True)
    return render(request, 'main_site/item_list.html', {'items': items})


@login_required
def delete_item_view(request, item_id):
    logger.error(f"Delete Item View Accessed for item {item_id}")
    try:
        item = Items.objects.get(id=item_id)
        if request.method == "POST":
            item.delete()
            logger.error(f"Item {item_id} deleted")
            return redirect('items')
    except Items.DoesNotExist:
        logger.error(f"Item {item_id} does not exist")
    return render(request, 'main_site/delete.html', {'item': item})


@login_required
def item_edit_view(request, item_id):
    logger.error(f"Edit Item View Accessed for item {item_id}")
    try:
        item = Items.objects.get(id=item_id)
        if request.method == 'POST':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                logger.error("Item Form Valid")
                item = form.save(commit=False)
                item.user = request.user
                item.save()
                logger.error(f"Item {item_id} updated")
                return redirect('items')
        else:
            form = ItemForm(instance=item)
    except Items.DoesNotExist:
        logger.error(f"Item {item_id} does not exist")
    return render(request, 'main_site/item_edit_form.html', {'form': form})


@login_required
def archive_dataset_view(request):
    logger.error("Archive Dataset View Accessed")
    if request.method == "POST":
        logger.error("Archiving Dataset")
        group = ArchiveGroup.objects.create()
        Items.objects.filter(archive_group__isnull=True).update(archive_group=group)
        logger.error("Dataset Archived")
        return redirect('items')  
    return render(request, 'main_site/archive.html')


def archive_view(request):
    logger.error("Archive View Accessed")
    if request.method == "GET":
        archive = ArchiveGroup.objects.all().order_by('-id')
        logger.error(f"Archive Groups Retrieved: {archive.count()}")
        return render(request, 'main_site/archived_list.html', {'archive': archive})


@login_required
def archive_clear_view(request):
    logger.error("Archive Clear View Accessed")
    if request.method == "POST":
        logger.error("Clearing Archives")
        Items.objects.filter(archive_group__isnull=False).delete()
        ArchiveGroup.objects.all().delete()
        logger.error("Archives Cleared")
        return redirect('archive_view')
    return render(request, 'main_site/clear_archive.html')


@login_required
def archive_delete_view(request, group_id):
    logger.error(f"Archive Delete View Accessed for group {group_id}")
    try:
        group = ArchiveGroup.objects.get(id=group_id)
        group.items_set.all().delete()
        group.delete()
        logger.error(f"Archive Group {group_id} deleted")
    except ArchiveGroup.DoesNotExist:
        logger.error(f"Archive Group {group_id} does not exist")
    return redirect('archive_view')  
