#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有Facebook Scraper API端点
验证每个端点是否能正常调用
"""

import os
import sys
import asyncio
import httpx

# 设置Windows控制台输出为UTF-8编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# RapidAPI配置
RAPIDAPI_HOST = "facebook-scraper3.p.rapidapi.com"
RAPIDAPI_BASE_URL = f"https://{RAPIDAPI_HOST}"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")

# 8个API端点
ENDPOINTS = {
    "1. 搜索位置": "/search/locations",
    "2. 搜索视频": "/search/videos",
    "3. 搜索帖子": "/search/posts",
    "4. 搜索地点": "/search/places",
    "5. 搜索主页": "/search/pages",
    "6. 搜索活动": "/search/events",
    "7. 搜索群组帖子": "/search/groups_posts",
    "8. 搜索用户": "/search/people",
}

# 测试参数
TEST_QUERIES = {
    "/search/locations": "New York",
    "/search/videos": "technology",
    "/search/posts": "AI",
    "/search/places": "restaurant",
    "/search/pages": "Tesla",
    "/search/events": "concert",
    "/search/groups_posts": "programming",
    "/search/people": "John",
}


async def test_endpoint(name: str, endpoint: str) -> dict:
    """
    测试单个API端点
    
    Args:
        name: 端点名称
        endpoint: 端点路径
        
    Returns:
        测试结果字典
    """
    if not RAPIDAPI_KEY:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "❌ 失败",
            "error": "未设置RAPIDAPI_KEY环境变量"
        }
    
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }
    
    params = {
        "query": TEST_QUERIES.get(endpoint, "test"),
        "limit": 5  # 测试时只获取5条结果
    }
    
    url = f"{RAPIDAPI_BASE_URL}{endpoint}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, 
                headers=headers, 
                params=params, 
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                # 检查返回数据
                if isinstance(data, dict):
                    result_count = len(data.get("data", []))
                elif isinstance(data, list):
                    result_count = len(data)
                else:
                    result_count = 0
                
                return {
                    "name": name,
                    "endpoint": endpoint,
                    "status": "✅ 成功",
                    "status_code": response.status_code,
                    "result_count": result_count,
                    "query": params["query"]
                }
            else:
                error_text = response.text[:200]
                return {
                    "name": name,
                    "endpoint": endpoint,
                    "status": "❌ 失败",
                    "status_code": response.status_code,
                    "error": error_text
                }
                
    except httpx.TimeoutException:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "⏱️ 超时",
            "error": "请求超时（30秒）"
        }
    except Exception as e:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "❌ 失败",
            "error": str(e)
        }


async def test_all_endpoints():
    """
    测试所有API端点
    """
    print("=" * 80)
    print("Facebook Scraper API 端点测试")
    print("=" * 80)
    print()
    
    if not RAPIDAPI_KEY:
        print("❌ 错误: 未设置RAPIDAPI_KEY环境变量")
        print()
        print("请先设置环境变量:")
        print("  Windows PowerShell: $env:RAPIDAPI_KEY='你的API密钥'")
        print("  Windows CMD: set RAPIDAPI_KEY=你的API密钥")
        print("  Linux/Mac: export RAPIDAPI_KEY='你的API密钥'")
        print()
        return
    
    print(f"API密钥已设置: {RAPIDAPI_KEY[:10]}...{RAPIDAPI_KEY[-4:]}")
    print(f"测试端点数量: {len(ENDPOINTS)}")
    print()
    print("-" * 80)
    print()
    
    # 并发测试所有端点
    tasks = [
        test_endpoint(name, endpoint) 
        for name, endpoint in ENDPOINTS.items()
    ]
    
    results = await asyncio.gather(*tasks)
    
    # 输出结果
    success_count = 0
    failed_count = 0
    
    for result in results:
        print(f"【{result['name']}】")
        print(f"  端点: {result['endpoint']}")
        print(f"  状态: {result['status']}")
        
        if result['status'] == "✅ 成功":
            print(f"  HTTP状态码: {result['status_code']}")
            print(f"  查询关键词: {result['query']}")
            print(f"  返回结果数: {result['result_count']}")
            success_count += 1
        else:
            print(f"  错误信息: {result.get('error', '未知错误')}")
            if 'status_code' in result:
                print(f"  HTTP状态码: {result['status_code']}")
            failed_count += 1
        
        print()
    
    # 总结
    print("=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"总计: {len(results)} 个端点")
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {failed_count} 个")
    print(f"成功率: {success_count / len(results) * 100:.1f}%")
    print()
    
    if failed_count > 0:
        print("⚠️  部分端点测试失败，可能的原因：")
        print("  1. API密钥无效或已过期")
        print("  2. 未订阅Facebook Scraper3 API")
        print("  3. API配额已用完")
        print("  4. 网络连接问题")
        print("  5. RapidAPI服务暂时不可用")
    else:
        print("🎉 所有端点测试通过！")


if __name__ == "__main__":
    asyncio.run(test_all_endpoints())

