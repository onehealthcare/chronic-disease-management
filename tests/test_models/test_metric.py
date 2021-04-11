from typing import List

import pytest
from models.chronic_condition_sys import (
    DuplicatedMetricException,
    MetricDTO,
    MetricLabelDTO,
    MetricLabelNotFoundException,
    MetricNotFoundException,
    UserMetricDTO,
    create_metric,
    create_metric_label,
    create_user_metric,
    delete_metric,
    delete_metric_label,
    get_metric,
    get_metric_by_name,
    query_metric_label_by_metric_id,
    query_user_metric_by_user_id,
)


def test_metric():
    name: str = 'glucose'
    text: str = '血糖'
    unit: str = 'mmol/L'
    user_id: int = 1
    label_name: str = 'pbg'
    label_text: str = '餐后'

    with pytest.raises(MetricNotFoundException):
        delete_metric(metric_id=0)

    with pytest.raises(MetricNotFoundException):
        get_metric_by_name(name=name)

    with pytest.raises(MetricNotFoundException):
        create_metric_label(metric_id=0, name=label_name, text=label_text)

    dto: MetricDTO = create_metric(name=name, text=text, unit=unit)
    assert dto.name == name
    assert dto.text == text

    with pytest.raises(DuplicatedMetricException):
        create_metric(name=name, text=text, unit=unit)

    dto = get_metric(metric_id=dto.id)
    assert dto.name == name
    assert dto.text == text

    # metric label
    label_dto = create_metric_label(metric_id=dto.id, name=label_name, text=label_text)
    assert label_dto.name == label_name
    assert label_dto.text == label_text

    label_list: List[MetricLabelDTO] = query_metric_label_by_metric_id(metric_id=dto.id)
    assert len(label_list) == 1

    # user metric
    user_metric_dto = create_user_metric(user_id=user_id, metric_id=dto.id)
    assert user_metric_dto.user_id == user_id
    assert user_metric_dto.metric_id == dto.id

    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 1

    # delete
    delete_metric(metric_id=dto.id)
    with pytest.raises(MetricNotFoundException):
        get_metric(metric_id=dto.id)

    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 0

    with pytest.raises(MetricLabelNotFoundException):
        delete_metric_label(metric_label_id=0)

    delete_metric_label(metric_label_id=label_list[0].id)
