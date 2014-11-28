function createpost() {
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
 
  $("#n_no").text(Object.keys(notification).length);
  $("#n_body").append( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending notification</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
   var time=(new Date() - new Date(notification[i].fields.time))/(1000);
   var days = Math.floor(time / 86400);
    time -= days * 86400;
    var hours = Math.floor(time / 3600) % 24;
    time -= hours * 3600;
    var minutes = Math.floor(time / 60) % 60;
    time -= minutes * 60;
  $("#n_body").append(' <li>'+

                              '<a href="/notification/notification_view/'+notification[i].pk+'/?next='+document.URL+'" style="white-space: wrap;Overflow:auto;">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[i].fields.title+'</span>'+
                                    '<span class="time">'+Math.floor(hours)+' Hr '+Math.floor(minutes)+' Mins ago</span>'+
                                    '</span>'+
                                    '<span class="message" style="display:block" >'+notification[i].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#n_body").append( '<li class="external">'+
                                '<a href="/notification/all_notification/">See All Tasks</a>'+
                            '</li>' );


}


function message_body(notification){
  

  console.log(time);
  $("#M_no").text(Object.keys(notification).length);
  $("#M_body").append( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending message</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
  var time=(new Date() - new Date(notification[i].fields.time))/(1000);
  var days = Math.floor(time / 86400);
    time -= days * 86400;
    var hours = Math.floor(time / 3600) % 24;
        time -= hours * 3600;
        var minutes = Math.floor(time / 60) % 60;
        time -= minutes * 60;
  $("#M_body").append(' <li>'+
                              '<a href="/notification/message_view/'+notification[i].fields.receiver+'" style="">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[i].fields.title+'</span>'+
                                    '<span class="time">'+Math.floor(hours)+' Hr '+Math.floor(minutes)+' Mins ago</span>'+
                                    '</span>'+
                                    '<span  class="time" style="float:left;display: inline-block;padding-right: 5px;clear:both" >'+notification[i].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#M_body").append( '<li class="external">'+
                                '<a href="#">See All Tasks</a>'+
                            '</li>' );


}



function addquestion( id){
  console.log(id);
  $.ajax({
  url: "http://localhost:8000/quiz/addquestion",
  type: "GET",
  data: { id : id },
  dataType: "text",
  success : function(msg) {
          // log the returned json to the console
          console.log(msg);
          msg=JSON.parse(msg);
          quiz_id=JSON.parse(msg.quiz_id);
          console.log(quiz_id);
          data=JSON.parse(msg.ques);
          console.log(data[0].fields.quizes.length);
          addremoveButton(quiz_id,data,id);

            // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log("fail"); // provide a bit more info about the error to the console
        }
});


}

function viewfullquestion(id){
   $.ajax({
    url: "http://localhost:8000/quiz/view_fullquestion",
    type: "GET",
    data: { id : id },
    dataType: "text",
    success : function(msg) {
            // log the returned json to the console
              msg=JSON.parse(msg)
            
            console.log(msg);
            questionbody(msg);
            
              // another sanity check
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log("fail"); // provide a bit more info about the error to the console
          }
  });
}

function questionbody(msg){


 $("#q_body").html('<p> <h3>1.'+msg[0].fields.statement+'</h3></p>'+
          '<ul>'+
          '<li id="1" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.a+'</li>'+
         '<li id="2" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.b+'</li>'+
          '<li id="3" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.c+'</li>'+
          '<li id="4" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.d+'</li>'+
          '</ul>'+
          '<p>Comment:'+msg[0].fields.extra_info+'</p>');

  if(msg[0].fields.ans=="a"){
       $("#1").toggleClass('fa-circle fa-check');
      }

    else if(msg[0].fields.ans=="b"){
       $("#2").toggleClass('fa-circle fa-check');
      }
      else if(msg[0].fields.ans=="c"){
       $("#3").toggleClass('fa-circle fa-check');
      }
  
   else{
       $("#4").toggleClass('fa-circle fa-check');
      }



}

function addremoveButton(quiz_id,data,id){
  var flag=false;
  var no_quiz=data[0].fields.quizes.length;
  var rating="#R_"+id;
  var add_id="#add"+id;
  var rm_id="#rm"+id;
  var ic_id="#i"+id;
  for(var i=0;i<no_quiz;i++){
  if(quiz_id==data[0].fields.quizes[i])
    flag=true;
  }

  if(flag){
      console.log(flag);
      $(rating).html(no_quiz);
      $(add_id).hide();
      $(rm_id).show();
      $(ic_id).toggleClass('fa-hand-o-right fa-check');
      $(ic_id).css("color","green");
    }
    else{
      console.log(flag);
      $(rating).html(no_quiz);
      $(add_id).show();
      $(rm_id).hide();
      $(ic_id).toggleClass('fa-check fa-hand-o-right');
      $(ic_id).css("color","");
    }
}



function removeQuestion(id){
  $.ajax({
    url: "http://localhost:8000/quiz/removeQuestion",
    type: "GET",
    data: { id : id },
    dataType: "text",
    success : function(msg) {
          // log the returned json to the console
          console.log(msg);
          msg=JSON.parse(msg);
          quiz_id=JSON.parse(msg.quiz_id);
          data=JSON.parse(msg.ques);
          console.log(data[0].fields.quizes.length);
          addremoveButton(quiz_id,data,id);

            // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log("fail"); // provide a bit more info about the error to the console
        }
});
}

function qizquestions(){
  console.log("inside all quiz");

  $.ajax({
    url: "http://localhost:8000/quiz/qizquestions",
    type: "GET",
    data: {},
    dataType: "text",
    success : function(msg) {
          // log the returned json to the console
          console.log(msg);
          msg=JSON.parse(msg);
          console.log(msg[0].pk);
          console.log("success");
          showbutton(msg);

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log("fail"); // provide a bit more info about the error to the console
        }
});

}

function showbutton(msg){
  for(var i=0;i<msg.length;i++){
    var add_id="#add"+msg[i].pk;
    var rm_id="#rm"+msg[i].pk;
    var ic_id="#i"+msg[i].pk;
      $(add_id).hide();
      $(rm_id).show();
      $(ic_id).toggleClass('fa-hand-o-right fa-check');
      $(ic_id).css("color","green");
  }

}