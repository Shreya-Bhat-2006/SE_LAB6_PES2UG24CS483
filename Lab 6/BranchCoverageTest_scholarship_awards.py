
import pytest
from scholarship_awards import (
    award_amount,
    is_eligible,
    application_status
)


# Tests for award_amount(): category validation

@pytest.mark.parametrize("category", ["merit", "sports", "arts"])
def test_valid_categories(category):
    assert award_amount(category, 100, "low", False) > 0


def test_invalid_category_branch():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("science", 90, "low", False)


# Tests for marks validation

@pytest.mark.parametrize("marks", [-1, -10])
def test_negative_marks_branch(marks):
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", marks, "low", False)


# Tests for renewal branches

def test_merit_renewal():
    assert award_amount("merit", 72, "low", True) == 200


def test_arts_renewal():
    assert award_amount("arts", 62, "low", True) == 200


def test_sports_renewal():
    assert award_amount("sports", 65, "low", True) == 500


# Tests for cutoff branches

def test_marks_exactly_at_cutoff():
    assert award_amount("merit", 75, "low", False) == 0


def test_marks_above_cutoff():
    assert award_amount("merit", 76, "low", False) == 100


# Tests for income branches

def test_low_income_rate():
    assert award_amount("merit", 80, "low", False) == 500


def test_non_low_income_rate():
    assert award_amount("merit", 80, "high", False) == 300


# Tests for large award and nested income branches

def test_above_fifteen_low_income():
    assert award_amount("merit", 91, "low", False) == 2560


def test_above_fifteen_high_income():
    assert award_amount("merit", 91, "high", False) == 1600


def test_exactly_fifteen_above_cutoff():
    assert award_amount("merit", 90, "low", False) == 1500


# Tests for eligibility branches

def test_special_quota_eligible():
    assert is_eligible(50, 2, True) is True


def test_special_quota_ineligible():
    assert is_eligible(90, 3, True) is False


def test_regular_low_attendance():
    assert is_eligible(74, 0, False) is False


def test_regular_attendance_boundary():
    assert is_eligible(75, 1, False) is True


def test_regular_applicant_too_many_backlogs():
    assert is_eligible(90, 2, False) is False


# Tests for application status branches

def test_regular_application_open():
    assert application_status(20, False, False) == "open"


def test_regular_application_closing():
    assert application_status(10, False, False) == "closing"


def test_regular_application_closed():
    assert application_status(4, False, False) == "closed"


def test_renewal_application_open():
    assert application_status(30, True, False) == "open"


def test_renewal_application_closing():
    assert application_status(15, True, False) == "closing"


def test_renewal_application_closed():
    assert application_status(14, True, False) == "closed"


def test_paper_application_open():
    assert application_status(30, False, True) == "open"


def test_paper_application_closing():
    assert application_status(15, False, True) == "closing"


def test_paper_application_closed():
    assert application_status(14, False, True) == "closed"
