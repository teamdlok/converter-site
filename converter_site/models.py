from django.db import models
from django.urls import reverse





class Youtube_To_File(models.Model):
    youtube_link = models.URLField()
    file_path = models.CharField(max_length=255, verbose_name='Путь к файлу')
    # time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    only_audio = models.BooleanField(default=False, verbose_name='Только аудио дорожка')

    class Meta:
        verbose_name = 'Конвертация ютуб ссылки в видео-файл'
        verbose_name_plural = 'Конвертация ютуб ссылки в видео-файл'


class FileConvertationAudio(models.Model):
    to_which_type = models.ForeignKey('CategoryAudio', on_delete=models.PROTECT, verbose_name='To which type need convert file')
    file_for_convertation = models.FileField(upload_to=f"temporary_files/Audio/%Y/%m/%d", verbose_name='File for convertation')
    file_converted = models.FileField(upload_to=f"temporary_files/Audio/%Y/%m/%d", verbose_name='Converted file')


class CategoryAudio(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):  # Тут мы делаем так, что вместо id поля в поле подставления вставляется название имя поля
        return self.name


class FileConvertationVideo(models.Model):
    to_which_type = models.ForeignKey('CategoryVideo', on_delete=models.PROTECT, verbose_name='To which type need convert file')
    file_for_convertation = models.FileField(upload_to=f"temporary_files/Video/%Y/%m/%d", verbose_name='File for convertation')
    file_converted = models.FileField(upload_to=f"temporary_files/Video/%Y/%m/%d", verbose_name='Converted file')


class CategoryVideo(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):  # Тут мы делаем так, что вместо id поля в поле подставления вставляется название имя поля
        return self.name


class FileConvertationPicture(models.Model):
    to_which_type = models.ForeignKey('CategoryPicture', on_delete=models.PROTECT, verbose_name='To which type need convert file')
    file_for_convertation = models.FileField(upload_to=f"temporary_files/Picture/%Y/%m/%d", verbose_name='File for convertation')
    file_converted = models.FileField(upload_to=f"temporary_files/Picture/%Y/%m/%d", verbose_name='Converted file')


class CategoryPicture(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):  # Тут мы делаем так, что вместо id поля в поле подставления вставляется название имя поля
        return self.name














