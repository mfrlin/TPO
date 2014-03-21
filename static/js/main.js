$('input[type=text]').first().focus();

/* toggle for active until, discount, etc. */
$('.toggle').each(function() {
	var el = $(this);

	if (el.find('input').val()) {
		el.find('.inactive').css('display', 'none');
		el.trigger('activate');
	} else {
		el.find('.active').css('display', 'none');
		el.trigger('deactivate');
	}

	el.find('a').css('display', 'inline');

	el.find('.inactive a').click(function() {
		el.find('.inactive').css('display', 'none');
		el.find('.active').css('display', 'block');
		el.find('.active input[type=text]').first().focus();
		el.trigger('activate');
	});
	el.find('.active a').click(function() {
		el.find('input').val('');
		el.find('.inactive').css('display', 'block');
		el.find('.active').css('display', 'none');
		el.find('.inactive a').first().focus();
		el.trigger('deactivate');
	});
});

$('.equalHeights').each(function() {
	var currentTallest = 0;
	$(this).find('.obrobe').each(function() {
		if ($(this).height() > currentTallest) {
			currentTallest = $(this).height();
		}
	});
	$(this).find('.obrobe').css({'min-height': currentTallest});
});

function sizing() {
	var windowwidth=$(window).width();
	if (windowwidth >= 1200) {
		$('.twothree').removeClass('span6').addClass('span4');
	} else {
		$('.twothree').removeClass('span4').addClass('span6');
	}
	if (windowwidth >= 980) {
		$('.twoone').removeClass('span9').addClass('span5');
		$('.twoone-main').children().each(function (i) {
			if (i == 0) {
				$(this).removeClass('span3').addClass('span2');
			} else {
				$(this).removeClass('span9').addClass('span10');
			}
		});
	} else {
		$('.twoone').removeClass('span5').addClass('span9');
		$('.twoone-main').children().each(function (i) {
			if (i == 0) {
				$(this).removeClass('span2').addClass('span3');
			} else {
				$(this).removeClass('span10').addClass('span9');
			}
		});
	}
	$('.obrobe-title, .obrobe-extra').ellipsis();
}

$(document).ready(sizing);
$(window).resize(sizing);
$(document).bind('sizing', sizing);
