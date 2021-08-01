// Ramos con descripción
const ramos_arr = Object.values(ramos).filter((ramo) => (ramo.descripcion != "lorem ipsum" && ramo.descripcion != ""));
var ramos_filtered;

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

    for (let i = 0; i < ramos_filtered.length; i += 1){
        let ramo = ramos_filtered[i];
        let codigo = ramo.codigo;
        let ramo_concat = codigo.concat(" ").concat(ramo.nombre);
        $('#ramo_select')
            .append($('<option />')
            .val(codigo)
            .text(ramo_concat))
    }
}

// Obtener atributos del ramo
function getRamo(cod) {
    let ramo = ramos_filtered.find(obj => obj.codigo === cod);
    let ramo_concat = ramo.codigo.concat(" ").concat(ramo.nombre);
    document.getElementById("ramo_gigante").innerText = ramo_concat;
    
    let tags_str = "Áreas:\n"
    for (const tag in ramo.tags) {
        tags_str += ramo.tags[tag] + '\n'
    }
    document.getElementById("areas").innerText = tags_str;

    let desc_str = "Descripciones:\n"
    for (const opi in ramo.descripcion) {
        desc_str += ramo.descripcion[opi] + '\n'
    }
    document.getElementById("descripcion").innerText = desc_str;
    let diff_str = 'Dificultad:\n' + ramo.dificultad + ' (' + ramo.opiniones + ' opiniones)';
    document.getElementById("dificultad").innerText = diff_str;
}