var { Connection, Request } = require("tedious");
var Connection = require('tedious').Connection;

// Create connection to database
var config = {
  authentication: {
    options: {
      userName: "Nhan", // update me
      password: "Talonss5" // update me
    },
    type: "default"
  },
  server: "fiaa.database.windows.net", // update me
  options: {
    database: "fiaa", //update me
    encrypt: true
  }
};

var connection = new Connection(config);

// Attempt to connect and execute queries if connection goes through
connection.on("connect", err => {
  if (err) {
    console.error(err.message);
  } else {
    testnum = 0;
    testnum = queryDatabase1();
    console.log("variable = " + testnum);
    // InsertStatement();
  }
});

connection.connect();

// function queryDatabase() {
//   console.log("Reading rows from the Table...");

// }

function queryDatabase1() {
  console.log("Reading rows from the Table...");
  // Read all rows from table
  num = 0;   
  var request = new Request(
    `SELECT * FROM dbo.users AS U WHERE U.username = '${'Nhan'}'`,
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);
      }
      num = rowCount;
    }
  );
  request.on("row", columns => {
    columns.forEach(column => {
      console.log("%s\t%s", column.metadata.colName, column.value);
    });
  });

  connection.execSql(request);
  return num;
}

// function InsertStatement() {
//   request = new Request(`INSERT dbo.users (username, useremail, Userpassword) VALUES ('${'Brandon'}', '${'Brandon@gmail.com'}', '${'1234'}')`, function(err) {
//    if (err) {
//       console.log(err);} 
//   });
//   request.on('row', function(columns) {
//       columns.forEach(function(column) {
//         if (column.value === null) {
//           console.log('NULL');
//         } else {
//           console.log("Inserted " + column.value);
//         }
//       });
//   });     
//   connection.execSql(request);
// }
