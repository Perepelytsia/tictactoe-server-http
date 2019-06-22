var fs = require('fs');

module.exports = function (file, msg) {
    fs.appendFile('/var/log/nodejs/'+file+'.log', new Date() +' '+ msg + "\n", function (err) {
        if (err) throw err;
    });
};
