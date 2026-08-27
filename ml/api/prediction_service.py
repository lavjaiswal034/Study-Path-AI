from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = ROOT / "models" / "student_performance_e46.joblib"
METADATA_PATH = ROOT / "models" / "student_performance_e46_metadata.json"


class PredictionService:
    """
    Production ML prediction service.

    Responsibilities:
    - Load the frozen production model.
    - Validate the required feature set.
    - Generate a percentage prediction.
    - Clip the prediction to the valid [0, 100] range.
    - Convert the percentage to marks when maximum marks are supplied.

    This class does not:
    - access databases;
    - perform authentication;
    - train models;
    - modify datasets;
    - call an LLM.
    """

    def __init__(
        self,
        model_path: Path = MODEL_PATH,
        metadata_path: Path = METADATA_PATH,
    ):
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: {model_path}"
            )

        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Model metadata not found: {metadata_path}"
            )

        self.model = joblib.load(model_path)

        with open(
            metadata_path,
            "r",
            encoding="utf-8",
        ) as file:
            self.metadata = json.load(file)

        self.features = self.metadata["features"]
        self.model_version = self.metadata["model_version"]
        self.feature_set_version = self.metadata["feature_set_version"]

    def predict(
        self,
        features: dict[str, float | int | None],
        final_exam_max_marks: float | int | None = None,
    ) -> dict:
        """
        Generate one academic-performance prediction.
        """

        missing_features = [
            feature
            for feature in self.features
            if feature not in features
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}"
            )

        row = {
            feature: features[feature]
            for feature in self.features
        }

        frame = pd.DataFrame([row])

        raw_prediction = float(
            self.model.predict(frame)[0]
        )

        predicted_percentage = max(
            0.0,
            min(100.0, raw_prediction),
        )

        result = {
            "predicted_percentage": predicted_percentage,
            "raw_predicted_percentage": raw_prediction,
            "final_exam_max_marks": (
                float(final_exam_max_marks)
                if final_exam_max_marks is not None
                else None
            ),
            "predicted_marks": None,
            "model_version": self.model_version,
            "feature_set_version": self.feature_set_version,
        }

        if final_exam_max_marks is not None:
            if final_exam_max_marks <= 0:
                raise ValueError(
                    "final_exam_max_marks must be greater than 0."
                )

            result["predicted_marks"] = (
                predicted_percentage
                / 100.0
                * float(final_exam_max_marks)
            )

        return result