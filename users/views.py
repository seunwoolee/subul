from django.contrib.auth.views import LoginView

from eventlog.models import LogginMixin
from users.models import CustomUser


class CustomLoginView(LogginMixin, LoginView):
    def form_valid(self, form):
        if super(CustomLoginView, self).form_valid(form):
            instance = CustomUser.objects.get(pk=self.request.user.pk)
            self.log(
                user=self.request.user,
                action="로그인",
                obj=instance
            )
        return super(CustomLoginView, self).form_valid(form)