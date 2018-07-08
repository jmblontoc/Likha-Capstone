$(function() {

    var startDate = $("#start_date").html();
    var endDate = $("#end_date").html();

    $.ajax({
        url: "/visualizations/maternal/get_data",
        method: "POST",
        dataType: "json",
        data: {
            start_date: startDate,
            end_date: endDate
        },
        success: function(data) {

            console.log(data);

            Highcharts.chart('container', {
              chart: {
                type: 'column'
              },
              title: {
                text: 'Total Maternal Care Count as of Today'
              },
              xAxis: {
                categories: data.fields,
                crosshair: true
              },
              yAxis: {
                min: 0,
                title: {
                  text: 'Total Count'
                }
              },
              tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">Total: </td>' +
                  '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
              },
              plotOptions: {
                column: {
                  pointPadding: 0.2,
                  borderWidth: 0
                }
              },
              series: [ {
                name: 'Fields',
                data: data.values

              }, {
                  name: 'Threshold',
                  marker: {
                    symbol: 'url(/static/visualizations/media/red.png)',
                    lineWidth: 3,
                    height: 3,
                    width: 150,
                    radius: 10
                  },
                  type: 'scatter',
                  data: data.thresholds
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