
function addComment(e){
    /* stop form from submitting normally */
      event.preventDefault();
        var post_id = $(this).attr('id');
        var user_id = $(this).next('#comment-user').val();
        var text = $(this).prev('#text').val()
        var text_field = $(this).prev('#text');
    /* Send the data using post with element id name and name2*/
      $.post( "/grumblr/add-comment/"+post_id,
          {user_id: user_id, post_id: post_id, text: text}
        ).done(function( data ) {


          var new_comment = $(data.html);
          var comment = $("#comment-area-"+post_id).append(new_comment);
          text_field.val("");
      })
      .error(function() { alert("You must write something to comment."); });


}


$(document).ready(function () {


  $(".comment-submit").click(addComment);


  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
