
from datetime import datetime, timedelta
from typing import List, Union
import motor.motor_asyncio
import requests

from app.api.models.overview import CountGroupResponse


async def agg_recent_days_count(
    recent_days: int,
    coll: motor.motor_asyncio.AsyncIOMotorCollection
) -> List[CountGroupResponse]:
    """聚合指定情报库最近天数的每日增长数量

    Args:
        recent_days (int): 聚合的最近天数
        coll (motor.motor_asyncio.AsyncIOMotorCollection): 数据库集合对象

    Returns:
        List[CountGroupResponse]: 结果集,用于前端折线图渲染
    """
    now = datetime.now()
    today_midnight = datetime(now.year, now.month, now.day)
    last_7day_midnight = today_midnight - timedelta(days=7)

    # 构建聚合查询
    pipeline = [
        {
            '$match': {
                'last_seen': {
                    '$gte': int(last_7day_midnight.timestamp())  # 获取时间戳并转换为整数
                }
            }
        },
        {
            '$project': {
                'date': {
                    '$toDate': {
                        '$multiply': ['$last_seen', 1000]  # 将时间戳转换为毫秒

                    }
                }
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {'format': '%Y%m%d', 'date': '$date',
                                      'timezone': 'Asia/Shanghai'}
                },
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'_id': 1}
        },
        {
            '$project': {
                'date': '$_id',
                '_id': 0,  # 不显示原始的_id字段
                'count': 1
            }
        }
    ]

    # 执行聚合查询
    results = await coll.aggregate(pipeline).to_list(None)
    return results


def get_ip_info(ip_address) -> Union[dict, None]:
    """查询ip额外信息,例如地理位置等

    Args:
        ip_address (string): IP地址

    Returns:
        _type_: None or json
    """
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
