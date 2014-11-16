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