let buttons  = document.querySelectorAll("#modalBtn")
 buttons.forEach(function (button) {
  button.addEventListener('click', async function() {
    console.log(button);
    let a = button.dataset.id;
    let response = await fetch(`/api/all_shows_actor_starred/${a}`);
    let apiResponse = await response.json();
    let titleOutput = `${apiResponse[0]['name']}`;
    let contentOutput = ``;
    for (let i=0; i < apiResponse.length ; ++i) {
        contentOutput += `<li>${apiResponse[i]['title']}</li>`}
        $(`#myModal${a}`).modal('show');
        document.querySelector('.modal-title').innerHTML = titleOutput;
        document.querySelector('.modal-body').innerHTML = contentOutput;
    });
 });

let buttonsSim = document.querySelectorAll("#modalBtnSim")
buttonsSim.forEach(function (button) {
  button.addEventListener('click', async function() {
    console.log(button);
    let a = button.dataset.id;
    let response = await fetch(`/api/actors_for_simulation_shows/${a}`);
    let apiResponse = await response.json();
    let titleOutput = `Starring`;
    let contentOutput = ``;
    for (let i=0; i < apiResponse.length ; ++i) {
        contentOutput += `<li>${apiResponse[i]['name']}</li>`}
        $(`#myModal${a}`).modal('show');
        document.querySelector('.modal-title').innerHTML = titleOutput;
        document.querySelector('.modal-body').innerHTML = contentOutput;
    });
 });



const button = document.querySelectorAll('.register_login_button');

const disableButton = () => {
    button.disabled = true;
};

button.addEventListener('click', disableButton);