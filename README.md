# staer
stear is an full admin page using flask. The philosophy behind stear is creating a lightweight widget based frontend with small connection to the backend whatever backend is used. 

staer is written in python and uses the microframework flask

```python

app = flask.Flask()
admin = Admin(app, {
    "name": "My Admin Page"
    "logo": "route/to/image.png",
    "mainColor": "lightblue"
    "pages":[]
})

```