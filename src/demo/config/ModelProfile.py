"""模型Profile管理类"""

class ModelProfile:
    @staticmethod
    def deepseek32_fast_profile() -> dict:
        """DeepSeekV3.2 快速配置"""
        return {
            "max_input_tokens": 16000,
            "max_output_tokens": 8192,
            "temperature": 0.3,
            "model_name": "deepseek-chat",
            "timeout": 30,
            "rate_limit": 3500,
            "description": "快速响应配置，适合简单任务"
    }