firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // User logged in already or has just logged in.
        $('#user_id').val(user.uid);
        console.log(user.uid);
    } else {
        console.log("not logged in");
        // User not logged in or has just logged out.
    }
});

// function patientsUid() {
//     firebase.auth().onAuthStateChanged((user) => {
//         if (user) {
//             window.location.replace("/patients");
//         }
//     });
// }

// function showData() {
//     // var database = firebase.database();
//     firebase.auth().onAuthStateChanged((user) => {
//         if (user) {
//             var userId = user.uid;
//             return firebase.database().ref(userId).once('value').then((snapshot) => {
//                 console.log(snapshot);
//                 // document.getElementById("").innerHTML = "";
//             });
//         }
//     });

// }
