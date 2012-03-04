var center = [100.45, 45.678];

var fountain_search;

$(function() {
  fountain_search = window.location.search.split('=')[1];

  initialize(fountain_search);

  // Find closest fountain button
  $('#find-closest').click(function() {
    $.getJSON('/fountains/closest/'+centre.lat()+','+centre.lng(), function(data) {
      var closest = new GLatLng(data.latitude, data.longitude);  //fountain location from mysql db
      var marker = new GMarker(closest);
      map.addOverlay(marker);

      marker.openInfoWindow(document.createTextNode("Closest fountain"));
    });
  });

});


var map = null;
var geocoder = null;
var centre;

function initialize(fountain_search) {
    if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById("map_canvas"));
        geocoder = new GClientGeocoder();
        geocoder.getLatLng(fountain_search, function(point) {
            centre = point;

            //set the center of the map based on the point returned by the geocoder
            map.setCenter(point, 16);

            // Add zoom control
            var zoomControl = new GLargeMapControl();
            map.addControl(zoomControl);
            map.addControl(new GNavLabelControl());

            var marker = new GMarker(point);
            map.addOverlay(marker);
            marker.openInfoWindow(document.createTextNode("You are here!"));

            $.getJSON('/fountains', function(data) {

              $.each(data, function(index, fountain) {
                var fountain_loc = new GLatLng(fountain.latitude, fountain.longitude);
                var fountain_name = 'fountain';

                var marker = new GMarker(fountain_loc);
                map.addOverlay(marker);

                //marker.openInfoWindow(document.createTextNode(fountain_name));
              });

            });

         });
    }
}



