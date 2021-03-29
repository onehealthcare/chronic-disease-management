from typing import List

import pytest
from models.chronic_condition_sys import (
    DocPackageIdentNotFoundException,
    DocPackageNotFoundException,
    create_doc_package,
    delete_doc_ident_by_id,
    delete_doc_package_by_user_id_and_package_id,
    get_doc_package_by_id,
    paged_doc_package_by_user_id,
    paged_search_doc_package_by_user_id,
    update_doc_package_by_user_id_and_package_id,
)
from models.const import CommonStatus
from models.exceptions import AccessDeniedError


def test_doc_package():
    user_id: int = 1
    idents: List[str] = ['a', 'b', 'c']
    test_desc = "test"

    with pytest.raises(DocPackageNotFoundException):
        get_doc_package_by_id(package_id=1)

    for _ in range(50):
        create_doc_package(user_id=user_id, idents=idents, desc=test_desc)

    doc_package_list = paged_doc_package_by_user_id(user_id=user_id)
    assert len(doc_package_list) == 21

    doc_package_list = paged_doc_package_by_user_id(user_id=user_id, cursor=40)
    assert len(doc_package_list) == 11

    size: int = 5
    doc_package_list = paged_doc_package_by_user_id(user_id=user_id, cursor=40, size=size)
    assert len(doc_package_list) == size + 1

    doc_package_list = paged_search_doc_package_by_user_id(user_id=user_id, keyword='')
    assert doc_package_list == []

    doc_package_list = paged_search_doc_package_by_user_id(user_id=user_id, keyword='test')
    assert len(doc_package_list) == 21

    new_desc: str = "new test desc"
    new_idents: List[str] = ['b', 'c']
    data = {
        "idents": new_idents,
        "desc": new_desc
    }

    doc_package = doc_package_list[0]
    update_doc_package_by_user_id_and_package_id(user_id=0, package_id=doc_package.id, data=data)
    dto = get_doc_package_by_id(package_id=doc_package.id)
    assert dto.desc == test_desc

    update_doc_package_by_user_id_and_package_id(user_id=user_id, package_id=0, data=data)
    dto = get_doc_package_by_id(package_id=doc_package.id)
    assert dto.desc == test_desc

    update_doc_package_by_user_id_and_package_id(user_id=user_id, package_id=doc_package.id, data=data)
    dto = get_doc_package_by_id(package_id=doc_package.id)
    assert dto.desc == new_desc
    assert set([ident.ident for ident in dto.idents]) == set(new_idents)

    with pytest.raises(DocPackageIdentNotFoundException):
        delete_doc_ident_by_id(10000)

    delete_doc_ident_by_id(dto.idents[0].id)
    dto = get_doc_package_by_id(package_id=doc_package.id)
    assert len(dto.idents) == 1

    with pytest.raises(DocPackageNotFoundException):
        delete_doc_package_by_user_id_and_package_id(user_id=user_id, package_id=1000)

    with pytest.raises(AccessDeniedError):
        delete_doc_package_by_user_id_and_package_id(user_id=2, package_id=doc_package.id)

    with pytest.raises(AccessDeniedError):
        update_doc_package_by_user_id_and_package_id(user_id=2, package_id=doc_package.id, data=data)

    with pytest.raises(DocPackageNotFoundException):
        update_doc_package_by_user_id_and_package_id(user_id=user_id, package_id=10000, data=data)

    delete_doc_package_by_user_id_and_package_id(user_id=user_id, package_id=doc_package.id)

    dto = get_doc_package_by_id(package_id=doc_package.id)
    assert dto.status == CommonStatus.DELETED
