"""
Utils to create lambda functions.
"""
import inspect
import uuid
import boto3

from .packaging import package_with_dependencies
from .config import AWS_ROLE_ARN, AWS_REGION, LAMBDA_UPDATE, VPC_CONFIG

lambdacli = boto3.client('lambda', region_name=AWS_REGION)


def uuid_str():
    """ Generate an unique id."""
    return str(uuid.uuid4())


def new_lambda(klass, handler):

    """
    Packages all files that the function *handler* depends on into a zip.
    Creates a new lambda with name *name* on AWS using that zip.
    This one does not have VPC config. So it has access to extern services
    such as SNS and SQS. (But can't connect directly to Redis)
    """

    klass_path = inspect.getfile(klass)
    module = inspect.getmodulename(klass_path)
    # zip function-module and dependencies
    zipfile, lamhand = package_with_dependencies(handler,
                                                 extra_modules=[klass_path])

    # create the new lambda by uploading the zip.
    try:
        response = lambdacli.create_function(
            FunctionName=handler.__name__,
            Runtime='python3.6',
            Role=AWS_ROLE_ARN,
            Handler=lamhand,
            Code={'ZipFile': zipfile.getvalue()},
            Publish=True,
            Description='Lambda included in the Workflow.',
            Timeout=45,
            MemorySize=3008,
            #VpcConfig=VPC_CONFIG,
            # DeadLetterConfig={
            #     'TargetArn': 'string'
            # },
             Environment={
               'Variables': {
                   'ACTOR_CLASS_NAME': str(klass),
                   'ACTOR_MODULE_NAME': str(module)
               }
             }
            # KMSKeyArn='string',
            # TracingConfig={
            #     'Mode': 'Active'|'PassThrough'
            # },
            # Tags={
            #     'string': 'string'
            # }
        )
        # print(response)
        print(f"New lambda {handler.__name__} created successfully.")
    except lambdacli.exceptions.ResourceConflictException:
        print("Lambda already exists...")
        if LAMBDA_UPDATE:
            print("Updating Lambda...")
            delete_lambda(handler.__name__)
            new_lambda(klass, handler)
        else:
            print("*NO* Lambda update. Proceeding...")


def delete_lambda(name):
    """ Deletes a lambda function from AWS with name *name*."""
    response = lambdacli.delete_function(FunctionName=name)
    # print(response)
    print(f"Lambda {name} deleted successfully.")
