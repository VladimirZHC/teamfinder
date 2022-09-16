let id = (id) => document.getElementById(id);

        let classes = (classes) => document.getElementsByClassName(classes);

        let fullname = id('id_full_name'),
            email = id("id_email"),
            password1 = id("id_password1"),
            password2 = id("id_password2"),
            form = id("reg_form"),
            errorMsg = classes("error"),
            errorMsg1 = classes("error1"),
            errorMsg2 = classes("error2");
        
        
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            
            if (fullname.value.trim() === "" || email.value.trim() === "" || password1.value.trim() === "" || password2.value.trim() === "") {
                fullname.style.border = "2px solid red";
                email.style.border = "2px solid red";
                password1.style.border = "2px solid red";
                password2.style.border = "2px solid red";
                fullname.classList.add('danger')
                email.classList.add('danger')
                password1.classList.add('danger')
                password2.classList.add('danger')
                errorMsg1[0].innerHTML = "Поле обязательное*";
                errorMsg2[0].innerHTML = "Поле обязательное*";
                errorMsg[0].innerHTML = "Поле обязательное*";
                errorMsg[1].innerHTML = "Поле обязательное*";
            } 
            if (fullname.value.trim() != "") {
                fullname.style.border = "2px solid green";
                errorMsg1[0].innerHTML = "";
            } 
            if (email.value.trim() !== "") {
                email.style.border = "2px solid green";
                errorMsg2[0].innerHTML = "";
            }
            if (password1.value.trim() != "") {
                password1.style.border = "2px solid green";
                errorMsg[0].innerHTML = "";
            }
            if (password2.value.trim() != "") {
                password2.style.border = "2px solid green";
                errorMsg[1].innerHTML = "";
            }
            if (fullname.value.trim() != "" && email.value.trim() != "" && password1.value.trim() != "" && password2.value.trim() != "") {
                form.submit();
            }
        });