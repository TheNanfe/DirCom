$("#id_category").change(function () {
    let dynamicSelect = $("#dynamic-select");
    let category = $("#id_category");
    if (category.val() === "PRENSA") {
        let html = (
            '<label for="id_service">Servicio a Solicitar:</label>\
            <select id="type-service" class="form-control  mb-3" name="press-redaction" style="margin-bottom:5px;">\
                <option selected value="0">---------</option>\
                <option value="DISCURSO">Discurso(Rectora/Vicerrector)</option>\
                <option value="GACETILLA">Gacetilla de Prensa</option>\
                <option value="REDES">Redacción y publicación de noticia en redes sociales</option>\
                <option value="WEB">Redacción y publicación de noticia en sitio web</option>\
                <option value="EVENTOS">Publicación de eventos, vinculados a la UNA, de otras instituciones</option>\
            </select>\
            <div id="extra-info"></div>'
        );
        dynamicSelect.html(html);
    } else if (category.val() === "AUDIOVISUAL") {
        let html = (
            '<label for="id_service">Servicio a Solicitar:</label>\
            <select id="type-service" class="form-control  mb-3" name="audiovisual" style="margin-bottom:5px;">\
                <option selected value="0">---------</option>\
                <option value="GUION">Desarrollo de guión</option>\
                <option value="GRABACION">Grabación</option>\
                <option value="AUDIOVISUAL">Edición Audiovisual</option>\
            </select>\
            <div id="extra-info"></div>'
        );
        dynamicSelect.html(html);
    } else if (category.val() === "DISENHO") {
        let html = (
            '<label for="id_service">Servicio a Solicitar:</label>\
            <select id="type-service" class="form-control  mb-3" name="graphic-design" style="margin-bottom:5px;">\
                <option selected value="0">---------</option>\
                <option value="FLYER">Diseño de Flyer</option>\
                <option value="COMUNICADO">Diseño de Aviso o Comunicado</option>\
            </select>\
            <div id="extra-info"></div>'
        );
        dynamicSelect.html(html);
    } else if (category.val() === "WEB") {
        let html = (
            '<label for="id_service">Servicio a Solicitar:</label>\
            <select id="type-service" class="form-control  mb-3 " name="web" style="margin-bottom:5px;">\
                <option selected value="0">---------</option>\
                <option value="WEB">Diseño de Sitio Web</option>\
                <option value="ACTUALIZACION">Diseño de Aviso o Comunicado</option>\
                <option value="CONCURSOS">Actualización de Datos en Web</option>\
                <option value="CONVENIOS">Publicación de Concursos y Selección de Personas</option>\
            </select>\
            <div id="extra-info"></div>'
        );
        dynamicSelect.html(html);
    } else {
        dynamicSelect.html('<div id="dynamic-select"></div>');
    }
});

$("#dynamic-select").on("change", "#type-service", function () {
    let typeService = $("#type-service");
    let extraInfo = $("#extra-info");
    if (typeService.val() === "DISCURSO") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Informe Completo:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Objetivo:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "GACETILLA") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Informe completo de la actividad:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Programa:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
                 <label for="id_content3">Contactos (Tel, Cel, e-mail, link):</label>\
                 <textarea name="content3" cols="40" rows="3" class="form-control mb-3" required="" id="id_content3"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "REDES") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Informe completo de la actividad:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Contactos (Tel, Cel, e-mail, link):</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "GUION") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Descripción general de la idea:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Objetivos del Material:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
                 <label for="id_content3">Fecha Limite para entrega:</label>\
                 <input type="date" name="content3" cols="20" rows="3" class="mb-3" required="" id="id_content3">\
                 <label for="id_content4">Destino: donde se presentará el material para realizarlo en el formato adecuado:</label>\
                 <textarea name="content4" cols="40" rows="3" class="form-control mb-3" required="" id="id_content4"></textarea>\
                 <label for="id_content5">Responsable del área y horario:</label>\
                 <textarea name="content5" cols="40" rows="3" class="form-control mb-3" required="" id="id_content5"></textarea>\
                 <label for="id_content6">Referencias (link material similar al deseado):</label>\
                 <textarea name="content6" cols="40" rows="3" class="form-control mb-3" required="" id="id_content6"></textarea>\
                 <label for="id_content7">Duración Deseada (aclarar si son minutos o segundos):</label>\
                 <textarea name="content7" cols="40" rows="3" class="form-control mb-3" required="" id="id_content7"></textarea>\
                 <label for="id_content8">Observaciones generales:</label>\
                 <textarea name="content8" cols="40" rows="3" class="form-control mb-3" id="id_content8"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "GRABACION") {
        let html = (
            '<div CLASS="mb-3">\
                  <label for="id_content1">Guión o detalle general para la grabación:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Observaciones generales:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
                 <label for="id_content3">Fecha de grabación:</label>\
                 <input type="date" name="content3" cols="20" rows="3" class="mb-3" required="" id="id_content3">\
                 <label for="id_content4">Referencias (link material similar al deseado):</label>\
                 <textarea name="content4" cols="40" rows="3" class="form-control mb-3" required="" id="id_content4"></textarea>\
                 <label for="id_content5">Responsable del área y horario:</label>\
                 <textarea name="content5" cols="40" rows="3" class="form-control mb-3" required="" id="id_content5"></textarea>\
                 <label for="id_content6">Equipos que disponen:</label>\
                 <textarea name="content6" cols="40" rows="3" class="form-control mb-3" required="" id="id_content6"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "AUDIOVISUAL") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Indicaciones generales para edición:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Fecha Limite para entrega:</label>\
                 <input type="date" name="content2" cols="20" rows="3" class="mb-3" required="" id="id_content2">\
                 <label for="id_content3">Responsable del área y horario:</label>\
                 <textarea name="content3" cols="40" rows="3" class="form-control mb-3" required="" id="id_content3"></textarea>\
                 <label for="id_content4">Objetivos del Material:</label>\
                 <textarea name="content4" cols="40" rows="3" class="form-control mb-3" required="" id="id_content4"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "FLYER") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Nombre de Actividad:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Fecha:</label>\
                 <input type="date" name="content2" cols="20" rows="3" class="mb-3" required="" id="id_content2">\
                 <label for="id_content3">Lugar de Actividad:</label>\
                 <textarea name="content3" cols="40" rows="3" class="form-control mb-3" required="" id="id_content3"></textarea>\
                 <label for="id_content4">Mensaje a Comunicar:</label>\
                 <textarea name="content4" cols="40" rows="3" class="form-control mb-3" required="" id="id_content4"></textarea>\
                 <label for="id_content5">Formato de Entrega Deseado:</label>\
                 <select name="content5" cols="40" rows="3" class="form-control mb-3" required="" id="id_content5">\
                    <option value=".jpg / .png">.jpg / .png</option>\
                    <option value=".pdf (Para Impresión)">.pdf (Para Impresión)</option>\
                    <option value=".eps / .psd / .ai (Editable)">.eps / .psd / .ai (Editable)</option>\
                 </select>\
            </div>');
        extraInfo.html(html);
    }else if (typeService.val() === "COMUNICADO") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Texto del Aviso o Comunicado:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Formato de Entrega Deseado:</label>\
                 <select name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2">\
                    <option value=".jpg / .png">.jpg / .png</option>\
                    <option value=".pdf (Para Impresión)">.pdf (Para Impresión)</option>\
                    <option value=".eps / .psd / .ai (Editable)">.eps / .psd / .ai (Editable)</option>\
                 </select>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "WEB") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Objetivos del sitio web:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Referencias para el sitio web:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "ACTUALIZACION") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Actualizaciones, Ajustes o Cambios a realizar:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Dirección URL de la Sección:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control mb-3" required="" id="id_content2"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "CONCURSOS") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Nombre Completo y Estado del Concurso (Formato Estándar):</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "CONVENIOS") {
        let html = (
            '<div CLASS="mb-3">\
                 <label for="id_content1">Nombre Completo del Convenio:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control mb-3" required="" id="id_content1"></textarea>\
            </div>');
        extraInfo.html(html);
    } else {
        extraInfo.html('<div id="extra-info"></div>');
    }
});