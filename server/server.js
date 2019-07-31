const http = require('http');
const gearman = require('gearman');
let logger  = require('./logger');
const hostname = 'localhost';
const port = 3000;
let client = gearman("localhost", 4730 , {timeout: 3000});

http.createServer((req, res) => {

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS'); // If needed
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    if (req.method == 'POST') {

        console.log("*****START*****");
        console.log("-----REQ-------");
        console.log(req.headers);
        
        var data = '';

        req.on('data', function(chunk) {
            data += chunk.toString();
        });

        req.on('end', function() {
            // connect to the gearman server
            client.connect(function() {
                client.submitJob('api', data);
                console.log(data);
                logger('info', 'Request ' + data);
            })
        });

        // handle finished jobs
        client.on('WORK_COMPLETE', function(job) {
            client.close();
            res.statusCode = 200;
            //res.setHeader('Content-Type', 'application/json');
            //res.write(job.payload.toString())
            //res.end();
            console.log("-----RES-------");
            console.log(res.getHeaders());
            console.log(job.payload.toString());
            console.log("*****FINISH*****");
            logger('info', 'Response ' + job.payload.toString());
            res.end(job.payload.toString())
        })

        // handle timeout 
        client.on('timeout', function() {
            client.close()
            let timeout = 'timeout error';
            res.statusCode = 408;
            res.end(timeout);
            logger('error', timeout);
        })

    } else if (req.method == 'OPTIONS') {

             // If needed
            //res.setHeader('Access-Control-Allow-Credentials', true); // If needed
            res.end('cors problem fixed');

    } else {
        console.log(req.headers);
        console.log(req.method);
        let er = 'Not implemented';
        res.statusCode = 501;
        res.end(er);
        logger('error', er);
    }

}).listen(port, hostname, (err) => {

    if (err) {
	    logger('error', err);
        return console.log(err)
    }
    console.log(`Server running at http://${hostname}:${port}/`);

}).on('error', (err) => {

    logger('error', err);
    console.log("+++++++++START ERROR+++++++")
    console.log(err)
    console.log("+++++++++END ERROR+++++++")

});
