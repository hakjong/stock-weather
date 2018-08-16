var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var mysql = require('mysql');

var indexRouter = require('./routes/index');

var app = express();

db = mysql.createConnection({
  host: "127.0.0.1",
  user: "root",
  password: "dbmaster",
  database: "stock_weather",
  port: 13306
});

db.connect(function(err) {
  if (err) throw err;
  console.log("DB connected");

  setInterval(function () {
      db.query('SELECT 1');
  }, 5000);
});

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
// app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);

module.exports = app;
