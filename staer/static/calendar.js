

const colors = [
    '#2a9d8f',
    '#2a9d8f',
    '#e9c46a',
    '#f4a261',
    '#e76f51',
    '#a2d2ff'
]

class Calender {
    #toolbarInnerHTML
    #monthTable = [
        'Januar',
        'Febuar',
        'Marts',
        'April',
        'Maj',
        'Juni',
        'Juli',
        'August',
        'September',
        'Oktober',
        'November',
        'December'
    ]

    constructor(qs, id) {
        this.id = id;
        this.#toolbarInnerHTML = `<div><button onclick="cal${this.id}.showToday()">Idag</button></div><div onclick="cal${this.id}.showMonth(cal${this.id}.currentYear,cal${this.id}.currentMonth-1)"><img src="https://icons.iconarchive.com/icons/icons8/ios7/512/Arrows-Back-icon.png"></div><div onclick="cal${this.id}.showMonth(cal${this.id}.currentYear,cal${this.id}.currentMonth+1)"><img src="https://icons.iconarchive.com/icons/icons8/ios7/512/Arrows-Forward-icon.png"></div><div><p>{}</p></div>`;
        this.times = [];
        this.qs = qs;

        this.element = document.querySelector(qs);
        this.element.classList.add('cal-wrapper')
        this.today = new Date();
        this.currentYear = this.today.getFullYear();
        this.currentMonth = this.today.getMonth();
        this.startWeek = undefined;
        this.endWeek = undefined;
        this.#createCalender();
        this.activeExtra;

        var calHeight = getComputedStyle(document.querySelector(qs)).height
        var cellHeight = Math.floor(parseInt(calHeight.replace('px','')) / 6);
        this.displayedEvents = Math.floor(cellHeight / 30);
    }

    #getDay(date) {
        // monday == 0
        // sunday == 6

        var day = date.getDay() - 1;
        if (day == -1) {
            day = 6
        }

        return day
    }

    #getWeek(date) {
        let firstDayOfYear = new Date(date.getFullYear(), 0, 1)
        let firstMonday = new Date(date.getFullYear(), 0, 7 - this.#getDay(firstDayOfYear) + 1);
        date = new Date(date.getFullYear(), date.getMonth(), date.getDate() - this.#getDay(date) + 3);
        var week = Math.min(Math.floor((date.getTime() - firstMonday.getTime()) / (1000 * 60 * 60 * 24 * 7)) + 1, 52)

        if (week == 0) {
            return 52
        }

        return week
    }


    #getEventsForDate(date) {
        var res = []
        for (let i = 0; i < this.times.length; i++) {
            let d = this.times[i];
            if (date - d.start >= 0 && d.end - date >= 0) {res.push(d);}
            else if (date.toDateString() == d.start.toDateString()) {res.push(d);}
            else if (date.toDateString() == d.end.toDateString()) {res.push(d);}

        }
        return res
    }


    #showDay(con, date) {
        
        if (this.activeExtra) {this.activeExtra.style.display = 'none';}
        this.activeExtra = con;

        date = new Date(...date.split('-'));
        con.innerHTML = '';

        var times = this.#getEventsForDate(date);
        for (let i = 0; i < times.length; i++) {
            const d = times[i];
            var div = document.createElement('div');
            div.style.backgroundColor = d.color
            div.innerHTML = `<p>${d.name} <span onclick="cal${this.id}.delete('${d.id}', '${d.name}')" class="material-symbols-outlined">delete</span> </p>`;
            con.appendChild(div)
            
        }
        
        con.style.display = 'flex';

    }


    #createCalender() {
        
        // clear cal
        this.element.innerHTML = '';

        // date variables
        let endOfMonth = new Date(this.today.getFullYear(), this.today.getMonth()+1, 0)
        let startOfMonth = new Date(this.today.getFullYear(), this.today.getMonth(), 1)
        let totalDaysInMonth = endOfMonth.getDate()
        let weeksInMonth = Math.ceil(totalDaysInMonth / 7)
        let currentDate = new Date();

        var firstDayOfMonth = startOfMonth.getDay() - 2;        
        var sneakWeek = startOfMonth.getDay() == 0; //when getDay == 0, a week is forgotten

        // create toolbar
        let toolbar = document.createElement('div');
        toolbar.innerHTML = this.#toolbarInnerHTML.replace('{}', this.#monthTable[this.today.getMonth()] + ' ' + this.today.getFullYear());
        toolbar.classList.add('cal-toolbar');
        this.element.appendChild(toolbar);

        // create week overhead
        let weekOverhead = document.createElement('div');
        weekOverhead.innerHTML = '<p><span>Mandag</span></p><p><span>Tirsdag</span></p><p><span>Onsdag</span></p><p><span>Torsdag</span></p><p><span>Fredag</span></p><p><span>Lørdag</span></p><p><span>Søndag</span></p>'
        weekOverhead.classList.add('cal-overhead');
        this.element.appendChild(weekOverhead);

        // calculate last displayed date
        if (new Date(this.today.getFullYear(), this.today.getMonth(), 7-firstDayOfMonth-1 + (weeksInMonth-1) * 7).getTime() < endOfMonth.getTime()) {
            weeksInMonth++
        }

        // create weeks
        var week, date, jsdate;
        for (let n = 0; n < weeksInMonth+sneakWeek; n++) {
            var i = n - sneakWeek

            week = document.createElement('div');
            week.dataset['weekNumber'] = this.#getWeek(new Date(this.today.getFullYear(), this.today.getMonth(), i*7 + 1));
            if (n == 0) {this.startWeek = parseInt(week.dataset['weekNumber']); this.endWeek = this.startWeek + parseInt(weeksInMonth)+sneakWeek - 1}
            week.classList.add('cal-week');
            
            // dates
            for (let j = -firstDayOfMonth; j < 7-firstDayOfMonth; j++) {
                
                date = document.createElement('div');
                date.classList.add('cal-date');

                date.onclick = (event) => {
                    const element = event.currentTarget;
                    this.#showDay(element.children[3], element.dataset.date);
                }

                jsdate = new Date(this.today.getFullYear(), this.today.getMonth(), j+i*7)
                if (jsdate.toDateString() == currentDate.toDateString()) {
                    date.classList.add('today')
                }

                if (jsdate.getMonth() != this.today.getMonth()) {
                    date.classList.add('notactive');
                }
                date.innerHTML = `<p class="cal-date-number">${jsdate.getDate()}</p><div class="cal-date-inner"></div><div class="cal-extra-events-container"></div> <div onclick="setTimeout(()=>{this.style.display = 'none'}, 10)" class="cal-date-show-extra"> </div> `;
                //date.onclick = event=>{this.openModal(event)};
                date.dataset.date = `${jsdate.getFullYear()}-${jsdate.getMonth()}-${jsdate.getDate()}`;

                week.appendChild(date)

            }
            
            this.element.appendChild(week);
        }

    }

    showMonth(year, month) {
        this.today = new Date(year, month, 1);
        this.currentYear = this.today.getFullYear();
        this.currentMonth = this.today.getMonth();
        this.#createCalender()

        this.times = [];
        fetch(`/admin/calendar/${this.id}/get?year=${this.currentYear}&month=${parseInt(this.currentMonth)}`).then(resp=>{
            resp.json().then((json)=>{
                for (let i = 0; i < json.length; i++) {
                    this.add(...json[i]);
                }
                this.showEvents();
            })
        });

    }

    showToday() {
        this.today = new Date();
        this.currentYear = this.today.getFullYear();
        this.currentMonth = this.today.getMonth();
        this.#createCalender();
        this.times = [];
        fetch(`/admin/calendar/${this.id}/get?year=${this.currentYear}&month=${parseInt(this.currentMonth)}`).then(resp=>{
            resp.json().then((json)=>{
                for (let i = 0; i < json.length; i++) {
                    this.add(...json[i]);
                }
                this.showEvents();
            })
        });
    }

    #connectDaysInWeek(week, date, days) {
        var week = document.querySelector(this.qs).querySelector(`.cal-week[data-week-number="${week}"]`);
        if (!week) {return}

        var time = document.createElement('div');
        time = document.createElement('div');
        time.classList.add('cal-date-time');
        time.style.width = `calc(${days*100}% - 10% + ${days}px)`;

        week.children[date].children[1].appendChild(time);

        time.dataset.span = days;
        time.dataset.pos = date;


        for (let i = date; i < date+days; i++) {
            const filler = document.createElement('div');
            filler.classList.add('cal-filler');
            week.children[i].children[1].appendChild(filler);
        }

        return time

    }


    #tetrisSort(week) {
        // order in html

        // algorithm:
        //  biggest first
        //  let each peace fall
        //  check caves

        const map = {}

        const fillMap = (e, n) => {
            for (let i = e.dataset.pos; i < parseInt(e.dataset.span) + parseInt(e.dataset.pos); i++) {
                map[parseInt(i) + n * 7] = e
            }
        }

        const checkMap = (e, n) => {
            for (let i = e.dataset.pos; i < parseInt(e.dataset.span) + parseInt(e.dataset.pos); i++) {
                if (map[parseInt(i) + n * 7]) return false
            }
            return true
        }
        
        // get all sizes
        var events = week.querySelectorAll('.cal-date-time');
        var inserted = [];
        events = [...events].sort((a,b) => b.dataset.span - a.dataset.span)
        
        // add back
        for (let j = 0; j < events.length; j++) {
         
            for (let i = 0; i < this.displayedEvents; i++) {
                if (checkMap(events[j], i)) {
                    fillMap(events[j], i);
                    inserted.push(events[j]);
                    break
                }
            }

        }
        
        // print map
        for (const key in map) {
            let row = Math.floor(key / 7);
            map[key].style.top = `calc(${row} * var(--time-height) + ${row} * var(--cal-event-gap))`;
        }

        // add hidden
        for (let j = 0; j < 7; j++) {
            var shown = 0;
            for (let i = 0; i < this.displayedEvents; i++) {
                if (map[7 * i + j]) {shown++}
            }
            week.children[j].dataset.shown = shown;
        }

        // inverse inserted
        for (let i = 0; i < events.length; i++) {
            if (inserted.indexOf(events[i]) == -1) {
                events[i].remove();
            }
        }

    }


    #addEventToHTML(id, start, end, name, color) {

        // rules in layout
        // antag at man har på 7 dage 
        // 7 * 3 pladser, altså 7 koloner og 3 rækker
        // hvor har man så plads til de forskellige

        //const cal = document.querySelector(this.qs);
        var startWeek = this.#getWeek(start);
        var endWeek = this.#getWeek(end);

        if (startWeek > this.endWeek) {return}
        if (endWeek < this.startWeek) {return}

        var time, day
        if (start.toDateString() == end.toDateString()) {
            time = this.#connectDaysInWeek(startWeek, this.#getDay(start), 1)
            time.dataset.id = id
            time.style.backgroundColor = color
            time.innerHTML = `<p> ${name} </p>`;

        } else if (startWeek == endWeek) {

            day = this.#getDay(end) - this.#getDay(start) + 1;
            time = this.#connectDaysInWeek(startWeek, this.#getDay(start), day);
            time.dataset.id = id
            time.style.backgroundColor = color;
            time.innerHTML = `<p> ${name} </p>`;

        } else {

            if (startWeek >= this.startWeek) {
                // add start
                day = this.#getDay(start);
                time = this.#connectDaysInWeek(startWeek, day, 7 - day);
                time.dataset.id = id
                time.innerHTML = `<p> ${name} </p>`;
                time.style.backgroundColor = color;
            }

            // add middle week
            for (let week = startWeek+1; week < endWeek; week++) {
                
                if (week > this.endWeek) {
                    return
                }
                if (week < this.startWeek) {
                    continue
                }


                time = this.#connectDaysInWeek(week, 0, 7);
                time.dataset.id = id
                time.innerHTML = `<p> ${name} </p>`;
                time.style.backgroundColor = color;
            }

            if (endWeek <= this.endWeek) {

                // add ending week
                day = this.#getDay(end);
                time = this.#connectDaysInWeek(endWeek, 0, day + 1);
                time.dataset.id = id
                time.innerHTML = `<p> ${name} </p>`;
                time.style.backgroundColor = color;
            }

        }

    }

    
    add(id, start, end, name, color) {
        if (!color) {
            color = colors[Math.floor(Math.random() * colors.length)];
        }

        start = new Date(...start.split('-'), 1);
        end = new Date(...end.split('-'), 1);

        this.times.push({start:start, end:end, name:name, color:color, id:id});
    }


    showEvents() {
        
        var cal = document.querySelector(this.qs);

        // clear all weeks
        var days = cal.querySelectorAll('.cal-date-inner');
        for (let i = 0; i < days.length; i++) {
            days[i].innerHTML = '';
        }
        

        // create html
        for (let i = 0; i < this.times.length; i++) {
            var e = this.times[i];
            this.#addEventToHTML(e.id,e.start, e.end, e.name, e.color);
        }

        // sort and assign top position
        for (let i = 2; i < cal.children.length; i++) {
            this.#tetrisSort(cal.children[i]);
        }

        // create extra places
        const dates = cal.querySelectorAll('.cal-date');
        for (let i = 0; i < dates.length; i++) {
            var children = dates[i].dataset.shown;
            var events =this.#getEventsForDate(new Date(...dates[i].dataset.date.split('-'))).length
            if (events > children) {
                dates[i].classList.add('extra-events');
            }
        }
        
        cal.style.setProperty('--cal-extra-top' ,this.displayedEvents);

    }

    delete(id, name) {
        confirm(`Vil du slette ${name} #${id}`, ()=>{
            fetch(`/admin/calendar/${this.id}/delete?timeid=${id}`).then(()=>{
                window.location.reload();
            })
        }, ()=>{
            console.log('abort');
        }) 

    }


}