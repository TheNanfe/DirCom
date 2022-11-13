import json


def get_json_data(form):
    extra_info = []
    service_info = {}
    if int(form.data["category"]) == 1:

        if form.data["press-redaction"] == "DISCURSO":
            extra_info.append({"content": form.data["content1"], "description": "Informe Completo"})
            extra_info.append({"content": form.data["content2"], "description": "Objetivo"})

            service_info = {"DISCURSO": extra_info}

        elif form.data["press-redaction"] == "GACETILLA":
            extra_info.append({"content": form.data["content1"], "description": "Informe completo de la actividad"})
            extra_info.append({"content": form.data["content2"], "description": "Programa"})
            extra_info.append({"content": form.data["content3"], "description": "Contactos(Tel, Cel, e-mail)"})

            service_info = {"GACETILLA": extra_info}

        elif form.data["press-redaction"] == "REDES":
            extra_info.append({"content": form.data["content1"], "description": "Informe completo de la actividad"})
            extra_info.append({"content": form.data["content2"], "description": "Contactos(Tel, Cel, e-mail)"})

            service_info = {"REDES": extra_info}

        elif form.data["press-redaction"] == "WEB":
            service_info = {"WEB": []}

        else:
            service_info = {"EVENTO": []}

    return service_info


def parse_json_data(json_to_parse):
    try:
        return json.loads(json_to_parse)
    except Exception as e:
        raise e


def get_service_name(service_key):
    if service_key == "DISCURSO":
        return "Discurso(Rectora/Vicerrector)"

    if service_key == "GACETILLA":
        return "Gacetilla de Prensa"

    if service_key == "REDES":
        return "Redacción y publicación de noticia en redes sociales"

    if service_key == "WEB":
        return "Redacción y publicación de noticia en sitio web"

    if service_key == "EVENTO":
        return "Publicación de eventos, vinculados a la UNA, de otras instituciones"

    return "---------"
