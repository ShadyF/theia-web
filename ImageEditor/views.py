from django.shortcuts import render
from django.views.generic import View


class Editor(View):
    template_name = 'ImageEditor/editor.html'

    def get(self, request):
        return render(request, self.template_name)
