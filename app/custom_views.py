from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from django.contrib.auth.decorators import login_required
import os

@login_required
def custom_upload_file(request):
    """
    В библиотеке django_ckeditor_5.views.py есть функция upload_file со строчкой:
        if request.method == "POST" and request.user.is_staff:
    проверка в этой строчке не позволяет юзерам загружать изображения если они не имеют
    статус staff в админ панели. Использовать именно ckeditor_5 для меня принципиально.
                    Эта функция призвана заменить функцию из библиотеки
    """
    if request.method == "POST":
        # Проверяем, имеет ли пользователь право загружать файлы.
        if not request.user.is_authenticated:  # Меняем условие под свои нужды
            return JsonResponse({"error": "Unauthorized"}, status=403)

        upload = request.FILES['upload']
        filename = get_valid_filename(upload.name)
        file_path = os.path.join('uploads', filename)
        saved_path = default_storage.save(file_path, upload)
        url = default_storage.url(saved_path)
        return JsonResponse({"url": url})
    return JsonResponse({"error": "Invalid request"}, status=400)
