var WhatColor = (function () {



  var getColor = function () {
    $.ajax({
      url: "./assets/cams.json",
      complete: function (data) {
        imageUrls = data.responseJSON.cams;
        grabImagesFromUrls(imageUrls);
      }
    });
  }
}());