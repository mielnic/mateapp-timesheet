const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementsByClassName('q');
const fSelector = document.getElementById('id_f');
const qForm = document.getElementById('qform');

for (var i =0; i < search.length; i++) {
    if (lan == "es") {
        search[i].placeholder = 'Cliente, Proyecto:';
    } else {
        search[i].placeholder = 'Customer, Project:';
    }
}

fSelector.addEventListener('change', (event) => { 
    qForm.submit();
});