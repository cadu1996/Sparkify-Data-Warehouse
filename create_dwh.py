import boto3
import json
import configparser
import time


def read_config(filename="dwh.cfg"):
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def create_aws_clients(config):
    key = config.get("AWS", "KEY")
    secret = config.get("AWS", "SECRET")

    ec2 = boto3.resource(
        "ec2",
        region_name="us-west-2",
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )
    iam = boto3.client(
        "iam",
        aws_access_key_id=key,
        aws_secret_access_key=secret,
        region_name="us-west-2",
    )
    redshift = boto3.client(
        "redshift",
        region_name="us-west-2",
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )

    return ec2, iam, redshift


def create_iam_role(iam, config):
    dwh_iam_role_name = config.get("DWH", "DWH_IAM_ROLE_NAME")

    try:
        print("Creating a new IAM Role")
        dwh_iam_role = iam.create_role(
            Path="/",
            RoleName=dwh_iam_role_name,
            Description="Allows Redshift clusters to call AWS services on your behalf.",
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Statement": [
                        {
                            "Action": "sts:AssumeRole",
                            "Effect": "Allow",
                            "Principal": {"Service": "redshift.amazonaws.com"},
                        }
                    ],
                    "Version": "2012-10-17",
                }
            ),
        )
    except Exception as e:
        print(e)

    return dwh_iam_role


def attach_iam_role_policy(iam, config):
    dwh_iam_role_name = config.get("DWH", "DWH_IAM_ROLE_NAME")
    print("Attaching Policy")
    iam.attach_role_policy(
        RoleName=dwh_iam_role_name,
        PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
    )["ResponseMetadata"]["HTTPStatusCode"]


def get_iam_role_arn(iam, config):
    dwh_iam_role_name = config.get("DWH", "DWH_IAM_ROLE_NAME")
    print("Get the IAM role ARN")
    dwh_iam_role_arn = iam.get_role(RoleName=dwh_iam_role_name)["Role"]["Arn"]
    print("Role ARN: ", dwh_iam_role_arn)
    return dwh_iam_role_arn


def create_redshift_cluster(redshift, iam_role_arn, config):
    dwh_cluster_type = config.get("DWH", "DWH_CLUSTER_TYPE")
    dwh_num_nodes = config.get("DWH", "DWH_NUM_NODES")
    dwh_node_type = config.get("DWH", "DWH_NODE_TYPE")
    dwh_cluster_identifier = config.get("DWH", "DWH_CLUSTER_IDENTIFIER")
    dwh_db = config.get("CLUSTER", "DWH_DB")
    dwh_db_user = config.get("CLUSTER", "DWH_DB_USER")
    dwh_db_password = config.get("CLUSTER", "DWH_DB_PASSWORD")

    try:
        print("Creating Redshift Cluster")
        response = redshift.create_cluster(
            ClusterType=dwh_cluster_type,
            NodeType=dwh_node_type,
            NumberOfNodes=int(dwh_num_nodes),
            DBName=dwh_db,
            ClusterIdentifier=dwh_cluster_identifier,
            MasterUsername=dwh_db_user,
            MasterUserPassword=dwh_db_password,
            IamRoles=[iam_role_arn],
        )
    except Exception as e:
        print(e)

    return response


def wait_for_cluster_availability(redshift, config):
    dwh_cluster_identifier = config.get("DWH", "DWH_CLUSTER_IDENTIFIER")
    print("Waiting for cluster to be available")

    cluster_properties = redshift.describe_clusters(
        ClusterIdentifier=dwh_cluster_identifier
    )["Clusters"][0]

    while cluster_properties["ClusterStatus"] != "available":
        cluster_properties = redshift.describe_clusters(
            ClusterIdentifier=dwh_cluster_identifier
        )["Clusters"][0]
        time.sleep(10)

    return cluster_properties


def open_tcp_port(ec2, cluster_properties, config):
    dwh_port = config.get("CLUSTER", "DWH_PORT")

    try:
        print("Open an incoming TCP port to access the cluster endpoint")
        vpc = ec2.Vpc(id=cluster_properties["VpcId"])
        default_sg = list(vpc.security_groups.all())[0]
        default_sg.authorize_ingress(
            GroupName=default_sg.group_name,
            CidrIp="0.0.0.0/0",
            IpProtocol="TCP",
            FromPort=int(dwh_port),
            ToPort=int(dwh_port),
        )
    except Exception as e:
        print(e)


def update_config(config, cluster_properties):
    config.set("CLUSTER", "DWH_HOST", cluster_properties["Endpoint"]["Address"])
    config.set("IAM_ROLE", "arn", cluster_properties["IamRoles"][0]["IamRoleArn"])


def save_config_to_file(config, filename="dwh.cfg"):
    with open(filename, "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    config = read_config()
    ec2, iam, redshift = create_aws_clients(config)

    iam_role = create_iam_role(iam, config)
    attach_iam_role_policy(iam, config)
    iam_role_arn = get_iam_role_arn(iam, config)

    create_redshift_cluster(redshift, iam_role_arn, config)
    cluster_properties = wait_for_cluster_availability(redshift, config)

    open_tcp_port(ec2, cluster_properties, config)

    update_config(config, cluster_properties)
    save_config_to_file(config)
