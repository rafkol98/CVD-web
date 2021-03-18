window.onload = function() {
    this.document.getElementById("download").addEventListener("click", ()=>{
        const report = this.document.getElementById("report");
        var opt = {
            filename: 'report.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2, letterRendering: true },
            jsPDF: {orientation: 'landscape'}
        }
        html2pdf().from(report).set(opt).outputPdf().then(function(pdf) {
            // This logs the right base64
            // console.log(btoa(pdf));
            const ref = firebase.storage().ref("image/2.pdf");
            ref.putString(btoa(pdf), 'base64');
            // ref.put(pdf);
    
        });
        

    })
}