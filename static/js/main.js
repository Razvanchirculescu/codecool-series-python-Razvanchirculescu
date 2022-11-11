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