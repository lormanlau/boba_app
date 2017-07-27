$('form').submit(function(form_data){
	form_data.preventDefault();
	$.ajax({
		url:'/getall',
		method: "POST",
		data: $(this).serialize(),
		success: function(data) {
			data = JSON.parse(data)
			for ( var boba in data.businesses){
				$('#boba_places').append('<tr><td>'+data.businesses[boba].name+'</td></tr>')
			}
		}
	});
	
});

function getLocation(pos){
	$.ajax({
		url:'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + pos['lat'] + ',' + pos['lng'] + '&key=AIzaSyD6JvfyfYbeSNIGmjjAVQ_94Aq63WYorhY',
		success:function(data){
			$('#city').val(data.results[3].formatted_address)
			console.log(data.results[3].formatted_address);
		}
	});
}

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
	getCoords(map);
}