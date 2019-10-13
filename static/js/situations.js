var situations, words;

function sampleRemove(arr, n) {
  var out = [];
  while (out.length < n && arr.length > 0) {
    var i = Math.floor(Math.random() * arr.length);
    out.push(arr[i]);
    arr.splice(i, 1);
  }
  return out;
}

function draw() {
  if ((typeof situations !== 'undefined') && (typeof words !== 'undefined')) {
    $("#situation").html(sampleRemove(situations, 1));
    $("#situation-bank").html(situations.join("<br/><br/>"));
    $("#words").html(sampleRemove(words, 3).join(', '));
    $("#word-bank").html(words.join(", "));
  }
}

function setSituations() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      situations = this.responseText.split("\n\n").map(s => s.replace(/\s+/, " "));
      draw();
    }
  };
  xhttp.open("GET", "/static/text/situations.txt", true);
  xhttp.send();
}

function setWords() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      words = this.responseText.split("\n");
      draw();
    }
  };
  xhttp.open("GET", "/static/text/situation_words.txt", true);
  xhttp.send();
}

$(document).ready(function() {
  setSituations();
  setWords();
});