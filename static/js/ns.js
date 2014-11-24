$(document).ready(function () {
  $('html').click(function() {
//Hide the menus if visible
    $("#notificationMenu").removeClass("open");
  });

  $("#notificationicon").click(function(event){
    event.stopPropagation();
    $("#notificationMenu").toggleClass("open");
    $("li").removeClass("open");


});
  $("#notificationMenu").click(function(event){
    event.stopPropagation();
    $("li").removeClass("open");

});
});

function notification(){


  function create_post() {
     // sanity check
    $.ajax({
        url : "notification/notificationicon_create", // the endpoint
        type : "POST", // http method
        dataType:"Text"
        data : { the_post : 'aman' }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
}