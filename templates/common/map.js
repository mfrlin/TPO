{% load l10n %}

(function(){
	if (canvas.length) {
		function initialize() {
			var pos = new google.maps.LatLng({% localize off %}{{ lat }}, {{ lng }}{% endlocalize %});
			var mapOptions = {
				center: pos,
				zoom: 15,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};
			var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
			marker = new google.maps.Marker({
				map: map,
				draggable: false,
				animation: google.maps.Animation.DROP,
				position: pos
			});
		}
		google.maps.event.addDomListener(window, 'load', initialize);
	}
})();
