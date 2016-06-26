/*TODO: Clean this mess up and fix enhancement buttons needing two clicks to trigger*/
/*TODO: Seperate everything*/
$(function () {
    "use strict";
    $('#imageLoader').on('change', uploadImageFromForm);
    $(".filter-button").click(processImage);
    $(".tint").click(applyTint);
    $(".image-forms").on('submit', processImage);

    var input_slider = '<span class="EnhancementValue">1.0</span>' +
        '<input class="EnhancementFilter" type="range" min="-1.0" max="4.0" step="0.1" value="1.0">';

    $('[data-toggle="popover"]').popover({
        placement: "top", html: true,
        content: input_slider
    });

    $('body').on('click', function (e) {
        $('[data-toggle="popover"]').each(function () {
            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).popover('hide');
            }
        });
    });

    /*TODO: Optimize some of this stuff here*/

    $('[data-toggle="popover"]').on('shown.bs.popover', function () {
        $("input[type=range]").data('enhancement', $(this).data('enhancement'));
        $("input[type=range]").on('input', function () {
            $(".EnhancementValue").text($(this).val())
        });
        $("input[type=range]").on('change', function () {
            event.preventDefault();
            var dataURL = canvas.toDataURL();
            $.post($(this).data('enhancement') + "/", {
                imgBase64: dataURL,
                params: $(this).val()
            }, redrawCanvas);
        })
    });


    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');

    $(canvas).jqScribble({width: 0, height: 0, draw: false, brushSize: 4});

    function uploadImageFromForm(event) {
        var reader = new FileReader();
        reader.onload = function (theFile) {
            var img = new Image();
            $.post("upload/", {
                imgBase64: theFile.target.result
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

    function applyTint(event) {
        var dataURL = canvas.toDataURL();
        $.post($(this).data('operation') + "/", {
            imgBase64: dataURL,
            params: $(this).data('tint_name')
        }, redrawCanvas);
    }

    function saveImageOnServer(img_data) {
        $.post("process/", {
            imgBase64: theFile.target.result,
            action: $(this).data("action"),
            save: true,
            params: $(this).serialize()
        });
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
        canvas.height = image.height;
        canvas.width = image.width;
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
        var rect = canvas.parentNode.getBoundingClientRect();
        canvas.width = rect.width - 15;
        canvas.height = rect.height - 15;
    };


    var draw = false;

    $('button#draw').click(function () {
        $(canvas).data('jqScribble').update({draw: !draw});
        if (!draw)
            $(canvas).css('cursor', 'crosshair');
        else
            $(canvas).css('cursor', 'default');
        draw = !draw;
    });

    $('#cp4').colorpicker({align: 'left'}).on('changeColor', function (e) {
        $(".glyphicon-tint")[0].style.color = e.color.toHex();
        $(canvas).data('jqScribble').update({brushColor: e.color.toString('rgb')})
    });
    $(".nav-tabs").click(function () {
        console.log($($(".active").children('a')[0]).css('backgound-color'));
        $(this).css.borderTopColor = $(".active").css.background
    });
    /*
     $(window).on('resize', function () {
     var div = document.getElementsByClassName("image-canvas")
     canvas.height = div[0].offsetHeight;
     canvas.width = div[0].offsetWidth;
     }); */

});