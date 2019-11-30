const fs = require('fs');

module.exports.writeFn = function (lines) {

  const stream = fs.createWriteStream('./texts.txt', {
    flags: 'a'
  });

  lines.forEach(l => {
    stream.write(`${l}\n`);
  });

  stream.end();
}
