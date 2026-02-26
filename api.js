async function getLocation(city) {
  let apiKey = "YOUR_API_KEY";

  let url = `https://maps.googleapis.com/maps/api/geocode/json?address=${city}&key=${apiKey}`;

  let res = await fetch(url);
  let data = await res.json();

  let loc = data.results[0].geometry.location;

  map.setCenter(loc);
  addMarker(loc.lat, loc.lng, city);

  return loc;
}
