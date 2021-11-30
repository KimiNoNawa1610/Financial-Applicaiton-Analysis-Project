var connection =require('tedious').Connection;

var config ={
    server : "your_server.database.windows.net",
    options:{},
    authentication :{
        type: "default",
        options:{
            userName:"Nahn",
            password:"Talonss5",
        }
    }
};

var connection = new Connection(config);

// Setup event handler when the connection is established. 
connection.on('connect', function(err) {
    if(err) {
        console.log('Error: ', err)
    }
    // If no error, then good to go...
    console.log('we are good')
    executeStatement();
    });

// Initialize the connection.
connection.connect();