$("#id_category").change(function () {
    let dynamicSelect = $("#dynamic-select");
    let category = $("#id_category");
    if (category.val() == 1) {
        let html = (
            '<label for="id_service">Servicio a Solicitar:</label>\
            <select id="type-service" class="form-control" name="press-redaction" style="margin-bottom:5px;">\
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
    } else {
        dynamicSelect.html('<div id="dynamic-select"></div>');
    }
});

$("#dynamic-select").on("change", "#type-service", function () {
    let typeService = $("#type-service");
    let extraInfo = $("#extra-info");
    if (typeService.val() === "DISCURSO") {
        let html = (
            '<div>\
                 <label for="id_content1">Informe Completo:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Objetivo:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control" required="" id="id_content2"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "GACETILLA") {
        let html = (
            '<div>\
                 <label for="id_content1">Informe completo de la actividad:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Programa:</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control" required="" id="id_content2"></textarea>\
                 <label for="id_content3">Contactos (Tel, Cel, e-mail, link):</label>\
                 <textarea name="content3" cols="40" rows="3" class="form-control" required="" id="id_content3"></textarea>\
            </div>');
        extraInfo.html(html);
    } else if (typeService.val() === "REDES") {
        let html = (
            '<div>\
                 <label for="id_content1">Informe completo de la actividad:</label>\
                 <textarea name="content1" cols="40" rows="3" class="form-control" required="" id="id_content1"></textarea>\
                 <label for="id_content2">Contactos (Tel, Cel, e-mail, link):</label>\
                 <textarea name="content2" cols="40" rows="3" class="form-control" required="" id="id_content2"></textarea>\
            </div>');
        extraInfo.html(html);
    } else{
        extraInfo.html('<div id="extra-info"></div>');
    }
});