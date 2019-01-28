from flask import Flask, render_template
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
   
    return "hello kubernetes"

@app.route("/info")
def info():
   config.load_kube_config()
   v1 = client.CoreV1Api()
   print("Listing pods with their IPs:")
#   ret = v1.list_pod_for_all_namespaces(watch=False)
   ret = v1.list_namespaced_pod("default")
#   print("aks",type(ret))
   name =[]
#   ip  =[]
   for i in ret.items:
#      print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
       name.append(i.metadata.name)
#       ip.append(i.status.pod_ip)
   return render_template('index.html',name=name)
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=3300,debug='True')
#  main()
