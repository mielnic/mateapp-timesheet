/* Paginator Helper */
let currentURL = window.location.pathname
let currentLink = document.querySelectorAll(`[href='${currentURL}']`)

function paginator(item){
    (item.getAttribute("id") == 'page-link')? item.parentNode.setAttribute('class','active') : item.parentNode.setAttribute('class', 'disabled');
}

currentLink.forEach(paginator)