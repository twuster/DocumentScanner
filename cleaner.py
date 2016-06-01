"""
Deletes all scanned images in the prod s3 bucket
"""

import boto

s3 = boto.connect_s3()

prod_bucket = s3.get_bucket('dray-assets-prod')
load_files = list(prod_bucket.list(prefix="media/loads"))
document_files = [f for f in load_files if "load_action_approvals" not in f.name]

for f in document_files:
    if "-scanned" in f.key:
        f.delete()
