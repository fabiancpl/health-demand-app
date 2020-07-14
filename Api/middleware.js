'use strict';

module.exports.useMiddleware = app => {
    const cors = require('cors');
    const bodyParser = require('body-parser');
    //const seguridad = require('./seguridad/seguridad.js');
    
    app.use(cors());

    app.use(bodyParser.urlencoded({
        extended: true
    }));
    app.use(bodyParser.json());

    app.use((req, res, next) =>{
        console.log(`recibida petición: ${req.url}`);
        next();
    });
    //seguridad.usarSeguridad(app, '/api/priv/');
}