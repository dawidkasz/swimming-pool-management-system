const labels = ["January", "February", "March", "April", "May", "June", "July", 
                "August", "September", "October", "November", "December"];

const primaryBackroundColor = 'rgba(255, 10, 10, 0.3)';
const primaryBorderColor = 'rgba(255, 10, 10, 0.8)';

const secondaryBackroundColor = 'rgba(20, 134, 255, 0.3)';
const secondaryBorderColor = 'rgba(20, 134, 255, 0.8)';

const apiUrl = "http://127.0.0.1:8000/stats";


var incomeChart = new Chart(document.getElementById('income-chart'), {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Private clients',
            data: [],
            backgroundColor: primaryBackroundColor,
            borderColor: primaryBorderColor,
            borderWidth: 1
        },
        {
            label: 'Swim schools',
            data: [],
            backgroundColor: secondaryBackroundColor,
            borderColor: secondaryBorderColor,
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Monthly income',
                padding: {
                    bottom: 5
                }
            }
        }  
    }
});


var reservationsChart = new Chart(document.getElementById('reservations-chart'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Paid reservations',
            data: [],
            backgroundColor: primaryBackroundColor,
            borderColor: primaryBorderColor,
            borderWidth: 1
        },
        {
            label: 'Unpaid reservations',
            data: [],
            backgroundColor: secondaryBackroundColor,
            borderColor: secondaryBorderColor,
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Monthly amount of paid/unpaid reservations',
                padding: {
                    bottom: 5
                }
            }
        }  
    }
});


const updateChartData = (chart, new_datasets) =>  {
    new_datasets.forEach((new_dataset, idx) => {
        if(idx >= chart.data.datasets.length)
            return;

        chart.data.datasets[idx].data = new_dataset;
    });

    chart.update();
}


const updateIncomeChart = (year) => {
    fetch(`${apiUrl}/income/?year=${year}`)
    .then(response => response.json())
    .then(data => {
        updateChartData(incomeChart, [data["private_clients"], data["swim_schools"]])
    });    
};


const updateReservationsChart = (year) => {
    fetch(`${apiUrl}/reservations/?year=${year}`)
    .then(response => response.json())
    .then(data => {
        updateChartData(reservationsChart, [data["paid_reservations"], data["unpaid_reservations"]])
    });  
};


window.onload = () => {
    let incomeChartYear = document.getElementById("income-chart-year");
    let reservationsChartYear = document.getElementById("reservations-chart-year");

    incomeChartYear.onchange = () => {
        updateIncomeChart(incomeChartYear.value);
    };

    reservationsChartYear.onchange = () => {
        updateReservationsChart(reservationsChartYear.value);
    };

    updateIncomeChart(incomeChartYear.value);
    updateReservationsChart(reservationsChartYear.value);
}
