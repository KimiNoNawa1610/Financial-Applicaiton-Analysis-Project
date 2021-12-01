const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    alert("button pressed");

    // if (username === "user" && password === "pass") { //change this to check database
    //     console.log("Test1");
    //     // alert("You have successfully logged in.");
    //     alert("Test Worked");
    //     location.reload();
    // } else {
    //     loginErrorMsg.style.opacity = 1;
    // }
    
    check = queryDatabaseNames(username, password);

    if (check = 1) { //change this to check database
        alert("Query work");
        alert("You have successfully logged in.");
        location.reload();
    }
     else {
         alert("Issue Happened")
        loginErrorMsg.style.opacity = 1;
    }
})

var { Connection, Request } = require("tedious");

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
    console.log(err.message);
  } else {
    queryDatabase();
  }
});

connection.connect();



function queryDatabase() {
  console.log("Reading rows from the Table...");
}

function queryDatabaseNames(username, password){
    alert("test1");
    var request = new Request(
        `SELECT * FROM dbo.users WHERE username = '${username}' AND Userpassword = '${password}'`,
        (err, rowCount) => {
          if (err) {
            console.error(err.message);
          } else {
              alert("Test2")
            console.log(`${rowCount} row(s) returned`);
            return rowCount;
          }
        }
      );
    
      request.on("row", columns => {
        columns.forEach(column => {
          console.log("%s\t%s", column.metadata.colName, column.value);
        });
      });
      
      connection.execSql(request);
}

