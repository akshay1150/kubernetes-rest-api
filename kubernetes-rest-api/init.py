from flask import Flask
import yaml
from kubernetes import client, config
app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

#if __name__ == "__main__":
#  app.run(port=3330)

#from kubernetes import client, config

#app = Flask(__name__)
@app.route("/enter")
def main():
    config.load_kube_config()
 
    with open("service.yaml") as f1:
        serv = yaml.safe_load(f1)
        k8s = client.CoreV1Api()
        resp1 = k8s.create_namespaced_service(
            body=serv, namespace="default")


    with open("nginx-deployment.yaml") as f:
        dep = yaml.safe_load(f)
        k8s_beta = client.ExtensionsV1beta1Api()
        resp = k8s_beta.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % str(resp.status))
       

#if __name__ == '__main__':
#   main()
if __name__ == '__main__':
#  main()
  app.run(port=3300)
#  main()
