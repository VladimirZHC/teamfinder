const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const test = document.getElementById('test')
const sendSearchData = (game) => {
    $.ajax({
        type: 'POST',
        url: '',
        data: {
            'csrfmiddlewaretoken': csrf,
            'game': game
        },
        success: (res)=>{
            console.log(res.data)
            const data = res.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(game=> {
                    resultsBox.innerHTML += `
                    <br>
                                    <div class="item">
                                        <div class="row mt-2 mb-2">
                                            <div class="col-3 user-image"> 
                                                <img src="${game.img}" class="game-img">
                                            </div>
                                            <div class="col-3">
                                                <h5> ${game.full_name} </h5>
                                                <p class="text-muted"> ${game.email}</p>
                                            </div>
                                            <div class="col-3">
                                                <input type="button" class="btn btn-outline-info" value="Посмотреть профиль" onClick='window.location.href = "/profile/${game.pk}"'>
                                            </div>
                                        </div> 
                                    </div>
                                `

                })
            } else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error: (err)=> {
            console.log(err)
        }
    })
}


searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)

    if (resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})

htmx.onLoad(function(content) {
    var sortables = content.querySelectorAll(".sortable");
    for (var i = 0; i < sortables.length; i++) {
      var sortable = sortables[i];
      new Sortable(sortable, {
          animation: 150,
          ghostClass: 'blue-background-class'
      });
    }
})