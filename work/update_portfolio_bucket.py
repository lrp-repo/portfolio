import boto3
import io
import zipfile
import mimetypes

# zip_file_name = 'portfoliobuild.zip'

s3 = boto3.resource('s3')

portfolio_bucket = s3.Bucket('portfolio.lpasf.org')
build_bucket = s3.Bucket('portfoliobuild.lpasf.org')

portfolio_zip = io.BytesIO()

build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        content_type = mimetypes.guess_type(nm)[0]
        # print(content_type)
        portfolio_bucket.upload_fileobj(obj, nm ,ExtraArgs={'ACL': 'public-read', 'ContentType': content_type })
