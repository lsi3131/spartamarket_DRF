from datetime import datetime
from django.http import HttpRequest

import hashlib
import os


def sha512_hash(text):
    encoded_text = text.encode('utf-8')
    sha512 = hashlib.sha512()
    sha512.update(encoded_text)
    hashed_text = sha512.hexdigest()
    return hashed_text


def upload_to_file(request: HttpRequest, dirname):
    file_path_list = []
    upload_dir_path = os.path.join('media', dirname)
    if not os.path.exists(upload_dir_path):
        os.mkdir(upload_dir_path)

    for uploaded_file in request.FILES.values():
        ext = uploaded_file.name.split(".")[-1]
        hashed_filename = sha512_hash(
            f"{request.user.username}image_file{datetime.now()}") + f".{ext}"

        file_path = upload_dir_path + hashed_filename
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_path_list.append(dirname + hashed_filename)

    return file_path_list
