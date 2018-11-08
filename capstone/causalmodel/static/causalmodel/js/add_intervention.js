$(function() {

    $("#add-intervention-btn").click(function() {


        var modalBody = $(this).parent().siblings(".modal-body");

        var interventionName = modalBody.find("#intervention-name").val();
        var interventionReason = modalBody.find("#intervention-reason").val();
        var metricID = modalBody.data("metric");

        // <div class="intervention-select">
        //    <input type="checkbox" name="interventions" value="{{ intervention.name }}">
        //    <label class="form-check-label" data-toggle="tooltip" data-placement="top" title="{{ intervention.reason }}">
        //        {{ intervention.name }}
        //        <span class="font-italic">({{ intervention.last_proposed }})</span>
        //    </label>
        // </div>

        console.log(interventionReason == "Select Reason");

        if (interventionReason == "Select Reason") {
            alert("Please choose a reason");
            return;
        }

        $.ajax({
            url: "/causal-models/add_intervention_from_modal",
            type: "POST",
            data: {
                'id': metricID,
                'name': interventionName,
                'reason': interventionReason
            },
            success: function(data) {

                modalBody.find("#intervention-name").val("");
                modalBody.find("#intervention-reason").val("");

                var html = "<div class='intervention-select'>" +
                    "<input type='checkbox' name='interventions' value='" + data.name + "'>" +
                    "<label class='form-check-label' data-toggle='tooltip' data-placement='top' title='"+ data.reason +"'>" + data.name +
                    "<span class='font-italic'>("+ data.last_proposed +")</span>" +
                    "</label>" +
                    "</div>";

                $(".intervention-container-manual").append(html);

                $("#add-intervention-modal").modal('hide');
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });
});