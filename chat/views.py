from django.shortcuts import render
from .models import Message
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse

class MessageCreateView(CreateView):
    model = Message
    fields = 'text',
    template_name = 'chat/index.html'
    success_url = reverse_lazy('chat:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     msgs = Message.objects.all().order_by('-created_at')[:5]
    #     data['msgs'] = msgs
    #     return data


def get_messages(request):
    msgs = Message.objects.all().order_by('-created_at')[:5]
    results = []
    for msg in msgs:
        results.append([msg.text, msg.created_at])
    return JsonResponse(results, safe=False)