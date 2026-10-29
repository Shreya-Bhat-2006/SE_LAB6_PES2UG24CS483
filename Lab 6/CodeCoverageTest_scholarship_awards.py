
import pytest
from scholarship_awards import (
    award_amount,
    is_eligible,
    application_status
)


# Tests for award_amount()

def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_merit_award_low_income():
    assert award_amount("merit", 80, "low", False) == 500


def test_merit_award_high_income():
    assert award_amount("merit", 80, "high", False) == 300


def test_large_award_low_income():
    assert award_amount("merit", 91, "low", False) == 2560


def test_large_award_high_income():
    assert award_amount("merit", 91, "high", False) == 1600


def test_renewal_reduces_merit_cutoff():
    assert award_amount("merit", 72, "low", True) == 200


def test_sports_renewal_does_not_reduce_cutoff():
    assert award_amount("sports", 65, "low", True) == 500


def test_arts_category():
    assert award_amount("arts", 70, "low", False) == 500


def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("science", 90, "low", False)


def test_negative_marks():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


# Tests for is_eligible()

def test_regular_eligible():
    assert is_eligible(90, 0, False) is True


def test_low_attendance():
    assert is_eligible(70, 0, False) is False


def test_regular_applicant_with_two_backlogs():
    assert is_eligible(90, 2, False) is False


def test_special_quota_with_two_backlogs():
    assert is_eligible(50, 2, True) is True


def test_special_quota_with_three_backlogs():
    assert is_eligible(90, 3, True) is False


# Tests for application_status()

def test_application_open():
    assert application_status(25, False, False) == "open"


def test_application_closing():
    assert application_status(10, False, False) == "closing"


def test_application_closed():
    assert application_status(4, False, False) == "closed"


def test_renewal_application_open():
    assert application_status(30, True, False) == "open"


def test_paper_application_open():
    assert application_status(30, False, True) == "open"
