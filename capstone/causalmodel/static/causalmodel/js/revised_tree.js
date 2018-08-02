$(function() {

    $.ajax({
        url: "/causal-models/p",
        success: function(data) {
            console.log(data, "woooh");

            var x = [];

            x.push({
                "key": 1,
                "name": "Hello",
                "parent": 2
            });

            x.push({
                "key": 2,
                "name": "JM",
                "parent": 4
            });


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

            myModel.nodeDataArray = data.data;

            diagram.model = myModel;
        },
        error: function(data) {
            console.log(data.responseText);
        }
    });


});