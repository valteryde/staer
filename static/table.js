
class Table {
    constructor(qs, route, tablename, values, types, deleteable, edit) {
        this.qs = '#'+qs;
        this.types = types;
        this.data = new DataCollector();
        this.route = route;
        this.values = values;
        this.tbname = tablename

        this.deleteable = deleteable
        this.edit = edit;

        this.searchWord = '';

        this.changedKeys = {};

        setTimeout(() => {
            document.querySelector(this.qs).parentElement.nextElementSibling.onclick = () => {
                this.addEmptyRow();
            }
        }, 100);

    }

    reset() {
        document.querySelector(this.qs).parentElement.previousElementSibling.classList.remove('uncommited-changes');
        document.querySelector(this.qs).parentElement.nextElementSibling.style.display = 'block';

        var rows = document.querySelector(this.qs).querySelectorAll('tr');
        for (let i = 1; i < rows.length; i++) {
            rows[i].remove()
            
        }

        this.changedKeys = {}

    }

    addEmptyRow() {
        this.addRow('blank', Array(this.values.length).fill(''));
        var parent = document.querySelector(this.qs).querySelectorAll('#blank');
        parent = parent[parent.length-1];
        var total = parent.children.length
        if (this.deleteable) {total--}
        for (let i = 0; i < total; i++) {
            parent.children[i].classList.add('changed-content');
        }
        document.querySelector(this.qs).parentElement.nextElementSibling.style.display = 'none';
    }


    deleteRow(id) {
        this.data.delete(this.tbname, id);
        this.data.commit(this.route)[0].then(()=>{
            this.reset();
            this.fetch();
        })
    }

    handleKeyPress(event) {
        let id = event.currentTarget.parentElement.parentElement.id + '-' + event.currentTarget.parentElement.dataset.num;
        
        if (event.key == 'Enter') {
            this.update(event.currentTarget.parentElement.parentElement.id, event.currentTarget.parentElement.dataset.num);
        }

        // change border
        if (!this.changedKeys[id]) return
        if (this.changedKeys[id][0] == event.currentTarget.value) {
            event.currentTarget.parentElement.classList.remove('changed-content');
            delete this.changedKeys[id];
        } else {
            this.changedKeys[id][3] = event.currentTarget.value;
            event.currentTarget.parentElement.classList.add('changed-content');
        }

        var h1 = document.querySelector(this.qs).parentElement.previousElementSibling;
        if (Object.keys(this.changedKeys).length > 0) {
            h1.classList.add('uncommited-changes');
        } else {
            h1.classList.remove('uncommited-changes')
        }

    }

    update() {
        
        var blank = document.querySelector(this.qs).querySelector('#blank');
        if (blank) {
            var values = [];
            for (let i = 0; i < this.values.length; i++) {
                let element = this.changedKeys[`blank-${i}`];
                if (!element) {
                    values.push(null);
                } else {
                    values.push(this.changedKeys[`blank-${i}`][3]);
                    delete this.changedKeys[`blank-${i}`];
                }
            }
            this.data.create(this.tbname, this.values, values);
        }


        for (const key in this.changedKeys) {
            let e = this.changedKeys[key];
            this.data.update(this.tbname, e[2], this.values[e[1]], e[3]);
        }
        
        this.data.commit(this.route).forEach((e)=>{e.then((resp)=>{
            if (this.data.last()) {
                this.reset();
                this.fetch();
            }
            resp.text().then((text)=>{

            });
        })});
    }

    addRow(id, values) {
        let row = document.createElement('tr');
        row.id = id;
        for (let i = 0; i < values.length; i++) {
            let cell = document.createElement('td');
            if (this.edit) {
                                    
                // regular text
                var input = document.createElement('input');

                input.value = values[i];
                if (values[i]) {
                    input.style.width = Math.min(input.value.length, 50) + 'ch';
                } else {
                    input.style.width = '10ch';
                }

                input.onkeyup = event => {
                    event.currentTarget.style.width = (event.currentTarget.value.length) + 'ch';
                    this.handleKeyPress(event)
                };
                input.onkeydown = event => {
                    event.currentTarget.style.width = (event.currentTarget.value.length) + 'ch';
                    let id = event.currentTarget.parentElement.parentElement.id + '-' + event.currentTarget.parentElement.dataset.num;
                    if (this.changedKeys[id] === undefined) {
                        this.changedKeys[id] = [];
                        this.changedKeys[id][0] = event.currentTarget.value;
                        this.changedKeys[id][1] = event.currentTarget.parentElement.dataset.num;
                        this.changedKeys[id][2] = event.currentTarget.parentElement.parentElement.id;
                        this.changedKeys[id][3] = event.currentTarget.value;
                    }
                };

                // images
                if (this.types[i] == "img") {
                    var img = document.createElement('img')
                    img.src = values[i];
                    
                    input.classList.add('table-hidden')
                    if (values[i] == '') {
                        input.classList.remove('table-hidden');
                        img.classList.add('table-hidden');
                    }

                    img.onclick = event => {
                        event.currentTarget.nextElementSibling.classList.remove('table-hidden');
                        event.currentTarget.classList.add('table-hidden');
                        event.currentTarget.nextElementSibling.focus();
                    }
                    input.addEventListener('focusout', event => {
                        if (!event.currentTarget.parentElement.classList.contains('changed-content') && event.currentTarget.value != '') {
                            event.currentTarget.previousElementSibling.classList.remove('table-hidden');
                            event.currentTarget.classList.add('table-hidden');
                        }
                    });

                    cell.appendChild(img);

                } else if (this.types[i] == 'status') {

                    var icon = document.createElement('span')
                    icon.classList.add('material-symbols-outlined')

                    if (input.value == '0') {
                        icon.innerText = 'close';
                        icon.style.color = 'red';
                    } else if (input.value == '1') {
                        icon.innerText = 'done';
                        icon.style.color = 'green';
                    } else if (input.value == '2') {
                        icon.innerText = 'question_mark';
                        icon.style.color = 'orange';
                    }

                    input.classList.add('table-hidden')

                    icon.onclick = event => {
                        event.currentTarget.nextElementSibling.classList.remove('table-hidden');
                        event.currentTarget.classList.add('table-hidden');
                        event.currentTarget.nextElementSibling.focus();
                    }
                    input.addEventListener('focusout', event => {
                        if (!event.currentTarget.parentElement.classList.contains('changed-content') && event.currentTarget.value != '') {
                            event.currentTarget.previousElementSibling.classList.remove('table-hidden');
                            event.currentTarget.classList.add('table-hidden');
                        }
                    });

                    cell.appendChild(icon);

                }

                cell.appendChild(input)

                
            } else {
                cell.innerHTML = values[i];
            }
            cell.dataset.num = i;
            
            row.appendChild(cell)
        }

        if (this.deleteable) {
            let cell = document.createElement('td');
            let del = document.createElement('span');
            del.classList.add('material-symbols-outlined');
            del.classList.add('delete-bucket');
            del.innerText = 'delete';
            cell.style.position = 'relative';
            del.onclick = event=>{this.deleteRow(event.currentTarget.parentElement.parentElement.id)}
            cell.appendChild(del);
            row.appendChild(cell);
        }

        document.querySelector(this.qs).children[0].appendChild(row);
    }

    clear() {
        var tb = document.querySelector(this.qs);
        var tr = tb.querySelectorAll('tr:not(:first-of-type)');
        tr.forEach(element => {
            element.remove();
        });
    }

    fetch(query) {
        this.data.fetch(this.tbname, this.values, query);
        this.data.commit(this.route)[0].then(resp => {
            resp.json().then(json=>{
                this.clear();
                for (let i = 0; i < json.length; i++) {
                    this.addRow(json[i][0],json[i].slice(1))
                }

            })
        })
    }



}

