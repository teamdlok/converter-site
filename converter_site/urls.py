
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('youtube_convertation/', youtube_convert_view, name='youtube_conv_link'),
    path('youtube_convertation/download', download_video, name='download_video_link'),
    path('file_convertation/', convertation_type_choise, name='convertation_type_choise'),
    path('file_convertation/video', convertation_video, name='convertation_video_url'),
    path('file_convertation/audio', convertation_audio, name='convertation_audio_url'),
    path('file_convertation/picture', convertation_picture, name='convertation_picture_url'),
    path('pictures_to_pdf', pictures_to_pdf, name='pictures_convert_to_pdf_url'),
    path('admin-without-pass-panel-test', admin_without_pass_panel_test)
]


