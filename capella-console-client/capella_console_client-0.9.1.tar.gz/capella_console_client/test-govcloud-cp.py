"""
try to copy s3://cirrus-prod-data-27qi4kja7o84/static-icons/ACD.png to govcloud bucket    
"""

import boto3

if __name__ == "__main__":

    GOVCLOUD_BUCKET = "<insert>"
    GOVCLOUD_PREFIX = "<insert-no-trailing-/>"
    GOVCLOUD_AWS_CLI_PROFILE_NAME = "<insert>"

    CIRRUS_PROD_DATA_BUCKET = "cirrus-prod-data-27qi4kja7o84"
    CIRRUS_ASSET_S3_KEY = "static-icons/ACD.png"

    source_s3 = boto3.Session(profile_name="e84-prod").client("s3")

    # check read access
    head_ret = source_s3.head_object(Bucket=CIRRUS_PROD_DATA_BUCKET, Key=CIRRUS_ASSET_S3_KEY)
    print(head_ret["ResponseMetadata"])

    dest_s3 = boto3.Session(profile_name=GOVCLOUD_AWS_CLI_PROFILE_NAME).client("s3")
    dest_s3_key = f"{GOVCLOUD_PREFIX}/{CIRRUS_ASSET_S3_KEY}"

    # pretty certain this will fail
    dest_s3.copy(
        CopySource={"Bucket": CIRRUS_PROD_DATA_BUCKET, "Key": CIRRUS_ASSET_S3_KEY},
        Bucket=GOVCLOUD_BUCKET,
        Key=dest_s3_key,
        SourceClient=source_s3,
    )

    # check if exists
    gc_head_ret = source_s3.head_object(Bucket=GOVCLOUD_BUCKET, Key=dest_s3_key)
    print(gc_head_ret["ResponseMetadata"])
