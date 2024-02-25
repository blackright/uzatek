from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from .models import Contact

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

def services(request):
  return render(request, 'services.html')
  
@csrf_exempt
def contact(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    number = request.POST.get('number')
    message = request.POST.get('message')
    subject = request.POST.get('subject')
    print(f'{name} and {email} and {number} and {message} and {subject}')
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    data = request.POST

    # Load the HTML template
    html_content = render_to_string('welcome_email.html', {'context_variable': 'THis is a test'})

    # Create the text content by stripping the HTML
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    if msg.send():
      
      #Save the data to the database
      form_save = Contact.objects.create(name=data['name'], email=data['email'], number=data['number'], message=data['message'], subject=data['subject'])
      if form_save:
        form_save.save()
      else:
        print("False")
        
      success_message = "Email Sent Successfully"
      return render(request, 'contact.html', {'success_ message' : success_message })
    else:
      print("Email Not sent")
      
  context = {
    'number'   : '+36 20 211 5165',
    'email'    :  'info@uzatek.com',
    'address'  :  'Budapest, Thököly út 7, Hungary'
  }
  
  return render(request, 'contact.html', context)