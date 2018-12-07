import json
import boto3
import io
import zipfile
import mimetypes


def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic(
        'arn:aws:sns:us-east-1:295510046388:deployPortfolioTopic')

    location = {
        "bucketName": 'portfoliobuild.lpasf.org',
        "objectKey": 'portfoliobuild.zip'
    }

    try:

        job = event.get("CodePipeline.job")

        print("Code pipeline job event  " + str(job))

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "buildPortfolio":
                    location = artifact["location"]["s3Location"]

        portfolio_bucket = s3.Bucket('portfolio.lpasf.org')
        build_bucket = s3.Bucket(location["bucketName"])
        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                content_type = mimetypes.guess_type(nm)[0]
                print(content_type)
                portfolio_bucket.upload_fileobj(
                    obj, nm, ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})

        print("Deployment Job Complete")
        topic.publish(Subject="SNS Message from Deployment Job",
                      Message="The Portfolio Deployment Job was Sucessful")
        if job:

            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="SNS Message from Deployment Job",
                      Message="The Portfolio Deployment Job was NOT Sucessful!")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Portfolio Lambda Job Completed Sucessfully')
    }
