from ploomber.clients.storage.abc import AbstractStorageClient


class MLflowStorageClient(AbstractStorageClient):
    def __init__(self, mlflow):
        self.mlflow = mlflow
        pass

    def download(self, local, destination=None):
        pass

    def upload(self, local):
        self.mlflow.log_artifact(str(local), local.parts[-2])

    def parent(self):
        """Parent where all products are stored"""
        pass

    def _download(self, local, destination):
        pass

    def _upload(self, local):
        pass

    def _is_file(self, remote):
        pass

    def _is_dir(self, remote):
        pass

    def _remote_path(self, local):
        pass

    def _remote_exists(self, local):
        pass

    def close(self):
        pass
