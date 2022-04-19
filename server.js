// load the things we need
var express = require('express');
var app = express();
const bodyParser = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page 
app.get('/', function (req, res) {

    res.render('pages/index', {
    });
});

// trips page 
app.get('/trips', function (req, res) {

    res.render('pages/trips', {
    });
});

// destinations page 
app.get('/destinations', function (req, res) {

    res.render('pages/destinations', {
    });
});


app.listen(8080);
console.log('8080 is the magic port');