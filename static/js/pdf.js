// this.document.getElementById("download").addEventListener("click", ()=>{
//         const report = this.document.getElementById("report");
//         name = {{ct|tojson}};
//         console.log(name);
//         var opt = {
//             filename: name,
//             image: { type: 'jpeg', quality: 0.98 },
//             html2canvas: { scale: 2, letterRendering: true },
//             jsPDF: {orientation: 'landscape'}
//         }
//         html2pdf().from(report).set(opt).outputPdf().then(function(pdf) {
//             // This logs the right base64
//             // console.log(btoa(pdf));
//             const ref = firebase.storage().ref(`image/${name}.pdf`);
//             ref.putString(btoa(pdf), 'base64');
//             // ref.put(pdf);
//         });


//         storageRef.child(`image/${name}.pdf`).getDownloadURL()
//         .then((url) => {
//             // `url` is the download URL for 'images/stars.jpg'

//             // This can be downloaded directly:
//             var xhr = new XMLHttpRequest();
//             xhr.responseType = 'blob';
//             xhr.onload = (event) => {
//             var blob = xhr.response;
//             };
//             xhr.open('GET', url);
//             xhr.send();
//         })
//         .catch((error) => {
//             // Handle any errors
//         });
// })