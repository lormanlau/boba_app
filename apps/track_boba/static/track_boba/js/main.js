var map;

function getCoords(map){
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			var pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};
			map.setCenter(pos);
			currentLocation = pos;
			getLocation(pos);
			}, function() {
			handleLocationError(true, map.getCenter());
		});
	} 
	else {
		// Browser doesn't support Geolocation
		handleLocationError(false, map.getCenter());
	}
}

function getLocation(pos){
	$.ajax({
		url:'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + pos['lat'] + ',' + pos['lng'] + '&key=AIzaSyD6JvfyfYbeSNIGmjjAVQ_94Aq63WYorhY',
		success:function(data){
			$('#lat').val(pos['lat']);
			$('#lng').val(pos['lng']);
			$('#city').val(data.results[3].formatted_address);
			console.log(pos['lat']);
			console.log(pos['lng']);
			console.log(data.results[3].formatted_address);
		}
	});
}



function addMarkers(location_data){
	var locations = []
	for (var things in location_data){
		locations[things] = new google.maps.Marker({
			position: {
				lat: parseFloat(location.latitude),
				lng: parseFloat(location.longitude)
			}
		})
		console.log(locations[things].position)
		locations[things].setMap(map)
	}
	console.log(locations)
}

$('form').submit(function(form_data){
	form_data.preventDefault();
	$.ajax({
		url:'/getall',
		method:'POST',
		data: $(this).serialize(),
		success: function(data) {
			data = JSON.parse(data)
			addMarkers(data.businesses)
			for (var boba in data.businesses){
				$('#boba_places').append('<tr><td><a href="">'+data.businesses[boba].name+'</a></td></tr>')
			}
		}
	});
});


var currentLocation;
function initMap(){
	var pos;
	$.ajax({
		url:'/givepos',
		success: function(data){
			pos = data
			console.log(pos);
		}
	});
	var options = {
			zoom:15,
			center: pos
		}
	console.log(options);
	map = new google.maps.Map(document.getElementById('map'), options);
	var marker = new google.maps.Marker({
		position: {
			lat: 37.3875545,
			lng: -121.8828977
		},
		map: map
	})
	console.log(marker)
	//gets users location
	getCoords(map);
}