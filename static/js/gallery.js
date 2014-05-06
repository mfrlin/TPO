$(document).ready(function () {

    $("body").on('click', ".img-selected", function (e) {
        e.stopPropagation();
    });

	function isInputDirSupported() {
		var tmpInput = document.createElement('input');
		if ('webkitdirectory' in tmpInput 
			|| 'mozdirectory' in tmpInput 
			|| 'odirectory' in tmpInput 
			|| 'msdirectory' in tmpInput 
			|| 'directory' in tmpInput) return true;

		return false;
	}

	var addGalleryImage = function(file){
		var outer_box = $('<div class="col-lg-3 col-md-4 col-xs-6"></div>');
		var fancy_box = $('<a></a>');
		fancy_box.addClass('fancybox');
		fancy_box.addClass('thumbnail');
		fancy_box.attr({'href':media_url+''+file.url,'data-fancybox-group':'gallery','title':file.name});
		
		var image = $('<img width="140" height="140" />');
		image.addClass('img-responsive');
		image.attr({'src':media_url+''+file.url});
		
		image.appendTo(fancy_box);
		
		fancy_box.appendTo(outer_box);
		
		var label = $('<label class="checkbox"></label>');
		
		var input_ceh = $('<input type="checkbox" class="img-selected" name="img_id" />');
		input_ceh.attr({'value':file.id});
		
		input_ceh.appendTo(label);
		
		label.appendTo(outer_box);
		
		outer_box.insertBefore($("#gallery_anchor"));
	};

	$(document).ready(function(){
		if(!isInputDirSupported()){
			$("#image_uploader_folder_button").hide();
		}
	
	
		$('.image-upload-bundle').fileupload({
			url: "/gallery/"+provider_id+"/upload",
			dataType: 'json',
			autoUpload: false,
			singleFileUploads: true,
			sequentialUploads: true,
			paramName:'image',
			//acceptFileTypes: /(\.|\/)(jpe?g|png)$/i,
			add: function(e, data){
			},
			done: function (e, data) {
			},
			progressall: function (e, data) {
				var progress = parseInt(data.loaded / data.total * 100, 10);
				//console.log(progress);
				$('#uploadprogress').css('width',progress + '%');
			}
		}).on('fileuploadadd', function (e, data) {
			//console.log("!",data, data.files.length);
			var added_count = 0;
		
			$.each(data.files, function (index, file) {
                var reg = /jpe?g|png|JPE?G|PNG/;
                var ext = file.name.split('.').slice(-1)[0];
                if (reg.exec(ext) === null){
                    return;
                }

				var row = $('<div class="fluid-row clearfix"><div class="innerdiv span12"></div></div>');
				
				data.context_row = row;
			
				var node = ($('<span class="caption-name" style="margin-left:10px"></span>').text(file.name));
				var control = $('<a class="file-control btn btn-danger btn-mini cancel"><i class="icon-remove"></i></a>');
				var control_upload = $('<a class="file-control btn btn-info btn-mini submit" style="margin-left:5px"><i class="icon-upload"></i></a>');
				
				control.appendTo(row.find('div.innerdiv'));
				control_upload.appendTo(row.find('div.innerdiv'));
				
				node.appendTo(row.find('div.innerdiv'));
			
				row.appendTo($('#image_list'));
				
				control.on('click', function(e){
					e.preventDefault();
					
					data.abort();
					
					row.remove();
				});
				
				control_upload.on('click', function(e){
					e.preventDefault();
					
					if($(this).attr('disabled'))
						return;
					
					data.submit();
				});
				
				added_count++;
			});
			
			if(added_count>0){
				$("#uploaded_files_list").show();
			}
			
		}).on('fileuploadsubmit', function(e, data){
			//console.log("submited", e, data);
			
			data.context_row.find("a.file-control").attr('disabled',true);
			
		}).on('fileuploaddone', function(e, data){
			//console.log("done", e, data);
			$.each(data.result.files,function(index, file){
				//console.log("\tfiel", file)
				
				if('error' in file){
					data.context_row.find('span.caption-name')
						.html('<span class="label label-important" >'+gettext("Error")+'</span> <span class="">'
							+file.name+' {%trans "failed with" %} '+file.error+'</span>');
				}else{
					addGalleryImage(file);
					
					data.context_row.find('span.caption-name')
						.html('<span class="label label-success" >'+gettext("Completed")+'</span> '+file.name);
						
				}
			});
			
			
		}).on('fileuploadprogress', function(e, data){
			//console.log("done", e, data);

			var progress = parseInt(data.loaded / data.total * 100, 10);
			
			data.context_row.find('span.caption-name')
				.html('<span class="label label-info" >'+progress+'%</span> '+data.files[0].name);
		}).on('fileuploadfail', function(e, data){
			//console.log("fileuploadfail", e, data);

			data.context_row.find('span.caption-name')
				.html('<span class="label label-important" >{% trans "Error" %}</span> <span class="">'
					+data.files[0].name+' Something went horribly wrong. Error message: '+data.errorThrown+'</span>');
		});
		
	
		$("#upload_files").on("click", function(e){
			e.preventDefault();
			
			$('#image_list a.submit').trigger('click');
			
		});
	});

    if (navigator.getUserMedia) {
        $("#take_photo_camera").show();
        //console.log("Camera supported");
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