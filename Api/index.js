'use strict';

const express = require('express');
const app = express();

app.set('port', (process.env.PORT || 3000));

const middleware = require('./middleware');
middleware.useMiddleware(app);
require('./api/index')(app);

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});