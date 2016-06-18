$(function () {
    "use strict";
    $('#imageLoader').on('change', handleImage);
    $(".filter-button").click(processImage);
    $(".image-forms").on('submit', processImage)
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');

    function handleImage(event) {
        var reader = new FileReader();
        reader.onload = function (theFile) {
            var img = new Image();
            img.onload = function () {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
            };
            img.src = theFile.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
    }

    function processImage(event) {
        event.preventDefault();
        console.log(event);
        var dataURL = canvas.toDataURL();
        $.post("process/", {
            imgBase64: dataURL,
            action: $(this).data("action"),
            params: $(this).serialize()
        }, redrawCanvas);
    }

    function redrawCanvas(json) {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        var image = new Image();
        image.src = json.processed_image;
        canvas.height = image.height;
        canvas.width = image.width;
        ctx.drawImage(image, 0, 0);
    }


});