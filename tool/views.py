import os
import tempfile
import uuid
import zipfile

from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.helpers import send_mail_sendinblue
from accounts.models import UserAPIKey, StripeCustomer
from config import settings
from tool.forms import ImageForm, ImageFormZip, ContactForm
from tool.models import ImageUpload
from tool.permissions import HasValidAPIKey
from tool.serializers import ImageSerializer


def display_index(request: HttpRequest):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            if request.user.is_authenticated:
                stripe_user_exists = StripeCustomer.objects.filter(user=request.user, stripe_subscription_status= True).exists()
                if not stripe_user_exists and request.user.credits < len(images):
                    return render(request, 'home/index.html',
                                  context={'form': form, 'max_images': True, 'nb_images_max': 100})
                batch_id = uuid.uuid4()
                for image in images:
                    img = ImageUpload(image=image)
                    img.user = request.user
                    img.batch = batch_id
                    img.save()
                request.user.credits -= len(images)
                request.user.save()

            else:
                #In case the user is not registered, we use the session key
                session_key = request.COOKIES.get('sessionid')
                print(f'Session key: {session_key}')
                images_already_uploaded = ImageUpload.objects.filter(session_key=session_key).exists()
                if images_already_uploaded:
                    images_already_uploaded_count = ImageUpload.objects.filter(session_key=session_key).count()
                    if images_already_uploaded_count + len(images) > 5:
                        return render(request, 'home/index.html', context={'form': form, 'max_images': True, 'nb_images_max': 5})
                batch_id = uuid.uuid4()
                for image in images:
                    img = ImageUpload(image=image)
                    img.session_key = session_key
                    img.batch = batch_id
                    img.anonymous_upload = True
                    img.save()
            return redirect('tool:upload', batch=batch_id)
        else:
            print(form.errors)
    return render(request, 'home/index.html', context={'form': form})


def upload_image(request: HttpRequest, batch: str) -> FileResponse or render:
    images = ImageUpload.objects.filter(batch=batch)
    form = ImageFormZip()
    if request.method == 'POST':
        form = ImageFormZip(request.POST, request.FILES)
        if form.is_valid():
            #We get all the images and generate a zip file
            #We return the zip file
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file_name = os.path.join(temp_dir, f'{batch}.zip')
                with zipfile.ZipFile(zip_file_name, 'w') as zipf:
                    for image in images:
                        file_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
                        zipf.write(file_path, os.path.basename(file_path))
                response = FileResponse(open(zip_file_name, 'rb'), as_attachment=True, filename=f'{batch}.zip')
                return response
        else:
            print(form.errors)
    return render(request, 'home/upload.html', context={'images': images})


def contact(request: HttpRequest) -> render:
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            #We send the email
            send_mail_sendinblue(
                template_id=4,
                to=os.getenv('EMAIL_HOST_USER'),
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                name=form.cleaned_data['name'],
                message=form.cleaned_data['message']
            )
            return redirect('tool:index')
        else:
            print(form.errors)
    return render(request, 'home/contact.html', context={'form': form})

@api_view(['POST'])
@permission_classes([HasValidAPIKey])
def api_image_view(request: Request) -> Response:
    if request.method == 'POST':
        print(request.headers)
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            #We're getting the user
            api_key_header = request.headers.get('Api-Key')
            user = UserAPIKey.objects.get(hashed_key=api_key_header).user
            img_upload = serializer.save()
            img_upload.user = user
            img_upload.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({'message': 'Not allowed'}, status=405)