// for the toggle function
// im bad at writing jquery
// don't copy this
// plz

$(document).ready(function() {
	$('.selector > .selection').click(function(e) {
		$(this).siblings().removeClass('selected');
		$(this).addClass('selected'); 
	});
});