window.onload = function() {
    this.document.getElementById("download").addEventListener("click", ()=>{
        const report = this.document.getElementById("report");
        var opt = {
            filename: 'report.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2, letterRendering: true },
            jsPDF: {orientation: 'landscape'}
        }
        html2pdf().from(report).set(opt).save();

    })
}