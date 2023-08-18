const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementsByClassName('q');

for (var i =0; i < search.length; i++) {
    if (lan == "es") {
        search[i].placeholder = 'Cliente, Proyecto o Nombre:';
    } else {
        search[i].placeholder = 'Customer, Project or Name:';
    }
}