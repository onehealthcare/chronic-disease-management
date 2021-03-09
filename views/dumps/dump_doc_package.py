from typing import Dict, List

from models.chronic_condition_sys import DocPackageDTO


def dump_doc_package(doc_package: DocPackageDTO) -> Dict:
    return {
        'id': str(doc_package.id),
        'user_id': str(doc_package.user_id),
        'desc': doc_package.desc,
        'ident_urls': doc_package.ident_urls,
        'idents': [ident.ident for ident in doc_package.idents],
        'created_at': doc_package.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }


def dump_doc_packages(doc_packages: List[DocPackageDTO]) -> List[Dict]:
    if not doc_packages:
        return []

    return [dump_doc_package(o) for o in doc_packages]
