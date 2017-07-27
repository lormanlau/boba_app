$.ajax({
	url:'/getall.json',
	success: function(hello) {
		console.log(hello);
	}
});
var currentLocation;
	function initMap(){
		var options = {
				zoom:15,
				center:{
					lat:37.7749,
					lng:-122.4194
				}
			}
		var map = new google.maps.Map(document.getElementById('map'), options);

		var marker = new google.maps.Marker({
			position: {
				lat: 37.3875545,
				lng: -121.8828977
			},
			map: map
		})
		
		//gets users location
		if (navigator.geolocation) {
        	navigator.geolocation.getCurrentPosition(function(position) {
	            var pos = {
	              	lat: position.coords.latitude,
	              	lng: position.coords.longitude
	            };
            	map.setCenter(pos);
            	currentLocation = pos;
          	}, function() {
            	handleLocationError(true, map.getCenter());
          	});
        } else {
          	// Browser doesn't support Geolocation
          	handleLocationError(false, map.getCenter());
        }

	}
	$('form').submit(function(){
		$('#lat').val(currentLocation['lat']);
		$('#lng').val(currentLocation['lng']);
		console.log($(this).serialize());
		$.ajax({
			url:'/addplace',
			method:'post',
			data: $(this).serialize()
			});
	});