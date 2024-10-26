"""Constants for the Oil Price integration."""
DOMAIN = "oil_price"
CONF_PROVINCE = "province"

# 这里定义支持的省份列表
PROVINCES = [
    "北京",
    "上海",
    "广东",
    "江苏",
    # 添加更多省份...
]

# 传感器类型
SENSOR_TYPES = {
    "92h": "92# 汽油",
    "95h": "95# 汽油",
    "98h": "98# 汽油",
    "0h": "0# 柴油"
}

# API URL
API_URL = "your_api_url_here"  # 替换为实际的API地址