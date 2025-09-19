require('dotenv').config();
const jwt = require('jsonwebtoken');

const key = process.env.GHOST_ADMIN_KEY;
if (!key) {
  throw new Error("Missing GHOST_ADMIN_KEY in .env");
}

const [id, secret] = key.split(':');

const token = jwt.sign({}, Buffer.from(secret, 'hex'), {
  keyid: id,
  algorithm: 'HS256',
  expiresIn: '60m',
  audience: '/admin/'
});

console.log(token);
