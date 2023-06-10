# Service reads data from websocket and stores it into files (data.json*) or to database

Data format:
```
{
 "component": "Realbridge Air Amplifier",
 "country": "Argentina",
 "description": "ut rerum ut quis nulla quasi quis est autem.",
 "model": "mh 80151"
 }
 ```
Data in wrong format is not stored (warning is printed).<p>

Storage can be chosen via environment variable STORAGE (FILE and DB values are possible).<p>

To run application start main.py file or use docker-compose. In case of DB storage run init_db.py file before.

Data could be retrieved by http request. Different URI are used for different storages.<p>
In FILE case:<p> 
http://localhost:8000/messages_file <p>
 or with pagination<p>
 http://localhost:8000/messages_file?offset=20&limit=10

In DB case:<p> 
http://localhost:8000/messages_db <p>
 or with pagination<p>
 http://localhost:8000/messages_db?offset=20&limit=10