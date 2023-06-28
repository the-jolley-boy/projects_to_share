from django.shortcuts import render, HttpResponseRedirect
from blog.models import Post
from django.core.mail import send_mail
from django.contrib import messages
import re

# Create your views here.
def index (request):
    blogs = Post.objects.all().order_by('-created_on')
    posts = blogs[:4]
    context = {
        "posts": posts,
    }
    return render(request, 'index.html', context)

def about (request):
    return render(request, 'about.html')

def contact (request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        invalid_imput = ['', ' ']
        if name in invalid_imput or email in invalid_imput or phone in invalid_imput or message in invalid_imput:
            messages.error(request, 'One or more fields are empty!')
        else:
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            phone_pattern = re.compile(r'^[0-9]{10}$')

            if email_pattern.match(email) and phone_pattern.match(phone):
                form_data = {
                'name':name,
                'email':email,
                'phone':phone,
                'message':message,
                }
                message = '''
                From:\n\t\t{}\n
                Message:\n\t\t{}\n
                Email:\n\t\t{}\n
                Phone:\n\t\t{}\n
                '''.format(form_data['name'], form_data['message'], form_data['email'],form_data['phone'])
                send_mail('You got mail!', message, email, ['kianjolley@gmail.com'])
                messages.success(request, 'Your message was sent.')
                #return HttpResponseRedirect('/thanks')
            else:
                messages.error(request, 'Email or Phone is Invalid!')
    return render(request, 'contact.html', {})