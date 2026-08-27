from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DomainAwareImputer(BaseEstimator, TransformerMixin):
    """
    Frozen E46 preprocessing.

    - Learns median fill values from the fitting data only.
    - Adds one missingness indicator per feature.
    - F011_BACKLOG_COUNT uses zero as its fill value.
    """

    def fit(self, X, y=None):
        frame = pd.DataFrame(X).copy()

        self.columns_ = list(frame.columns)

        self.fill_values_ = (
            frame.median(numeric_only=True)
            .reindex(self.columns_)
        )

        if "F011_BACKLOG_COUNT" in self.fill_values_.index:
            self.fill_values_["F011_BACKLOG_COUNT"] = 0.0

        return self

    def transform(self, X):
        frame = pd.DataFrame(X).copy()
        frame = frame[self.columns_]

        indicators = frame.isna().astype(float)

        indicators.columns = [
            f"{column}_missing"
            for column in self.columns_
        ]

        filled = frame.copy()

        for column in self.columns_:
            filled[column] = filled[column].fillna(
                self.fill_values_[column]
            )

        return pd.concat(
            [filled, indicators],
            axis=1,
        ).to_numpy()