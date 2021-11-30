// const { Connection, Request } = require("tedious");

// // Create connection to database
// const config = {
//   authentication: {
//     options: {
//       userName: "Nhan", // update me
//       password: "Talonss5" // update me
//     },
//     type: "default"
//   },
//   server: "fiaa.database.windows.net", // update me
//   options: {
//     database: "fiaa", //update me
//     encrypt: true
//   }
// };

// const connection = new Connection(config);

// // Attempt to connect and execute queries if connection goes through
// // connection.on("connect", err => {
// //   if (err) {
// //     console.error(err.message);
// //   } else {
// //     queryDatabase();
// //   }
// // });

// connection.connect();

//Connect to database

const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "user" && password === "pass") { //change this to check database
        alert("You have successfully logged in.");
        location.reload();
    } else {
        loginErrorMsg.style.opacity = 1;
    }
    // if (queryDatabaseNames(username,password) = 1) { //change this to check database
    //     alert("You have successfully logged in.");
    //     location.reload();
    // } else {
    //     loginErrorMsg.style.opacity = 1;
    // }
})

function queryDatabaseNames(username, password){
    const request = new Request('SELECT * FROM [USERPASS] WHERE USER = ' + username 
    + ' AND PASS =' + password + '', (err, rowCount) => {
        if(err){
            console.error(err.message);
        } else {
            return rowCount;
        }
    }
    );
    
    connection.execSql(request);
}
