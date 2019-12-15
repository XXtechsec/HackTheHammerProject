var crypto = require('crypto');
const {encode, decode} = require("base64-arraybuffer")
const atob = require("atob")

// console.log(process.argv)

pub = atob(process.argv[2])
sig = process.argv[3] // b64 encoded sig
txt = process.argv[4] // b64 encoded challenge

var verify = crypto.createVerify('sha256');
verify.update(new Uint8Array(decode(txt)));
console.log(verify.verify(pub, new Uint8Array(decode(sig))));
