
// function getCookie(cname) {
//     let name = cname + "=";
//     let decodedCookie = decodeURIComponent(document.cookie);
//     let ca = decodedCookie.split(';');
//     for (let i = 0; i <ca.length; i++) {
//         let c = ca[i];
//         while (c.charAt(0) == ' ') {
//             c = c.substring(1);
//         }
//         if (c.indexOf(name) == 0) {
//             return c.substring(name.length, c.length);
//         }
//     }
//     return "";
// }

class DataCollector {
    constructor() {
        this.commands = [];
    }

    fetch(tablename, values, query) {
        this.commands.push(`tp=get&tbname=${tablename}&p=${values.join("<s>")}&qs=${query}`);
    }

    update(tablename, rowid, key, val) {
        this.commands.push(`tp=update&tbname=${tablename}&rowid=${rowid}&key=${key}&val=${val}`);
    }
    
    delete(tablename, id) {
        this.commands.push(`tp=delete&tbname=${tablename}&rid=${id}`);
    }

    create(tablename, para, values) {
        this.commands.push(`tp=create&tbname=${tablename}&p=${para.join("<s>")}&val=${values.join("<s>")}`);
    }

    flush() {
        this.commands = [];
    }


    commit(route) {
        var promises = [];
        for (let i = 0; i < this.commands.length; i++) {
            var command = `${route}?${this.commands[i]}`;
            promises.push(fetch(command));
        }
        this.awaiting = this.commands.length;
        this.commands = [];
        return promises;
    }

    last() {
        this.awaiting--
        if (this.awaiting <= 0) {
            return true
        }
        return false
    }

}

