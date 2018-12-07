import boto3
import io
import zipfile
zip_file = 'portfoliobuild.zip'

s3 = boto3.resource('s3')

portfolio_bucket = s3.Bucket('portfolio.lpasf.org')
build_bucket = s3.Bucket('portfoliobuild.lpasf.org')

for obj in build_bucket.objects.all():
   if obj.key == zip_file:
       print("object key found, processing zip file")

 ##   build_bucket.download_file('portfoliobuild.zip' , zip_file)

       with zipfile.ZipFile(zip_file) as myzip:
           for nm in myzip.namelist():
              obj = myzip.open(nm)
              portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ACL': 'public-read'})
   else:
       print("obect key not found")


    