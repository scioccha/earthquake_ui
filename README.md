## Map Microservice

To use the microservice, just run the command below to install all the dependencies.

```
npm install 

```

Then, run this command to start the server running. 

```
npm start

```

The project should then be running on port 5000 or whatever port you set in the .env file. 

To get a map, you just need to provide the latitude and longitude data to a url in the form 

"http://localhost:5000/microservice/map/{latitude}&{longitude}"

example:

"http://localhost:5000/microservice/map/50.25&35.00"