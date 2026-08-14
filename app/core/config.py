from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Software Engineer"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:8b"
    ollama_num_gpu: int | None = 0
    ollama_timeout_seconds: int = 600

    frontend_origin: str = "http://localhost:5173"

    workspace_root: str = "./workspaces"

    max_workflow_iterations: int = 3

    test_timeout_seconds: int = 120
    command_timeout_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
