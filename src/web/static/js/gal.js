(function () {

	$gallery = $('#gallery');

	$.getJSON('http://localhost:5000/api/test', function (data) {

		data.forEach(function (entry) {

		    $template =
		    	'<li><strong>' + 
		    	entry.DestinationId +
		    	':</strong> ' +
		    	entry.Price +
		    	'</li>';

		    $gallery.append($template);

		});

	});

})($);