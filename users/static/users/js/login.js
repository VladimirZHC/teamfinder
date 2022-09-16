$(document).ready(function(){
    $(".btn-close").click(function(){
        $("#hide").fadeOut(500,function() {
            $("#hide").hide();
        });
    });
    setTimeout(function(){ $("#hide").fadeOut(500,function() {
        $("#hide").hide();
    }); }, 5000);
});

let id = (id) => document.getElementById(id);

        let classes = (classes) => document.getElementsByClassName(classes);

        let email = id("id_username"),
            password = id("id_password"),
            form = id("login_form"),
            errorMsg = classes("error");
        
        
        

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            
            if (email.value.trim() === "" && password.value.trim() === "") {
                email.style.border = "2px solid red";
                password.style.border = "2px solid red";
                email.classList.add('danger')
                password.classList.add('danger')
                errorMsg[0].innerHTML = "Поле обязательное*";
                errorMsg[1].innerHTML = "Поле обязательное*";
            } 
            if (email.value.trim() != "" && password.value.trim() === "") {
                email.style.border = "2px solid green";
                errorMsg[0].innerHTML = "";
                password.style.border = "2px solid red";
                errorMsg[1].innerHTML = "Поле обязательное*";
            }
            if (password.value.trim() != "" && email.value.trim() === "" ) {
                password.style.border = "2px solid green";
                errorMsg[1].innerHTML = "";
                email.style.border = "2px solid red";
                errorMsg[0].innerHTML = "Поле обязательное*";
            }
            if (email.value.trim() != "" && password.value.trim() != "") {
                form.submit();
            }
            
        });
