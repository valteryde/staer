
function openFilePreview(url, element) {
    element = element.parentElement;
    if (url.indexOf('.') == -1) {
        fetch(url).then(resp=>{
            resp.text().then(res=>{
                element.innerHTML = res
            })
        })
    } else {
        window.open(url)
    }
}

class FilePreview {
    constructor(id) {
        this.id = id;
        this.status = 'open';
        this.folder = undefined;

        // check size
        setTimeout(()=>{
            const con = document.querySelector('#file-'+this.id);
            const holder = con.querySelector('.folder-wrapper');

            var width = parseInt(getComputedStyle(con).width)
            console.log(width)
            if (width > 600) {} else if (width > 500) {
                holder.style.gridTemplateColumns = 'repeat(4, 1fr)';
            } else if (width > 350) {
                holder.style.gridTemplateColumns = 'repeat(3, 1fr)';
            } else if (width > 200) {
                holder.style.gridTemplateColumns = 'repeat(2, 1fr)';
            }

        }, 10);

    }


    resetIcons() {
        var spans = document.querySelector('#file-'+this.id).querySelectorAll('span.material-symbols-outlined');
        for (let i = 0; i < spans.length; i++) {
            spans[i].classList.remove('active');
        }
    }


    mode(t, element) {
        this.status = t;
        this.resetIcons()
        element.classList.add('active');
        element.style.background = element.dataset.color;
    }

    goToParent(element) {
        
        if (this.folder === undefined) {
            return
        }
        var allFolders = this.folder.split('/');
        var otherFolders = allFolders[2].split('-');
        var rootFolder = allFolders[1].split('-');

        var folders = otherFolders.slice(0,otherFolders.length-1).join('-');
        var path = `/${rootFolder}/${folders}`
        openFilePreview(path, element.parentElement.nextElementSibling.children[0])
        this.folder = path;
    }

    click(file, element) {
        if (file.indexOf('.') == -1) {this.folder = file;}
        if (this.status == "open") {
            openFilePreview(file, element)
        } else if (this.status == "copy") {
            var text = file.replaceAll('-', '/');
            navigator.clipboard.writeText(text);
            alert(`Kopirede ${text}`);

        } else if (this.status == "del") {
            
            confirm(`Vil du slette ${file}?`, ()=>{
                fetch(file + '?delete=1').then(()=>{
                    window.location.reload()
                })
            }, ()=>{

            })

        } else if (this.status == "download") {
            if (file.indexOf('.') > -1) {
                openFilePreview(file + '?download=1', element);
            } else {
                openFilePreview(file, element);
            }
        }
    }

    upload(form) {
        this.resetIcons();
        this.status = 'open';
        form.children[0].click();
    }

    setPath(input) {
        if (this.folder) {
            input.value = this.folder;
        } else {
            input.value = '';
        }
    }


}