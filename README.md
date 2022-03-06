# applehealth-k8s-watcher

Watch for published changes of Apple Health uploaded files. If a file is changed, create a job that will import apple health data. When a file is changed, the script will generate a new Kubernetes batch job to process the data. The batch job can be found at [skomil/applehealth-importer](https://github.com/skomil/applehealth-importer) 

## Currently setup for local kubenetes cluster

This project is mainly based on personal needs. It can easily be improved to support any container and improved to better recognize status of completed jobs.

* Currently this job uses Docker images from a local docker image registry
* This is currently based on a job running at most once per hour.
