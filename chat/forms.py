from django import forms
from django_svg_image_form_field import SvgAndImageFormField

from chat.models import Conversation, Message, Section


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = []
        field_classes = {
            'image': SvgAndImageFormField,
        }


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ('text',)

    # def clean_text(self):
    #     text = self.cleaned_data['text']
    #     text.replace('Привет', '***')
    #     return text


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)

