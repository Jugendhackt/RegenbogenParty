window.onload = function() {
    //document.getElementById("otherbutton").style.visibility = "hidden";
}
function toggleMenu() {
    var menu = document.getElementById("menu");
    var otherbutton = document.getElementById("otherbutton");
    if (menu.style.visibility == "hidden") {
        menu.style.visibility = "visible";
        otherbutton.style.visibility = "hidden";
    } else {
        menu.style.visibility = "hidden";
        otherbutton.style.visibility = "visible";
    }
}