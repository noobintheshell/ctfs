// server.js

const initDb = require("./db").initDb;
const getDb = require("./db").getDb;
const express = require('express');
const app = express();
var bodyParser = require('body-parser')
app.use(bodyParser.json())

var path = require("path");

const PORT = 4000;

function sanitize(v) {
  if (v instanceof Object) {
    for (var key in v) {
      if (/^\$/.test(key)) {
        delete v[key];
      }
    }
  }
  return v;
};

initDb(function (err) {
    app.get('/', function(req, res) {
        res.sendFile(path.join(__dirname+'/index.html'));
    });  

    app.post('/login', function (req, res) {

        const db = getDb();
        c = db.db('test');
        
        var name = sanitize(req.body.username)
	var passwd = sanitize(req.body.password)   
        var query = {
            username: name,
            password: passwd
        }

        c.collection('users').findOne(query, function (err, user) {
            if(user == null) {
                res.send(JSON.stringify("Login Failed"))
            }
            else {
                resp = "Welcome: " + user['username'] + "!";
                res.send(JSON.stringify(resp));
            }
        });
    });
 
    app.listen(PORT, function (err) {
        const db = getDb();

        user = {username: 'bob', password: 'lVeYMg4U4$@L'}
        admin = {username: 'admin', password: '945IYMib!u@u'}

        c = db.db('test');
        c.collection('users').insertOne(user)
        c.collection('users').insertOne(admin)

        if (err) {
            throw err; //
        }
        console.log("Up and running on port " + PORT);
    });
});
