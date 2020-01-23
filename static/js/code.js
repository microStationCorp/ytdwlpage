let btn = document.getElementsByClassName('btn-js');
let names = ['text-primary', 'text-secondary', 'text-success', 'text-danger', 'text-warning', 'text-info', 'text-light', 'text-dark']
for (let item of btn) {
    item.addEventListener('click', (e) => {
        let i = 0;
        setInterval(() => {
            if (i == names.length) {
                i = 0;
            }
            document.getElementById('btn-loading').innerHTML = `<div class='brdr'><div class="spinner-grow ${names[i]}" role="status">
                <span class="sr-only">Loading...</span>
              </div></div>`
            i++;
        }, 700)

    })
}