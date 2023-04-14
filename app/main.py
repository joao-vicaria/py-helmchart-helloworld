from flask import Response, Flask
import prometheus_client
from prometheus_client import Counter, Histogram
import time
import os


app = Flask(__name__)

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'Total processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Duration/s.', buckets=(1, 2, 5, 6, 10, _INF))


@app.route("/")
def hello():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    return "Hello from my PythonApp deployed with Helm!"
    end = time.time()
    graphs['h'].observe(end - start)

@app.route("/envvar")
def envvar():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    return os.environ['ENV_VAR_EXAMPLE']
    end = time.time()
    graphs['h'].observe(end - start)

@app.route("/readfile")
def readfile():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    with open("/config/configmap-test.yaml", "r") as f:
        content = f.read()
    return Response(content, mimetype='text/plain')
    end = time.time()
    graphs['h'].observe(end - start)

@app.route("/secretmanager")
def secretmanager():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    secret_detail = f"projects/cliq-vermiculus-int-01/secrets/teste/versions/1"
    response = client.access_secret_version(request={"name": secret_detail})
    data = response.payload.data.decode("UTF-8")
    print("Data: {}".format(data))
    return data
    end = time.time()
    graphs['h'].observe(end - start)

@app.route("/metrics")
def requests_count():
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")
#if __name__ == "__main__":
#    app.run(host='0.0.0.0')