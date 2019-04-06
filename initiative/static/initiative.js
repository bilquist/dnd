window.Dnd = {};

window.Dnd.initialize = function() {
	$('input[name="name"]').on('keypress', function() {
		$('.has-error').hide();
	});
};

window.Dnd.initialize_focus = function() {
	$('input[name="name"]').on('focus', function() {
		$('.has-error').hide();
	});
};
