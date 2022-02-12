
(function($){
    /*  VIDEO PLAY BUTTON */
    $('#video-btn').click(function(){
        $(this).toggleClass('video-play-btn');
    });
    /* video */
    var vid = document.getElementById("bgvid");
    var pauseButton = document.querySelector("#polina button");

    vid.addEventListener('ended', function()
    {
    // only functional if "loop" is removed
    vid.pause();
    // to capture IE10
    vidFade();
    });

    pauseButton.addEventListener("click", function() {

      if (vid.paused) {
        vid.play();
        pauseButton.innerHTML = "&nbsp;";
      } else {
        vid.pause();
        pauseButton.innerHTML = "&nbsp;";
      }
    });
})(jQuery);
