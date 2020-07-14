'use strict';

const rlcpd = require('./rlcpd.js');

module.exports = app => {
    rlcpd(app, '/api/priv/rlcpd');
}