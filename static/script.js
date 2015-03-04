function sendYoutube(evt) {
  var f = document.getElementById("user_text");
  var params = "v=" + f.value
  var req = new XMLHttpRequest();
  req.open("POST", "/watch", true);
  req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  req.send(params);
  evt.preventDefault();
  req.onreadystatechange = function () {
    if (req.readyState === 4 && req.status === 200) {
      var data = JSON.parse(req.responseText);
      document.getElementById("title").innerText = "shuffled~";
      document.getElementById("content").innerText = data.shuffled;
    }
  };
}

var b = document.getElementsByTagName("button")[0];
b.addEventListener("click", sendYoutube);
