
class EditorHandler {
    constructor(editor, id) {
        this.id = id;
        this.editor = editor;
        this.filename = '';
    }

    openNew() {
        document.querySelector(`#editor-name-${this.id}`).value = '';
        this.editor.setContents({});
        this.filename = '';
    }

    open(filename) {

        this.filename = filename;
        var url = `/admin/editor/open/${this.id}?filename=${this.filename}`;

        fetch(url, {
            method: 'GET',
        }).then(resp=>{
            resp.json().then((json)=>{
                this.editor.setContents(json);
                document.querySelector(`#editor-name-${this.id}`).value = filename;
            })
        })

        this.editor.setContents();
    }

    save() {
        
        var input = document.querySelector(`#editor-name-${this.id}`);
        
        var url = `/admin/editor/save/${this.id}`;

        var filename = input.value;
        var data = {
            filename : filename,
            body : this.editor.getContents(),
        }

        fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify(data)
        }).then(resp=>{
            resp.json().then((json)=>{
                var element = document.querySelector(`#filebar-${this.id}`);
                element.innerHTML = element.children[0].outerHTML + json["html"];
                this.filename = json["filename"];
                this.open(json["filename"]);
            })
        })


    }

    delete() {
        confirm(`Er du sikker på du vil slette ${this.filename}?`, ()=>{

            var url = `/admin/editor/delete/${this.id}?filename=${this.filename}`;
            fetch(url, {
                method: 'GET',
            }).then(resp=>{
                window.location.reload();
            })

        }, ()=>{});
    }

    rename(input) {
        
        if (this.filename) {
            fetch(`/admin/editor/rename/${this.id}?old=${this.filename}&new=${input.value}`).then((resp)=>{
                resp.text().then((filename)=>{
                    input.value = filename;
                    this.filename = filename;
                })
            });
        }
    }
}

setTimeout(() => {
    [...document.querySelectorAll(".editor-filename")].forEach((element)=>{
        element.value = '';
    });
}, 10);