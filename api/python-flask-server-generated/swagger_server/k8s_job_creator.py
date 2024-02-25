from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import List, Optional, Union
from kubernetes.client.models.v1_job import V1Job
from kubernetes.client.models.v1_cron_job import V1CronJob

# TODO code clone
def create_kubernetes_job(job_name: str, command: List[str], image: str, schedule: Optional[str] = None) -> Union[V1Job, V1CronJob]:
    """
    Create a Kubernetes Job or CronJob to run a specific command in a Docker container.

    :param job_name: The name of the Kubernetes Job or CronJob.
    :type job_name: str
    :param command: The command to run in the container, provided as a list.
    :type command: List[str]
    :param image: The Docker image to use for the container.
    :type image: str
    :param schedule: The schedule in Cron format, used only if creating a CronJob. Defaults to None.
    :type schedule: Optional[str]
    :return: The created Kubernetes Job or CronJob object.
    :rtype: Union[V1Job, V1CronJob]
    """
     # Ensure command is a list of strings
    assert isinstance(command, List) and all(isinstance(elem, str) for elem in command), \
        "Command must be a list of strings"
    
    # Load the kubeconfig file from the default location or set up in-cluster config
    try:
        config.load_kube_config() # For local development
    except:
        config.load_incluster_config() # For use within a Kubernetes cluster

    # Define the Kubernetes API client
    api_instance = client.BatchV1Api()

    # Define the container to run
    container = client.V1Container(
        name=job_name,
        image=image,
        command=command
    )

    # Define the template for the job
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": job_name}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container])
    )

    if schedule:
        # Define the CronJob spec
        job_spec = client.V1JobSpec(template=template)
        cronjob_spec = client.V1CronJobSpec(
            schedule=schedule,
            job_template=client.V1beta1JobTemplateSpec(spec=job_spec)
        )
        job = client.V1CronJob(
            api_version="batch/v1",
            kind="CronJob",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=cronjob_spec
        )
        api_instance = client.BatchV1beta1Api()
        create_func = api_instance.create_namespaced_cron_job
    else:
        # Define the Job spec
        spec = client.V1JobSpec(template=template, backoff_limit=4)
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=spec
        )
        create_func = api_instance.create_namespaced_job

    # Create the Kubernetes Job
    api_response = create_func(
        body=job,
        namespace="default" 
    )
    return api_response