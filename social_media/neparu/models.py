from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import datetime
import os

class User(AbstractUser):
    A = ''
    a = 'AB+'
    b = 'AB-'
    c = 'A+'
    d = 'A-'
    d = 'B+'
    e = 'B-'
    f = 'O+'
    g = 'O-'

    group = [
         (A,''),(a ,'AB+'),(b, 'AB-'),(c , 'A+'),(d , 'A-'),(d , 'B+'),(e , 'B-'),( f , 'O+'),( g , 'O-')
    ]
    first_name = models.CharField(('first name'),max_length=30,blank=False)
    last_name = models.CharField(('last name'),max_length=30,blank=False)
    email = models.EmailField(('email address'), unique=True,blank=False)
    photo = models.ImageField(upload_to='profile',default='profile/avtar.jpg')
    bio  = models.CharField(max_length=100,blank=True)
    account_type  = models.CharField(max_length=15,default='public')
    following  =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='user_following')
    follower  =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='user_follower')
    blood_group =models.CharField(max_length=5,blank=True,choices=group,default=A)




# User.add_to_class('photo', models.ImageField(upload_to='profile',default='profile/avtar.jpg'))
# User.add_to_class('bio', models.CharField(max_length=255,blank=True))
# User.add_to_class('account_type', models.CharField(max_length=255,default='public'))
# User.add_to_class('following',models.ManyToManyField(User,blank=True,related_name='user_following'))
# User.add_to_class('follower',models.ManyToManyField(User,blank=True,related_name='user_follower'))

class Post(models.Model):
    title = models.CharField(max_length=255)
    actor = models.ForeignKey(User,on_delete='CASCADE')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,blank=True,related_name='like_posts')
    report = models.ManyToManyField(User,blank=True,related_name='report_posts')
    def __str__(self):
        return self.title

class Photo(models.Model):
    photo = models.ImageField(upload_to='photos')
    post = models.ForeignKey(Post, on_delete='CASCADE',
                             related_name='my_photo')
  
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.photo.path):
            os.remove(self.photo.path)

        super(Photo, self).delete(*args,**kwargs)

class Comment(models.Model):
    content =models.CharField(max_length=255)
    actor =models.ForeignKey(User,on_delete='CASCADE')
    post = models.ForeignKey(Post,on_delete='CASCADE',related_name='my_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content



class Inbox(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver',null=True)
    feedback_receiver = models.ManyToManyField(User,blank=True,related_name='feedback_receiver')
    image = models.ImageField(upload_to='message',null=True,blank='true')
    message = models.CharField(max_length=1000,null=True,blank='true')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return self.sender.username
    
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super(Inbox, self).delete(*args,**kwargs)



class Rental(models.Model):
    title =models.CharField(max_length=15,blank=False)
    price =models.IntegerField(blank=False)
    space_no =models.IntegerField(blank=False)
    description =models.TextField(max_length=1000,blank=False)
    location  =models.CharField(max_length=125,blank=False)
    actor =models.ForeignKey(User,on_delete='CASCADE',related_name='rental_actor')
    bookedby = models.ManyToManyField(User,blank=True,related_name='bookedby')
    book_accepted = models.ManyToManyField(User,blank=True,related_name='book_accepted')
    published_date =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


    
class RentalPhoto(models.Model):
    photo = models.ImageField(upload_to='rental')
    rental = models.ForeignKey(Rental, on_delete='CASCADE',related_name='rentalphoto')

    def delete(self,*args,**kwargs):
        if os.path.isfile(self.photo.path):
            os.remove(self.photo.path)

        super(RentalPhoto, self).delete(*args,**kwargs)

        

class Notification(models.Model):
    A = ''
    a = 'AB+'
    b = 'AB-'
    c = 'A+'
    d = 'A-'
    d = 'B+'
    e = 'B-'
    f = 'O+'
    g = 'O-'

    group = [
         (A,''),(a ,'AB+'),(b, 'AB-'),(c , 'A+'),(d , 'A-'),(d , 'B+'),(e , 'B-'),( f , 'O+'),( g , 'O-')
    ]
    
    content =models.CharField(max_length=255,blank=True)
    receiver=models.ManyToManyField(User,related_name='notification_receiver')
    actor =models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_actor')
    post = models.ForeignKey(Post,on_delete='CASCADE',related_name='my_notification',blank=True,null=True)
    rental = models.ForeignKey(Rental,on_delete='CASCADE',related_name='my_rental',blank=True,null=True)
    action = models.CharField(max_length=25,blank=False)
    blood_group = models.CharField(max_length=10,blank=True,choices=group,default=A)
    description = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=125,blank=True)
    blood_available=models.ManyToManyField(User,blank= True,related_name='blood_responder')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return self.action

    class Meta:
        ordering = ('-created_at',)






