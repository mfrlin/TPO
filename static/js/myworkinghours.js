$(document).ready(function () {
    function timeFields(el) {
        el.find('.time-field').parent().datetimepicker({pickDate: false, pickSeconds: false,
            language: '{{ request.LANGUAGE_CODE }}'});
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
    var ctrls = $("#data_ctrls");

    ctrls.on("click", "a.add_wblock", function (e) {
        e.preventDefault();

        var week_id = $(this).attr("week_id");

        var block_div = $(this).before(time_block_template({"seq_id": sq_id, "key": week_id, "from": "", "to": ""}));

        timeFields($("#XK_" + sq_id));

        sq_id++;

    });


    ctrls.on("click", "a.clone_wblock", function (e) {
        e.preventDefault();

        var week_id = $(this).attr("week_id");

        var time_blck_vals = timeBlockValues($(this).closest(".week_times"));

        for (var i = 1; i <= 7; i++) {
            if (i == week_id) {
                continue;
            }

            var week_blck = $("#week_id_" + i);

            if (week_blck.find(".edit-time-block").length) {
                continue;
            }

            $.each(time_blck_vals, function (j, v) {

                var data = time_block_template({"seq_id": sq_id, "key": i, "from": v[0], "to": v[1]});

                week_blck.prepend(data);

                sq_id++;
            });

        }

    });


    ctrls.on("click", "a.remove_wblock", function (e) {
        e.preventDefault();

        $(this).closest(".edit-time-block").remove();
    });

    $("#save_btn").on("click", function (e) {
        field_full_check();

        $(".page_save_error").remove();

        if ($(".error_container:visible").length) {

            $(".prep_save_erro").before(error_msg_template_page_errors({}));

            e.preventDefault();
        }

    });

    var getIntTimeFromInput = function (inpt) {
        var time_test = /^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$/;

        var match = time_test.exec(inpt.val());

        if (match) {
            return parseInt(match[1], 10) * 100 + parseInt(match[2], 10);
        } else {
            return null;
        }
    };

    var overlapCheck = function (blockA, blockB) {
        //(StartA <= EndB)  and  (EndA >= StartB)
        return (blockA.start <= blockB.end) && (blockA.end >= blockB.start);
    };


    var dayBlockTimesCheck = function (dayblock, timeblockx) {
        var time_blocks = [];

        var sl = null;

        dayblock.find(".edit-time-block").each(function (i, val) {
            var inputs = $(val).find("input.time-field");

            var f_input = $(inputs.get(0));
            var s_input = $(inputs.get(1));

            if (timeblockx.get(0) == val) {
                sl = {'start': getIntTimeFromInput(f_input), 'end': getIntTimeFromInput(s_input), 'start_input': f_input, 'end_input': s_input, 'timeblock': $(val)};

                return;
            }


            time_blocks.push({'start': getIntTimeFromInput(f_input), 'end': getIntTimeFromInput(s_input), 'start_input': f_input, 'end_input': s_input, 'timeblock': $(val)});

        });

        if (!sl) {
            return false;
        }

        var status = true;
        for (var i = 0; i < time_blocks.length; i++) {
            if (!time_blocks[i].start || !time_blocks[i].end || !sl.start || !sl.end) {
                continue;
            }
            //(StartA <= EndB)  and  (EndA >= StartB)
            if (overlapCheck(time_blocks[i], sl)) {
                status = false;
            }

        }

        return status;
    };

    var timeBlockValue = function (edit_time_block) {
        var inputs = edit_time_block.find("input.time-field");

        var f_input = $(inputs.get(0));
        var s_input = $(inputs.get(1));


        return [f_input.val(), s_input.val()];
    };

    var timeBlockValues = function (week_block) {
        var vals = [];

        week_block.find(".edit-time-block").each(function (i, v) {
            vals.push(timeBlockValue($(v)));
        });

        return vals;
    };

    var timeBlockCheck = function (edit_time_block, input) {
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

        var functionError = function () {
            //edit_time_block.addClass("alert");
            //edit_time_block.addClass("alert-error");
            error_block.show();
        };

        var error0 = false;
        var error1 = false;

        var val0, val1;
        if (!(val0 = getIntTimeFromInput(f_input))) {
            f_input.addClass("error");
            error0 = true;
        }


        if (!(val1 = getIntTimeFromInput(s_input))) {
            s_input.addClass("error");
            error1 = true;
        }

        if (error0 || error1) {
            functionError();

            error_block.append(error_msg_template({}));

            return false;
        }


        if (val0 > val1) {
            functionError();

            error_block.append(error_msg_template_gt({}));

            return false;
        } else if (val0 == val1) {
            functionError();

            error_block.append(error_msg_template_eq({}));

            return false;
        }

        //TODO: overlap test!
        var dayblock = edit_time_block.closest(".week_times");
        if (!dayBlockTimesCheck(dayblock, edit_time_block)) {
            functionError();

            error_block.append(error_msg_template_overlap({}));

            return false;
        }


        return true;
    };


    var field_full_check = function () {
        var edit_time_block = $(".edit-time-block");

        edit_time_block.each(function (i, v) {
            timeBlockCheck($(v), null);
        });
    };

    var field_change_clbck = function () {
        var inpt = $(this);
        var edit_time_block = inpt.closest(".edit-time-block");
        timeBlockCheck(edit_time_block, inpt);
    };

    var field_change_clbck_dp = function (a, b, c) {

        var inpt = $(this).find("input.time-field");

        var edit_time_block = inpt.closest(".edit-time-block");

        timeBlockCheck(edit_time_block, inpt);
    };

    ctrls.on("blur", "input.time-field", field_change_clbck);
    ctrls.on("focusin", "input.time-field", field_change_clbck);
    ctrls.on("focusout", "input.time-field", field_change_clbck);
    ctrls.on("keyup", "input.time-field", field_change_clbck);

    ctrls.on("change.dp", ".t_ff", "change.dp", field_change_clbck_dp);
    ctrls.on("dp.change", ".t_ff", "dp.change", field_change_clbck_dp);
    ctrls.on("dp.hide", ".t_ff", "dp.change", field_change_clbck_dp);
    ctrls.on("hide.dp", ".t_ff", "dp.change", field_change_clbck_dp);
});