let id = (id) => document.getElementById(id);

        let classes = (classes) => document.getElementsByClassName(classes);

        let new_password1 = id("id_new_password1"),
            new_password2 = id("id_new_password2")
            form = id("newpassword-fromID"),
            errorMsg = classes("error");
        
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            
            if (new_password1.value.trim() === "" && new_password2.value.trim() === "") {
                new_password1.style.border = "2px solid red";
                new_password1.classList.add('danger')
                errorMsg[0].innerHTML = "Поле обязательное*";
                new_password2.style.border = "2px solid red";
                new_password2.classList.add('danger')
                errorMsg[1].innerHTML = "Поле обязательное*";
            } 
            if (new_password1.value.trim() !== "") {
                new_password1.style.border = "2px solid green";
                errorMsg[0].innerHTML = "";
            }
            if (new_password2.value.trim() !== "") {
                new_password2.style.border = "2px solid green";
                errorMsg[1].innerHTML = "";
            }
            if (new_password1.value.trim() !== "" && new_password2.value.trim() !== "") {
                form.submit();
            } 
        });