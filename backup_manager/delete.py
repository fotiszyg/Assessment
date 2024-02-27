from google.cloud.compute_v1 import SnapshotsClient, DeleteSnapshotRequest


def delete_snapshot(project, name):
    client = SnapshotsClient.from_service_account_json('xcc-fotis.json')
    request = DeleteSnapshotRequest(
        project=project,
        snapshot=name,
    )

    # Make the request
    client.delete(request=request)


if __name__ == '__main__':
    delete_snapshot('xcc-fotis', 'second-snapshot')
