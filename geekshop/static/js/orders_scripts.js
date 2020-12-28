let dropdown_menu_label = document.querySelector(".dropdown");
let dropdown_menu = document.querySelector(".dropdown-menu");

dropdown_menu_label.addEventListener('click', function (event) {
    if (dropdown_menu.style.display){
        dropdown_menu.style.display = ''
    }
    else{
        dropdown_menu.style.display = 'block'
    }

});