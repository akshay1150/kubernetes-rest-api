from flask import Flask, render_template, request
from werkzeug import secure_filename
import yaml
import json
import pandas as pd 
from kubernetes import client, config
app = Flask(__name__)

@app.route("/upload")
def index():
    return render_template('upload.html')

@app.route("/kuber",methods = ['GET',  'POST'])
def upload():
    config.load_kube_config()
    if request.method == 'POST':
        posted_file = str(request.files['file'].read())
        serv = yaml.safe_load(posted_file)
        k8s = client.CoreV1Api()
        resp1 = k8s.create_namespaced_service(body=serv,namespace="default")

        posted_file1 = str(request.files['file1'].read())
        dep = yaml.safe_load(posted_file1)
        k8s_beta = client.ExtensionsV1beta1Api()
        resp = k8s_beta.create_namespaced_deployment(body=dep, namespace="default")
 
    return render_template('cluster.html')
'''    with open("nginx-deployment.yaml") as f:
        dep = yaml.safe_load(f)
        k8s_beta = client.ExtensionsV1beta1Api()
        resp = k8s_beta.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % str(resp.status))
   
    return "hello kubernetes"'''

@app.route("/info")
def info():
   config.load_kube_config()
   v1 = client.CoreV1Api()
#   print("Listing pods with their IPs:")
#   ret = v1.list_pod_for_all_namespaces(watch=False)
   ret = v1.list_namespaced_pod("default")
#   print("aks",type(ret))
   name =[]
   ip  =[]
   namespace =[]
   status=[]
   for i in ret.items:
#      print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
       name.append(i.metadata.name)
       ip.append(i.status.pod_ip)
       namespace.append(i.metadata.namespace)
       status.append(i.status.phase)
     #  status.append(i.status.pod)
   list=pd.DataFrame({'name':name,'ip':ip,'namespace':namespace,'status':status})
#   print(type(ret))
   return render_template('index2.html',name=list.to_html()) 
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=3301,debug='True')

