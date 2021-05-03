from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from chat.forms import ConversationForm, MessageForm
from chat.models import Section, Conversation, Message


def index_view(request):
    context = {
        'sections': Section.objects.all(),
    }
    return render(request, 'chat/index.html', context=context)


class SectionView(TemplateView):
    template_name = 'chat/section.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        section_id = kwargs.get('section_id')
        conversations = Conversation.objects.filter(section_id=section_id)
        conversation_id = self.request.GET.get('conversation')
        if conversation_id:
            messages = Message.objects.filter(conversation_id=conversation_id)
        else:
            messages = []

        conversation_form = kwargs.get('conversation_form', ConversationForm())
        message_form = kwargs.get('message_form', MessageForm())
        context.update({
            'section_id': section_id,
            'conversations': conversations,
            'conversation_id': conversation_id,
            'messages': messages,
            'conversation_form': conversation_form,
            'message_form': message_form,
        })
        return context

    def post(self, request, *args, **kwargs):
        section_id = kwargs.get('section_id')
        conversation_id = self.request.GET.get('conversation')
        user = self.request.user

        form_type = request.POST.get('form')
        if form_type == 'conversation':
            conversation_form = ConversationForm(request.POST)

            if user.is_anonymous:
                conversation_form.add_error(None, 'Вы не вошли в систему')
            elif conversation_form.is_valid():
                conversation = conversation_form.save(commit=False)
                conversation.section_id = section_id
                conversation.user = user
                conversation.save()
            if not conversation_form.is_valid():
                kwargs['conversation_form']= conversation_form
        elif form_type == 'message' and conversation_id:
            message_form = MessageForm(request.POST)

            if user.is_anonymous:
                message_form.add_error(None, 'Вы не вошли в систему')
            elif message_form.is_valid():
                message = message_form.save(commit=False)
                message.conversation_id = conversation_id
                message.user = user
                message.save()
            if not message_form.is_valid():
                kwargs['message_form'] = message_form

        return self.get(request,*args, **kwargs)