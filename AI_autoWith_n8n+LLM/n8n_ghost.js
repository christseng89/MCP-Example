const jwt = require('jsonwebtoken');

const key = '68ca96da4254690001aa6327:ad1d2fc7e222df8231bf27e5adf5c5b2879dfc28c014867d6a407b8ec62ea597';
const [id, secret] = key.split(':');

const token = jwt.sign({}, Buffer.from(secret, 'hex'), {
  keyid: id,
  algorithm: 'HS256',
  expiresIn: '5m',
  audience: '/admin/'
});

console.log(token);
