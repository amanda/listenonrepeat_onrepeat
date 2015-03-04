// readable
(function () {
  if (location.search !== "") {
    var localURL = "localhost:5000" + location.search;
    location = localURL;
  }
})();

// bookmarklet
javascript:(function()%7B(function%20()%20%7Bif%20(location.search%20!%3D%3D%20%22%22)%20%7Bvar%20localURL%20%3D%20%22localhost%3A5000%22%20%2B%20location.search%3Blocation%20%3D%20localURL%3B%7D%7D)()%7D)()