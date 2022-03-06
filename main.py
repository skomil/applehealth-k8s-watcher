from time import sleep
from datetime import datetime
from os import path
import yaml
import argparse
from kubernetes import config, client


class Watcher():
    filepath = None;
    fileupdate = None;

    def __init__(self, filepath) -> None:
        super().__init__()
        self.filepath = filepath
        self.fileupdate = path.getmtime(self.filepath)

    def watch(self):
        while True:
            if self.fileupdate != path.getmtime(self.filepath):
                print("File has changed, starting health ingestion")
                self.fileupdate = path.getmtime(self.filepath)

                # Run Kubernetes task
                config.load_incluster_config()
                self.create_job()
            else:
                print("...Last Updated: {}".format(datetime.fromtimestamp(self.fileupdate)))
            sleep(300)

    def create_job(self):
        batch = client.BatchV1Api()

        # Delete job if it exists
        try:
            batch.delete_namespaced_job("health-importer-poll", "batch-jobs")
            print("deleted job... Waiting to create")
            sleep(30)
        except client.ApiException:
            print(" No job found, continuing...")

        # Create job from yaml
        with open(path.join(path.dirname(__file__), "health-importer-poll.yml")) as f:
            dep = yaml.safe_load(f)
            resp = batch.create_namespaced_job(
                body=dep, namespace="batch-jobs")
            print("Job created. status='%s'" % str(resp.status))


argparser = argparse.ArgumentParser()
argparser.add_argument("filepath", help="path where health zip has been added")

if __name__ == '__main__':
    args = argparser.parse_args()
    w = Watcher(args.filepath)
    w.watch()

