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

function getPatients() {
  $("#items_table").empty();
  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      var userId = firebase.auth().currentUser.uid;
      const url = `/getPatients?uid=${userId}`
      fetch(url)
        .then(response => response.json())
        .then(patients => {
    
          if (patients !== null) {
            
            items_table = document.getElementById("items_table");
           
            for (var key in patients) {
              
              var condition = patients[key].latest;
              var badge;
  
              if (condition == 1) {
                condition = "Cardio Disease";
                badge = "danger";
              } else {
                condition = "Healthy";
                badge = "success";
              }
  
              items_table.innerHTML +=
                `<tr><td> <a href="javascript:editOrInfo('${userId}','${key}',true);"><i class='fas fa-edit'></i></a>` +
                
                "</td>"+"<td>" +
                key +
                "</td>"+"<td>" +
                patients[key].name +
                `</td> <td><a href="javascript:editOrInfo('${userId}','${key}',false);"><i class="fas fa-info-circle"></i> Info</a></td>  <td><a href="javascript:getHistory('${userId}','${key}');"><i class="fas fa-file-medical-alt"></i> History</a></td> <td><h5><span class="badge badge-${badge}">${condition}</span></h5></td> <td><a href="/diagnose/?pid=${key}" class="btn btn-function"><i class="fas fa-heartbeat"></i> Diagnose</a></td> </tr>`;
            }
    
          }
    
        });

    }
  });
}

function editOrInfo(userId, pid, edit) {
  const url = `/patients/info?uid=${userId}&pid=${pid}`
  fetch(url)
    .then(response => response.json())
    .then(json => {
      if(edit) {
        //Show current data of user.
        $("#editPatientModal").modal('show');
        $("#name_edit").val(json.name);
        $("#email_edit").val(json.email);
        $("#age_edit").val(json.age);
        $("#gender_edit").val(json.gender);
        // TODO : FIX THIS! DOESNT GET VALUE.
        $("#uid").val(pid);
        $("#patient_id").val(pid);
        console.log(userId);   
      } 
      else {
        $("#infoModal").modal('show');
        $("#info-age").html(json.age);
        $("#info-gender").html(json.gender);
        $("#info-email").html(json.email);
      }
     

      
    });
}

function getHistory(userId, pid) {
  const url = `/patients/history?uid=${userId}&pid=${pid}`
  fetch(url)
    .then(response => response.json())
    .then(history => {

      if (history !== null) {
        $("#historyModal").modal('show');
        console.log(history);

        for (var key in history) {
          var date = new Date(key * 1000).toISOString().slice(0, 19).replace('T', ' ');
          console.log(key + " " + history[key].bps);
          document.getElementById("history-accord").innerHTML += `<div class="card"><div class="card-header" id="headingOne"><h2 class="mb-0"> <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapse${key}" aria-expanded="true" aria-controls="collapse${key}"> ${date} </button> </h2> </div> <div id="collapse${key}" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionExample"> <div class="card-body"> <h6>Bps:${history[key].bps}</h6><br><h6>Chest: ${history[key].chest}</h6><br><h6>Cholestrol: ${history[key].chol}</h6><br><h6>Electro Cardiogram: ${history[key].ecg}</h6><br><h6>Exang: ${history[key].exang}</h6><br><h6>Fasting Blood Sugar: ${history[key].fbs}</h6><br><h6>Max Heart Rate Achieved: ${history[key].maxheart}</h6><br><h6>Oldpeak: ${history[key].oldpeak}</h6><br><h6>St Slope: ${history[key].stslope}</h6>  </div></div></div>`
        }

      } else {
        alert("This patient does not have any medical history yet.")
      }

    });
}