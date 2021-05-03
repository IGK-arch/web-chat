from django.urls import path

from chat.views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('chat/<int:section_id>/', SectionView.as_view(), name='section')

]
