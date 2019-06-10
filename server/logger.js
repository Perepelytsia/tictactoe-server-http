var fs = require('fs');

module.exports = function (file, msg) {
    fs.writeFile('/var/log/nodejs/'+file+'.log', new Date() +' '+ msg, function (err) {
        if (err) throw err;
    });
};
