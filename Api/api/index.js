#!/usr/bin/env node

'use strict';

const general = require('./general.js');
const ruv = require('./ruv.js');
const rlcpd = require('./rlcpd.js');
const rips = require('./rips.js');

module.exports = app => {
    ruv(app, '/api/priv/ruv');
    rlcpd(app, '/api/priv/rlcpd'); 
    rips(app, '/api/priv/rips');
}