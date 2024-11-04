"""Constants for the Oil Price integration."""
DOMAIN = "oil_price"
CONF_PROVINCE = "province"

# 这里定义支持的省份列表
PROVINCES = [
    "北京",
    "天津",
    "上海",
    "重庆",
    "河北",
    "山西",
    "辽宁",
    "吉林",
    "黑龙江",
    "江苏",
    "浙江",
    "安徽",
    "福建",
    "江西",
    "山东",
    "河南",
    "湖北",
    "湖南",
    "广东",
    "海南",
    "四川",
    "贵州",
    "云南",
    "陕西",
    "甘肃",
    "青海",
    "内蒙古",
    "广西",
    "西藏",
    "宁夏",
    "新疆",
]

# 传感器类型
SENSOR_TYPES = {
    "92h": "92# 汽油",
    "95h": "95# 汽油",
    "98h": "98# 汽油",
    "0h": "0# 柴油"
}

# API URL
API_URL = "https://hacloud.online/oilprice"