from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from .models import *
from .forms import *

@login_required
def home(request):

    if 'post_new' in request.POST:
        errors = []

        # Creates a new item if it is present as a parameter in the request
        if not 'text' in request.POST or not request.POST['text']:
            errors.append('You must write something to post.')
        elif len(request.POST['text']) > 42:
            errors.append('text should not exceed 42 characters.')

        else:
            new_post = Post(text=request.POST['text'], user=request.user)
            new_post.save()

        posts = Post.objects.all().order_by('-date')
        context = {'posts': posts, 'errors': errors}
        return render(request, './grumblr/global.html', context)

    # Sets up list of just the logged-in user's (request.user's) items
    posts = Post.objects.all().order_by('-date')
    return render(request, 'grumblr/global.html', {'posts': posts})

def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, './grumblr/register.html', context)

    errors = []
    context['errors'] = errors


    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'first_name' in request.POST or not request.POST['first_name']:
        errors.append('First name is required.')
    else:
        context['first_name'] = request.POST['first_name']

    if not 'last_name' in request.POST or not request.POST['last_name']:
        errors.append('First name is required.')
    else:
        context['last_name'] = request.POST['last_name']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if 'username' in request.POST and len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, './grumblr/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'], \
                                        first_name=request.POST['first_name'],\
                                        last_name=request.POST['last_name'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/')

@login_required
def profile(request, pk):
    p_user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(user=p_user).order_by('-date')

    return render(request, './grumblr/profile.html',{'posts': posts, 'p_user': p_user})


@login_required
def profile_self(request):
    p_user = get_object_or_404(User, pk=request.user.pk)
    posts = Post.objects.filter(user=p_user).order_by('-date')

    return render(request, './grumblr/profile.html', {'posts': posts, 'p_user': p_user})




