$(document).ready(function(){
	function timeFields(el) {
		el.find('.time-field').parent().datetimepicker({pickDate: false, pickSeconds: false, 
			language:'{{ request.LANGUAGE_CODE }}'});
			$(document).trigger('sizing');
	
	}

	timeFields($('body'));

	var sq_id = 0;
	
	var time_block_template = _.template($("#time_block_template").html());
	
	var error_msg_template = _.template($("#error_msg_template").html());
	var error_msg_template_gt = _.template($("#error_msg_template_gt").html());
	var error_msg_template_eq = _.template($("#error_msg_template_eq").html());
	var error_msg_template_overlap = _.template($("#error_msg_template_overlap").html());
	var error_msg_template_page_errors = _.template($("#error_msg_template_page_errors").html());
	
	$("#data_ctrls").on("click","a.add_wblock", function(e){		
		e.preventDefault();
		
		var week_id = $(this).attr("week_id");
		
		//console.log(time_block_template({"key":week_id}));

		var block_div = $(this).before(time_block_template({"seq_id":sq_id,"key":week_id}));
		
		timeFields($("#XK_"+sq_id));
		//timeFields(block_div);
		
		//console.log(block_div);
		
		sq_id++;

	});
	
	
	$("#data_ctrls").on("click","a.remove_wblock", function(e){		
		e.preventDefault();
		
		//console.log($(this).parent());
		
		$(this).closest(".edit-time-block").remove();
	});
	
	$("#save_btn").on("click",function(e){
		field_full_check();
		
		$(".page_save_error").remove();
		
		if($(".error_container:visible").length){
			
			$(".prep_save_erro").before(error_msg_template_page_errors({}));
			
			e.preventDefault();
		}
		
	});
	
	var getIntTimeFromInput = function(inpt){
		var time_test = /^([0-9]{1,2}):([0-9]{1,2})$/;
		
		var match = time_test.exec(inpt.val());	
		
		//console.log(match);
		
		if(match){
			//console.log(parseInt(match[1],10) , parseInt(match[2]),10);
			return parseInt(match[1],10)*100 + parseInt(match[2],10);
		}else{
			return null;
		}
	}
	
	var overlapCheck = function(blockA, blockB){
		//(StartA <= EndB)  and  (EndA >= StartB)
		return (blockA.start<=blockB.end) && (blockA.end>=blockB.start);
	}
	
	
	var dayBlockTimesCheck = function(dayblock, timeblockx){
		var time_blocks = [];
	
		sl = null;
	
		dayblock.find(".edit-time-block").each(function(i,val){	
			var inputs = $(val).find("input.time-field");

			var f_input = $(inputs.get(0));
			var s_input = $(inputs.get(1));	
		
			if(timeblockx.get(0)==val){
				sl = {'start':getIntTimeFromInput(f_input),'end':getIntTimeFromInput(s_input),'start_input':f_input,'end_input':s_input,'timeblock':$(val)};
			
				return;
			}
		
	
		
			time_blocks.push({'start':getIntTimeFromInput(f_input),'end':getIntTimeFromInput(s_input),'start_input':f_input,'end_input':s_input,'timeblock':$(val)});
		
		});
	
		if(!sl){
			//console.log("not gud", timeblockx);
			return false;
		}
	
		var status = true;
		for(var i=0;i<time_blocks.length;i++){
				if(!time_blocks[i].start || !time_blocks[i].end || !sl.start || !sl.end){
					continue;
				}
				//(StartA <= EndB)  and  (EndA >= StartB)
				if(overlapCheck(time_blocks[i],sl)){
					//console.log(time_blocks[i],sl);
					//displayTimeBlockError(time_blocks[j]);
					status = false;
				}
			
		}
		
		return status;
	}
	
	var timeBlockCheck = function(edit_time_block, input){
		var error_block = edit_time_block.find(".error_container");

		error_block.hide();
		error_block.empty();
		
		var inputs = edit_time_block.find("input.time-field");

		var f_input = $(inputs.get(0));
		var s_input = $(inputs.get(1));
		
		f_input.removeClass('error');
		s_input.removeClass('error');
		
		//edit_time_block.removeClass("alert");
		//edit_time_block.removeClass("alert-error");
		
		var functionError = function(){
			//edit_time_block.addClass("alert");
			//edit_time_block.addClass("alert-error");
			error_block.show();
		}
		
		var error0 = false;
		var error1 = false;
		
		var val0, val1;
		if(!(val0 = getIntTimeFromInput(f_input))){
			f_input.addClass("error");
			error0 = true;
		}
		
		
		if(!(val1 = getIntTimeFromInput(s_input))){
			s_input.addClass("error");
			error1 = true;
		}
		
		if(error0 || error1){
			functionError();
			
			error_block.append(error_msg_template({}));
		
			return false;
		}
		
		
		if(val0 > val1){
			functionError();
			
			error_block.append(error_msg_template_gt({}));

			return false;
		}else
		if(val0 == val1){
			functionError();
			
			error_block.append(error_msg_template_eq({}));

			return false;
		}
		
		//TODO: overlap test!
		var dayblock = edit_time_block.closest(".week_times");
		if(!dayBlockTimesCheck(dayblock, edit_time_block)){
			functionError();
			
			error_block.append(error_msg_template_overlap({}));
			
			return false;
		}
		
		
		return true;
	}
	

	var field_full_check = function(){
		var edit_time_block = $(".edit-time-block");
		
		edit_time_block.each(function(i,v){
			//console.log("INP",v);
			timeBlockCheck($(v), null);
		});
	}
	
	var field_change_clbck = function(){
		var inpt = $(this);
		var edit_time_block = inpt.closest(".edit-time-block");
		timeBlockCheck(edit_time_block, inpt);
	}
	
	
	$("#data_ctrls").on("change","input.time-field", field_change_clbck);
	$("#data_ctrls").on("blur","input.time-field", field_change_clbck);
	//$("#data_ctrls").on("","input.time-field", field_change_clbck);
	
});