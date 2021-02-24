import tempfile

import boto3
from PIL import Image
from chalice import Chalice

# The app and S3 client will stay initialized between function executions
# if they happen before the execution environment is tore down.
app = Chalice(app_name='hello-world')
s3 = boto3.client('s3')

AWS_REGION = '<your_aws_region>'
BUCKET_NAME = '<your_s3_bucket_name>'
IMAGES_PREFIX = 'images/'
THUMBNAILS_PREFIX = 'thumbnails/'


@app.route('/')
def index():
    """Example 1. Hello world!"""
    return {'hello': 'world'}


@app.on_s3_event(
    bucket=BUCKET_NAME,
    events=['s3:ObjectCreated:Put'],
    prefix=IMAGES_PREFIX,
    suffix='.jpg'
)
def resize_image(event):
    """Example 2. When an image is uploaded to an S3 bucket, generate a thumbnail."""
    with tempfile.NamedTemporaryFile('w') as f:
        s3.download_file(event.bucket, event.key, f.name)

        # TODO: add error-checking code, this assumes everything always goes according to plan.
        im = Image.open(f.name)
        im.thumbnail((50, 50))
        im.save(f.name, "JPEG", quality=80)

        s3.upload_file(f.name, event.bucket, _get_thumnail_key(event.key))


@app.route('/images')
def list_images():
    """Naive implementation of an API endpoint to list S3 objects."""
    images = []
    for obj in s3.list_objects(Bucket=BUCKET_NAME, Prefix=IMAGES_PREFIX)['Contents']:
        image_key = obj['Key']
        thumb_key = _get_thumnail_key(image_key)

        images.append({
            'url': f'https://s3-{AWS_REGION}.amazonaws.com/{BUCKET_NAME}/{image_key}',
            'thumb': f'https://s3-{AWS_REGION}.amazonaws.com/{BUCKET_NAME}/{thumb_key}',
            'size': obj['Size']
        })

    return images


def _get_thumnail_key(image_key: str) -> str:
    """
    Given the key of an image, return the key of the corresponding thumbnail.

    e.g. `images/foo.jpg` -> `thumbnails/foo.jpg`
    """
    return f'{THUMBNAILS_PREFIX}{image_key.lstrip(IMAGES_PREFIX)}'
