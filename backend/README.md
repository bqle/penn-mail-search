# PMS Backend
Remember to create the .config files with correct MongoDB username and password in JSON format.<br>

## To run a WSGI server
```
$gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

## To run a development server
```
$pipenv shell
$python app.py
```