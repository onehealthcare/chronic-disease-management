from utils.enum import StrEnum


class ChartType(StrEnum):
    LINE = 'line'
    COLUMN = 'column'

    @classmethod
    def get_text(cls, name: 'ChartType') -> str:
        return {
            cls.LINE: '折线图',
            cls.COLUMN: '柱状图',
        }.get(name, '')

    @classmethod
    def get_all(cls):
        li = [cls.LINE, cls.COLUMN]
        return [{"name": i, "text": cls.get_text(i)} for i in li]
