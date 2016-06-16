//GET csrf token
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

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//Event handler on episode action
$(".episode__approve").click(function(){
  var epid = $(this).parents("li").attr("id"),
      dataMerged = {"itemid":epid};
  $(this).addClass("episode__checked");

  $.ajax({
    type: 'POST',
    url: "/requestmedia/approve",
    data: dataMerged,
    dataType: "text",
    success: function() {
      $("#"+epid).fadeOut(800, function(){ $(this).remove();});
      var snackbarContainer = document.querySelector('#snackbar-success'),
          data = {
        message: 'Success!',
        timeout: 1000,
      };
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    },
    error: function(ts) {
      var snackbarContainer = document.querySelector('#snackbar-error'),
          data = {
        message: 'Could not remove entry '+epid,
        timeout: 3000,
      };
      console.log(ts.responseText);
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
  });
});
