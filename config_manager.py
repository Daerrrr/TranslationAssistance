# -*- coding: utf-8 -*-
"""
配置管理器重构（LangChain 版）
1. 创建 LangChainConfig 数据类，将原有配置管理迁移到 Pydantic 模型；
2. 配置适配到 LangChain 的 ChatOpenAI，从环境变量加载 DeepSeek API。
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import httpx


class LangChainConfig(BaseModel):
    """
    LangChain 配置数据类（Pydantic 模型）。
    替代原有 dict/多变量配置，提供类型安全与校验。
    """
    api_key: str = Field(description="DeepSeek API密钥")
    base_url: str = Field(default="https://api.deepseek.com")
    model: str = Field(default="deepseek-chat")
    temperature: float = Field(default=0.1)
    max_tokens: Optional[int] = Field(default=2000)
    timeout: int = Field(default=30)
    max_retries: int = Field(default=3)


class ConfigManager:
    """
    配置管理器（LangChain 版本）。
    使用 LangChainConfig 承载配置，并创建 ChatOpenAI 实例。
    """

    def __init__(self):
        self.config = self._load_config()
        self.llm = self._create_llm()

    def _load_config(self) -> LangChainConfig:
        """从环境变量加载配置，并封装为 LangChainConfig（Pydantic 模型）"""
        api_key = "sk-47513f93dfbd4082b3c15e51a2d58bb3"
        if not api_key:
            print("[警告] 未检测到DEEPSEEK_API_KEY环境变量，使用默认测试密钥")
            print("   请在运行前设置环境变量：")
            print("   Windows CMD: set DEEPSEEK_API_KEY=你的密钥")
            print("   Windows PowerShell: $env:DEEPSEEK_API_KEY='你的密钥'")
            print("   Linux/macOS: export DEEPSEEK_API_KEY='你的密钥'")
            api_key = "sk-47513f93dfbd4082b3c15e51a2d58bb3"

        return LangChainConfig(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            temperature=0.1,
            max_tokens=2000,
            timeout=30,
            max_retries=3,
        )

    def _create_llm(self) -> ChatOpenAI:
        """创建 LangChain LLM 实例，用于与 DeepSeek API 通信"""
        # 创建自定义的 httpx 客户端，避免 proxies 参数兼容性问题
        http_client = httpx.Client(
            timeout=self.config.timeout,
            limits=httpx.Limits(max_connections=10)
        )
        
        return ChatOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            http_client=http_client
        )
