
function confirm(msg, pro, con) {
    let modal = document.querySelector('#modal-confirm-alert');
    modal.style.display = 'block';
    document.querySelector( '#modal-backdrop').style.display = 'block';
    modal.innerHTML = ''
    
    var h1 = document.createElement('h1');
    h1.innerText = msg;
    
    var ybutton = document.createElement('button');
    ybutton.innerText = 'Godkend';
    ybutton.onclick = ()=>{
        modal.style.display = 'none';
        document.querySelector( '#modal-backdrop').style.display = 'none';
        pro();
    }
    var nbutton = document.createElement('button');
    nbutton.innerText = 'Afbryd';
    nbutton.onclick = ()=>{
        modal.style.display = 'none';
        document.querySelector( '#modal-backdrop').style.display = 'none';
        con();
    }

    modal.appendChild(h1);
    modal.appendChild(ybutton);
    modal.appendChild(nbutton);

}

function alert(msg) {
    let modal = document.querySelector('#modal-confirm-alert');
    document.querySelector( '#modal-backdrop').style.display = 'block';
    modal.style.display = 'block';
    modal.innerHTML = ''

    var h1 = document.createElement('h1');
    h1.innerText = msg;
    
    var button = document.createElement('button');
    button.innerText = 'OK';
    button.onclick = ()=>{
        modal.style.display = 'none';
        document.querySelector( '#modal-backdrop').style.display = 'none';
    }

    modal.appendChild(h1);
    modal.appendChild(button);
}

setTimeout(() => {
    const modal = document.createElement('div');
    const backdrop = document.createElement('div');
    modal.id = 'modal-confirm-alert';
    backdrop.id = 'modal-backdrop';
    document.body.appendChild(modal)
    document.body.appendChild(backdrop);
}, 1000);
