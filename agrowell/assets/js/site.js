requirejs(["chartjs"], function(chart) {
    var ctx = document.getElementById("moisture").getContext('2d');
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: [20, 10],
        options: {}
    });
});