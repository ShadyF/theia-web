/*TODO: Fix enhancement buttons needing two clicks to trigger*/
/*TODO: Seperate everything*/
/*TODO: Save image after drawing */
/*TODO: Add a radio button to either keep original image size or scale down to fit page */
$(function () {
    "use strict";
    var canvas = document.getElementsByTagName("canvas")[0];
    var ctx = canvas.getContext('2d');
    var current_image = new Image();
    requestImageOperation('reset/', null);
    var draw = false;
    var canvas_wrapper = $("#canvas-wrapper")[0];
    var all_popovers = $('[data-toggle="popover"]');

    /*###############################################
     ##        DRAWING RELATED FUNCTIONS          ##
     ###############################################*/

    $(canvas).jqScribble({width: 0, height: 0, draw: false, brushSize: 4});

    $('#color-picker').colorpicker({align: 'left'}).on('changeColor', function (e) {
        $(".glyphicon-tint")[0].style.color = e.color.toHex();
        $(canvas).data('jqScribble').update({brushColor: e.color.toString('rgb')})
    });

    $('#draw-button').click(function () {
        $(canvas).data('jqScribble').update({draw: !draw});
        if (!draw)
            $(canvas).css('cursor', 'crosshair');
        else
            $(canvas).css('cursor', 'default');
        draw = !draw;
    });

    /*###############################################*/

    $(window).on('resize', redrawCanvas);
    $('#imageLoader').on('change', uploadImageFromForm);

    $('.btn-reset').click(function () {
        requestImageOperation('reset/', null);
    });
    $('.btn-download').click(function () {
        console.log(current_image.width);
        var dataURL = canvas.toDataURL('image/png');
        $(this)[0].href = dataURL;
    });
    $(".tint").click(function () {
        requestImageOperation($(this).data('operation') + '/', $(this).data('tint_name'));
    });

    $(".color-filter").click(function () {
        requestImageOperation($(this).data('operation') + '/', $(this).data('filter_name'));
    });

    $('.nav-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show')
    });

    all_popovers
        .popover({
            placement: "top", html: true
        })
        .on('shown.bs.popover', function () {
            var slider = $('.slider-input');
            slider.on('input', function () {
                $('.slider-value').text($(this).val())
            });
            slider.on('change', function (e) {
                e.preventDefault();
                requestImageOperation($(this).data('operation') + "/", $(this).val());
            });
        });


    $('body').on('click', function (e) {
        all_popovers.each(function () {
            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).popover('hide');
            }
        });
    });

    function uploadImageFromForm(event) {
        var reader = new FileReader();
        reader.onload = function (theFile) {
            var img = new Image();
            img.src = theFile.target.result;

            $.post("upload/", {
                imgBase64: theFile.target.result
            });
            img.onload = function () {
                current_image = img;
                redrawCanvas();
            };
        };
        reader.readAsDataURL(event.target.files[0]);
    }


    function requestImageOperation(op_url, op_params) {
        var dataURL = canvas.toDataURL();
        var op_data = null;

        if (op_url != 'reset/')
            op_data = {
                imgBase64: dataURL,
                params: op_params
            };

        $.ajax({
            url: op_url,
            type: 'POST',
            data: op_data,
            success: updateCurrentImage
        });
    }

    $(".menu-toggle").click(function (e) {
        e.preventDefault();
        var wrapper = $('#wrapper');
        wrapper.toggleClass("toggled");
        $(this).toggleClass('menu-toggle-active');

        wrapper.one(' otransitionend oTransitionEnd msTransitionEnd transitionend', function () {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            var divHeight = canvas_wrapper.offsetHeight - 30;
            var divWidth = canvas_wrapper.offsetWidth - 30;
            var aspectRatio = current_image.width / current_image.height;

            var newImgHeight = current_image.height;
            var newImgWidth = current_image.width;

            if (newImgHeight > divHeight && newImgWidth > divWidth) {
                if (newImgHeight > newImgWidth) {
                    newImgHeight = divHeight;
                    newImgWidth = newImgHeight * aspectRatio;
                }
                else {
                    newImgWidth = divWidth;
                    newImgHeight = newImgWidth / aspectRatio;
                }
            }
            else if (newImgWidth > divWidth) {
                newImgWidth = divWidth;
                newImgHeight = newImgWidth / aspectRatio;
            }
            else if (newImgHeight > divHeight) {
                newImgHeight = divHeight;
                newImgWidth = newImgHeight * aspectRatio;
            }
            canvas.width = newImgWidth;
            canvas.height = newImgHeight;
            ctx.drawImage(current_image, 0, 0, canvas.width, canvas.height);
        })
    });

    window.onload = function () {
        var divHeight = canvas_wrapper.clientHeight - 30;
        var divWidth = canvas_wrapper.clientWidth - 30;
        canvas.height = divHeight + 600;
        canvas.width = divWidth + 600;
        current_image.height = divHeight;
        current_image.width = divWidth;
        redrawCanvas()
    };


    /* TODO: Make tab panes have the same background color as their nav tab links */
    $(".nav-tabs").click(function () {
        console.log($($(".active").children('a')[0]).css('backgound-color'));
        $(this).css.borderTopColor = $(".active").css.background
    });

    function updateCurrentImage(json) {
        var image = new Image();
        image.src = json.processed_image;
        current_image = image;
        redrawCanvas();
    }

    /*TODO: Take into account the aspect ratio of the div aswell as the canvas overflows, in some cases, when image is large*/
    function redrawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var divHeight = canvas_wrapper.clientHeight - 30;
        var divWidth = canvas_wrapper.clientWidth - 30;
        var aspectRatio = current_image.width / current_image.height;

        var newImgHeight = current_image.height;
        var newImgWidth = current_image.width;

        if (newImgHeight > divHeight && newImgWidth > divWidth) {
            if (newImgHeight > newImgWidth) {
                newImgHeight = divHeight;
                newImgWidth = newImgHeight * aspectRatio;
            }
            else {
                newImgWidth = divWidth;
                newImgHeight = newImgWidth / aspectRatio;
            }
        }
        else if (newImgWidth > divWidth) {
            newImgWidth = divWidth;
            newImgHeight = newImgWidth / aspectRatio;
        }
        else if (newImgHeight > divHeight) {
            newImgHeight = divHeight;
            newImgWidth = newImgHeight * aspectRatio;
        }
        canvas.width = newImgWidth;
        canvas.height = newImgHeight;
        ctx.drawImage(current_image, 0, 0, canvas.width, canvas.height);
    }
});