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


function create_post() {
     // sanity check
     console.log("inside javascript");
   $.ajax({
  url: "http://localhost:8000/notification/notificationicon_create",
  type: "POST",
  data: { id : 'menuId' },
  dataType: "text",
  success : function(msg) {
          // log the returned json to the console
          var data=JSON.parse(msg);
          notification_body(data);
            message_body(data);
            // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
});
 

}

function notification_body(notification){
  var time=(new Date() - new Date(notification[0].fields.time))/(1000);
  console.log(notification[0].fields.time);
  var days = Math.floor(time / 86400);
    time -= days * 86400;
    var hours = Math.floor(time / 3600) % 24;
        time -= hours * 3600;
        var minutes = Math.floor(time / 60) % 60;
        time -= minutes * 60;
  $("#n_no").text(Object.keys(notification).length);
  $("#n_body").append( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending notification</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
  $("#n_body").append(' <li>'+
                              '<a href="/notification/notification_view/'+notification[0].fields.receiver+'/?id='+1+'" style="white-space: wrap;Overflow:auto;">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[0].fields.title+'</span>'+
                                    '<span class="time">'+Math.floor(hours)+' Hr '+Math.floor(minutes)+' Mins ago</span>'+
                                    '</span>'+
                                    '<span class="message" style="display:block" >'+notification[0].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#n_body").append( '<li class="external">'+
                                '<a href="/notification/all_notification/">See All Tasks</a>'+
                            '</li>' );


}


function message_body(notification){
  var time=(new Date() - new Date(notification[0].fields.time))/(1000);
  var days = Math.floor(time / 86400);
    time -= days * 86400;
    var hours = Math.floor(time / 3600) % 24;
        time -= hours * 3600;
        var minutes = Math.floor(time / 60) % 60;
        time -= minutes * 60;

  console.log(time);
  $("#M_no").text(Object.keys(notification).length);
  $("#M_body").append( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending message</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
  $("#M_body").append(' <li>'+
                              '<a href="/notification/message_view/'+notification[0].fields.receiver+'" style="">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[0].fields.title+'</span>'+
                                    '<span class="time">'+Math.floor(hours)+' Hr '+Math.floor(minutes)+' Mins ago</span>'+
                                    '</span>'+
                                    '<span  class="time" style="float:left;display: inline-block;padding-right: 5px;clear:both" >'+notification[0].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#M_body").append( '<li class="external">'+
                                '<a href="#">See All Tasks</a>'+
                            '</li>' );


}