## Earthquake UI

To use this app, download all .py files in the Earthquake UI folder. The os system call 
at the beginning of the Command_Line.py file is set to a specific path and may need to be
changed to fit that of the current user. 

Next steps: 
1. Launch Map Microservice as detailed below
2. Make sure all python packages are installed in your download location
3. Launch Command_Line.py through a terminal

The homepage of the app (as printed in text in the terminal window), will describe the app to the 
user and prompt them to take further steps. 

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
