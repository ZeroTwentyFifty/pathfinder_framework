import pytest

from pact_methodology.exceptions import DuplicateIdError
from pact_methodology.urn import CompanyId
from pact_methodology.product_footprint.company_id_list import CompanyIdList


def test_company_id_list_valid_company_ids():
    company_ids = [
        CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp")
    ]
    company_id_list = CompanyIdList(company_ids)
    assert len(company_id_list) == 1
    assert isinstance(company_id_list[0], CompanyId)


@pytest.mark.parametrize(
    "company_ids",
    [
        123,
        1.0,
        None,
        "string",
        {},
        CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp"),
    ],
)
def test_company_id_list_invalid_company_ids(company_ids):
    with pytest.raises(ValueError, match="company_ids must be a list of CompanyId"):
        CompanyIdList(company_ids)


@pytest.mark.parametrize(
    "company_ids",
    [
        ["string"],  # list with a single invalid item
        [
            CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp"),
            "string",
        ],  # list with a mix of valid and invalid items
        [1, 2, 3],  # list with invalid items of a different type
        [
            CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp"),
            CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp"),
            "string",
        ],  # list with multiple valid items and an invalid item
    ],
)
def test_company_id_list_invalid_company_ids_list(company_ids):
    with pytest.raises(ValueError, match="company_ids must be a list of CompanyId"):
        CompanyIdList(company_ids)


def test_company_id_list_duplicate_company_ids():
    company_ids = [
        CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp"),
        CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp"),
    ]
    with pytest.raises(DuplicateIdError, match="Duplicate company_ids are not allowed"):
        CompanyIdList(company_ids)


def test_company_id_list_append_duplicate_company_id():
    company_ids = [
        CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp")
    ]
    company_id_list = CompanyIdList(company_ids)
    with pytest.raises(DuplicateIdError, match="Duplicate company_ids are not allowed"):
        company_id_list.append(company_ids[0])


def test_company_id_list_insert_duplicate_company_id():
    company_ids = [
        CompanyId("urn:pathfinder:company:customcode:buyer-assigned:acme-corp")
    ]
    company_id_list = CompanyIdList(company_ids)
    with pytest.raises(DuplicateIdError, match="Duplicate company_ids are not allowed"):
        company_id_list.insert(0, company_ids[0])
