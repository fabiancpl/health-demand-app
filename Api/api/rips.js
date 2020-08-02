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
        db.query('select "Anno", "Mes", "CodigoDepartamento", "Departamento", "TipoAtencion", "PerteneceEtnia", "TieneDiscapacidad", "EsAdultoMayor", "Total" ' + 
                 'from vm_rips_agg_mesanno', null, (err, response) => {
            if (err) {
                console.error(err);
                res.status(500).send(err);
            } else {
                let rows = response.rows;
                response.rowCount > 0 ? res.json(rows) : res.status(204).send();
            }            
        })
    });
    app.route(ruta+"/usopromedio")
    .get((req, res) => {
        db.query('select categoria "Categoria", subcategoria "Subcategoria", anoatencion "AnnoAtencion", promedio "Promedio", error "Error" ' + 
                 'from vm_rips_agg_usopromedio', null, (err, response) => {
            if (err) {
                console.error(err);
                res.status(500).send(err);
            } else {
                let rows = response.rows;
                response.rowCount > 0 ? res.json(rows) : res.status(204).send();
            }            
        })
    });
    app.route(ruta+"/promediodeptos")
    .get((req, res) => {
        db.query('select coddptoatencion "CodigoDepartamento", departamentoatencion "Departamento", promedio "Promedio", promedioanno "PromedioAnno" ' + 
                 'from vm_rips_agg_promediodptos', null, (err, response) => {
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