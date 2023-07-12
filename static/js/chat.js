let id_message_click ;

function send_message_text() {
  $.ajax({
    url: '/send_message',
    type: 'POST',
    data:{
      "chat_textarea":document.getElementById("chat_textarea").value,
      "id_chat": id_message_click
    },
    success: function(data) {
      $("#chat").append($(data));
      const text = document.getElementById("chat_textarea").value;
      document.getElementById("chat_textarea").value="";
      response_message(text)
    }
  });
}

function response_message(text) {
  $.ajax({
    url: '/respost_message',
    type: 'POST',
    data: {
      "chat_textarea":text,
      "id_chat": id_message_click
    },
    success: function(data) {
      $("#chat").append($(data));
    }
  });
}


function create_new_chat() {
  $.ajax({
    url: '/create_new_chat',
    type: 'POST',
    success: function(data) {
      $("#new_chat").append($(data));
      document.getElementById("send_text").disabled = true;
    }
  });
}

function view_chat_message(element) {
  id_message_click =element.id;
  $.ajax({
    url: '/view_chat_message',
    type: 'POST',
    data: {
      "id_chat":id_message_click,
    },
    success: function(data) {
      $("#chat").html($(data));
      document.getElementById("send_text").disabled = false;
    }
  });
}

function reformulate_message(id_message){
  $.ajax({
      url: '/reformulate_message',
      type: 'POST',
      data: {
      "id_chat":id_message_click,
       "id_message":id_message
    },success: function (data){
      const paragrafo = document.getElementById(id_message);
      paragrafo.textContent= data;
    }
  });
}

function send_message_text_pepper(id_message){
  $.ajax({
      url: '/send_message_text_pepper',
      type: 'POST',
      data: {
      "id_chat":id_message_click,
       "id_message":id_message
    },success: function (data){
      console.log("cliccato");
    }
  });
}

