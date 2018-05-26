$(".del").click(function(){
    var t=$("input:checked").parent().parent("tr").remove();//移除选中的行  
});

$(function(){
    $('a#getReaction').on('shown.bs.tab', function (e) {
        $("div#reactions").empty();
        var snodes = "";
        var num = 0;
        $("#select-node tr").each(function(){
            var treatment = $(this).children('td:eq(2)').text();
            var drug = $(this).children('td:eq(3)').text();
            if(drug != ""){
                snodes += treatment + "/" + drug + "\t";
                num++;
            }   
        });
        
        snodes.trim();
        console.log(snodes);
        //如果不存在用药，则不存在冲突
        if(num > 1){
            $.get("getReaction", {"snodes": snodes}, function(data){
                if(!data.flag){
                    //console.log("hello");
                    $("div#reactions").html("<img src='static/image/reaction.jpg' class='img-thumbnail' style='margin-top:5px'><h4>所选节点无不良相互作用</h4>");
                }else{
                    for(var treatments in data.reactions){
                        html = "";
                        for(var prop in data.reactions[treatments])
                            html += "<tr><td>" + prop + "</td><td>" + data.reactions[treatments][prop] + "</td></tr>";
                        $("div#reactions").append("<h4>" + treatments + "</h4><table class='table  table-bordered' style='margin-top:5px'><thead><tr><th style='text-align:center'>属性</th><th style='text-align:center'>值</th></tr></thead><tbody>" + html + "</tbody></table><HR style='border:1 dashed #987cb9' width='100%' color=#987cb9 SIZE=5>");
                    }
                }
            })
        }else{
            $("div#reactions").html("<img src='static/image/reaction.jpg' class='img-thumbnail' style='margin-top:5px'><h4>所选节点无不良相互作用</h4>");
        }
    });
});

$("#SearchButton").click(function(){
    var diseases = "";
    $("li.search-choice > span").each(function(){
        diseases += $(this).text() + ",";
    });
    console.log("diseases:" + diseases);
    $("#user_text").attr("value", diseases);
    $("#searchRelationForm").submit();
});