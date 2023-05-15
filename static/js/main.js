let buttons = document.querySelectorAll("#modalBtn")
buttons.forEach(function (button) {
    button.addEventListener('click', async function () {
        console.log(button);
        let a = button.dataset.id;
        let response = await fetch(`/api/all_shows_actor_starred/${a}`);
        let apiResponse = await response.json();
        let titleOutput = `${apiResponse[0]['name']}`;
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            contentOutput += `<li>${apiResponse[i]['title']}</li>`
        }
        $(`#myModal${a}`).modal('show');
        document.querySelector('.modal-title').innerHTML = titleOutput;
        document.querySelector('.modal-body').innerHTML = contentOutput;
    });
});


let buttonsSim = document.querySelectorAll("#modalBtnSim")
buttonsSim.forEach(function (button) {
    button.addEventListener('click', async function () {
        console.log(button);
        let a = button.dataset.id;
        let response = await fetch(`/api/actors_for_simulation_shows/${a}`);
        let apiResponse = await response.json();
        let titleOutput = `Starring`;
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            contentOutput += `<li>${apiResponse[i]['name']}</li>`
        }
        $(`#myModal${a}`).modal('show');
        document.querySelector('.modal-title').innerHTML = titleOutput;
        document.querySelector('.modal-body').innerHTML = contentOutput;
    });
});


let buttonSim2 = document.querySelectorAll(".actor")
buttonSim2.forEach(function (button) {
    button.addEventListener('click', async function () {
        let actor_name = button.dataset.name;
        console.log(actor_name)
        let response = await fetch(`/api/sim2/${actor_name}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            contentOutput += `<li>${apiResponse[i]['title']}</li>`
        }
        document.querySelector('.popupSim2').innerHTML = contentOutput;
    });
});


let buttonSim3 = document.querySelectorAll(".genres")
buttonSim3.forEach(function (button) {
    button.addEventListener("click", async function () {
        let genres_name = button.dataset.name;
        console.log(genres_name)
        let response = await fetch(`/api/sim3/${genres_name}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            contentOutput += `<li> ${apiResponse[i]['title']}</li>`
        }
        document.querySelector('.popupSim3').innerHTML = contentOutput;
    });
});

let buttonSim4 = document.querySelectorAll(".runtime")
buttonSim4.forEach(function (button) {
    button.addEventListener("click", async function () {
        let genres = button.dataset.id;
        console.log(genres);
        let response = await fetch(`/api/sim4/${genres}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            contentOutput += `<li> ${apiResponse[i]['name']}</li>`
        }
        document.querySelector(".popupSim4").innerHTML = contentOutput

    })
})


let buttonSim5 = document.querySelectorAll('.tenLatest')
buttonSim5.forEach(function (button) {
    button.addEventListener("click", async function () {
        let actors_starring = button.dataset.id;
        console.log(actors_starring)
        let response = await fetch(`/api/ten_latest/${actors_starring}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            contentOutput += `<li>${apiResponse[i]['name']}</li>`
        }
        document.querySelector(".popupSim5").innerHTML = contentOutput
    })
})


let buttonSim6 = document.querySelectorAll(".tenOldest")
buttonSim6.forEach(function (button) {
    button.addEventListener("click", async function () {
        let seasons_and_episodes_count = button.dataset.id;
        let response = await fetch(`/api/ten_oldest/${seasons_and_episodes_count}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            console.log(apiResponse)
            contentOutput += `<li>${apiResponse[i]['season_title']}</li>
                                <ul>${apiResponse[i]['count']} Episodes</ul>
<br>`
        }
        document.querySelector(".popupSim6").innerHTML = contentOutput
    })

})


let buttonSim7 = document.querySelectorAll('.actShows')
buttonSim7.forEach(function (button) {
    button.addEventListener("click", async function () {
        let show_runtime = button.dataset.id
        let response = await fetch(`/api/runtime/${show_runtime}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            console.log(apiResponse)
            contentOutput += `<li>${apiResponse[i]['runtime']} Minutes</li>`
        }
        document.querySelector(".popupSim7").innerHTML = contentOutput
    })
})


let buttonPA = document.querySelectorAll('.genresSim9');
buttonPA.forEach(function (button) {
    button.addEventListener("click", async function () {
        let movies_in_genre = button.dataset.id;
        let genre_id = await fetch(`/api/shows/${movies_in_genre}`);
        let genre_id_response = await genre_id.json();
        let contentOutput = ``
        console.log(genre_id_response)
        for (let i = 0; i < genre_id_response.length; ++i) {
            contentOutput += `<li>${genre_id_response[i]['title']}</li> `
        }
        document.querySelector('.popupSim9').innerHTML = contentOutput
    })
})


let buttonSim8 = document.querySelectorAll('.sim8')
buttonSim8.forEach(function (button) {
    button.addEventListener("click", async function () {
        let biography = button.dataset.id;
        let response = await fetch(`/api/biography/${biography}`);
        let apiResponse = await response.json();
        let contentOutput = ``;
        for (let i = 0; i < apiResponse.length; ++i) {
            console.log(apiResponse)
            contentOutput += `<li>${apiResponse[i]['biography']}</li>`
        }
        document.querySelector('.popupSim8').innerHTML = contentOutput
    })
})

//method using document.createElement // PA version
let buttonActorsTotalRuntime = document.querySelectorAll('.actorsPA')
buttonActorsTotalRuntime.forEach(function (button) {
    button.addEventListener("click", async function (data) {
        let actorId = button.dataset.id;
        let actorIdResponse = await fetch(`/api/PA/${actorId}`);
        let apiResponse = await actorIdResponse.json();
        console.log(apiResponse)

        const newDiv = document.createElement("li")
        newDiv.setAttribute('id', 'listJS')

        for (let i = 0; i < apiResponse.length; ++i) {
            if (document.contains(document.getElementById("listJS"))) {
                document.getElementById("listJS").remove();

                createData(`${apiResponse[i]['total_runtime']}`, newDiv)
            } else {
                createData(`${apiResponse[i]['total_runtime']}`, newDiv)
            }
        }

    })
})

function createData(value, whereToAdd) {
    const newContent = document.createTextNode(value)
    whereToAdd.appendChild(newContent)
    document.getElementById("listPa").append(whereToAdd)
}

























