$(function() {

    const id = $("#main").attr('data-id');

    $.ajax({
        url: "/causal-models/details",
        type: "post",
        data: { 'id': id },
        dataType: "json",
        success: function(data) {

            console.log(data);

            var GO = go.GraphObject.make;

            var diagram = GO(go.Diagram, "tree", { layout: GO(go.TreeLayout, { angle: 90, layerSpacing: 35 }) });
            var myModel = GO(go.TreeModel);

            diagram.nodeTemplate =
               GO(go.Node, "Vertical",
                   GO(go.Panel, "Vertical", { background: "#f4f5f7", padding: 10 },
                       GO(go.TextBlock, new go.Binding("text", "name"), { font: "bold 12pt Arial" }),
                       GO(go.Panel, "Vertical", new go.Binding("itemArray", "quantifiable_data"),
                           {
                               itemTemplate:
                                   GO(go.Panel, "Auto",
                                    { margin: 2 },
                                   GO(go.TextBlock, new go.Binding("text", ""),
                                    { margin: 2, font: "italic bold 10pt Arial", stroke: "red" })
                                )

                           }
                       )
                   )
               );

            myModel.nodeDataArray = data;

            diagram.model = myModel;
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