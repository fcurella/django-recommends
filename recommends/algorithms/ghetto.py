
import warnings

from .naive import NaiveAlgorithm


class GhettoAlgorithm(NaiveAlgorithm):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`GhettoAlgorithm` is pending deprecation and it will be removed in "
            "future versions. Use `recommends.algorithms.naive.NaiveAlgorithm instead.",
            PendingDeprecationWarning,
        )
        super(GhettoAlgorithm, self).__init__(*args, **kwargs)
