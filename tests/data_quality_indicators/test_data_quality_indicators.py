import pytest

from pact_methodology.carbon_footprint.reference_period import ReferencePeriod
from pact_methodology.data_quality_indicators.data_quality_indicators import (
    DataQualityIndicators,
)
from pact_methodology.data_quality_indicators.data_quality_rating import (
    DataQualityRating,
)
from pact_methodology.datetime import DateTime


@pytest.fixture
def valid_data():
    return {
        "reference_period": ReferencePeriod(
            start=DateTime("2025-01-01T00:00:00Z"), end=DateTime("2026-01-01T00:00:00Z")
        ),
        "coverage_percent": 80.0,
        "technological_dqr": DataQualityRating(2),
        "temporal_dqr": DataQualityRating(2),
        "geographical_dqr": DataQualityRating(1),
        "completeness_dqr": DataQualityRating(2),
        "reliability_dqr": DataQualityRating(3),
    }


@pytest.mark.parametrize(
    "missing_attribute",
    [
        "coverage_percent",
        "technological_dqr",
        "temporal_dqr",
        "geographical_dqr",
        "completeness_dqr",
        "reliability_dqr",
    ],
)
def test_dqi_missing_attributes_after_2025(valid_data, missing_attribute):
    del valid_data[missing_attribute]
    with pytest.raises(ValueError) as excinfo:
        DataQualityIndicators(**valid_data)
    assert (
        str(excinfo.value)
        == f"Attribute '{missing_attribute}' must be defined and not None for reporting periods including 2025 or later"
    )


def test_dqi_valid_before_2025():
    reference_period = ReferencePeriod(
        start=DateTime("2023-01-01T00:00:00Z"), end=DateTime("2024-01-01T00:00:00Z")
    )
    dqi = DataQualityIndicators(
        reference_period=reference_period, technological_dqr=DataQualityRating(2)
    )  # Other attributes are optional
    assert dqi.technological_dqr == DataQualityRating(2)


def test_dqi_valid_after_2025_all_attributes():
    reference_period = ReferencePeriod(
        start=DateTime("2025-01-01T00:00:00Z"), end=DateTime("2026-01-01T00:00:00Z")
    )
    dqi = DataQualityIndicators(
        reference_period=reference_period,
        coverage_percent=80.0,
        technological_dqr=DataQualityRating(2),
        temporal_dqr=DataQualityRating(2),
        geographical_dqr=DataQualityRating(1),
        completeness_dqr=DataQualityRating(2),
        reliability_dqr=DataQualityRating(3),
    )
    assert dqi.coverage_percent == 80.0


def test_dqi_missing_reference_period():
    with pytest.raises(TypeError):
        DataQualityIndicators()


def test_dqi_invalid_dqr_type():
    reference_period = ReferencePeriod(
        start=DateTime("2025-01-01T00:00:00Z"), end=DateTime("2026-01-01T00:00:00Z")
    )
    with pytest.raises(TypeError):
        DataQualityIndicators(
            reference_period=reference_period,
            coverage_percent=50,
            technological_dqr=2.0,
        )  # DQR should be a DataQualityRating instance
