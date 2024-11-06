from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.shortcuts import render, redirect
from .models import User_DB,admin_add_auction_items,Bid
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def homePage(request):
    auction_items = admin_add_auction_items.objects.all()
    
    return render(request, 'home.html', {'auction_items': auction_items})
# authenticate API'S work
def handlesignup(request):
    if request.method=='POST':
        #get post parqmeters
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        bio=request.POST['bio']
        website=request.POST['website']
        insta=request.POST['insta']
        linkedin=request.POST['linkedin']
        twitter=request.POST['twitter']
        other=request.POST['other']

        #no errors part
        if len(username)>12:
            messages.warning(request, "Your username must be under 12 characters. Please create an appropriate one")
            return redirect('bloghome')
        count_uup=0
        for s in username:
            if s.isupper():
                count_uup+=1
                break
            
        if not username.isalnum() or count_uup != 0:
            messages.warning(request, "Your username must be alphanumeric and lowecase only! Please create an appropriate one")
            return redirect('bloghome')
        if pass1!=pass2:
            messages.warning(request, "Your passwords dont match. Please enter same password for verification")
            return redirect('bloghome')
            print(pass1)
        count_pnum=0
        count_pal=0
        for s in pass1:
            if s.isnumeric():
                count_pnum+=1
            if s.isalpha():
                count_pal+=1
        if not count_pal and not count_pnum:
            messages.warning(request, "Password criteria not match. Please enter password with alphabets and numbers")
            return redirect('bloghome')
            
        # create user
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        profile=User_DB(username=username,bio=bio, website=website,insta=insta, linkedin=linkedin, twitter=twitter, other=other)
        profile.save()
        messages.success(request, "Your account has been created successfully")
        return redirect('/blog')
    else:
        return HttpResponse('404 - Not found')
def userlogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In!")
            return redirect("bloghome")
        else:
            messages.error(request, "Invalid Credentials, please try again")
            return redirect("bloghome")
    return HttpResponse('ERROR 404-not found')

def userlogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("/blog")
def profile(request):
    
    user = request.user
    theuser=User_DB.objects.filter(username=user).first()
    print(user, theuser)
    pid=theuser.profile_id
    print(pid)
    return render(request, 'blog/profile.html',{'user':user, 'pid':pid})



def updateProfile(request):
    if request.method == "POST":
        new_name = request.POST.get("newName")
        new_password = request.POST.get("newPassword")
        
        user_profile = User_DB.objects.get(id=request.user.id)

        user_profile.name = new_name
        user_profile.password = new_password
        user_profile.save()
        
        auction_items = admin_add_auction_items.objects.all()

        return render(request, 'home.html',{'name': new_name, 'password': new_password,'auction_items': auction_items})

    return render(request, 'signinForm.html')

def place_bid(request):
    if request.method == 'POST':
        bid_value = request.POST.get('bid')
        item_id = request.POST.get('item_id')
        
        user = User_DB.objects.get(id=1)
        
        auction_item = admin_add_auction_items.objects.get(id=item_id)
        
        highest_bid = Bid.objects.filter(auction_item=auction_item).order_by('-bid_amount').first()
        
        if not highest_bid or int(bid_value) > highest_bid.bid_amount:
            bid = Bid(user=user, auction_item=auction_item, bid_amount=bid_value)
            bid.save()
            
        else:
            pass
        
        user_profile = User_DB.objects.get(id=user.id)
        
        auction_items = admin_add_auction_items.objects.all()
        
        return render(request, 'home.html', {
            'name': user_profile.name,
            'password': user_profile.password,
            'available_tokens': user_profile.tokens,
            'auction_items': auction_items,
            'highest_bid':highest_bid
        })

    return redirect('signinForm.html')  
