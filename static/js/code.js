let hme = document.getElementById('home');
let srch = document.getElementById('search');

let box = document.getElementById('formBox');
box.addEventListener('click', (e) => {
    if (e.target.classList['1'] == undefined) {
        if (e.target['id'] == 'home') {
            srch.className = srch.classList['0']
            hme.className = hme.className + ' active'
            document.getElementById('form').innerHTML = `<form action="" method="GET">
						<div class="input-group mb-3 mt-2 col-sm-11 mx-auto">
						<div class="input-group-prepend">
						<span class="input-group-text" id="inputGroup-sizing-default">URL</span>
						</div>
						<input type="text" class="form-control"
						placeholder="e.g : https://www.youtube.com/watch?v=67aR580Yqw8" aria-label="YouTube link"
						aria-describedby="button-addon2" name="urlBox">
						</div>
						<div class="input-group-append">
						<button class="btn btn-primary btn-font" type="submit" id="button-addon2">Convert</button>
						</div>
						</form>`;
        } else if (e.target['id'] == 'search') {
            hme.className = hme.classList['0']
            srch.className = srch.className + ' active'
            document.getElementById('form').innerHTML = `<form action="/search" method="GET">
						<div class="input-group mb-3 mt-2 col-sm-11 mx-auto">
						<div class="input-group-prepend">
						<span class="input-group-text" id="inputGroup-sizing-default">Name</span>
						</div>
						<input type="text" class="form-control" placeholder="search video by name" aria-label="search value"
						aria-describedby="button-addon2" name="searchName">
						</div>
						<div class="input-group-append">
						<button class="btn btn-primary btn-font" type="submit" id="button-addon2">SEARCH</button>
						</div>
						</form>`;
        }
    }

})