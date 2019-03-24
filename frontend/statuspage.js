function status(message) {
  // Navigate to the status page, append a pseudo-random number to
  // trick Twitter into letting us post the same status message
  // repeatedly. The feed filter will edit out the added number.
  var d = new Date();
  var ms = d.getMilliseconds();
  //var urlvar = "https://mobile.twitter.com/?status="+encodeURI(message+" {"+ms+"}");
  //var urlvar = "https://twitter.com/home?status="+encodeURI(message+" {"+ms+"}");
  // var urlvar = "https://twitter.com/share?url=&text="+encodeURI(message+" {"+ms+"}");
  var urlvar = "https://twitter.com/intent/tweet?text="+encodeURI(message+" {"+ms+"}");
  window.location.assign(urlvar);
  // Refs:
  // http://stackoverflow.com/questions/743129/mobile-detection-using-javascript
  // http://stackoverflow.com/questions/1691781/i-need-to-build-my-url-in-a-javascript-function-then-return-the-string-back-to-hr
  // http://www.w3schools.com/jsref/met_loc_assign.asp
}
