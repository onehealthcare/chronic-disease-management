from typing import List

import pytest
from models.chronic_condition_sys import (
    DuplicatedMetricException,
    MetricDTO,
    MetricNotFoundException,
    UserMetricDTO,
    create_metric,
    create_user_metric,
    delete_metric,
    get_metric,
    get_metric_by_name,
    query_user_metric_by_user_id,
)


def test_metric():
    name: str = 'glucose'
    text: str = '血糖'
    unit: str = 'mmol/L'
    user_id: int = 1

    with pytest.raises(MetricNotFoundException):
        delete_metric(metric_id=0)

    with pytest.raises(MetricNotFoundException):
        get_metric_by_name(name=name)

    dto: MetricDTO = create_metric(name=name, text=text, unit=unit)
    assert dto.name == name
    assert dto.text == text

    with pytest.raises(DuplicatedMetricException):
        create_metric(name=name, text=text, unit=unit)

    dto = get_metric(metric_id=dto.id)
    assert dto.name == name
    assert dto.text == text

    user_metric_dto = create_user_metric(user_id=user_id, metric_id=dto.id)
    assert user_metric_dto.user_id == user_id
    assert user_metric_dto.metric_id == dto.id

    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 1

    delete_metric(metric_id=dto.id)
    with pytest.raises(MetricNotFoundException):
        get_metric(metric_id=dto.id)

    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 0
