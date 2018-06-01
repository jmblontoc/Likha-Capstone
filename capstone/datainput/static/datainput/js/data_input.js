$(document).ready(function() {

    console.log("ready");

    $("div.family-div").click(function () {

        id = $(this).attr('id');

        $.ajax({
            url: '/data-input/bns/family_profile/show_ajax',
            data: {
                'family_id': id
            },
            dataType: 'json',
            type: "POST",
            success: function (data) {

                var parsed = JSON.parse(data.profile)[0].fields;

                $("#number").html(parsed.household_no);
                $("#countMembers").html(parsed.no_members);
                $("#05").html(parsed.count_05);
                $("#623").html(parsed.count_623);
                $("#2459").html(parsed.count_2459);
                $("#60").html(parsed.count_60);
                $("#education").html(parsed.educational_attainment);
                $("#occupation").html(parsed.occupation);
                $("#pregnant").html(parsed.is_mother_pregnant);
                $("#familyPlanning").html(parsed.is_family_planning);
                $("#ebf").html(parsed.is_ebf);
                $("#mmf").html(parsed.is_mixed_milk_feeding);
                $("#bottled").html(parsed.is_bottle_feeding);
                $("#salt").html(parsed.is_using_iodized_salt);
                $("#iron").html(parsed.is_using_ifr);
                $("#toilet").html(parsed.toilet_type);
                $("#water").html(parsed.water_sources);
                $("#food").html(parsed.food_production_activity);

                $("div.fields").children().each(function () {
                    console.log($(this).children('span')[0].innerHTML);
                    var text = $(this).children('span')[0];
                    if (text.innerText == '') {
                        text.innerText = 'false';
                    }
                });

            },
            error: function (data) {
                console.log(data.responseText);
            }
        });
    });

    $("li.health_care_record").click(function() {
        console.log("please");
        var id = $(this)[0].id;

        $.ajax({
            url: "/data-input/nutritionist/show_health_care",
            type: "POST",
            dataType: "json",
            data: {
                'id': id
            },
            success: function(data) {

                var parsed = JSON.parse(data.record)[0].fields;
                console.log(parsed);

                $("span.hc1").html(parsed.with_syringe);
                $("span.hc2").html(parsed.with_safe_water);
                $("span.hc3").html(parsed.with_sanitary_toilet);
                $("span.hc4").html(parsed.with_satisfactoral_disposal);
                $("span.hc5").html(parsed.with_complete_facilities);
            },
            error: function(data) {
                console.log(data.responseText);
            }
        });
    });
});

















    // to prevent 403 nvm this code
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