from django.conf.urls import url
import django.contrib.auth.views

import grumblr.views

urlpatterns = [

    url(r'^$',grumblr.views.home, name='home'),
    url(r'^register', grumblr.views.register, name='register'),
    url(r'^profile$', grumblr.views.profile_self, name='profile_self'),
    url(r'^profile/(?P<pk>[0-9]+)/$', grumblr.views.profile, name='profile'),
    url(r'^edit_profile$', grumblr.views.edit_profile, name='edit_profile'),
    url(r'^change_password$', grumblr.views.change_password, name='change_password'),
    url(r'^photo/(?P<pk>[0-9]+)/$', grumblr.views.upload_photo, name='photo'),
    url(r'^follow/(?P<pk>[0-9]+)/$', grumblr.views.follow_stream, name='follow_stream'),
    url(r'^activate', grumblr.views.activate_account, name='activate_account'),

    url(r'^password_reset/$', django.contrib.auth.views.password_reset,
        {"template_name": "grumblr/password_reset_start.html",
         "post_reset_redirect": "done/",
         "email_template_name": "grumblr/password_reset_email.html"},
        name='password_reset'),
    url(r'password_reset/done/$', grumblr.views.password_reset_done),

    url(r'reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',
        django.contrib.auth.views.password_reset_confirm,
        {"template_name": "grumblr/password_reset_change.html",
         "post_reset_redirect": "password_reset_complete"},
        name="password_reset_confirm"),
    url(r'^reset-done', grumblr.views.password_reset_complete, name='password_reset_complete'),

]
