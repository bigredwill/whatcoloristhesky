var WhatColor =  (function () {
    var imageUrls = [],
      images = [],
      CF = new ColorThief();

    var grabImagesFromUrls = function (urls) {
      var i;
      for (i = 0; i < urls.length; i += 1) {
        images.push(getImageFromUrl(urls[i].url));

      }
    };
    //Gets an Image from an url
    var getImageFromUrl = function (url) {
      return $.ajax({
        url: url,
        datatype: "image/jpg",
        crossDomain: true,
        success: function (data) {
          console.log(data);
        },
        error: function (data) {
          console.log(data);
        }
      });
    };

    $.ajax({
      url: "./assets/cams.json",
      complete: function (data) {
        imageUrls = data.responseJSON.cams;
        grabImagesFromUrls(imageUrls);
      }
    });

  }());