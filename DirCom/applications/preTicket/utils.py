DEFAULT_PATH = "C:/Users/nanre/Documents/DirComUploads"


def documents_upload(f):
    successfully_saved = False
    try:
        with open(DEFAULT_PATH + "/documents/" + f.name, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        successfully_saved = True
        return successfully_saved
    except Exception as e:
        print(e)
        return successfully_saved


def images_upload(f):
    successfully_saved = False
    try:
        with open(DEFAULT_PATH + "/documents/" + f.name, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        successfully_saved = True
        return successfully_saved
    except Exception as e:
        print(e)
        return successfully_saved


def handle_uploaded_file(f):
    # TODO: Mejorar el guardado de los archivos segun el tipo de documento.
    if f.content_type == "application/pdf":
        return documents_upload(f)
    else:
        return images_upload(f)


