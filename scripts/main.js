// Ramos con descripción
const ramos_arr = Object.values(ramos).filter((ramo) => (ramo.dificultad !== -1));
let ramos_filtered;

const diff_dict = {
    1: "Muy fácil",
    2: "Fácil",
    3: "Medio",
    4: "Difícil",
    5: "Muy difícil"
}

const tiempo_dict = {
    1: "Mucho menos de su valor en créditos",
    2: "Menos de su valor en créditos",
    3: "Aproximadamente su valor en créditos",
    4: "Más de su valor en créditos",
    5: "Mucho más de su valor en créditos"
}

const area_dict = {
    "Programación": "programacion",
    "Teoría": "teoria",
    "Datos": "datos",
    "Arquitectura": "arquitectura",
    "Redes": "redes",
    "Software": "software",
    "Gráfica": "grafica",
    "Seguridad": "seguridad",
    "HCI": "hci",
    "Investigación": "investigacion",
    "Machine Learning": "machinelearning",
    "Sistemas": "sistemas",
    "Industria": "industria"
}

// Función para ordenar por código
function compareByPK(a, b) {
    if (a.codigo < b.codigo) {
        return -1;
    }
    if (a.codigo > b.codigo) {
        return 1;
    }
    return 0;
}

// Tras seleccionar si es de malla o no, llenar el dropdown
function malla_check(value) {
    let malla = value === "1";

    ramos_filtered = ramos_arr.filter((obj) => obj.malla === malla)
    ramos_filtered.sort(compareByPK);

    let ramo_select = $('#ramo_select')
    ramo_select.empty();

    for (let i = 0; i < ramos_filtered.length; i += 1){
        let ramo = ramos_filtered[i];
        let codigo = ramo.codigo;
        let ramo_concat = codigo.concat(" ").concat(ramo.nombre);
        ramo_select
            .append($('<option />')
            .val(codigo)
            .text(ramo_concat))
    }
    
    ramo_select.append($('<option />').val("").text("---------------------------------"));
    let ramo_select_option = $('#ramo_select option[value=""]')
    ramo_select_option.prop("selected", "selected");
    ramo_select_option.prop("disabled", "disabled");
    ramo_select_option.prop("hidden", "hidden");
}

// Función para llenar las descripciones/comentarios del ramo
function feed(lista_respuestas, div) {
    for (const opi in lista_respuestas) {
        let respuesta = document.createElement('div');

        let respuestaFecha = document.createElement('div');
        $(respuestaFecha)
            .addClass("respuesta-fecha")
            .html('(' + lista_respuestas[opi].fecha + ')')
            .appendTo(respuesta)

        let respuestaTexto = document.createElement('div');
        $(respuestaTexto)
            .addClass("respuesta-texto")
            .html(lista_respuestas[opi].texto)
            .appendTo(respuesta)

        $(respuesta).appendTo(div)
    }
}

// Obtener atributos del ramo
function getRamo(codigo) {
    
    // Nombre
    
    let ramo = ramos_filtered.find(obj => obj.codigo === codigo);
    document.getElementById("ramo_gigante_p").innerText = ramo.codigo.concat(" ").concat(ramo.nombre);
    
    // Áreas

    let areas = $('#areas')
    areas.empty();
    for (const tag in ramo.tags) {
        let tag_str = ramo.tags[tag];
        let tag_div = area_dict[tag_str];
        if (tag_div === undefined) {
            tag_div = "otro";
        }

        let d = document.createElement('div');
        $(d).addClass("area border rounded area-" + tag_div)
            .html(tag_str)
            .appendTo(areas)
    }

    // Descripciones

    let descripciones = $('#descripciones')
    document.getElementById("descripcionHead").innerText = "¿De qué se trata este ramo?";
    descripciones.empty();
    feed(ramo.descripciones, descripciones)

    // Comentarios

    let comentarios = $('#comentarios')
    document.getElementById("comentarioHead").innerText = "Comentarios adicionales:";
    comentarios.empty();
    feed(ramo.comentarios, comentarios)

    // Dificultad

    let diff_str = "Dificultad:\n"
    let diff
    if (ramo.dificultad !== -1) {
        diff = ramo.dificultad
        let diff_val = diff_dict[Math.round(diff)]
        diff_str += ramo.dificultad + '/5 - ' + diff_val + ' (' + ramo.opiniones + ' opiniones)';
    } else {
        diff_str += 'No hemos recibido comentarios.'
    }
    document.getElementById("dificultad").innerText = diff_str;

    $('.diff').each(function() {
        let color_class = 'diff' + Math.round(diff).toString();
        
        for (let i = 1; i <= 5; i++) {
            $(this).removeClass("diff" + i.toString());
        }

        $(this).addClass(color_class);
    })

    // Tiempo

    let tiempo_str = 'Tiempo dedicado:\n'
    if (ramo.tiempo !== -1) {
        let tiempo = ramo.tiempo
        let tiempo_val = tiempo_dict[Math.round(ramo.tiempo)]
        tiempo_str += tiempo + '/5 - ' + tiempo_val + ' (' + ramo.opiniones + ' opiniones)'
    } else {
        tiempo_str += 'No hemos recibido comentarios.'
    }
    document.getElementById("tiempo").innerText = tiempo_str;

    if (ramo.tiempo !== -1) {
        console.log(ramo.tiempo)
        $('.tiempo').each(function() {
            let color_class = 'tiempo' + Math.round(ramo.tiempo).toString();
            console.log(color_class)

            for (let i = 1; i <= 5; i++) {
                $(this).removeClass("tiempo" + i.toString());
            }

            $(this).addClass(color_class);
        })
    }
}