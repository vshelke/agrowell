type = ['','info','success','warning','danger'];

function getChart(id, low, high) {
  var data = {
    labels: [],
    series: [[],[]]
  };
  var options = {
    lineSmooth: true,
    low: low,
    high: high,
    showArea: false,
    height: "245px",
    axisX: {
      showGrid: true,
    },
    lineSmooth: Chartist.Interpolation.simple({
      divisor: 3
    }),
    showLine: true,
    showPoint: false,
  };
  var responsive = [
    ['screen and (max-width: 640px)', {
      axisX: {
        labelInterpolationFnc: function (value) {
          return value[0];
        }
      }
    }]
  ];
  return new Chartist.Line(id, data, options, responsive);
}

function updateData(charts, date) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', date, true);
  xhr.onreadystatechange = function () {
    if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      var dict = JSON.parse(xhr.responseText);
      // console.log(xhr.responseText);
      if (dict.hasOwnProperty("status")) {
        $.notify({
          icon: "ti-na",
          message: dict.status
        },{
            type: 'warning',
            timer: 2000,
            placement: {
                from: 'top',
                align: 'right'
            }
        });
        $("#loader").css('display','none');
        return;
      }
      var raw = JSON.parse(dict.raw);
      var predicted = JSON.parse(dict.predicted);
      for (var ch in charts) {
        var chart = charts[ch];
        var x = chart.data.labels;
        var y = chart.data.series;
        for (var i in raw) {
            var d = new Date(raw[i].time);
            x.push(d.getHours() + ":" + d.getMinutes());
            if (ch == '0') {
              y[0].push(raw[i].moisture);
              y[1].push(predicted[i]);
            }
            if (ch == '1') {
              y[0].push(raw[i].temperature);
            }
            if (ch == '2') {
              y[0].push(raw[i].humidity);
            }
        }
        chart.update({
            labels: x,
            series: [y[0], y[1]]
        });
      }
      // growth rate
      var oldSlope = parseInt(JSON.parse(dict.oldCoefs)[0]);
      var newSlope = parseInt(JSON.parse(dict.newCoefs)[0]);
      $("#growthRate").html("<p>Growth Rate</p>" + ((oldSlope/newSlope)*100).toFixed(3) + "%");
      // plant friendly
      var moist = charts[0].data.series[0];
      var temp = charts[1].data.series[0];
      var humi = charts[2].data.series[0];
      var avgMoist = 0;
      var avgTemp = 0;
      var avgHumi = 0;
      for (var i in temp) {
        avgMoist += moist[i];
        avgTemp += temp[i];
        avgHumi += humi[i];
      }
      avgTemp /= temp.length;
      avgHumi /= humi.length;
      avgMoist /= moist.length;
      var friendly = ((20/avgTemp)+(70/avgHumi))/2;
      $("#plantFriendly").html("<p>Plant Friendly</p>" + (friendly*100).toFixed(2) + "%");
      // transpiration rate
      var minTemp = getMin(temp);
      var maxTemp = getMax(temp);
      var ahLower = (216.7 * (getMin(humi)/100) * 6.112 * (Math.exp((17.62 * minTemp)/(243.12+minTemp)) / (273.15 + minTemp)));
      var ahHigher = (216.7 * (avgHumi) * 6.112 * (Math.exp((17.62 * avgTemp)/(243.12+avgTemp)) / (273.15 + avgTemp)));
      var rate = Math.abs(avgMoist - ahHigher) * (300/2000);
      $("#transpirationRate").html("<p>Transpiration</p>" + rate.toFixed(2) + "%");

      $("#loader").css('display','none');
    }
  };
  xhr.send();
  $("#loader").css('display','');
}

function changeData(charts) {
  var date = "/".concat($('#selectedDate').val()).concat("/");
  for (var i in charts) {
    var chart = charts[i];
    chart.data = {
      labels: [],
      series: [[],[]]
    };
  }
  updateData(charts, date);
}

function getMax(arr) {
  var max = arr.reduce(function(a, b) {
      return Math.max(a, b);
  });
  return max;
}

function getMin(arr) {
  var min = arr.reduce(function(a, b) {
    return Math.min(a, b);
  });
  return min;
}