# Clothing_store_API
how to run:

```
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  python manage.py runserver
```

how to use minikube to deploy
This link show how you can download minikube and how to set up it: https://minikube.sigs.k8s.io/docs/start/
```
minikube start
minikube kubectl -- get po -A
alias kubectl="minikube kubectl --"
```
first we have to dockerize and push our code to dockerhub
```
docker build -t your-dockerhub-username/myproject:lastest .
docker login
docker push your-dockerhub-username/myproject:lastest
```

We start deploying it 
```
kubectl create deployment myporject --image=your-dockerhub-username/myproject:lastest
kubectl expose deployment myproject --type=NodePort --port=8080
minikube service myproject-service
```
