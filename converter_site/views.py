import random
import time
from imp import reload
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, FileResponse, StreamingHttpResponse
from pytube.exceptions import VideoUnavailable

from djangoProject.settings import BASE_DIR
from .forms import *

from django.utils.encoding import escape_uri_path

from pytube import YouTube

import ffmpeg

from fpdf import FPDF

from hurry.filesize import size, si

import sys

import time

list_bad_symbols = ['"', ':', '/', '\\', '*', '<', '>', '?', '|', '.']


def index(request):

    context = {
        'title': "choice convertation type"
    }
    return render(request, 'converter_site/index.html', context=context)


def youtube_convert_view(request):

    if request.method == 'POST':   # Тут делается так, что если какие-то поля были неравильно заполнены, то
        # заполненные поля не очищаются, а остаются для исправления ошибок.s
        form = PostFormYoutube(request.POST, request.FILES)
        if form.is_valid():
            submit = True
            link = form.data.get('youtube_link')
            splited_link = link.split('?v=')[-1:][0]
            yt = YouTube(link)
            try:
                stream = yt.streams
            except VideoUnavailable:
                print(VideoUnavailable)
                return render(request, 'converter_site/Youtube_download_app.html', {'title': 'youtube-converter',
                                                                                    'type_error': 'video with this link does not exist',
                                                                                    'form': form})

            stream_highest = stream.get_highest_resolution()
            stream_lowest = stream.get_lowest_resolution()
            stream_audio = stream.get_audio_only()
            stream_highest_size = stream_highest.filesize
            stream_lowest_size = stream_lowest.filesize
            stream_audio_size = stream_audio.filesize
            # Получаем все необходимые типы видео, и их размер для вывода пользователю
            filesize_highest = size(stream_highest_size)
            filesize_lowest = size(stream_lowest_size)
            filesize_audio = size(stream_audio_size)

            if yt.length > 8000:
                print('Ошибка, видео слишком долгое.')
                type_error = 'Youtube video is too long'
                return render(request, 'converter_site/Youtube_download_app.html', {'title': 'youtube-converter',
                                                                                    'type_error': type_error,
                                                                                    'form': form})

            title = stream_lowest.title.translate({ord(i): None for i in list_bad_symbols})
            # Получаем заголовок и отсекаем "плохие символы"
            post = form.save(commit=False)

            image_url = yt.thumbnail_url
            print(f"Current time - {time.strftime('%H:%M:%S', time.localtime())} \nDownload youtube video by name - {title} \nlink - {link} \nFilesize:\n highest - {filesize_highest} \n lowest  - {filesize_lowest} \n audio   - {filesize_audio}")
            print(f"video duration - {round(yt.length/60, 2)} minute")
            post.file_path = f'./files\youtube_downloaded_dir{title}.mp4'
            return render(request, 'converter_site/Youtube_download_app.html', {'Submit': submit,
                                                                                'splited_link': splited_link,
                                                                                'image_url': image_url,
                                                                                'video_title': title,
                                                                                'filesize_hight': filesize_highest,
                                                                                'filesize_low': filesize_lowest,
                                                                                'filesize_audio': filesize_audio,
                                                                                'form': None},)

    else:
        form = PostFormYoutube()
    return render(request, 'converter_site/Youtube_download_app.html', {'title': 'youtube-converter',
                                                                        'form': form})


def download_video(request):

    reload(sys)
    buffer = BytesIO()
    def on_progress(stream, chunk, bytes_remaining):
            print(f'{round(100 - (bytes_remaining / stream.filesize * 100), 2)}%')

    link = request.GET.get('link')
    download_rule = int(request.GET.get('rule'))
    title = request.GET.get('title')

    youtube_link = f'https://www.youtube.com/watch?v={link}'
    yt = YouTube(youtube_link, on_progress_callback=on_progress)

    if download_rule == 1:
        stream = yt.streams.get_highest_resolution().stream_to_buffer(buffer)
        file_name = f'{title}'
        file_type = 'mp4'
        print('choised hight-quality type')
    elif download_rule == 2:
        stream = yt.streams.get_lowest_resolution().stream_to_buffer(buffer)
        file_name = f'{title}'
        file_type = 'mp4'
        print('choised low-quality type')
    elif download_rule == 3:
        stream = yt.streams.get_audio_only().stream_to_buffer(buffer)
        file_name = f'{title}'
        file_type = 'mp3'
        print('choised audio type')
    else:
        return HttpResponseNotFound('<h1>Page not found 😟</h1> <h2>Bad download rule</h2>')
    # Тут из get-запроса выбирается качество видео, которое выбрал пользователь

    file = buffer.getvalue()
    file_to_send = ContentFile(file)
    if file_type == 'mp4':
        response = HttpResponse(file_to_send, content_type='video/mp4')
    else:
        response = HttpResponse(file_to_send, content_type='audio/mp3')
    response['Content-Length'] = file_to_send.size
    print(title)
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(f"{file_name}.{file_type}"))
    # Видео с ютуба записывается в буффер, оттуда же оно и отправляется пользователю, из плюсов - не занимает место
    # на ЖД, из минусов - занимает место в оперативке
    return response


def convertation_type_choise(request):
    return render(request, 'converter_site/file_convertation/file_convertation_choise_type.html', {'title': 'choice-type'})


def convert(input_file, output_file):
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream, overwrite_output=True, quiet=True)


def convertation_video(request):

    if request.method == 'POST' and request.FILES['file_for_convertation']:
        if request.FILES['file_for_convertation'].size > 100*1024*1024:
            return render(request, 'converter_site/file_convertation/video.html', {'title': 'pdf-converter',
                                                                              'type_error': 'Video file too large ( > 100mb )'})
        type_for_convertation = request.POST.getlist('to_which_type')[0]  # Можно было POST.get ,
        # но сделал через getlist чтобы запомнить что так можно. Он как get, но можно нескольким html объектам давать
        # одно имя, и их вывод будет в этом списке getlist
        file = request.FILES['file_for_convertation']

        if file.name.split('.')[-1:][0] not in ['webp', 'mkv', 'gif', 'mp4']:
            type_error = 'Wrong file format entered'
            return render(request, 'converter_site/file_convertation/video.html', {'type_error': type_error})
        # Проверяем формат файла, он должен быть видео)

        if type_for_convertation in ['webp', 'gif'] and request.FILES['file_for_convertation'].size > 3*1024*1024:
            return render(request, 'converter_site/file_convertation/video.html', {'title': 'pdf-converter',
                                                                                   'type_error': 'Too big file'
                                                                                                 ' for this file type output 😡 ( > 3mb )'})
        fs = FileSystemStorage('./files/video_convertation/input')
        filename = fs.save(file.name, file)
        file_object = fs.open(filename)
        file_path = file_object.name
        file_path_splited = file_path.split('.')
        # Переменные, сохраняем файл из Post запроса в файловую систему

        filename_splited = file.name.split('.')
        filename_splited_string = ''
        for i in range(0, len(filename_splited)-1):
            filename_splited_string = filename_splited_string + filename_splited[i]
        # Тут мы получаем название файла без его формата

        file_path_splited_output = f"{BASE_DIR}/files/video_convertation/output/{file.name}"
        # Формируем конечный путь для вывода файла

        print(f"Converting a file named {filename} from {file_path_splited[-1:][0]} format to {type_for_convertation} format")

        video_path = f"{file_path_splited_output}.{type_for_convertation}"

        convert(file_path, video_path)

        filename = f"{filename_splited_string}.{type_for_convertation}"
        return FileResponse(open(video_path, 'rb'), as_attachment=True, filename=filename)
    return render(request, 'converter_site/file_convertation/video.html', {'title': 'video-convertation',
                                                                            'type_error': False})


def convertation_audio(request):

    if request.method == 'POST' and request.FILES['file_for_convertation']:
        if request.FILES['file_for_convertation'].size > 100*1024*1024:
            type_error = 'Audio file too large ( > 100mb )'
            return render(request, 'converter_site/file_convertation/audio.html', {'title': 'pdf-converter',
                                                                              'type_error': type_error})

        type_for_convertation = request.POST.getlist('to_which_type')[0]  # Можно было POST.get ,
        # но сделал через getlist чтобы запомнить что так можно. Он как get, но можно нескольким html объектам давать
        # одно имя, и их вывод будет в этом списке getlist
        file = request.FILES['file_for_convertation']

        if file.name.split('.')[-1:][0] not in ['flac', 'ogg', 'wav', 'mp3', 'mp4']:
            type_error = 'Wrong file format entered'
            return render(request, 'converter_site/file_convertation/audio.html', {'type_error': type_error})
        # Проверяем формат файла, он должен быть аудио

        fs = FileSystemStorage('./files/audio_convertation/input')
        filename = fs.save(file.name, file)
        file_object = fs.open(filename)
        file_path = file_object.name
        file_path_splited = file_path.split('.')
        # Переменные, сохраняем файл из Post запроса в файловую систему

        filename_splited = file.name.split('.')

        filename_splited_string = ''
        for i in range(0, len(filename_splited)-1):
            filename_splited_string = filename_splited_string + filename_splited[i]
        # Тут мы получаем название файла без его формата

        file_path_splited_output = f"{BASE_DIR}/files/audio_convertation/output/{file.name}"

        # Формируем конечный путь для вывода файла
        print(file_path_splited_output)

        print(f"Converting a file named {filename} from {file_path_splited[-1:][0]} format to {type_for_convertation} format")

        audio_path = f"{file_path_splited_output}.{type_for_convertation}"
        try:
            convert(file_path, audio_path)
        except ffmpeg._run.Error:
            type_error = 'Audio track not found in file'
            return render(request, 'converter_site/file_convertation/audio.html', {'type_error': type_error})

        filename = f"{filename_splited_string}.{type_for_convertation}"

        return FileResponse(open(audio_path, 'rb'), as_attachment=True, filename=filename)
    return render(request, 'converter_site/file_convertation/audio.html', {'title': 'audio-convertation',
                                                                            'type_error': False})


def convertation_picture(request):
    if request.method == 'POST' and request.FILES.get('file_for_convertation', False):
        if request.FILES['file_for_convertation'].size > 10*1024*1024:
            return render(request, 'converter_site/file_convertation/picture.html', {'title': 'pdf-converter',
                                                                          'type_error': 'Picture file too large ( > 10mb )'})

        type_for_convertation = request.POST.getlist('to_which_type')[0]  # Можно было POST.get ,
        # но сделал через getlist чтобы запомнить что так можно. Он как get, но можно нескольким html объектам давать
        # одно имя, и их вывод будет в этом списке getlist
        file = request.FILES['file_for_convertation']
        if file.name.split('.')[-1:][0] not in ['jpg', 'png', 'gif', 'ico', 'webp', 'bmp']:
            type_error = 'Wrong file format entered'
            return render(request, 'converter_site/file_convertation/picture.html', {'type_error': type_error})
        # Проверяем формат файла, он должен быть картинкой

        fs = FileSystemStorage('./files/pictures_convertation/input')
        filename = fs.save(file.name, file)
        file_object = fs.open(filename)
        file_path = file_object.name
        file_path_splited = file_path.split('.')
        # Переменные, сохраняем файл из Post запроса в файловую систему

        filename_splited = file.name.split('.')

        filename_splited_string = ''
        for i in range(0, len(filename_splited)-1):
            filename_splited_string = filename_splited_string + filename_splited[i]
        # Тут мы аккуратно получаем название файла без типа файла

        file_path_splited_output = f"{BASE_DIR}/files/pictures_convertation/output/{file.name}"

        print(f"Converting a file named {filename} from {file_path_splited[-1:][0]} format to {type_for_convertation} format")

        if file_path_splited[-1:][0] in ['gif', 'webp'] and type_for_convertation in ['gif', 'webp']:
            print('Файл имеет более одного кардра')
            save_all = True
        else:
            print('Файл имеет лишь один кадр')
            save_all = False
        # Если формат может иметь несколько кадров, тогда даём соотв. параметр

        img_path = f"{file_path_splited_output}.{type_for_convertation}"
        img = Image.open(file_path)

        if type_for_convertation == "jpg":
            print('convertation picture to RGB format')
            img = img.convert("RGB")
        # Если преобразовываем в jpg то конвертируем картинку в RGB цвета

        img.save(img_path, save_all=save_all)
        img.close()
        filename = f"{filename_splited_string}.{type_for_convertation}"
        return FileResponse(open(img_path, 'rb'), as_attachment=True, filename=filename)

    return render(request, 'converter_site/file_convertation/picture.html', {'title': 'picture-convertation',
                                                                             'type_error': False})


def pictures_to_pdf(request):
    if request.method == 'POST' and request.FILES['pictures_for_pdf']:
        filename_list = []
        if request.FILES['pictures_for_pdf'].size > 100*1024*1024:
            return render(request, 'converter_site/picture_to_pdf_app.html', {'title': 'pdf-converter',
                                                                              'type_error': 'Audio file too large ( > 100mb )'})

        filename_list_for_output = []
        filename_pdf = request.POST.getlist('pdf_name_output')
        files = request.FILES.getlist('pictures_for_pdf')
        fs = FileSystemStorage('./files/pdf_converter/input')
        for file in files:
            file_type = file.name.split('.')[-1:][0]
            if file_type not in ['png', 'jpg']:
                return render(request, 'converter_site/picture_to_pdf_app.html', {'title': 'pdf-converter',
                                                                                  'type_error': 'Available'
                                                                                  ' only png and jpg file types'})

            filename = fs.save(file.name, file)
            filename_list.append(filename)
        print(f"Конвертируем следующие картинки в pdf - {filename_list}")

        pdf = FPDF()
        sdir = f'{BASE_DIR}/files/pdf_converter/input/'
        width, height = 0, 0

        for i in range(0, len(filename_list)):
            picture_path = sdir+filename_list[i]
            if i == 0:
                page = Image.open(picture_path)
                width, height = page.size
                pdf = FPDF(unit='pt', format=[width+((width/30)),height+((height/15))]) # Разрешение вставляемой картинки
            image = picture_path
            pdf.add_page()
            pdf.image(image,(width/80),(height/80),width,height)
        output_dir = f'{BASE_DIR}/files/pdf_converter/output/{filename_pdf[0]}.pdf'
        pdf.output(output_dir, "f")

        return FileResponse(open(output_dir, 'rb'), as_attachment=False, filename=f"{filename_pdf[0]}.pdf")

    return render(request, 'converter_site/picture_to_pdf_app.html', {'title': 'pdf-converter',
                                                                        })


def admin_without_pass_panel_test(request):
    image_list = ['0.png', '1.jpg', '2.png', '3.jpg', '4.jpg', '5.png', '6.jpg', '7.jpg', '9.jpg']
    random_nubmer = random.randint(0,8)
    image = image_list[random_nubmer]
    print(image)
    for i in range(0, 20):
        print('Хе-хе кто-то открыл интересную страницу.')
        print('Хе-хе кто-то открыл интересную страницу.')
    return render(request, 'converter_site/fun.html', {'image': image})


def pagenotfound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 😟</h1>')
