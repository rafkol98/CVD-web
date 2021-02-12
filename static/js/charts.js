var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'radar',

    // The data for our dataset
    data: {
        labels: ['Beats Per Second', 'Resting Blood Pressure', 'Cholestrol', 'Max Heart Rate Achieved', 'Oldpeak'],
        datasets: [{
            label: 'Patient Values',
            pointBackgroundColor: 'rgb(55, 99, 132,0.2)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20]
        },{
            label: 'Average values',
            pointBackgroundColor: 'rgb(0, 0, 0,0.5)',
            borderColor: 'rgb(0, 0, 0)',
            data: [10, 20, 12, 5, 25]
        } ]
    },

    // Configuration options go here
    options: {}
});

