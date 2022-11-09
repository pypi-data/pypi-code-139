import logging

import os
import time
from google.cloud import firestore


class FirestoreWriteBatch:
    def __init__(self, client: firestore.Client):
        self.updates = 0
        self.client = client
        self.batch = client.batch()

    def __enter__(self):
        self.updates += 1

        if self.updates >= 500:
            self.batch.commit()
            self.batch = self.client.batch()

        return self.batch

    def __exit__(self, type, value, traceback):
        self.batch.commit()

    def commit(self):
        self.batch.commit()
        self.batch = self.client.batch()


def is_testing():
    """ Returns True if the binary is running inside a Kubernetes cluster."""
    return os.environ.get("PYTEST_CURRENT_TEST") is not None


def current_time_ms():
    """ Returns the current time in milliseconds since EPOCH """
    return time.time_ns() // 1_000_000


def set_sequence_counts(
        job_ref: firestore.DocumentReference,
        seq_collection_ref: firestore.CollectionReference):
    if job_ref.get(['failed_sequences']).to_dict():
        return

    logging.info(f'[{job_ref.path}] Updating sequence counts')
    failed_count = sum([seq.get('status') in {'MSA_FAILED', 'FOLDING_FAILED'}
                        for seq in seq_collection_ref.stream()])
    job_ref.update({
        'failed_sequences': failed_count,
        'completed_sequences': 0})
