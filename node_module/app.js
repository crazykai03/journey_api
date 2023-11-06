var express = require('express');
const fs = require('fs');
const path = require('path')
const bp = require('body-parser')
var dataroute = require('./route/route_data');
var conf = require('./route/conf');
var app = express();
var cors = require('cors'); 

app.use(cors());

app.use(bp.json())
app.use(bp.urlencoded({ extended: true }))

app.use('/', dataroute);

app.listen(conf.port, function () {
    console.log('app listening on port ' + conf.port + '!');
});
