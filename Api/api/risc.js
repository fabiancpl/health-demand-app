'use strict';

const db = require('../database.js');
module.exports = (app, ruta) => {
    app.route(ruta)
    .get((req, res) => {
        res.json('../json/risc_gender.json')
    });
}