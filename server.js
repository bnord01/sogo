'use strict';

var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.json());

app.use(express.static(__dirname + '/dist'));

var port = process.env.PORT || 3003;
var ready = new Promise(function willListen(resolve, reject) {
    app.listen(port, function didListen(err) {
        if (err) {
            reject(err);
            return;
        }
        console.log('app.listen on http://localhost:%d', port);
        resolve();
    });
});

exports.ready = ready;
exports.app = app;
