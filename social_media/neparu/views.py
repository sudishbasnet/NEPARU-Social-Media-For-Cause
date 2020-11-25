from django.shortcuts import render, HttpResponseRedirect, redirect
from neparu import forms,models,serializers
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.utils import timezone
import json




@login_required(login_url='/auth/login')
def home(request):
    uprofile = forms.UploadProfile() 
    post=models.Post.objects.order_by('-uploaded_at')
    # to delete notification after 1 week
    time = timezone.now()-timezone.timedelta(hours=168)
    models.Notification.objects.filter(created_at=time).delete()
    if not request.user:
        return redirect('/auth/login/')
    if request.user.is_staff ==True:
        return redirect('/neparu/admin/none/none/0')
    data ={
          'uprofile':uprofile,
          'post':post,
          'name':'Postfeed',
        }
    return render(request,'postfeed.html',data)


def gallery(request,post=None):
    if post!= '0':
        post = models.Post.objects.filter(id=post)
        d = {
            'post': post
        }
    else :
        post = models.Post.objects.filter(actor=request.user).order_by('-uploaded_at')
        d = {
            'post': post,
            'name': 'Gallery'
        }
    return render(request, 'postfeed.html', d)


@login_required(login_url='/auth/login')
def sathiharu(request):
    if request.is_ajax():
        sathiharu = models.User.objects.filter(username__icontains=request.GET.get("q")).exclude(is_staff=True)
        if  request.GET.get("a")=='1':
            html = render_to_string(template_name="msgusers.html", context={"sathiharu": sathiharu,"user":request.user}                        )
            data = {"html_view": html}
        elif request.GET.get("a")=='0' :
            html = render_to_string(template_name="user_list.html", context={"sathiharu": sathiharu,"user":request.user}                        )
            data = {"html_view": html}
        elif request.GET.get("a")=='admin' :
            user = models.User.objects.filter(username__icontains=request.GET.get("q"))
            html = render_to_string(template_name="admintable.html", context={"users": user})
            data = {"html_view": html}
        return JsonResponse(data=data, safe=False)
    else :
        sathiharu = ""

    return render(request, "sathiharu.html")


@login_required(login_url='/auth/login')
def rental(request,rentalid=None):
    response_data = {}
    # search rental spaces
    if request.is_ajax():
        if request.POST.get("action") == 'book':
            rental = models.Rental.objects.get(pk=request.POST.get('rental'))
            if (request.user in rental.bookedby.all()):
                rental.bookedby.remove(request.user)
                models.Notification.objects.filter(rental=rental,receiver=request.user).delete()
                response_data['result'] = ''
            else:
                rental.bookedby.add(request.user)
                response_data['result'] = 'book'
        elif request.POST.get("action") == 'bookings':
            content = 'have confirmed your booking for space please contact the owner or the user who posted. Thank You !'
            user = models.User.objects.get(pk=request.POST.get('id'))
            rental = models.Rental.objects.get(pk=request.POST.get('rental'))
            if (user in rental.book_accepted.all()):
                models.Notification.objects.filter(rental=rental,receiver=user).delete()
                rental.book_accepted.remove(user)
                response_data['result'] = ''
            else:
                notification = models.Notification(content=content,actor=request.user,rental=rental,action='rental')
                notification.save()
                notification.receiver.add(user)
                rental.book_accepted.add(user)
                response_data['result'] = 'bookings'
        elif request.POST.get('price'):
            response = models.Rental.objects.get(id=rentalid)
            form = forms.Rental(request.POST or None, instance=response)
            if form.is_valid():
                form.save()
            response_data['title'] = response.title
            response_data['description'] = response.description
            response_data['space_no'] = response.space_no
            response_data['price'] = response.price
            response_data['location'] = response.location

        elif request.POST.get('action') == 'photo':
           models.RentalPhoto.objects.get(id=rentalid).delete()

        elif request.POST.get("action") == 'delete':
            query =models.Rental.objects.get(pk=request.POST.get("id"))
            models.RentalPhoto.objects.filter(rental=query).delete()
            models.Notification.objects.filter(rental=query).delete()
            query.delete()

        else:
            if request.GET.get("u")  == 'Booked':
                rental = models.Rental.objects.filter(title__icontains=request.GET.get("q"),space_no__icontains=request.GET.get("s"),location__icontains=request.GET.get("t"),bookedby=request.user)
            elif request.GET.get("r")  == '':
                rental = models.Rental.objects.filter(title__icontains=request.GET.get("q"),space_no__icontains=request.GET.get("s"),location__icontains=request.GET.get("t"))
            else:
                rental = models.Rental.objects.filter(title__icontains=request.GET.get("q"),price__lte=request.GET.get("r"),space_no__icontains=request.GET.get("s"),location__icontains=request.GET.get("t"))
            html = render_to_string(template_name="rental.html", context={"rentaldetails": rental,'user':request.user})
            data = {"html_view": html}
            return JsonResponse(data=data, safe=False)
        return HttpResponse(json.dumps(response_data),content_type="application/json")


    # upload spaces
    elif request.POST.get("title"):
        upload = models.Rental(title=request.POST.get("title"),price=request.POST.get("price"),space_no=request.POST.get("space_no"),description=request.POST.get("description"),location=request.POST.get("location"),actor=request.user)
        upload.save()
        files = request.FILES.getlist('photo')
        rental=models.Rental.objects.latest('id')    
        for f in files:
            uFile = models.RentalPhoto(rental=rental, photo=f)
            uFile.save()

    if rentalid == '0':
        rentaldetails = models.Rental.objects.filter(actor=request.user)
    else:
        rentaldetails = models.Rental.objects.filter(id=rentalid)
    return render(request, "rentalservice.html",{'rentaldetails':rentaldetails,'user':request.user})





@login_required(login_url='/auth/login')
def addProfile(request):
    if request.method == 'POST' and request.FILES['profileimage']:
        details = models.User.objects.get(username=request.user)
        details.photo =request.FILES['profileimage']
        details.save()
        return redirect('/neparu')




def signup(request,action):
    name="SignUp"
    if action=="update":
        details =models.User.objects.get(username=request.user)
        form = forms.SignUpFormUpdate(request.POST or None, instance=details)
        name ="Update Info"
        if form.is_valid():
            form.save()
            return redirect('/neparu')
    elif request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/neparu')
    else:
        form = forms.SignUpForm()
    data ={
        'form' :form,
        'name' :name
        }
    return render(request,'signup.html',data)


@login_required(login_url='/auth/login')
def UploadPost(request):
    if request.POST.get('id'):
        response = models.Post.objects.get(id=request.POST.get('id'))
        form = forms.UploadPost(request.POST or None, instance=response)
        if form.is_valid():
            form.save()
        response_data = {}
        response_data['title'] = response.title
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        if request.method == 'POST':
            title = request.POST.get("title")
            uPost = models.Post(title=title, actor=request.user)
            uPost.save()
            files = request.FILES.getlist('photo')
            post=models.Post.objects.latest('id')    
            for f in files:
                uFile = models.Photo(post=post, photo=f)
                uFile.save()
            return redirect('/neparu/gallery/0')
        else:
            return render(request,'upost.html')


@login_required(login_url='/auth/login')
def comment(request):
    if request.method=='POST':
        post = models.Post.objects.get(pk=request.POST.get('feed'))
        actor = request.user
        content = 'Commented on your Post'
        receiver = post.actor
        models.Comment.objects.create(
            content=request.POST.get('content'),
            actor=request.user,
            post=post
        )
        if receiver != request.user :
            notification = models.Notification(content=content,actor=actor,post=post,action='comment')
            notification.save()
            notification.receiver.add(post.actor)
        response =models.Comment.objects.latest('id')
        response_data = {}
        response_data['content'] = response.content
        response_data['post'] = 'com'+str(post.id)
        response_data['actor'] = response.actor.username
        response_data['actorid'] = response.actor.id
        response_data['comment'] =response.id
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
        )


@login_required(login_url='/auth/login')
def delComment(request):
    try:
        if request.method == 'POST':
            comment = models.Comment.objects.get(pk=request.POST.get('id'))
            actor = request.user
            content = 'Commented on your Post'
            receiver = comment.post.actor
            post=comment.post
            models.Notification.objects.filter(actor=actor,content=content,receiver=receiver,post=post,action='comment').delete()
            comment.delete()
            response_data = {}
            response_data['success'] = 'success'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"cannot delete comment right now"}),
        )


@login_required(login_url='/auth/login')
def deleteimg(request):
    try:
        if request.method == 'POST':
            photo = models.Photo.objects.get(pk=request.POST.get('id'))
            photo.delete()
            response_data = {}
            response_data['success'] = 'success'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"cannot delete comment right now"}),
        )


@login_required(login_url='/auth/login')
def deleteReportPost(request):
    if request.method == 'POST':
        pid =request.POST.get('id')
        response_data = {}
        postss =models.Post.objects.get(pk=pid)
        if request.POST.get('action') == 'delete':
            models.Notification.objects.filter(post=pid).delete()
            models.Photo.objects.filter(post=pid).delete()
            models.Comment.objects.filter(post=pid).delete()
            postss.delete()
        elif request.POST.get('action') == 'report':
            if (models.Post.objects.filter(pk=pid, report=request.user)):
                request.user.report_posts.remove(postss)
                response_data['report'] ='Report'
            else:
                request.user.report_posts.add(postss)
                response_data['report'] ='Cancel Report'
                if(postss.report.count() > (postss.actor.follower.count()/100*20)):
                    models.Notification.objects.filter(post=pid).delete()
                    models.Photo.objects.filter(post=pid).delete()
                    models.Comment.objects.filter(post=pid).delete()
                    postss.delete()
                    response_data['action']='remove'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"cannot delete post right now"}),
        )


@login_required(login_url='/auth/login')
def like(request):
    try: 
        if request.method=='POST':
            response_data = {}
            post = models.Post.objects.get(pk=request.POST.get('id'))
            actor = request.user
            content = 'liked your post'
            postid =post.id
            if (models.Post.objects.filter(pk=request.POST.get('id'), like=request.user)):
                request.user.like_posts.remove(post)
                response ="fa fa-heart-broken"
                if post.actor != request.user :
                    models.Notification.objects.filter(actor=actor,content=content,receiver=post.actor,post=postid,action='like').delete()

            else:
                request.user.like_posts.add(post) 
                response ="fa fa-heart"
                if post.actor != request.user :
                    notification = models.Notification(content=content,actor=actor,post=post,action='like')
                    notification.save()
                    notification.receiver.add(post.actor)

            response_data['like'] = post.like.count()
            response_data['id'] =post.id
            response_data['span'] = response
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"cannot like post right now"}),
        )
    
@login_required(login_url='/auth/login')
def blood(request):
    try: 
        response ={}
        if request.method=='POST':
            if request.POST.get('notification_id'):
                editnotification = models.Notification.objects.get(id=request.POST.get('notification_id'))
                if request.POST.get('cancel_blood'):
                    editnotification.delete()
                elif request.user in editnotification.blood_available.all():
                    editnotification.blood_available.remove(request.user)
                    response['action']='add'
                else:
                    editnotification.blood_available.add(request.user)
                    response['action']='remove'
                    
            else:
                model =models.Notification.objects.filter(actor=request.user,action='blood')
                if (model):
                    response['warn']='yes'
                else:
                    bloodgroup =request.POST.get('bloodgroup')
                    if str(request.POST.get('description')) =='':
                        content = 'Blood needed urgently please reply this thread as soon as possible. Thank you'
                    else:
                        content =''
                    notification = models.Notification(content=content,actor=request.user,action='blood',blood_group=bloodgroup,description=request.POST.get('description'),location=request.POST.get('location'))
                    notification.save()
                    if bloodgroup =='':
                        users = models.User.objects.all().exclude(pk=request.user.id)
                    else:
                        users = models.User.objects.filter(blood_group=bloodgroup).exclude(pk=request.user.id)|models.User.objects.filter(blood_group='').exclude(pk=request.user.id)
                    notification.receiver.set(users)

            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"feature isn't available"}),
        )

        
@login_required(login_url='/auth/login')
def follow(request):
    if request.method=='POST':
        followuser = models.User.objects.get(username=request.POST.get('followuser'))
        eduser = models.User.objects.get(username=request.user)
        if (models.User.objects.filter(username=request.user,following=followuser)):
            content = 'Unfollowed you'
            models.Notification.objects.filter(actor=request.user,receiver=followuser,action='follow').delete()
            followuser.user_following.remove(eduser)
            eduser.user_follower.remove(followuser)
            
        else:
            models.Notification.objects.filter(actor=request.user,receiver=followuser,action='follow').delete()
            content = 'Started following you'
            followuser.user_following.add(eduser) 
            eduser.user_follower.add(followuser)

        notification = models.Notification(content=content,actor=request.user,action='follow')
        notification.save()
        notification.receiver.add(followuser)
        return redirect(request.POST.get('url')) 
        

@login_required(login_url='/auth/login')
def user(request,id):
    user = models.User.objects.get(pk=id)
    post = models.Post.objects.filter(actor=id)
    data={
        'user':user,
        'post':post,

    }
    return render(request,'user.html',data)


@login_required(login_url='/auth/login')
def followers(request,action,id):
    users = models.User.objects.get(pk=id)
    if action=='following':
        data={
            'users':users.following.all,
            'name':'Following'
        }
    else:
        data={
            'users':users.follower.all,
            'name':'Followers'
        }
    return render(request,'followers.html',data)




#chat app
@csrf_exempt
@login_required(login_url='/auth/login')
def inbox(request, sender=None, receiver=None):
    if request.POST.get("action"):
        checkimg = models.Inbox.objects.filter(sender_id=request.POST.get("sender"), receiver_id=request.POST.get("receiver")).latest('id')
        response = {}
        if checkimg:
            response['url']=checkimg.image.url
        else:
            response['url']=''
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif request.method == 'GET':
        inboxcontent = models.Inbox.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = serializers.Inbox(inboxcontent, many=True, context={'request': request})
        for msg in inboxcontent:
            msg.is_read = True
            msg.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        message = request.POST.get("message")
        receiver =models.User.objects.get(username=request.POST.get("receiver"))
        files = request.FILES.getlist('image')
        if message or files :
            readmsg = models.Inbox.objects.filter(sender=request.user,receiver=receiver)
            for msg in readmsg:
                msg.is_read = True
                msg.save()

        if files:
            for f in files:
                msg = models.Inbox(sender=request.user, receiver=receiver,message=message,image=f)
                msg.save()
        else:
            msg = models.Inbox(sender=request.user, receiver=receiver,message=message)
            msg.save()
        response = {}
        imgrep =models.Inbox.objects.latest('id')
        if imgrep.image:
            response['imgurl'] = imgrep.image.url
        return HttpResponse(json.dumps(response),content_type="application/json")


@login_required(login_url='/auth/login')
def msg(request):
    if request.method == "GET":
        data ={
            'unread':models.Inbox.objects.filter(receiver=request.user,is_read=False).order_by('-created_at')
        }
        return render(request, 'online.html',data)





@login_required(login_url='/auth/login')
def msg_details(request, sender, receiver):
    if request.method == "GET":
        sender= models.User.objects.get(id=sender)
        receiver= models.User.objects.get(id=receiver)
        inboxcontent = models.Inbox.objects.filter(sender_id=sender, receiver_id=receiver)|models.Inbox.objects.filter(sender_id=receiver, receiver_id=sender)
        for msg in inboxcontent:
            msg.is_read = True
            msg.save()
        data ={
            'sender': sender,
            'receiver': receiver,
            'inboxcontent': inboxcontent
        }
        return render(request, "msg.html",data)



@login_required(login_url='/auth/login')
def Feedback(request):
    if request.method == 'POST':
        response = {}
        msg = models.Inbox(message=request.POST.get('feedback'),sender=request.user).save()
        msg1 = models.Inbox.objects.latest('id')
        msg = models.Inbox.objects.get(id=msg1.id)
        users = models.User.objects.filter(is_staff=True)
        for user in users:
            msg.feedback_receiver.add(user)
        return HttpResponse(json.dumps(response),content_type="application/json")
    return redirect('/neparu/')



@login_required(login_url='/auth/login')
def Notification(request):
    inboxcontent = models.Notification.objects.filter(receiver=request.user,is_read=False)
    serializer = serializers.Notification(inboxcontent, many=True, context={'request': request})
    for notification in inboxcontent:
        notification.is_read = True
        notification.save()
    return JsonResponse(serializer.data, safe=False)



@login_required(login_url='/auth/login')
def Admin(request,location,action,id):
    data = {}
    if request.user.is_staff == True :
        if location == 'users':
            form = forms.SignUpForm
            name = 'Users'
            user = models.User.objects.all()
            if action == "update":
                name = 'Update Information'
                details =models.User.objects.get(pk=id)
                form = forms.SignUpFormUpdate(request.POST or None, instance=details)
                title ="Update Information"
                if form.is_valid():
                    form.save()
                    return redirect('/neparu/admin/users/none/0')
                    
            elif action == 'delete':
                user = models.User.objects.get(pk=request.POST.get('id'))
                if user:
                    models.Notification.objects.filter(actor=user).delete()
                    posts = models.Post.objects.filter(actor=user)
                    for post in posts:
                        models.Photo.objects.filter(post=post).delete()
                        models.Notification.objects.filter(post=post).delete()
                        models.Comment.objects.filter(post=post).delete()
                    posts.delete()
                    rentals =  models.Rental.objects.filter(actor=user)
                    for rental in rentals:
                        models.RentalPhoto.objects.filter(rental=rental).delete()
                        models.Notification.objects.filter(rental=rental).delete()
                    rentals.delete()
                    models.Inbox.objects.filter(sender=user).delete()
                    models.Inbox.objects.filter(receiver=user).delete()
                    user.delete()
                response_data = {}
                return HttpResponse(json.dumps(response_data),content_type="application/json")

            elif action == 'staff':
                name = 'Staff'
                user = models.User.objects.filter(is_staff=True)
                
            elif action == 'user':
                name = 'Neparu Users'
                user = models.User.objects.filter(is_staff=False)
            
            elif action == 'add':
                name = 'Add New User'
                if request.method == 'POST':
                    form = forms.SignUpForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect('/neparu/admin/users/none/0')
            data={
                'location' : 'users',
                'name' : name,
                'users' : user,
                'form' : form,
                'action' : action            
            }
        



        elif location == 'posts':
            details = ''
            form = ''
            name = 'Posts'
            post = models.Post.objects.all()
            if action == "update":
                name = 'Update Information'
                details =models.Post.objects.get(pk=id)
                form = forms.SignUpFormUpdate(request.POST or None, instance=details)
                title ="Update Information"
                if form.is_valid():
                    form.save()
                    return redirect('/neparu/admin/user/none/0')
                    
            elif action == 'delete':
                post = models.Post.objects.get(id=request.POST.get('id'))
                if post:
                    models.Photo.objects.filter(post=post).delete()
                    models.Notification.objects.filter(post=post).delete()
                    models.Comment.objects.filter(post=post).delete()
                    post.delete()
                response_data = {}
                return HttpResponse(json.dumps(response_data),content_type="application/json")
            
            elif action == "normal":
                name = 'Non Reported Posts'

            elif action == "report":
                name = 'Reported Posts'
            
            data={
                'location' : 'posts',
                'name' : name,
                'post' : post,
                'form' : form,
                'action' : action,
                'details' : details          
            }


        elif location == 'queries':
            name = 'Queries'
            queries = models.Inbox.objects.filter(feedback_receiver=request.user,is_read=False)
            data={
                'location' : 'queries',
                'name' : name,
                'queries' : queries,
                'action' : action            
            }



        elif location == 'blood':
            form = ''
            name = 'Blood Request'
            blood = models.Notification.objects.filter(action='blood')
            if action == "update":
                name = 'Update Information'
                details =models.Notification.objects.get(pk=id)
                form = forms.Blood(request.POST or None, instance=details)
                title ="Update Information"
                if form.is_valid():
                    form.save()
                    return redirect('/neparu/admin/blood/none/0')
                    
            elif request.is_ajax():
                models.Notification.objects.get(pk=request.POST.get('id')).delete()
                response_data = {}
                return HttpResponse(json.dumps(response_data),content_type="application/json")
            
            data={
                'location' : 'blood',
                'name' : name,
                'bloods' : blood,
                'form' : form,
                'action' : action            
            }


        elif location == 'rental':
            form = ''
            name = 'Rental Service'
            rental = models.Rental.objects.all()
            if action == "update":
                name = 'Update Information'
                details =models.Rental.objects.get(pk=id)
                form = forms.Rental(request.POST or None, instance=details)
                title ="Update Information"
                if form.is_valid():
                    form.save()
                    return redirect('/neparu/admin/rental/none/0')
                    
            elif request.is_ajax():
                rental = models.Rental.objects.get(id=request.POST.get('id'))
                if rental and location == 'rental':
                    models.RentalPhoto.objects.filter(rental=rental).delete()
                    models.Notification.objects.filter(rental=rental).delete()
                    rental.delete()
                response_data = {}
                return HttpResponse(json.dumps(response_data),content_type="application/json")
            
            data={
                'location' : 'rental',
                'name' : name,
                'rentals' : rental,
                'form' : form,
                'action' : action            
            }




        else:
            form = forms.Notification
            name = 'Notification'
            notifiction = models.Notification.objects.filter(actor=request.user)
            if action == "update":
                name = 'Update Notification'
                details =models.Notification.objects.get(pk=id)
                form = forms.Notification(request.POST or None, instance=details)
                title ="Update Notification"
                if form.is_valid():
                    form.save()
                    return redirect('/neparu/admin/dashboard/none/0')
                    
            elif request.is_ajax():
                models.Notification.objects.get(pk=request.POST.get('id')).delete()
                response_data = {}
                return HttpResponse(json.dumps(response_data),content_type="application/json")
            
            elif action == 'add':
                name = 'Add New Notification'
                if request.method == 'POST':
                    notification = models.Notification(description=request.POST.get("description"),actor=request.user,action='neparu')
                    notification.save()
                    users = models.User.objects.all().exclude(is_staff=True)
                    for user in users:
                        notification.receiver.add(user)
                    return redirect('/neparu/admin/dashboard/none/0')


            use = models.User.objects.all()
            vis = models.User.objects.filter(is_staff=False)
            sta = models.User.objects.filter(is_staff=True)
            anim = models.Notification.objects.filter(action='blood')
            spon = models.Rental.objects.all()
            rep = models.Post.objects.filter(report=True).all()


            nepuser = (vis.count()/use.count())*100
            reports = (rep.count()/use.count())*100
            bloodreq   = (anim.count()/use.count())*100
            staffper     = (sta.count()/use.count())*100
            rentalrate   = (spon.count()/use.count())*100

            sa = models.User.objects.all().count()
            ca = models.Post.objects.all().count()
            na = models.Comment.objects.all().count()
            da = models.Photo.objects.all().count()+models.RentalPhoto.objects.all().count()



            data={
                'location' : 'dashboard',
                'name' : name,
                'notifications' : notifiction,
                'form' : form,
                'action' : action,
                'nepuser' : nepuser,
                'reports' : reports,
                'bloodreq' : bloodreq,
                'staffper' : staffper,
                'rentalrate' : rentalrate,
                'sa' : sa,
                'ca' : ca,
                'na' : na,
                'da' : da,         
            }
    return render(request, "admin.html",data)
