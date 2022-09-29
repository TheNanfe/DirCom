DEFAULT_PATH = "C:/Users/nanre/Documents/DirComUploads"


def documents_upload(f):
    file_path = DEFAULT_PATH + "/documents/" + f.name
    try:
        with open(file_path, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path
    except Exception as e:
        print(e)
        return None


def images_upload(f):
    file_path = DEFAULT_PATH + "/images/" + f.name
    try:
        with open(file_path, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path
    except Exception as e:
        print(e)
        return None


def handle_uploaded_file(f):
    # TODO: Mejorar el guardado de los archivos segun el tipo de documento.
    if f.content_type == "application/pdf":
        return documents_upload(f)
    else:
        return images_upload(f)


