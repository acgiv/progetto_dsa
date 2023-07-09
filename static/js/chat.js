function send_message_text() {
  $.ajax({
    url: '/send_message',
    type: 'POST',
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

    }
  });
}