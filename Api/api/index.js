'use strict';

const rlcpd = require('./rlcpd.js');
const rips = require('./rips.js');

module.exports = app => {
    rlcpd(app, '/api/priv/rlcpd');
    rips(app, '/api/priv/rips');
}