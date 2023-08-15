$(document).ready(function () {
  // Handle like button click
  $('.like-comment').click(function () {
    var comment_id = $(this).data('comment-id');
    $.ajax({
      url: '/comments/' + comment_id + '/like/',
      method: 'POST',
      data: {
        'csrfmiddlewaretoken': '{{ csrf_token }}'
      },
      success: function (response) {
        $('.comment-likes[data-comment-id=' + comment_id + ']').text(response.likes);
      },
      error: function (xhr, status, error) {
        console.log(xhr.responseText);
      }
    });
  });

  // Handle dislike button click
  $('.dislike-comment').click(function () {
    var comment_id = $(this).data('comment-id');
    $.ajax({
      url: '/comments/' + comment_id + '/dislike/',
      method: 'POST',
      data: {
        'csrfmiddlewaretoken': '{{ csrf_token }}'
      },
      success: function (response) {
        $('.comment-dislikes[data-comment-id=' + comment_id + ']').text(response.dislikes);
      },
      error: function (xhr, status, error) {
        console.log(xhr.responseText);
      }
    });
  });
});