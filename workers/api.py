import gear
import json
import sys
sys.path.append('../api')
from controllerBase import Controller

worker = gear.Worker('apiWorker')
worker.addServer(host='localhost', port=4730)
worker.registerFunction('api')

while True:
    job = worker.getJob()
    data = json.loads(job.arguments.decode('utf-8'))
    controller = Controller(data)
    data = controller.action();
    data = json.dumps(data)
    job.sendWorkComplete(bytes(data, 'utf8'))
