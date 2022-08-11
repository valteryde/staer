
function checkRadioButton(element) {
    
    [...element.parentElement.children].forEach(element => {
        element.classList.remove('active');
    });

    element.classList.add('active');
    element.querySelector('input').click();
}

setTimeout(() => {
    
    var inputs = document.querySelectorAll('input[type="radio"]');

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].checked) {inputs[i].parentElement.classList.add('active')}
    }

}, 100);

setTimeout(() => {
    
    var inputs = document.querySelectorAll('input[type="file"]');

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].files[0]  && inputs[i].parentElement.classList.contains('input-file-upload')) {
            inputs[i].nextElementSibling.nextElementSibling.innerText = inputs[i].files[0].name;
        }
    }

}, 100);

setTimeout(() => {
    
    var containers = document.querySelectorAll('.input-card');

    for (let i = 0; i < containers.length; i++) {
        
        var inputs = containers[i].querySelectorAll('input');
        
        // textarea
        if (inputs.length == 1) {
            containers[i].querySelector('textarea').innerText = containers[i].dataset.value;
            continue
        }


        // inputs
        var type = inputs[0].type;
        if (type == 'text' || type == 'password') {
            inputs[0].value = containers[i].dataset.value

            if (inputs[0].value.length > 0) {
                inputs[0].classList.add('notempty');
            }

        } else if (type == "radio") {
            
            for (let j = 0; j < inputs.length; j++) {
                
                if (inputs[j].value == containers[i].dataset.value) {
                    inputs[j].parentElement.click();
                }
                
            }

        }

    }

}, 10);