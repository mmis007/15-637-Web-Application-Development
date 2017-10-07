from django.contrib.auth.forms import PasswordChangeFormfrom django.contrib.auth.tokens import default_token_generatorfrom django.core.exceptions import ObjectDoesNotExistfrom django.http import HttpResponseRedirectfrom django.shortcuts import render, redirect, get_object_or_404from django.http import HttpResponse, Http404from django.contrib.auth.decorators import login_requiredfrom django.contrib.auth import login,  update_session_auth_hashfrom django.db import transactionfrom django.urls import reversefrom .forms import *from .models import *from django.core.mail import send_mailfrom django.views.decorators.csrf import ensure_csrf_cookie@login_requireddef index(request):    return HttpResponseRedirect("/grumblr/")@login_requireddef home(request):    context = {}    if request.method == 'GET':        context['form_new_post'] = PostForm()    else:        form = PostForm(request.POST)        context['form_new_post'] = form        if form.is_valid():            new_post = Post(text=request.POST['text'], user=request.user)            new_post.save()    posts = Post.objects.all().order_by('-date')    context['posts'] = posts    context['max_time'] = Post.objects.all().aggregate(Max('date'))['date__max'].isoformat()    return render(request, './grumblr/global.html', context)# # Returns all recent additions in the database, as JSON# def get_posts(request, time="1970-01-01T00:00+00:00"):#     max_time = Post.get_max_time()#     posts = Post.get_posts(time)#     context = {"max_time": max_time, "posts": posts}#     return render(request, 'json/posts.json', context, content_type='application/json')# Returns all recent changes to the database, as JSONdef get_changes(request, time):    # print(time)    max_time = Post.objects.all().aggregate(Max('date'))['date__max']    # print(max_time )    posts = Post.objects.filter(date__gt=time).distinct()    context = {"max_time": max_time, "posts": posts}    return render(request, 'json/posts.json', context, content_type='application/json')# Returns all recent changes to the database, as JSONdef add_comment(request, pk):    context = {}    if request.method == 'GET':        context['form_new_comment'] = CommentForm()    else:        form = CommentForm(request.POST)        context['form_new_comment'] = form        # print('add_comment view')        # print(form)        if form.is_valid():            print("valid")            new_comment = Comment(text=request.POST['text'], user_id=request.POST['user_id'],                                  post_id=request.POST['post_id'])            print(new_comment.text)            new_comment.save()            context = {"comment": new_comment}    return render(request, 'json/comment.json', context, content_type='application/json')@transaction.atomicdef register(request):    context = {}    # Just display the registration form if this is a GET request.    if request.method == 'GET':        context['form'] = RegistrationForm()        return render(request, 'grumblr/register.html', context)    # Creates a bound form from the request POST parameters and makes the    # form available in the request context dictionary.    form = RegistrationForm(request.POST)    context['form'] = form    # Validates the form.    if not form.is_valid():        return render(request, 'grumblr/register.html', context)    # If we get here the form data was valid.  Register and login the user.    new_user = User.objects.create_user(username=form.cleaned_data['username'],                                        password=form.cleaned_data['password1'],                                        first_name=form.cleaned_data['first_name'],                                        last_name=form.cleaned_data['last_name'],                                        email=form.cleaned_data['email'])    new_user.is_active = False    new_user.save()    token = default_token_generator.make_token(new_user)    new_profile = Profile(user=new_user)    new_profile.confirm_token = token    new_profile.save()    email_body = "http://"+request.get_host()+"/grumblr/activate?user_pk="+str(new_user.pk)+"&confirm_token="+token    send_mail(subject="Verify your email address",              message=email_body,              from_email="yyin3@andrew.cs.cmu.edu",              recipient_list=[new_user.email])    return render(request, 'grumblr/needs-confirmation.html', context)@login_requireddef profile(request, pk):    context = {}    try:        pk_int = int(pk)    except:        raise Http404    p_user = get_object_or_404(User, pk=pk)    posts = Post.objects.filter(user=p_user).order_by('-date')    context['posts'] = posts    context['p_user'] = p_user    user_self = get_object_or_404(Profile, user_id=request.user.id)    user_follow = get_object_or_404(User, pk=pk)    if 'follow' in request.POST:        if not user_self.follow.filter(pk=pk):            user_self.follow.add(user_follow)            status = "Unfollow"        else:            user_self.follow.remove(user_follow)            status = "Follow"    else:        if user_self.follow.filter(pk=pk):            status = 'Unfollow'        else:            status = "Follow"    context['status'] = status    return render(request, './grumblr/profile.html', context)@login_requireddef profile_self(request):    try:        p_user = User.objects.get(pk=request.user.pk)    except ObjectDoesNotExist:        return redirect('/')    posts = Post.objects.filter(user=p_user).order_by('-date')    return render(request, './grumblr/profile.html', {'posts': posts, 'p_user': p_user})@login_required@transaction.atomicdef edit_profile(request):    if request.method == 'GET':        form_user = UserForm(instance=request.user)        form_profile = ProfileForm(instance=request.user.profile)  # Creates form from the        context = {'form_profile': form_profile,'form_user': form_user}          # existing entry.        return render(request, './grumblr/edit_profile.html', context)    # if method is POST, get form data to update the model    form_user = UserForm(request.POST, instance=request.user)    form_profile = ProfileForm(request.POST, request.FILES, instance=request.user.profile)    context = {'form_profile': form_profile, 'form_user': form_user}    if not form_user.is_valid():        return render(request, './grumblr/edit_profile.html', context)    form_profile.fields['age'].required = False    if not form_profile.is_valid():        return render(request, './grumblr/edit_profile.html', context)    form_user.save()    form_profile.save()    message = "Profile changed."    context['message'] = message    return render(request, './grumblr/edit_profile.html', context)@login_requireddef change_password(request):    message = ""    if request.method == 'POST':        form = PasswordChangeForm(request.user, data=request.POST)        if form.is_valid():            form.save()            update_session_auth_hash(request, form.user) # dont logout the user.            message = "Password changed."            # return redirect("edit_profile")    else:        form = PasswordChangeForm(request.user)    context = {'form_password': form, 'message': message}    return render(request, "grumblr/change_password.html", context)@login_requireddef upload_photo(request, pk):    get_profile = get_object_or_404(Profile, user_id=pk)    # print(get_profile.photo)    if not get_profile.photo:        raise Http404    return HttpResponse(get_profile.photo)def follow_stream(request, pk):    context = {}    print(pk)    try:        pk_int = int(pk)    except ValueError:        raise Http404    user_self = get_object_or_404(Profile, user_id=pk)    p_user = get_object_or_404(User, pk=pk)    # except Profile.DoesNotExist:    #     redirect('login')    # except User.DoesNotExist:    #     redirect('login')    if 'follow' in request.POST:        if not user_self.follow.filter(pk=pk):            user_self.follow.add(p_user)            status = "Unfollow"        else:            user_self.follow.remove(p_user)            status = "Follow"    else:        if user_self.follow.filter(pk=pk):            status = 'Unfollow'        else:            status = "Follow"    whom = Profile.objects.get(user_id=pk).follow.all()    posts = []    for follower in whom:        post = Post.objects.filter(user=follower)        posts += post    posts.sort(key=lambda x: x.date, reverse=True)    context['posts'] = posts    context['p_user'] = p_user    context['status'] = status    return render(request, 'grumblr/follower.html', context)def activate_account(request):    if 'user_pk' in request.GET and 'confirm_token' in request.GET:        try:            check_user = Profile.objects.get(user_id=request.GET['user_pk'])            print(request.GET['user_pk'])            user = User.objects.get(id = request.GET['user_pk'])        except ObjectDoesNotExist:            return redirect('login')        else:            user_token = default_token_generator.make_token(user)            print(user_token)        print("check_user")        print(check_user.user_id)        if check_user:            try:                user_token = request.GET['confirm_token']                print(user_token)                print(check_user.confirm_token)            except ObjectDoesNotExist:                return redirect('login')            else:                if check_user.confirm_token == user_token:                    print(1)                    check_user.user.is_active = True                    check_user.user.save()                    login(request, check_user.user)                    return redirect('/')    return render(request, 'grumblr/needs-confirmation.html')def password_reset_done(request):    return render(request, 'grumblr/password_reset_sent.html')def password_reset_complete(request):    return render(request, 'grumblr/password_reset_done.html')