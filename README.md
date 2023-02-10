# Service reads data from websocket and stores it to files (data.json*)

# Data format:
```
{
 "component": "Realbridge Air Amplifier",
 "country": "Argentina",
 "description": "ut rerum ut quis nulla quasi quis est autem.",
 "model": "mh 80151"
 }
 ```
# Data in wrong format is not stored (warning is printed)

 # Data could be retrieved by http request:
 http://localhost:8000/messages
 # or with pagination
 http://localhost:8000/messages?offset=20&limit=10