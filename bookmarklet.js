// readable
(function () {
  if (location.search !== "") {
    var localURL = "http://localhost:5000/watch" + location.search;
    location = localURL;
  }
})();

// bookmarklet
javascript:(function()%7B(function%20()%20%7Bvar%20localURL%20%3D%20%22http%3A%2F%2Flocalhost%3A5000%2Fwatch%22%20%2B%20location.search%3Blocation%20%3D%20localURL%3B%7D)()%7D)()