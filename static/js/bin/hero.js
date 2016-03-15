$(document).ready(function(){
 // Defining a function to set size for #hero
    function fullscreen(){
        $('#hero').css({
            width: $(window).width(),
            height: $(window).height()
        });
    }

    fullscreen();

  // Run the function in case of window resize
  $(window).resize(function() {
       fullscreen();
    });

});
