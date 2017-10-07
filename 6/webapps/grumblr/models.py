from django.db import models
from django.db.models import Max
from django.utils.html import escape

from django.contrib.auth.models import User
from django.db.models import CASCADE
from django.utils import timezone


class Post(models.Model):

    user = models.ForeignKey(User)
    text = models.CharField(max_length=42,  default='', blank=True)
    date = models.DateTimeField(default=timezone.now)

    # # Returns all recent additions and deletions to the to-do list.
    # @staticmethod
    # def get_changes(time="1970-01-01T00:00+00:00"):
    #     return Post.objects.filter(date__gt=time).distinct()
    #
    # # Returns all recent additions to the to-do list.
    # @staticmethod
    # def get_posts(time="1970-01-01T00:00+00:00"):
    #     return Post.objects.filter(date__gt=time).distinct()

    # Generates the HTML-representation of a single to-do list item.
    @property
    def html(self):
        return "<div class='row posts-box'><div class='row'><div class='col-xs-3 col-md-2'> \
               <img class='head' src='/grumblr/photo/%(post_user_pk)d' ></div><div class='col-sm-9'> \
               <p class='id-title'><a href='profile/%(post_user_pk)d'>@%(post_user)s</a></p> \
               <p class='post-date'>%(post_date)s</p></div></div><div class='row'><p class='post-content'>\
               %(post_text)s </p></div><div class='row'><form method='post'>\
               <input class='form-control' name='text' id='text' type='text' placeholder='Comment here :)'>\
               <button id='%(post_pk)d' class='btn btn-sm comment-submit' type='submit'>Submit</button>\
               <input type='hidden' id='comment-user' name='user' value=''>\
               <input id='comment_csrf' type='hidden' name='csrfmiddlewaretoken' value=''>\
               </form></div><div id='comment-area-%(post_pk)d'></div></div>" \
               % {'post_user_pk': self.user.pk, 'post_text': escape(self.text), 'post_user': escape(self.user),
                  'post_date': escape(self.date.ctime()), 'post_pk': self.pk}


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    text = models.CharField(max_length=100, default='')
    date = models.DateTimeField(default=timezone.now)

    @property
    def html(self):
        return "<div class='row comment-box'><div class='col-xs-3 col-md-2'>\
               <img class='head' src='/grumblr/photo/%(comment_user_pk)d'></div>\
               <div class='col-sm-2'><p class='id-title'><a href='profile/%(comment_user_pk)d'>\
               @%(comment_user)s</a></p><p class='post-date'>%(comment_date)s</p></div>\
               <div class='col-sm-7'><p class='comment-content'>%(comment_text)s</p></div></div>" \
               % {'comment_user_pk': self.user.pk, 'comment_text': escape(self.text), 'comment_user': escape(self.user),
                  'comment_date': escape(self.date.ctime())}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    bio = models.TextField(max_length=420, default='', blank=True)
    age = models.SmallIntegerField(default=0, blank=True)
    photo = models.ImageField(upload_to="img", blank=True)

    follow = models.ManyToManyField(User, related_name="follow_user")

    confirm_token = models.CharField(max_length=100, default='', blank=True)
