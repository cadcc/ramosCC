// Ramos con descripción
const ramos_arr = Object.values(ramos).filter((ramo) => (ramo.descripcion != "lorem ipsum" && ramo.descripcion != ""));
var ramos_filtered;

const diff_dict = {
    1: "Muy fácil",
    2: "Fácil",
    3: "Medio",
    4: "Difícil",
    5: "Muy difícil"
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
    if (value == 1) {
        var malla = true
    } else {
        var malla = false
    }

    ramos_filtered = ramos_arr.filter((obj) => obj.malla === malla)
    ramos_filtered.sort(compareByPK);

    $('#ramo_select').empty();

    for (let i = 0; i < ramos_filtered.length; i += 1){
        let ramo = ramos_filtered[i];
        let codigo = ramo.codigo;
        let ramo_concat = codigo.concat(" ").concat(ramo.nombre);
        $('#ramo_select')
            .append($('<option />')
            .val(codigo)
            .text(ramo_concat))
    }
    
    $('#ramo_select').append($('<option />').val("").text("---------------------------------"));
    $('#ramo_select option[value=""]').prop("selected", "selected");
    $('#ramo_select option[value=""]').prop("disabled", "disabled");
    $('#ramo_select option[value=""]').prop("hidden", "hidden");


}

// Obtener atributos del ramo
function getRamo(cod) {
    
    // Nombre
    
    let ramo = ramos_filtered.find(obj => obj.codigo === cod);
    let ramo_concat = ramo.codigo.concat(" ").concat(ramo.nombre);
    document.getElementById("ramo_gigante_p").innerText = ramo_concat;
    
    // Áreas

    $("#areas").empty();
    for (const tag in ramo.tags) {
        tag_str = ramo.tags[tag];
        tag_div = area_dict[tag_str];
        if (tag_div === undefined) {
            tag_div = "otro";
        }

        d = document.createElement('div');
        $(d).addClass("area border rounded area-" + tag_div)
            .html(tag_str)
            .appendTo($("#areas"))
    }
    

    // Descripciones

    let desc_str = "Descripciones:\n"
    var descs = [];
    document.getElementById("descripcionHead").innerText = "Descripciones de este ramo:";
    $('#descripcion').empty();
    for (const opi in ramo.descripcion) {
        descs.push($('<li/>').text(ramo.descripcion[opi]));
    }
    $('#descripcion').append.apply($('#descripcion'), descs);

    // Dificultad

    if (ramo.dificultad != -1) {
        var diff = ramo.dificultad
        var diff_val = diff_dict[Math.round(diff)]
        var diff_str = 'Dificultad:\n' + ramo.dificultad + ' - ' + diff_val + ' (' + ramo.opiniones + ' opiniones)';
    } else {
        var diff_str = 'Dificultad:\n' + 'No hemos recibido comentarios.'
    }
    document.getElementById("dificultad").innerText = diff_str;

    $('.diff').each(function() {
        color_class = 'diff' + Math.round(diff).toString();
        
        for (var i = 1; i <= 5; i++) {
            $(this).removeClass("diff" + i.toString());
        }

        $(this).addClass(color_class);
    })
}