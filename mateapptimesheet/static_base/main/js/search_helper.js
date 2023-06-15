const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementById('id_q');

if (lan == "es") {
    search.placeholder = 'Lo que busques:';
} else {
    search.placeholder = 'Anything:';
}