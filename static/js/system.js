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
              
              var condition = patients[key].latest
              var badge;
  
              if(condition!== undefined) {
                if (condition == 1) {
                  condition = "Cardio";
                  badge = "danger";
                } else {
                  condition = "Healthy";
                  badge = "success";
                }
              } else {
                condition = "Not Diagnosed";
                badge = "dark";
              }
              
  
              items_table.innerHTML +=
                `<tr><td> <a href="/edit/?uid=${userId}&pid=${key}"><i class='fas fa-edit'></i></a>` +
                "</td>"+"<td>" +
                patients[key].name + " " + patients[key].lastName +
                `</td> <td><a href="javascript:info('${userId}','${key}');"><i class="fas fa-info-circle"></i> Info</a></td>  <td><a href="/history?uid=${userId}&pid=${key}");"><i class="fas fa-file-medical-alt"></i> History</a></td> <td><h5><span class="badge badge-${badge}">${condition}</span></h5></td> <td><a href="/diagnose/?pid=${key}" class="btn btn-function"><i class="fas fa-heartbeat"></i> Diagnose</a></td> </tr>`;
                // `</td> <td><a href="javascript:info('${userId}','${key}');"><i class="fas fa-info-circle"></i> Info</a></td>  <td><a href="javascript:getHistory('${userId}','${key}');"><i class="fas fa-file-medical-alt"></i> History</a></td> <td><h5><span class="badge badge-${badge}">${condition}</span></h5></td> <td><a href="/diagnose/?pid=${key}" class="btn btn-function"><i class="fas fa-heartbeat"></i> Diagnose</a></td> </tr>`;
            }
    
          }
    
        });

    }
  });
}

function info(userId, pid) {
  const url = `/patients/info?uid=${userId}&pid=${pid}`
  fetch(url)
    .then(response => response.json())
    .then(json => {
        $("#infoModal").modal('show');
        $("#info-age").html(json.age);
        $("#info-gender").html(json.gender);
        $("#info-email").html(json.email);
    });
}

// function getHistory(userId, pid) {
//   const url = `/patients/history?uid=${userId}&pid=${pid}`
//   fetch(url)
//     .then(response => response.json())
//     .then(history => {

//       if (history !== null) {
//         $("#historyModal").modal('show');
//         console.log(history);

//         for (var key in history) {
//           var date = new Date(key * 1000).toISOString().slice(0, 19).replace('T', ' ');
//           console.log(key + " " + history[key].bps);
//           document.getElementById("history-accord").innerHTML += `<div class="card"><div class="card-header" id="headingOne"><h2 class="mb-0"> <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapse${key}" aria-expanded="true" aria-controls="collapse${key}"> ${date} </button> </h2> </div> <div id="collapse${key}" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionExample"> <div class="card-body"> <h6>Bps:${history[key].bps}</h6><br><h6>Chest: ${history[key].chest}</h6><br><h6>Cholestrol: ${history[key].chol}</h6><br><h6>Electro Cardiogram: ${history[key].ecg}</h6><br><h6>Exang: ${history[key].exang}</h6><br><h6>Fasting Blood Sugar: ${history[key].fbs}</h6><br><h6>Max Heart Rate Achieved: ${history[key].maxheart}</h6><br><h6>Oldpeak: ${history[key].oldpeak}</h6><br><h6>St Slope: ${history[key].stslope}</h6><br><h4 class="text-center">Cardio: ${history[key].cardio}</h4>  </div></div></div>`
//         }

//       } else {
//         alert("This patient does not have any medical history yet.")
//       }

//     });
// }

function getHistory(userId, pid) {
  const url = `/patients/history?uid=${userId}&pid=${pid}`
  fetch(url)
    .then(response => response.json())
    .then(history => {

      if (history !== null) {
        // $("#historyModal").modal('show');
        console.log(history);
        items_table = document.getElementById("history_items_table");

        for (var key in history) {

          var condition = history[key].cardio;
          var badge;

          if (condition == 1) {
            condition = "Cardio";
            badge = "danger";
          } else {
            condition = "Healthy";
            badge = "success";
          }

          var date = new Date(key * 1000).toISOString().slice(0, 19).replace('T', ' ');
          items_table.innerHTML +=
                `<tr><td> ${date}` +
                "</td>"+"<td>" +
                `<h5><span class="badge badge-${badge}">${condition}</span></h5>` +
                `</td> <td><a href="javascript:infoSpecificHistory('${userId}','${pid}','${key}');"><i class="fas fa-eye"></i> View</a></td>  <td><a href=""><i class="fas fa-download"></i> PDF</a></td> </tr>`;
        }

      } else {
        alert("This patient does not have any medical history yet.")
      }

    });
}

function infoSpecificHistory(userId,pid,key) {
  console.log(userId+"  "+pid+"  "+key);
  const url = `/patients/history/specific?uid=${userId}&pid=${pid}&key=${key}`
  fetch(url)
    .then(response => response.json())
    .then(history => {
      console.log(history);
      $("#specificModal").modal('show');
      
      hist_spec = document.getElementById("hist_spec");
      hist_spec.innerHTML = '';
    
      hist_spec.innerHTML +=  `<div class="text-center"><h5>Bps:${history.bps}</h5><br><h5>Chest: ${history.chest}</h5><br><h5>Cholestrol: ${history.chol}</h5><br><h5>Electro Cardiogram: ${history.ecg}</h5><br><h5>Exang: ${history.exang}</h5><br><h5>Fasting Blood Sugar: ${history.fbs}</h5><br><h5>Max Heart Rate Achieved: ${history.maxheart}</h5><br><h5>Oldpeak: ${history.oldpeak}</h5><br><h5>St Slope: ${history.stslope}</h5><br> <div class="bg-outcome"><h4 class="text-center">Cardio: ${history.cardio}</h4></div> </div>`    
    });
  }