const hideElement = (elementId) => {
    document.getElementById(elementId).style.display = "none";
}

const generateReport = () => {
    let reportDate = document.getElementById("report-date").value;
    if(!reportDate) return;
    console.log(reportDate);
    
    fetch('http://127.0.0.1:8000/stats/report/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"report_date": reportDate})
    })
    .then((response) => response.blob())
    .then(data => {
        let reportDownload = document.createElement("a");
        reportDownload.href = window.URL.createObjectURL(data);
        reportDownload.download = `report-${reportDate}.txt`;
        reportDownload.click();
    })
}