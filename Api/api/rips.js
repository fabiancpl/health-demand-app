'use strict';

const db = require('../database.js');
module.exports = (app, ruta) => {
    app.route(ruta)
    .get((req, res) => {
        db.query('select "Sexo", "CodigoDepartamento", "Departamento", "TipoAtencion", "CapituloDX", "EsAdultoMayor", "PerteneceEtnia", "Etnia", "TieneDiscapacidad", "Discapacidad", "Total" ' + 
                 'from vm_rips_agg', null, (err, response) => {
            if (err) {
                console.error(err);
                res.status(500).send(err);
            } else {
                let rows = response.rows;
                response.rowCount > 0 ? res.json(rows) : res.status(204).send();
            }            
        })
    });
    app.route(ruta+"/annomes")
    .get((req, res) => {
        db.query('select r.anoatencion as "Anno", r.mesatencion as "Mes", trim(r.coddptoatencion) as "CodigoDepartamento", trim(r.departamentoatencion) as "Departamento", r.tipoatencion as "TipoAtencion", sum(n) as "Total" ' + 
                 'from tb_rips_agg_mesanno r ' + 
                 'where coddptoatencion not in (\'00\',\'NA\') ' + 
                 'group by r.anoatencion, r.mesatencion, r.coddptoatencion, r.departamentoatencion, r.tipoatencion ' + 
                 'order by r.anoatencion, r.mesatencion, r.coddptoatencion, r.departamentoatencion, r.tipoatencion', null, (err, response) => {
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