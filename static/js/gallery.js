$(document).ready(function () {

    $("body").on('click', ".img-selected", function (e) {
        e.stopPropagation();
    });

    $(".form-actions").on('click', "#select_files_mode > .btn", function (e) {
        e.stopPropagation();

        $("#select_files_mode > button").removeClass("active");
        $(this).addClass("active");

        var state = $("#select_files_mode").find(".active").val();
        var images_id = $("#" + id);
        if (state === "files") {
            images_id.removeAttr("directory");
            images_id.removeAttr("webkitdirectory");
            images_id.removeAttr("mozdirectory");
            images_id.removeAttr("capture");

            //console.log("files");
        } else if (state === "folder") {
            images_id.removeAttr("directory");
            images_id.removeAttr("webkitdirectory");
            images_id.removeAttr("mozdirectory");
            images_id.removeAttr("capture");

            images_id.attr({"directory": "", "webkitdirectory": "", "mozdirectory": ""});

            //console.log("folder");
        } else if (state === "camera") {
            images_id.removeAttr("directory");
            images_id.removeAttr("webkitdirectory");
            images_id.removeAttr("mozdirectory");
            images_id.removeAttr("capture");

            images_id.attr({"capture": "camera", "accept": "image/*"});

            //console.log("camera");
        }
    });

    if (navigator.getUserMedia) {
        $("#take_photo_camera").show();
        console.log("Camera supported");
    } else {
        $("#take_photo_camera").hide();
        console.log("Camera unsupported");
    }

    $("#take_photo_camera").on('click', function (e) {
        $("#camera_display").toggle();
        $("#take_photo_camera").toggleClass('active');

        e.stopPropagation();

        if ($("#camera_display").is(":visible")) {

            var video = document.getElementById('video');
            if (navigator.getUserMedia) {
                video.onclick = function () {
                    if (!video.paused) {

                        var canvas = document.getElementById("canvastt");
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;

                        var context = canvas.getContext("2d");
                        context.drawImage(video, 0, 0);

                        $("#upload_photo").show();

                        setTimeout(function () {
                            video.pause();
                        }, 200);

                        $("#captured_photo").val(canvas.toDataURL("image/jpeg"));
                    } else {
                        $("#upload_photo").hide();

                        video.play();
                    }
                };
                var success = function (stream) {
                    video.src = stream;
                };

                var error = function (err) {
                    console.log("Error: " + err.code, err);
                };

                navigator.getUserMedia('video', success, error);

            }

        } else {
            var video = document.getElementById('video');
            video.pause();
        }
    });
});