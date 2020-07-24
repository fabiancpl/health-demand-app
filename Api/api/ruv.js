'use strict';

const db = require('../database.js');
module.exports = (app, ruta) => {
    app.route(ruta)
    .get((req, res) => {
        db.query('select r.departamentoocurrencia as "Departamento", r.indadultomayor as "EsAdultoMayor", r.indetnia as "PerteneceEtnia", r.etnia as "Etnia", r.inddiscapacidad as "TieneDiscapacidad", r.tipoalteracion as "Discapacidad", sum(n) as "Total" ' + 
                 'from tb_ruv_agg r ' + 
                 'group by r.departamentoocurrencia, r.indadultomayor, r.indetnia, r.etnia, r.inddiscapacidad, r.tipoalteracion ' + 
                 'order by r.departamentoocurrencia, r.indadultomayor, r.indetnia, r.etnia, r.inddiscapacidad, r.tipoalteracion', null, (err, response) => {
            if (err) {
                console.error(err);
                res.status(500).send(err);
            } else {
                let rows = response.rows;
                response.rowCount > 0 ? res.json(rows) : res.status(204).send();
            }            
        })
    });
    app.route(ruta+"/sexo")
    .get((req, res) => {
        db.query('select sexo as "Sexo", count(1) as "Total" ' + 
                 'from tb_ruv_agg ' + 
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
        db.query('select coddepocur as "CodigoDepartamento", departamentoocurrencia as "Departamento", count(1) as "Total" ' + 
                 'from tb_ruv_agg ' + 
                 'group by coddepocur, departamentoocurrencia ' + 
                 'order by departamentoocurrencia', null, (err, response) => {
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