from typing import Optional

from openai import OpenAI

from app.config import settings

_client: Optional[OpenAI] = None


def get_client() -> OpenAI:

    """
    获取OpenAI客户端实例的函数

    该函数使用单例模式确保全局只有一个OpenAI客户端实例。
    如果客户端实例尚未创建，则使用配置的API密钥和基础URL创建新实例。

    Returns:
        OpenAI: 返回一个OpenAI客户端实例
    """
    global _client  # 声明使用全局变量_client
    if _client is None:  # 检查客户端实例是否已创建
        # 创建新的OpenAI客户端实例，使用配置的API密钥和基础URL
        _client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _client  # 返回客户端实例


async def chat_completion(
    system_prompt: str,
    messages: list[dict],
) -> str:
    """Send a chat completion request to DeepSeek API."""
    client = get_client()
    payload = [
        {"role": "system", "content": system_prompt},
        *messages,
    ]
    print(f"[DEBUG] Full API Payload: {payload}")
    
    response = client.chat.completions.create(
        model=settings.deepseek_model,
        messages=payload,
        temperature=0.8,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""


async def chat_completion_stream(
    system_prompt: str,
    messages: list[dict],
):
    """Stream a chat completion from DeepSeek API."""
    client = get_client()
    response = client.chat.completions.create(
        model=settings.deepseek_model,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages,
        ],
        temperature=0.8,
        max_tokens=1024,
        stream=True,
    )
    for chunk in response:
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and delta.content:
            yield delta.content
