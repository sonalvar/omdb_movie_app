from google.cloud import secretmanager


client = secretmanager.SecretManagerServiceClient()

def access_secret_version(project_id, secret_id, version_id):
    name = f"projects/{GCP_PROJECT_NO}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")


def get_secret(project_id, secret_id, version_id='latest'):
    return access_secret_version(project_id, secret_id, version_id)
