const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementsByClassName('q');
const fSelector = document.getElementById('id_f');
const qForm = document.getElementById('qform');


for (var i =0; i < search.length; i++) {
    if (lan == "es") {
        search[i].placeholder = 'Nombre:';
    } else {
        search[i].placeholder = 'Name:';
    }
} 

fSelector.addEventListener('change', (event) => { 
    qForm.submit();
});