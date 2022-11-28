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

    if int(form.data["category"]) == 2:
        if form.data["audiovisual"] == "GUION":
            extra_info.append({"content": form.data["content1"], "description": "Descripción general de la idea"})
            extra_info.append({"content": form.data["content2"], "description": "Objetivos del Material"})
            extra_info.append({"content": form.data["content3"], "description": "Fecha Limite para entrega"})
            extra_info.append({"content": form.data["content4"], "description": "Destino: donde se presentará el material para realizarlo en el formato adecuado"})
            extra_info.append({"content": form.data["content5"], "description": "Responsable del área y horario"})
            extra_info.append({"content": form.data["content6"], "description": "Referencias (link material similar al deseado)"})
            extra_info.append({"content": form.data["content7"], "description": "Duración Deseada (aclarar si son minutos o segundos)"})
            extra_info.append({"content": form.data["content8"], "description": "Informe completo de la actividad"})

            service_info = {"GUION": extra_info}

        elif form.data["audiovisual"] == "GRABACION":
            extra_info.append({"content": form.data["content1"], "description": "Guión o detalle general para la grabación"})
            extra_info.append({"content": form.data["content2"], "description": "Observaciones generales"})
            extra_info.append({"content": form.data["content3"], "description": "Fecha de grabación"})
            extra_info.append({"content": form.data["content4"], "description": "Referencias (link material similar al deseado)"})
            extra_info.append({"content": form.data["content5"], "description": "Responsable del área y horario"})
            extra_info.append({"content": form.data["content6"], "description": "Equipos que disponen"})

            service_info = {"GRABACION": extra_info}

        elif form.data["audiovisual"] == "AUDIOVISUAL":
            extra_info.append({"content": form.data["content1"], "description": "Indicaciones generales para edición"})
            extra_info.append({"content": form.data["content2"], "description": "Fecha Limite para entrega"})
            extra_info.append({"content": form.data["content3"], "description": "Responsable del área y horario"})
            extra_info.append({"content": form.data["content4"], "description": "Objetivos del Material"})

            service_info = {"AUDIOVISUAL": extra_info}

    if int(form.data["category"]) == 3:
        if form.data["graphic-design"] == "FLYER":
            extra_info.append({"content": form.data["content1"], "description": "Nombre de Actividad"})
            extra_info.append({"content": form.data["content2"], "description": "Fecha"})
            extra_info.append({"content": form.data["content3"], "description": "Lugar de Actividad"})
            extra_info.append({"content": form.data["content4"], "description": "Mensaje a Comunicar"})
            extra_info.append({"content": form.data["content5"], "description": "Formato de Entrega Deseado"})

            service_info = {"FLYER": extra_info}

        if form.data["graphic-design"] == "COMUNICADO":
            extra_info.append({"content": form.data["content1"], "description": "Texto del Aviso o Comunicado"})
            extra_info.append({"content": form.data["content2"], "description": "Formato de Entrega Deseado"})

            service_info = {"COMUNICADO": extra_info}

    if int(form.data["category"]) == 4:
        if form.data["WEB"] == "WEB":
            extra_info.append({"content": form.data["content1"], "description": "Objetivos del sitio web"})
            extra_info.append({"content": form.data["content2"], "description": "Referencias para el sitio web"})

            service_info = {"WEB": extra_info}

        if form.data["WEB"] == "ACTUALIZACION":
            extra_info.append({"content": form.data["content1"], "description": "Actualizaciones, Ajustes o Cambios a realizar"})
            extra_info.append({"content": form.data["content2"], "description": "Dirección URL de la Sección"})

            service_info = {"ACTUALIZACION": extra_info}

        if form.data["WEB"] == "CONCURSOS":
            extra_info.append({"content": form.data["content1"], "description": "Nombre Completo y Estado del Concurso (Formato Estándar)"})

            service_info = {"CONCURSOS": extra_info}

        if form.data["WEB"] == "CONVENIOS":
            extra_info.append({"content": form.data["content1"], "description": "Nombre Completo del Convenio"})

            service_info = {"CONVENIOS": extra_info}

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

    if service_key == "GUION":
        return "Desarrollo de guión"

    if service_key == "GRABACION":
        return "Grabación"

    if service_key == "AUDIOVISUAL":
        return "Edición Audiovisual"

    if service_key == "FLYER":
        return "Diseño de Flyer"

    if service_key == "COMUNICADO":
        return "Diseño de Aviso o Comunicado"

    if service_key == "WEB":
        return "Diseño de Sitio Web"

    if service_key == "ACTUALIZACION":
        return "Actualización de Datos en Web"

    if service_key == "CONCURSOS":
        return "Publicación de Concursos y Selección de Personas"

    if service_key == "CONVENIOS":
        return "Publicación de Convenios"

    return "---------"
