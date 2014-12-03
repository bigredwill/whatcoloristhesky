var WhatColor =  (function () {
    var imageUrls,
      images = [],
      colors = [],
      CF = new ColorThief();

    var loadCams = function() {
      images = [];
      var grabImagesFromUrls = function (urls) {
        var i;
        for (i = 0; i < urls.length; i += 1) {
          images.push(getImageFromUrl(urls[i].url));
        }
      };
      //Gets an Image from an url
      var getImageFromUrl = function (url) {
        // var img = new Image();
        // img.src = url;
        // img.crossOrigin = "Anonymous";
        debugger;
        // var img = document.createElement('img');
        // img.src = url;
        // img.crossOrigin = "Anonymous";


        var wat = $.ajax({
         url: "proxy.php",
         data: {requrl: url}
        });
        console.log(wat);

        return img;
      };
      if(!imageUrls){
        $.ajax({
         url: "./assets/cams.json",
          complete: function (data) {
            imageUrls = data.responseJSON.cams;
            grabImagesFromUrls(imageUrls);
          }
        });
      }
      
    };

    loadCams();
    // camColorSteal();

  }());