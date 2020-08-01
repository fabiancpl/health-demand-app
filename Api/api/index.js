#!/usr/bin/env node

'use strict';

const ruv = require('./ruv.js');
const rips = require('./rips.js');
const models = require('./models.js');

module.exports = app => {
    ruv(app, '/api/priv/ruv');
    rips(app, '/api/priv/rips');
    models(app, '/api/priv/models');
}