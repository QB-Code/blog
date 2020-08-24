import os
import tempfile

from PIL import Image
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from requests import get

from .randomcolor import RandomColor
from .tokens import email_confirm_token_generator

color_generator = RandomColor()


def send_email_confirmation(user):
    subject = 'Subject'
    context = {'token': email_confirm_token_generator.make_token(user=user),
               'user_id': user.pk}

    html_message = render_to_string('messages/email-confirm.html', context=context)
    plain_message = strip_tags(html_message)
    from_email = 'From <from@example.com>'

    mail.send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)


def set_default_user_pic(my_user, username):
    background_color = color_generator.generate()[0][1:]
    initials = "".join([string[0] for string in username.split()])

    response = get(url=f'https://eu.ui-avatars.com/api/?size=128&font-size=0.7&background={background_color}'
                       f'&color=fff&name={initials}', stream=True)

    image_path = os.path.join('users', 'avatars', f'{username}.png')
    image_full_path = os.path.join(settings.MEDIA_DIR, image_path)

    if response.status_code == 200:
        with open(image_full_path, 'wb') as f:
            for chunk in response:
                f.write(chunk)

        my_user.picture.name = image_path
        my_user.save()


def temporary_image():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)  # important because after save(), the fp is already at the end of the file
    return tmp_file
