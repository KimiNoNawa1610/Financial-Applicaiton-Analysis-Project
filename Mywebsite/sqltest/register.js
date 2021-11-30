const { Connection, Request } = require("tedious");

// Create connection to database
const config = {
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

const connection = new Connection(config);

// Attempt to connect and execute queries if connection goes through
connection.on("connect", err => {
  if (err) {
    console.error(err.message);
  } else {
   
  queryDatabase();
    
  }
});

connection.connect();

function queryDatabase() {
  console.log("Reading rows from the Table...");

 let sql="INSERT INTO dbo.users
     ( [user]
     , [useremail]
     , [Userpassword]
     )
  VALUES
     ('myNewProduct'
     ,'hello'
     ,'NewColor'
      );
  con.query(sql, function (err, result) {
  if (err) throw err;
  console.log("1 record inserted");
  });

}


function PassCheck() {

    let password=document.getElementById('psw');
    let vpassword=document.getElementById('pswrepeat');

    if (password.value != vpassword.value)
    {
       
        document.getElementById("registerbtn").disabled=true;
    }
    else
    {
        document.getElementById("registerbtn").disabled = false;
    }

}






