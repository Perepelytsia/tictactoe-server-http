const http = require('http');
const gearman = require('gearman');
let logger  = require('./logger');
const hostname = 'localhost';
const port = 3000;
let client = gearman("localhost", 4730 , {timeout: 3000});

http.createServer((req, res) => {
    if (req.method == 'POST') {

        var data = '';

        req.on('data', function(chunk) {
            data += chunk.toString();
        });

        req.on('end', function() {
            // connect to the gearman server
            client.connect(function() {
                client.submitJob('api', data);
		logger('info', 'Request ' + data);
            })
        });

        // handle finished jobs
        client.on('WORK_COMPLETE', function(job) {
            client.close();
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            res.write(job.payload.toString())
            res.end();
	    logger('info', 'Response ' + job.payload.toString());
        })

        // handle timeout 
        client.on('timeout', function() {
            client.close()
	    let timeout = 'timeout error';
            res.statusCode = 408;
            res.write(timeout);
            res.end();
	    logger('error', timeout);
        })
    } else {
	let er = 'Not implemented';
        res.statusCode = 501;
        res.write(er)
        res.end();
	logger('error', er);
    }

}).listen(port, hostname, (err) => {

    if (err) {
	logger('error', err);
        return console.log(err)
    }
    console.log(`Server running at http://${hostname}:${port}/`);

});
