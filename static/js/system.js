//Prevent resubmissions on refresh or back button.
if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

// Get patients from the server and populate "patients" table.
function getPatients() {
  $("#items_table").empty();
      const url = `/getPatients`
      fetch(url)
        .then(response => response.json())
        .then(patients => {
    
          if (patients !== null) {
            
            items_table = document.getElementById("items_table");
           
            for (var key in patients) {
              
              var condition = patients[key].latest
              var badge;

              // Change the badge colour and text depending on patient's condition.
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

              var gender = (patients[key].gender === "0") ? "Male" : (patients[key].gender === "1") ? "Female" : "";

              // Populate table.
              items_table.innerHTML +=
                `<tr><td> <a href="/edit?pid=${key}"><i class='fas fa-edit'></i></a>` +
                "</td>"+"<td>" +
                key +
                `</td> <td>${patients[key].age}</td> <td>${gender}</td>  <td><a href="/history?pid=${key}");"><i class="fas fa-file-medical-alt"></i> History</a></td> <td><h5><span class="badge badge-${badge}">${condition}</span></h5></td> <td><a href="/diagnose?pid=${key}" class="btn btn-function"><i class="fas fa-heartbeat"></i> Diagnose</a></td> </tr>`;
            }
          }
        });
  //   }
  // });
}

// Get history of patient.
function getHistory(pid) {
  const url = `/patients/history?pid=${pid}`
  fetch(url)
    .then(response => response.json())
    .then(history => {

      if (history !== null) {
        console.log(history);
        items_table = document.getElementById("history_items_table");

        // Loop through every child of history.
        for (var key in history) {

          var condition = history[key].cardio;
          var pdf_url = history[key].pdf;
  
          var badge;

           // Change the badge colour and text depending on patient's condition.
          if (condition == 1) {
            condition = "Cardio";
            badge = "danger";
          } else {
            condition = "Healthy";
            badge = "success";
          }

          // Populate history table.
          var date = new Date(key * 1000).toISOString().slice(0, 19).replace('T', ' ');
          items_table.innerHTML +=
                `<tr><td> ${date}` +
                "</td>"+"<td>" +
                `<h5><span class="badge badge-${badge}">${condition}</span></h5>` +
                `</td> <td><a href="javascript:infoSpecificHistory('${pid}','${key}');"><i class="fas fa-eye"></i> View</a></td>  <td><a href="${pdf_url}" target="_blank"><i class="fas fa-download"></i> PDF</a></td> </tr>`;
        }

      } 
      // If the patient doesn't have any medical history show an alert.
      else {
        alert("This patient does not have any medical history yet.")
      }

    });
}

// Get specific history for info.
function infoSpecificHistory(pid,key) {
  // Fetch data from the server.
  const url = `/patients/history/specific?pid=${pid}&key=${key}`
  fetch(url)
    .then(response => response.json())
    .then(history => {
      console.log(history);
      // Show history specific modal.
      $("#specificModal").modal('show');
      
      hist_spec = document.getElementById("hist_spec");
      hist_spec.innerHTML = '';
      
      // Populate the history specific modal with the specific history data.
      hist_spec.innerHTML +=  `<div class="text-center"><h5>Bps:${history.bps}</h5><br><h5>Chest: ${history.chest}</h5><br><h5>Cholestrol: ${history.chol}</h5><br><h5>Electro Cardiogram: ${history.ecg}</h5><br><h5>Exang: ${history.exang}</h5><br><h5>Fasting Blood Sugar: ${history.fbs}</h5><br><h5>Max Heart Rate Achieved: ${history.maxheart}</h5><br><h5>Oldpeak: ${history.oldpeak}</h5><br><h5>St Slope: ${history.stslope}</h5><br> <div class="bg-outcome"><h6 class="text-left">${history.comments}</h6></div> </div>`    
    });
  }
  