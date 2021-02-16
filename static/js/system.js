//Prevent resubmissions on refresh or back button.
if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    // User logged in already or has just logged in.
    $("#user_id").val(user.uid);
    console.log(user.uid);
  } else {
    console.log("not logged in");
    // User not logged in or has just logged out.
  }
});

function loggedIn() {
  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      window.location.replace("/patients");
    }
  });
}

function logout() {
  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      firebase.auth().signOut().then(() => {
        window.location.replace("/");
      }).catch((error) => {
        console.log("Error" + error);
      });
    }
  });
}

function showData() {
  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      var userId = firebase.auth().currentUser.uid;
      return firebase
        .database()
        .ref(userId + "/Patients")
        .once("value")
        .then((snapshot) => {
          console.log(snapshot.val());
          items_table = document.getElementById("items_table");
          snapshot.forEach(function (child) {
            // items_table.innerHTML += '<tr>'

            items_table.innerHTML +=
              "<tr><td>" +
              child.key +
              "</td><td>" +
              child.val().name +
              `</td> <td><a href="javascript:getInfo('${userId}','${child.key}');"><i class="fas fa-info-circle"></i> Info</a></td>  <td><a href="./diagnose.html"><i class="fas fa-file-medical-alt"></i> History</a></td> <td><h5><span class="badge badge-danger">Cardio Disease</span></h5></td> <td><a href="/diagnose/?pid=${child.key}" class="btn btn-function"><i class="fas fa-heartbeat"></i> Diagnose</a></td> </tr>`;

          });
        });
    }
  });
}

function getInfo(userId,pid) {
  const url = `/patients/hello?uid=${userId}&pid=${pid}`
  fetch(url)
    .then(response => response.json())
    .then(json => {
      $("#infoModal").modal('show');
      document.getElementById("info-age").innerHTML = JSON.stringify(json.age)
      document.getElementById("info-gender").innerHTML = JSON.stringify(json.gender)
      document.getElementById("info-email").innerHTML = JSON.stringify(json.email)
      console.log(json);
    })
}