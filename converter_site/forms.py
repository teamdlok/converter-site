from django import forms
from django.core.exceptions import ValidationError


from .models import *



class PostFormYoutube(forms.ModelForm):  # Ахахахаахха, тут я вставил вместо .ModelForm - .Form ; Потратил 2 часа чтобы
    # найти почему ничего не работает хотя всё правильно, так и живём.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Youtube_To_File  # Ссылка на модель данных
        fields = ['youtube_link']
        widgets = {
            'youtube_link': forms.TextInput(attrs={'class': 'form-input'})
        }

    def clean_youtube_link(self):
        link = self.cleaned_data['youtube_link']
        domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'http://www.youtube.com']
        for x in domains:
            if link.startswith(x):
                print("Вошёл в True, ссылка ведёт на ютуб\n")
                return link
        print("Ошибка, ссылка не ведёт на ютуб\n")
        raise ValidationError('Please, insert youtube link')


class ConverterAudio(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_which_type'].empty_label = "Choice to convert. type"

    class Meta:
        model = FileConvertationAudio
        fields = ['file_for_convertation', 'to_which_type']
        widgets = {

        }


class FewFileUploader(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    pdf_filename = forms.CharField(max_length=255)


class ConverterVideo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_which_type'].empty_label = "Choice to convert. type"

    class Meta:
        model = FileConvertationVideo
        fields = ['file_for_convertation', 'to_which_type', ]
        widgets = {

        }


class ConverterPicture(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_which_type'].empty_label = "Choice to convert. type"

    class Meta:
        model = FileConvertationPicture
        fields = ['file_for_convertation', 'to_which_type', ]
        widgets = {

        }
