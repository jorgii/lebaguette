$(".episode__check").click(function(){
  var imdbid = $(this).parents("li").attr("id");
  $(this).addClass("episode__checked");
  $.ajax({
    type: 'POST',
    url: "/requestmedia/episodes/complete",
    data: imdbid,
    dataType: "text",
    success: function() {
      $(this).parents("li").fadeOut(800, function(){ $(this).remove();});
      var snackbarContainer = document.querySelector('#snackbar-success');
      var data = {
        message: 'Success!',
        timeout: 3000,
      };
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    },
    error: function() {
      var snackbarContainer = document.querySelector('#snackbar-error');
      var data = {
        message: 'Could not remove entry '+imdbid,
        timeout: 3000,
      };
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
  });
});
