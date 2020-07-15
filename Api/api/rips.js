'use strict';

const db = require('../database.js');
module.exports = (app, ruta) => {
    app.route(ruta+"/sexo")
    .get((req, res) => {
        db.query('select sexo as "Sexo", count(1) as "Total" ' + 
                 'from tb_rips ' + 
                 'where sexo <> \'NULL\' ' + 
                 'group by sexo ' + 
                 'order by sexo', null, (err, response) => {
            if (err) {
                console.error(err);
                res.status(500).send(err);
            } else {
                let rows = response.rows;
                response.rowCount > 0 ? res.json(rows) : res.status(204).send();
            }            
        })
    });
    app.route(ruta+"/departamentos")
    .get((req, res) => {
        db.query('select dptoatencion as "Departamento", count(1) as "Total" ' + 
                 'from tb_rips ' + 
                 'group by dptoatencion ' + 
                 'order by dptoatencion', null, (err, response) => {
            if (err) {
                console.error(err);
                res.status(500).send(err);
            } else {
                let rows = response.rows;
                response.rowCount > 0 ? res.json(rows) : res.status(204).send();
            }            
        })
    });
}