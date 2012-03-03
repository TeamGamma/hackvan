$(function() {
  var geolocation_enabled = true;

  if(typeof window.navigator.geolocation == 'undefined') {
    geolocation_enabled = false;
  }

  // Geolocation button
  $('#geolocation').click(function() {
    if(!geolocation_enabled) {
      alert("Sorry, your browser doesn't support geolocation...");
      return false;
    }

    window.navigator.geolocation.getCurrentPosition(function(position) {
      if(typeof position.coords.latitude == 'number' && typeof position.coords.longitude == 'number') {
        var url = '/map?query=' + position.coords.latitude + ',' + position.coords.longitude;
        window.location = url;
      }
    });

    return false;
  });

});
