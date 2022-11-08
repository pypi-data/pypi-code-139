from abc import ABCMeta

import numpy as np


class PredictionDecoder(metaclass=ABCMeta):
    """Base class for prediction decoders.

    .. note::
        This class should not be used directly. Use derived classes instead.

    Parameters
    ----------
    dataset : Dataset
    """

    def __init__(self, dataset):
        self.dataset = dataset


class SeqToSeqPredictionDecoder(PredictionDecoder):
    """Prediction decoder for encoder-decoder architectures.

    Removes sliding window format.

    Parameters
    ----------
    dataset : SeqToSeqDataset or PytorchForecastingDataset
    """
    def __init__(self, dataset):
        super().__init__(dataset)

    def decode(self, prediction, out=None):
        """Decodes predictions.

        Parameters
        ----------
        prediction : array_like
            Raw prediction.

        out : pd.DataFrame, default=None
            If provided, the destination to place the result. The shape must be
            correct, matching that of what decode would have returned if no out
            argument were specified.
        """
        groupby = self.dataset.decoded_index.groupby(self.dataset.group_ids)
        sequence_len = self.dataset.max_prediction_length
        decoded_prediction = []

        for i, group_id in enumerate(groupby.groups):
            group = groupby.get_group(group_id)
            index = group.index[::sequence_len].tolist()
            group_prediction = prediction[index].flatten()

            # Get number of remaining sequences.
            mod = (len(group) - 1) % sequence_len
            if mod > 0:
                # Get the last element of each of the last `mod` sequences.
                mod_sequence = prediction[-mod:, -1]
                group_prediction = np.concatenate(
                    (group_prediction, mod_sequence)
                )
            decoded_prediction.append(group_prediction)

        decoded_prediction = np.concatenate(decoded_prediction)

        if out is None:
            return decoded_prediction

        return self._insert_in_X(out, decoded_prediction, list(groupby.groups))

    def _insert_in_X(self, X, decoded_prediction, groups_order):
        # Retrieve settings from ``dataset``.
        encoder_length = self.dataset.max_encoder_length
        group_ids = self.dataset.group_ids

        # Drop first ``max_encoder_length`` rows from each group.
        X = X.drop(X.groupby(group_ids).head(encoder_length).index)

        X = X.set_index(group_ids).loc[groups_order].reset_index()
        X[self.dataset.target] = decoded_prediction
        cols = group_ids + [self.dataset.time_idx, self.dataset.target]
        return X[cols]
