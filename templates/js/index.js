var loadFile = function(event, IMG) {
    var image = document.getElementById(IMG);
    image.src = URL.createObjectURL(event.target.files[0]);
};