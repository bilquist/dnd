var initialize = function() {
	$('input[name="name"]').on('keypress', function() {
		$('.has-error').hide();
	});
};