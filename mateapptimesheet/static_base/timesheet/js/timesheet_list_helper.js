const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementById('id_q');

if (lan == "es") {
    search.placeholder = 'Cliente, Proyecto o Nombre:';
} else {
    search.placeholder = 'Customer, Project or Name:';
}