import boto3
import json
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read("dwh.cfg")
    return config

def init_aws_clients(config):
    key = config.get("AWS", "KEY")
    secret = config.get("AWS", "SECRET")

    iam = boto3.client("iam", aws_access_key_id=key, aws_secret_access_key=secret)
    redshift = boto3.client(
        "redshift",
        region_name="us-west-2",
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )
    return iam, redshift

def delete_cluster(redshift, cluster_identifier):
    print("Deleting cluster")
    redshift.delete_cluster(
        ClusterIdentifier=cluster_identifier, SkipFinalClusterSnapshot=True
    )

def wait_for_cluster_deletion(redshift, cluster_identifier):
    print("Waiting for cluster to be deleted")
    while True:
        try:
            cluster_properties = redshift.describe_clusters(
                ClusterIdentifier=cluster_identifier
            )["Clusters"][0]
            if cluster_properties["ClusterStatus"] == "deleted":
                print("Cluster deleted")
                break
        except:
            print("Cluster not found")
            break

def delete_role(iam, role_name):
    print("Deleting role")
    iam.detach_role_policy(
        RoleName=role_name,
        PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
    )
    iam.delete_role(RoleName=role_name)

if __name__ == "__main__":
    config = load_config()

    dwh_cluster_identifier = config.get("DWH", "DWH_CLUSTER_IDENTIFIER")
    dwh_iam_role_name = config.get("DWH", "DWH_IAM_ROLE_NAME")

    iam, redshift = init_aws_clients(config)

    delete_cluster(redshift, dwh_cluster_identifier)
    wait_for_cluster_deletion(redshift, dwh_cluster_identifier)
    delete_role(iam, dwh_iam_role_name)

