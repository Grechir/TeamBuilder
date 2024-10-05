from app.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'
    success_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)

            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('account_login')
