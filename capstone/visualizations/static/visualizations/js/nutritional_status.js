$(document).ready(function() {

    $.ajax({
        url: "/visualizations/nutritional_status/get_weights",
        method: "POST",
        dataType: "json",
        success: function(data) {
            var statuses = JSON.parse(data.statuses);

            console.log(data.male);


            Highcharts.chart('container', {
              chart: {
                type: 'column'
              },
              title: {
                text: 'Total Nutritional Status Count as of Today'
              },
              xAxis: {
                categories: statuses
              },
              yAxis: {
                min: 0,
                title: {
                  text: 'Total Count'
                },
                stackLabels: {
                  enabled: true,
                  style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                  }
                }
              },
              legend: {
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
              },
              tooltip: {
                headerFormat: '<b>{point.x}</b><br/>',
                pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
              },
              plotOptions: {
                column: {
                  stacking: 'normal',
                  dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                  }
                }
              },
              series: [{
                name: 'Male',
                data: data.male
              }, {
                name: 'Female',
                data: data.female
              }]
            });
        },
        error: function(data) {
            console.log(data.responseText);
        }
    });

});






























function getCookie(name) {

        var cookieValue = null;

        if (document.cookie && document.cookie != '') {

            var cookies = document.cookie.split(';');

            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });