if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}

let counter = localStorage.getItem('counter');

function count() {
    counter++;
    document.querySelector('h1').innerHTML = counter;
    localStorage.setItem('counter', counter);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').onclick = count;
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
});

