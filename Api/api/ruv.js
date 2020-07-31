'use strict';

const db = require('../database.js');
module.exports = (app, ruta) => {
    app.route(ruta)
    .get((req, res) => {
        db.query('select "IndMuestra", "GrupoEdad", "Sexo", "CodigoDepartamento", "Departamento", "EsAdultoMayor", "PerteneceEtnia", "Etnia", "TieneDiscapacidad", "Discapacidad", "Total" ' + 
                 'from vm_ruv_agg limit 100', null, (err, response) => {
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