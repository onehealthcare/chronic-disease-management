from pydantic import BaseModel


class FujixRecipe(BaseModel):
    film_simulation: str
    dynamic_range: str
    grain_effect: str  # 颗粒效果
    color_chrome_effect: str  # 彩色效果
    color_chrome_effect_blue: str  # 彩色FX蓝色
    white_balance: str
    highlight: str
    shadow: str
    color: str
    sharpness: str  # 锐度
    noise_reduction: str  # 降噪（高 ISO 降噪）
    clarity: str  # 清晰度
    iso: str
    exposure_compensation: str  # 曝光补偿
