from typing import List

import pytest
from models.chronic_disease_sys import (
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
    remove_user_metric,
)


def test_metric():
    name: str = 'glucose'
    text: str = '血糖'
    unit: str = 'mmol/L'
    user_id: int = 1
    ref_value = 1.1
    labels = [('pbg', '餐后', 2), ('fpg', '餐前', 1), ('default', '一般', 0)]

    with pytest.raises(MetricNotFoundException):
        delete_metric(metric_id=0)

    with pytest.raises(MetricNotFoundException):
        get_metric_by_name(name=name)

    with pytest.raises(MetricNotFoundException):
        create_metric_label(metric_id=0, name='', text='')

    dto: MetricDTO = create_metric(name=name, text=text, unit=unit, ref_value=ref_value)
    assert dto.name == name
    assert dto.text == text
    assert dto.ref_value == ref_value

    with pytest.raises(DuplicatedMetricException):
        create_metric(name=name, text=text, unit=unit)

    dto = get_metric(metric_id=dto.id)
    assert dto.name == name
    assert dto.text == text

    # metric label
    for label_name, label_text, label_order in labels:
        label_dto = create_metric_label(metric_id=dto.id, name=label_name, text=label_text, order=label_order)
        assert label_dto.name == label_name
        assert label_dto.text == label_text

    label_list: List[MetricLabelDTO] = query_metric_label_by_metric_id(metric_id=dto.id)
    assert len(label_list) == len(labels)

    # order 顺序
    _labels = [(dto.name, dto.text, dto.order) for dto in label_list]
    assert _labels == sorted(labels, key=lambda x: x[2])

    # user metric
    user_metric_dto = create_user_metric(user_id=user_id, metric_id=dto.id)
    assert user_metric_dto.user_id == user_id
    assert user_metric_dto.metric_id == dto.id
    assert user_metric_dto.ref_value == dto.ref_value

    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 1

    remove_user_metric(user_id=user_id, metric_id=dto.id)
    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 0

    # delete
    delete_metric(metric_id=dto.id)
    with pytest.raises(MetricNotFoundException):
        get_metric(metric_id=dto.id)

    li: List[UserMetricDTO] = query_user_metric_by_user_id(user_metric_dto.user_id)
    assert len(li) == 0

    with pytest.raises(MetricLabelNotFoundException):
        delete_metric_label(metric_label_id=0)

    label_list: List[MetricLabelDTO] = query_metric_label_by_metric_id(metric_id=dto.id)
    assert len(label_list) == 0
