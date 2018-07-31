$(function() {

    const submitThreshold = $("#submitThreshold");

    $("#thresholdModal").on("show.bs.modal", function(e) {

        const button = $(e.relatedTarget);
        const field = button.attr("data-field");

        $("b#field").html(field);

        $.ajax({
            url: '/data-pre_processing/ajax/get_values',
            type: "POST",
            data: { 'field': field },
            success: function(data) {
                console.log(data);

                var source = data.source;
                const withForecast = data.current.slice();
                withForecast.push({
                    'y': data.forecast,
                    'color': '#daffc4'
                });

                if (source === 'ChildCare') {
                    source = 'Child Care';
                }

                if (source === 'MaternalCare') {
                    source = 'Maternal Care';
                }

                submitThreshold.attr('data-source', source);
                submitThreshold.attr('data-field', field);
                submitThreshold.attr('data-json', JSON.stringify(data));

                Highcharts.chart('value-body', {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: "Yearly Totals of " + field
                    },
                    xAxis: {
                        categories: cheatYears(data.data),
                        crosshair: true
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Population'
                        },
                        plotLines: [{
                            value: data.average,
                            color: 'green',
                            width: 2,
                            label: {
                                text: 'Average = ' + data.average
                            },
                            zIndex: 4
                        }]
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
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
                    series: [{
                        name: field,
                        data: withForecast

                    }]
                });
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });

    submitThreshold.click(function() {

        const source = $(this).attr('data-source');
        const field = $(this).attr('data-field');
        const json = $(this).attr('data-json');

        const metric = source + "|" + field;
        const threshold = $("#threshold").val();

        $.ajax({
            url: "/data-pre_processing/ajax/insert_metric",
            type: "POST",
            data: {
                'metric': metric,
                'jsonData': json,
                'threshold': threshold
            },
            success: function(x) {
                alert("Threshold successfully set");
                window.location.replace('/data-pre_processing/set_thresholds');
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });
});









function cheatYears(length) {

    var yearNow = moment().year();
    var years = [yearNow];

    for (var x = 0; x < length - 1; x++) {
        yearNow--;
        years.push(yearNow);
    }

    console.log(years.sort());
    return years.sort();
}















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