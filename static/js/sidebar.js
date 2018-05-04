$(document).ready(function(){
   $(".btn btn-default").click(function(){
    alert("12131")
    var id=$(this).attr("id");
    $("div#"+id).slidetoggle();
  });

  $("#01").click(function(){
    $("#01title").show();
    $(this).attr("class","active");
    $("#02").attr("class","disabled");
    $("#02title").hide();
  });

  $("#02").click(function(){
    $("#01title").hide();
    $(this).attr("class","active");
    $("#01").attr("class","disabled");
    $("#02title").show();
  });
});