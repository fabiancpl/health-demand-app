'use strict';

/** librería de encriptado */
const jwt = require('jsonwebtoken')
const randtoken = require('rand-token')

const secreto = 'ds4a_team61'
var refreshTokens = {}

/** cifra el usuario durante un margen de tiempo */
exports.generaToken = (usuario) => {
    const refreshToken = randtoken.uid(256);
    refreshTokens[refreshToken] = usuario;
    const sesionId = jwt.sign(usuario, secreto, { expiresIn: 60 });
    return { sesionId: sesionId, refreshToken: refreshToken };
};

exports.generaSoloToken = (usuario) => {
    const sesionId = jwt.sign(usuario, secreto, { expiresIn: 60 });
    return { sesionId: sesionId };
};

/** verifica al usuario a partir del token  */
exports.verify = (token) => {
    try {
        return jwt.verify(token, secreto)
    }
    catch(err){
        return false;
    }
}

exports.decode = (sessionId) => {
    return jwt.decode(sessionId, secreto);
}