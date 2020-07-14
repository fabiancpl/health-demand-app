'use strict';

/** Módulos de ayuda */
const jwt = require('./jwt');
/**
 * Módulo con funciones útiles para la seguridad de la aplicación
 */
module.exports = {
    /** determina si una ruta debe usar seguirdad o no */
    usarSeguridad: usarSeguridad,
    /** crea un nuevo token de sesión */
    nuevaSesion: (usuario) => jwt.generaToken(usuario)
}

function usarSeguridad(app, ruta) {
    app.use(ruta, (req, res, next) => {
        // la validación de la sesión es en memoria
        // jwt descifra y valida un token
        const sessionId = req.get('sessionId');
        const sesion = jwt.verify(sessionId);
        console.log(sessionId, sesion);
        if (sesion) {
            req.usuario = sesion.email
            next()
        } else {
            res.status(401).send('Credencial inválida')
        }
    })
}