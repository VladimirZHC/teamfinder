let id = (id) => document.getElementById(id);

        let classes = (classes) => document.getElementsByClassName(classes);

        let email = id("id_email"),
            form = id("pass-reset-form-id"),
            errorMsg = classes("error");
        
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            
            if (email.value.trim() === "") {
                email.style.border = "2px solid red";
                email.classList.add('danger')
                errorMsg[0].innerHTML = "Поле обязательное*";
            } 
            else {
                form.submit();
            }
            
        });