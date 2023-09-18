from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.shortcuts import redirect
from shopping import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_str
from . tokens import generate_token
from django.core.mail import EmailMessage , send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone
from . models import searched_product

# Create your views here.
def home(request):
    return render(request , "login/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST.get('username') # or username = request.['username'] both will work.
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request , "Username already exists! Please enter different username.")
            return redirect('home')

        # if User.objects.filter(email = email):
        #     messages.error(request , "Email already registered! Please try different email address")
        #     return redirect('home')
        
        if len(username) > 10 :
            messages.error(request , "Usename must be under 10 characters")

        if pass1 != pass2 :
            messages.error(request , "Confirm Password didn't match! Please write the same password")

        if not username.isalnum():
            messages.error(request , "User should consists of alphabets and numbers only.")

            return redirect('home')

        myuser = User.objects.create_user(username , email , pass1)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.is_active = False
        myuser.save()

        messages.success(request , "Your account has been successfully created. We have also sent you a confirmation email. Please confirm it in order to activate your account.")


        # Welcome Email

        subject = "Welcome to ShOOping Login!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to ShOOping!! \nThank you for visiting our website \nWe have also sent you a confirmation email. Please confirm your email address in order to activate your account. \n \nThaking You \nEnjoy ShOOping!! "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject , message , from_email , to_list , fail_silently = True)


        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ ShOOping Login!!" 
        message2 = render_to_string('email_confirmation.html' , {
            'name' : myuser.first_name ,
            'domain' : current_site.domain ,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)) ,
            'token' : generate_token().make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email] ,
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request , "login/signup.html")

def signin(request):

    if request.method == "POST" :
        username = request.POST.get('username')
        pass1 = request.POST['pass1']
    
        user = authenticate(username=username , password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request , "login/index.html" , {'fname' : fname})
        else:
            messages.error(request , "Bad Credential")
            return redirect('home')

    return render(request , "login/signin.html")


def product_detail(request):

    # if request.method == "POST" :
    #     p_Id = request.POST['product_detail']

    #     product = searched_product(product_Id=p_Id , frequency =1)

    #     product.save()

    #     return render(request , "login/product_detail.html")
    
    # else:
    #     messages.error(request , "Some Error Occured")
    #     return render(request , "login/index.html")

    products = {
        'p_name' : "Samsung Qled 8k TV" ,
        'p_size, ' : [ {"size" : "45 inch"  , 'price' : 45000 } , {"size" : "55 inch"  , 'price' : 55000 } ,
        {"size" : "85 inch"  , 'price' : 85000 }  ]
    }
    return render(request , "login/product_detail.html" , products)


def signout(request):
    logout(request)
    messages.success(request , "Logged Out Successfully")
    return redirect('home')


def activate(request, uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk = uid)
    except (TypeError , ValueError , OverflowError , User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token().check_token(myuser , token):
        myuser.is_active = True
        myuser.save()
        login(request , myuser)
        return redirect('home')
    else :
        return render(request , 'activation_failed.html')
    
def company(request , company_name):
    return HttpResponse(f"Welcome to SMI { company_name }")