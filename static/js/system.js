firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // User logged in already or has just logged in.
        $('#uid').val(user.uid);
    } else {
        console.log("not logged in");
        // User not logged in or has just logged out.
    }
});


function doSomething() {
    var x = $( '#uid' ).val();
    window.location.replace("/patients/"+x);
  }