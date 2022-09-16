$(document).ready(function() {
    $("#close_account").on("click", function(e) {
      e.preventDefault();
      Swal.fire({
        icon: 'warning', 
        title: 'Вы действительно хотите выйти из аккаунта?',  
        showDenyButton: false,  showCancelButton: true,  
        confirmButtonText: `Да`,
        confirmButtonColor: '#6F8EFF',  
        cancelButtonText: `Отмена`
      }).then((result) => {  
          if (result.isConfirmed) {    
            window.location = "/exit"; 
          }
      });
    });
    });

document.querySelectorAll('.icon').forEach(link => {
    if (link.href == window.location.href){
        link.setAttribute('aria-current', 'page')
    }
})


function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }