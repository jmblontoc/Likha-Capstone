$(function() {

    const button = $("button.diagram_btn");
    const submitComment = $("#submit_comment");
    const treeHolder = $("#tree-holder");
    const commentHolder = $(".comment-holder");
    const approveCM = $(".approve-cm");

    function getID() {

        var cm = $(this).attr("data-id");
        console.log(cm);

        submitComment.attr('data-id', cm);
        approveCM.attr('data-id', cm);

        // show commands
        $(".cm-commands").show();

        $.ajax({
            url: "/causal-models/details",
            type: "post",
            data: { 'id': cm },
            dataType: "json",
            success: function(data) {

                treeHolder.empty();
                commentHolder.empty();

                var html = "<div id='tree' style='height: 600px; width: 1300px;' class='card'></div>";
                treeHolder.append(html);
                console.log(data);

                // comments
                if (data.comments.length === 0) {
                    var a = '<div class="no-comments text-center">' +
                        '                                        <p>There are no comments for this causal model yet</p>' +
                        '                                    </div>';

                        commentHolder.append(a);
                }
                else {

                    const commentHolder = $(".comment-holder");

                    for (var x = 0; x < data.comments.length; x++) {

                        var template = "<div class='card m-2 p-2'>" +
                        "<div><span class='sender text-bold'>"+data.comments[x].profile+"</span> <span class='user_type font-italic'>"+data.comments[x].user_type+"</span></div>" +
                        "<div class='commentMain'>\""+data.comments[x].comment+"\"</div>" +
                        "<div class='timeWhen font-italic'>"+data.comments[x].date+"</div>" +
                        "</div>";

                        commentHolder.append(template);
                    }
                }


                // tree

                var GO = go.GraphObject.make;

                var diagram = GO(go.Diagram, "tree", { layout: GO(go.TreeLayout, { angle: 90, layerSpacing: 35 }) });
                var myModel = GO(go.TreeModel);


                myModel.nodeDataArray = data.data;

                diagram.model = myModel;

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

                },
            error: function(data) {
                console.log(data.responseText);
            }
        });

        return cm;
    }

    button.click(getID);

    submitComment.click(function() {
        const comment = $("#comment-main").val();
        const id = $(this).attr('data-id');
        // call ajax
        $.ajax({
            url: "/causal-models/insert_comment",
            type: "POST",
            data: {
                'comment': comment,
                'id': id
            },
            success: function(data) {

                console.log(data);

                var template = "<div class='card m-2 p-2'>" +
                "<div><span class='sender text-bold'>"+data.profile+"</span> <span class='user_type font-italic'>"+data.user_type+"</span></div>" +
                "<div class='commentMain'>\""+data.comment+"\"</div>" +
                "<div class='timeWhen font-italic'>"+data.date+"</div>" +
                "</div>";

                commentHolder.prepend(template);
                $("#comment-main").val('');
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });

    approveCM.click(function() {

        const id = $(this).attr('data-id');

        $.ajax({
            url : "/causal-models/approve",
            type: "post",
            data: {
                'id': id
            },
            success: function(e) {
                alert("Causal model approved");
                location.reload();
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