$(document).ready(function(){
    $(".show-hide-btn").click(function(){
        var id = $(this).data("id");
        $("#half-"+id).hide();
        $("#full-"+id).show();
    });
    $(".show-full-btn").click(function(){
        var id = $(this).data("id");
        $("#full-"+id).hide();
        $("#half-"+id).show();
    });
    $(".btn-close").click(function(){
        $("#hide").fadeOut(500,function() {
            $("#hide").hide();
        });
    });
    setTimeout(function(){ $("#hide").fadeOut(500,function() {
        $("#hide").hide();
    }); }, 5000);
});

const check = document.getElementsByClassName('half-content')[0].innerHTML;
const text = document.querySelector('.half-content');
if (check.length > 200) {
    text.classList.add('grad');
}




        
        
        
            
            