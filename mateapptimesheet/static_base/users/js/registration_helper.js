const spinner = document.getElementById('spinner')
const regform = document.getElementById('regform')

spinner.style.display = 'none';

function displaySpinner(){
    spinner.style.display = 'block';
    regform.style.display = 'none';
}