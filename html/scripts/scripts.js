// для секции
function show_hide(id){
    var node = document.getElementById(id);
    var parentNode = node.parentNode;
    var ch = parentNode.children[1];

    display = ch.style.display;
    if (display == "block"){
        ch.style.display = "none";
    } 
    else{
        ch.style.display = "block";
    }
}