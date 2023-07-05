const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementById('id_q');

if (lan == "es") {
    search.placeholder = 'Proyecto, Cliente, Inactive:';
} else {
    search.placeholder = 'Project, Customer, Inactive:';
}