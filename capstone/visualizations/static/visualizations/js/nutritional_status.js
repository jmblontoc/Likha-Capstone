$(document).ready(function() {

    const status = $("#status");
    const startDate = $("#start_date").html();
    const endDate = $("#end_date").html();

    $.ajax({
            url: "/visualizations/nutritional_status/get_data",
            type: "post",
            data: {
                'start_date': startDate,
                'end_date': endDate,
                'status': 'Weight for Age'
            },
            dataType: "json",
            success: function(data) {
                console.log(data);

                Highcharts.SVGRenderer.prototype.symbols['c-rect'] = function (x, y, w, h) {
                    return ['M', x, y + h / 2, 'L', x + w, y + h / 2];
                };


                Highcharts.chart('container', {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Stacked column chart'
                    },
                    xAxis: {
                        categories: data.statuses
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Total ' + name
                        },
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
                            dataLabels: {
                                enabled: true,
                                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                            }
                        }
                    },
                    series: [{
                        name: 'Total',
                        data: data.values
                    }, {
                        name: 'Threshold',
                        marker: {
                            symbol: 'url(/static/visualizations/media/red.png)',
                            lineWidth:3,
                            height: 2,
                            width: 180,
                            radius: 10
                        },
                      type: 'scatter',
                      data: data.thresholds
                    }]
                });

            },
            error: function(e) {
                console.log(e.responseText);
            }
            // {

            //         }

        });

    status.on('change', function() {

        var name = $(this).val();

        $.ajax({
            url: "/visualizations/nutritional_status/get_data",
            type: "post",
            data: {
                'start_date': startDate,
                'end_date': endDate,
                'status': name
            },
            dataType: "json",
            success: function(data) {
                console.log(data);

                Highcharts.SVGRenderer.prototype.symbols['c-rect'] = function (x, y, w, h) {
                    return ['M', x, y + h / 2, 'L', x + w, y + h / 2];
                };


                Highcharts.chart('container', {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Stacked column chart'
                    },
                    xAxis: {
                        categories: data.statuses
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Total ' + name
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
                        name: 'Total',
                        data: data.values
                    }, {
                        name: 'Threshold',
                        marker: {
                            symbol: 'url(/static/visualizations/media/red.png)',
                            lineWidth:3,
                            height: 2,
                            width: 180,
                            radius: 10
                        },
                      type: 'scatter',
                      data: data.thresholds
                    }]
                });

            },
            error: function(e) {
                console.log(e.responseText);
            }
            // {

            //         }

        });
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