/*TODO: Fix enhancement buttons needing two clicks to trigger*/
/*TODO: Seperate everything*/
/*TODO: Save image after drawing */
/*TODO: Add a radio button to either keep original image size or scale down to fit page */
/*TODO: Fix drawing and using the same last operation erasing what was drawn on canvas*/

$(function () {
    "use strict";
    var canvas = document.getElementsByTagName("canvas")[0];
    var ctx = canvas.getContext('2d');
    var current_image = new Image();
    var draw = false;
    var canvas_drawn_on = false;
    var processing_image = false;
    var canvas_wrapper = $("#canvas-wrapper")[0];
    var all_popovers = $('[data-toggle="popover"]');
    var imageLoader = $('#imageLoader');
    var nav_tabs = $('.nav-tabs');
    var navbar = $('.navbar');
    var tab_content = $('.tab-content');
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
        canvas_drawn_on = true;
    });

    /*###############################################*/

    $(window).on('resize', redrawCanvas);
    imageLoader.on('change', uploadImageFromForm);

    $('.btn-reset').click(function () {
        requestImageOperation('reset/', null, $(this));
    });

    $(".tint").click(function () {
        requestImageOperation($(this).data('operation') + '/', $(this).data('tint_name'), $(this));
    });

    $(".color-filter").click(function () {
        requestImageOperation($(this).data('operation') + '/', $(this).data('filter_name'), $(this));
    });
    $(".kernel-filter").click(function () {
        requestImageOperation($(this).data('operation') + '/', $(this).data('filter_name'), $(this));
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
            var button = $(this);
            var slider = $('.slider-input');
            slider.on('input', function () {
                $('.slider-value').text($(this).val())
            });
            slider.on('change', function (e) {
                e.preventDefault();
                requestImageOperation($(this).data('operation') + "/", $(this).val(), button);
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
        if (processing_image)
            return;
        processing_image = true;
        var reader = new FileReader();
        canvas_drawn_on = false;
        reader.onload = function (theFile) {
            var img = new Image();
            var temp_img = new Image();
            img.src = theFile.target.result;
            img.onload = function () {
                temp_img.src = jic.compress(img, 70, 'jpeg').src;
            };
            temp_img.onload = function () {
                $.ajax({
                    url: 'upload/',
                    type: 'POST',
                    dataType: 'json',
                    data: {imgBase64: temp_img.src},
                    beforeSend: function (xhr, settings) {
                        $.ajaxSettings.beforeSend(xhr, settings);
                        $('.btn-browse').html('<i class="fa fa-cog fa-spin fa-lg"></i>');
                    },
                    success: function () {
                        $('.btn-browse').html("Browse<input type='file' id='imageLoader' style='display: none;'>");
                        imageLoader = $('#imageLoader');
                        imageLoader.on('change', uploadImageFromForm);
                        processing_image = false;
                        updateCurrentImage({processed_image: temp_img.src})
                    }
                });
            };
        };
        reader.readAsDataURL(event.target.files[0]);
    }


    function requestImageOperation(op_url, op_params, button) {
        if (processing_image)
            return;
        processing_image = true;
        var op_data = {params: op_params};
        var original_text = button.html();
        /*var original_width = button.css('width');*/

        $.ajax({
            url: op_url,
            type: 'POST',
            data: op_data,
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
                button.html('<i class="fa fa-cog fa-spin fa-lg fa-fw"></i>')
            },
            success: function (json) {
                button.html(original_text);
                processing_image = false;
                updateCurrentImage(json)
            }
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
    $(".nav-tabs > li > a").click(function () {
        var background_color = $(this).css('background-color');
        nav_tabs.css({'border-top-color': background_color});
        navbar.css({'border-top-color': background_color});
    });

    function updateCurrentImage(json) {
        var image = new Image();
        image.src = json.processed_image;
        image.onload = function () {
            current_image = image;
            redrawCanvas();
        }
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