
// var patient_id = {{ pid|tojson }};
// firebase.auth().onAuthStateChanged((user) => {
//   if (user) {
//     var userId = firebase.auth().currentUser.uid;
//     return firebase
//       .database()
//       .ref(userId + "/Patients" + patient_id+"/test")
//       .once("value")
//       .then((snapshot) => {
//         console.log(snapshot.val());
//       });
//   }
// });
function callGraphs() {
var ctx = document.getElementById("myChart").getContext("2d");
var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "radar",

  // The data for our dataset
  data: {
    labels: [
      "Beats Per Second",
      "Resting Blood Pressure",
      "Cholestrol",
      "test"
    ],
    datasets: [
      {
        label: "Patient Values",
        pointBackgroundColor: "rgb(55, 99, 132,0.2)",
        borderColor: "rgb(255, 99, 132)",
        data: [0, 4, 5,2],
      },
      {
        label: "Average values",
        pointBackgroundColor: "rgb(0, 0, 0,0.5)",
        borderColor: "rgb(0, 0, 0)",
        data: [10, 12, 12,2],
      },
    ],
  },

  // Configuration options go here
  options: {},
});
}