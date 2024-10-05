import random
from string import hexdigits

from django.core.mail import send_mail
from django.conf import settings

from allauth.account.forms import SignupForm


class CommonSignupForm(SignupForm):
    def save(self, request):

        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject='Код активации',
            message=f'Ваш код активации: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        ),

        return user
