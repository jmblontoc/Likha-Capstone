$(function() {



    $("#viewCorrelationGraph").on("show.bs.modal", function(e) {
        const button = $(e.relatedTarget);

        const category = button.parent().siblings(".category").html();
        const source = button.parent().siblings(".source").html();
        const field = button.parent().siblings(".field").html();


        $.ajax({
            url: "/data-mining/get_variables",
            type: "post",
            data: {
                'category': category,
                'source': source,
                'field': field
            },
            dataType: "json",
            success: function(d) {

                const variables = d.variables;

                Highcharts.chart('scatterGraph', {
                    chart: {
                        type: 'scatter',
                        zoomType: 'xy'
                    },
                    title: {
                        text: category + ' vs. ' + source
                    },
                    xAxis: {
                        title: {
                            enabled: true,
                            text: source
                        },
                        startOnTick: true,
                        endOnTick: true,
                        showLastLabel: true
                    },
                    yAxis: {
                        title: {
                            text: category
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'left',
                        verticalAlign: 'top',
                        x: 100,
                        y: 70,
                        floating: true,
                        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
                        borderWidth: 1
                    },
                    plotOptions: {
                        scatter: {
                            marker: {
                                radius: 5,
                                states: {
                                    hover: {
                                        enabled: true,
                                        lineColor: 'rgb(100,100,100)'
                                    }
                                }
                            },
                            states: {
                                hover: {
                                    marker: {
                                        enabled: false
                                    }
                                }
                            },
                            tooltip: {
                                headerFormat: '<b>{series.name}</b><br>',
                                pointFormat: '{point.x} cm, {point.y} kg'
                            }
                        }
                    },
                    series: [{
                        name: 'Observation',
                        color: 'rgba(119, 152, 191, .5)',
                        data: variables
                    }]
                });
            },
            error: function(e) {
                console.log(e.responseText);
            }
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