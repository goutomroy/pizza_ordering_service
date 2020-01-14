from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView


class SwaggerUIView(LoginRequiredMixin, TemplateView):
    template_name = 'swagger_render/index.html'
    raise_exception = True
    permission_denied_message = "You are not allowed here."

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.is_staff:
            return HttpResponse("Only admin or staff can access this doc.")
        return self.render_to_response(None)
