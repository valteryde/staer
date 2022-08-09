# staer
stear is an full admin page using flask. The philosophy behind stear is creating a lightweight widget based frontend with small connection to the backend whatever backend is used. 

staer is written in python and uses the microframework flask

To start create the admin class
```python

app = flask.Flask()
admin = Admin(app, {
    "name": "My Admin Page"
    "logo": "route/to/image.png",
    "mainColor": "lightblue"
    "pages":[]
})

```
"pages" is where pages can be setup and customized.

To create a page simply insert an object e. g.
```python
{
    "name": "name_of_page",
    "icon": "google_icon",
    "body": [
        LineChart("Økonomi", apichartline, size=(2,2)),
        PieChart("Markedsaktie", apichartpie, size=(1,1)),
        Input(lambda: 10, lambda:'', 'Input','test-text', 'Tekstfelt'),
        Text('Hello', 'The world is cool')
    ]
}
```

Theese widgets is avaliable
```python
Calendar(title, get, delete, size:tuple=(2,3))
LineChart(title, cb, size:tuple=(2,2))
PieChart(title, cb, size=(1,1))
Editor(folder, title, showFiles:bool=True, size:tuple=(3,1))
FileExplorer(folder:str, handler:any=None, deletable:bool=False, size:tuple=(2,2))
Form(title, *elements, size:tuple=(1,2), api:str or function='')
Input(get, update, title, name, placeholder, hidden:bool=False)
RadioButtons(get, update, title, name, options)
Textarea(get, update, title, name, placeholder)
FileUpload(update, title, name)
```

All inputs can be used in forms by accesing them in Form.Input e. g. 

```python
Form('A title', Form.Input(), Form.TextArea())
```

There is also an IPLogger included. Use the `IPLogger` class. 