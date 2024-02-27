# microk8s kubectl get svc,pods
# curl -X POST http://127.0.0.1:30000/smartsawhuman/kb-indexer/1.0.0/jobs -H "Content-Type: application/json" -d '{"command":"sleep 60"}'
# 
RELEASE_NAME := kms-generic
NAMESPACE := default
HELM_CHART_PACKAGE := ./dev_deployment/kms-generic-helm-charts-0.1.1.tgz
VALUES_FILE := ./dev_deployment/test-values.yml
FLASK_DOCKER := python-flask-server-local
CONFIG_FILES := ./dev_deployment/flask-deployment.yml ./dev_deployment/mongodb-deployment.yml 
# ./dev_deployment/dashboard-deployment.yml

# Kubernetes test env setup rule
k8: flask-docker start-microk8s save-and-import-flask-image apply-configs prometheus
	@echo "Deployment completed successfully."

# Start MicroK8s and ensure it's ready
start-microk8s:
# Check if the Kubernetes cluster is accessible
	@kubectl cluster-info > /dev/null 2>&1 || (echo "Kubernetes cluster is not accessible"; \
		echo "Attempting to start MicroK8s cluster..."; \
		sudo microk8s start; \
		sudo microk8s status --wait-ready; \
		echo "MicroK8s cluster started successfully."; \
		echo "Configuring kubectl to use MicroK8s..."; \
		sudo microk8s config > ~/.kube/config; \
		echo "kubectl is now configured to use MicroK8s."; \
	)

# Apply Kubernetes configurations
apply-configs:
	@echo "Applying Kubernetes configurations..."
	$(foreach file,$(CONFIG_FILES),kubectl apply -f $(file) --namespace $(NAMESPACE);)

prometheus:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update
	kubectl create namespace monitoring
	helm install prometheus prometheus-community/prometheus --namespace monitoring

# Build the Flask Docker image
flask-docker: 
	@echo "Building Flask Docker image..."
	cd api/python-flask-server-generated && \
	docker build -t $(FLASK_DOCKER) .

# Save the Flask Docker image to a tarball
save-and-import-flask-image:
	@echo "Saving Flask Docker image to tarball and importing into MicroK8s"
	docker save $(FLASK_DOCKER) > $(FLASK_DOCKER).tar
	microk8s ctr image import $(FLASK_DOCKER).tar
	@echo "Verifying that the Flask Docker image is present in MicroK8s..."
	@microk8s ctr image list | grep $(FLASK_DOCKER) || (echo "Image not found in MicroK8s" && exit 1)


tree: 
	tree -I 'indexers|__pycache__'
