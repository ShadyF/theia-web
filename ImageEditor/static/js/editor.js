$(function () {
    "use strict";
    $('#imageLoader').on('change', handleImage);
    $("#upload").click(sharpen);
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

    function sharpen(event) {
        var dataURL = canvas.toDataURL();
        $.post("process/", {imgBase64: dataURL, action: "sharpen"}, redrawCanvas);
    }

    function redrawCanvas(json) {
        var image = new Image();
        image.src = json.processed_image;
        ctx.drawImage(image, 0, 0);
    }


});