$(function () {
    "use strict";
    $('#imageLoader').on('change', uploadImageFromForm);
    $(".filter-button").click(processImage);
    $(".image-forms").on('submit', processImage)
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');

    function saveImageOnServer(img_data) {
        $.post("process/", {
            imgBase64: theFile.target.result,
            action: $(this).data("action"),
            save: true,
            params: $(this).serialize()
        });
    }

    function uploadImageFromForm(event) {
        var reader = new FileReader();
        reader.onload = function (theFile) {
            var img = new Image();
            $.post("process/", {
                imgBase64: theFile.target.result,
                action: $(this).data("action"),
                save: true
            });
            img.onload = function () {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
            };
            img.src = theFile.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
    }

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
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var image = new Image();
        image.src = json.processed_image;
        if (image.width > canvas.width || image.height > canvas.height)
            fitToContainer(canvas);
        else {

            canvas.height = image.height;
            canvas.width = image.width;
        }
        ctx.drawImage(image, 0, 0);

    }

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        $(this).toggleClass("toggled");
    });

    $('.nav-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show')
    });
    function fitToContainer(canvas) {
        // Make it visually fill the positioned parent
        console.log(canvas.style.width);
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        // ...then set the internal size to match
        canvas.width = canvas.style.width;
        canvas.height = canvas.style.height;
    }

    window.onload = function () {
        var div = document.getElementsByClassName("image-canvas")
        canvas.height = div[0].offsetHeight - 7;
        canvas.width = div[0].offsetWidth - 7;
    };
    /*
     $(window).on('resize', function () {
     var div = document.getElementsByClassName("image-canvas")
     canvas.height = div[0].offsetHeight;
     canvas.width = div[0].offsetWidth;
     }); */
});