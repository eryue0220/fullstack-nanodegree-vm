function signOut() {
  var $signOut = $('.js-user-signout');
  if ($signOut.length) {
    $signOut.on('click', function() {
      $.ajax({
        type: 'POST',
        url: "/gdisconnect",
        proccess: false,
        success: function(result) {
          console.log(result);
          window.location.href = '/';
        }
      })
    })
  }
}

signOut();
