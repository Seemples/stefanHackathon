(function () {

	var $gallery = $('#gallery');

	$.getJSON('http://localhost:5000/api/test', function (data) {

		var id = 0;

		data.forEach(function (entry) {
			var city = entry.DestinationId;

			var template =
			   	'<li class="gallery-item" data-city="' + city + '">' +
			   	'<div class="gallery-block gallery-id">' + (++id) + '</div>' +
			   	'<div class="gallery-block gallery-name">' + city + '</div>' +
			   	'<div class="gallery-block gallery-wiki">' + 
				   	'<img class="gallery-image" src="static/img/beach.png">' +
				   	'<img class="gallery-image" src="static/img/mountain.png">' +
				   	'<img class="gallery-image" src="static/img/island.png">' +
			   	'</div>' +
			   	'<div class="gallery-block gallery-weather>"' + 'Weather' + '</div>';
			    
			template += '</li>';
			$gallery.append(template);
		});

		var $li = $gallery.find('li');
		$li.each(function () {
			var $img = $(this).find('img');
			$.getJSON('http://localhost:5000/api/wiki', {city: $(this).data('city')}, function (data) {
				for (var i = 0; i < 3; i++) if (data[i]) { $img.eq(i).css({display: 'block'}); }
			});
		});

	});

})($);