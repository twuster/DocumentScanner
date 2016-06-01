import boto
import os

from boto.s3.key import Key
from scanner import Scanner


class Runner:
    def __init__(self):
        pass

    @classmethod
    def run(cls):
        s3 = boto.connect_s3()

        prod_bucket = s3.get_bucket('dray-assets-prod')
        load_files = list(prod_bucket.list(prefix="media/loads"))
        document_files = [f for f in load_files if "load_action_approvals" not in f.name]

        for f in document_files:
            # Check for existing scanned version
            filename, file_extension = os.path.splitext(f.key)
            result_keyname = filename + "-scanned" + file_extension
            possible_key = prod_bucket.get_key(result_keyname)
            if possible_key is not None or "-scanned" in f.key:
                # Scanned file already exists, move on
                continue

            # Read image and scan
            image = prod_bucket.get_key(f.key)
            image.get_contents_to_filename('tmp/tmp-src.png')
            result_filename = Scanner.scan('tmp/tmp-src.png')

            # Create new key for result file
            k = Key(prod_bucket)
            k.key = result_keyname
            k.set_contents_from_filename(result_filename)
