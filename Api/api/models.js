'use strict';

const db = require('../database.js');
module.exports = (app, ruta) => {
    app.route(ruta + '/:page')
    .get((req, res) => {
        let page = req.params.page;
        let pageSize = 100000;
        let offset = ((page-1)*pageSize);
        db.query('select personaid "PersonaId", cerebro "Cerebro", diabetes "Diabetes", hipertension "hipertension", infarto "Infarto", mental "Mental", tumor "Tumor", sexo "Sexo", ' + 
                 'etnia "Etnia", inddiscapacidad "IndDiscapacidad", indadultomayor "IndAdultomayor", indetnia "IndEtnia", fechanacimiento "FechaNacimiento", hecho "Hecho",  ' + 
                 'trim(departamentoocurrencia) "DepartamentoOcurrencia", trim(muncipioocurrencia) "MuncipioOcurrencia", sujetodesc "SujetoDesc", probablemaneramuerteviolenta "ProbableManeraMuerteViolenta", ' +
                 'probablemaneramuerte "ProbableManeraMuerte", tipoalteracion "TipoAlteracion", origendiscapacidad "OrigenDiscapacidad", tiporegimen "TipoRegimen", edad "Edad", ' + 
                 'grupoedad "GrupoEdad", ciclovida "CicloVida", total "Total", consultas "Consultas", hospitalizaciones "Hospitalizaciones", procedimientos_de_salud "ProcedimientosDeSalud", ' + 
                 'urgencias "Urgencias", region "Region" ' + 
                 'from tb_modelos ' +
                 'where total <= 30 ' +
                 'order by random() ' + 
                 'offset ' + offset + ' limit ' +  pageSize, null, (err, response) => {
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