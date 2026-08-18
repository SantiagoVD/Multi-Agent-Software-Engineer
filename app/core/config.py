from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Software Engineer"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:8b"
    ollama_num_gpu: int | None = None
    ollama_timeout_seconds: int = 300
    ollama_think: bool = False
    ollama_num_predict: int = 512
    review_llm_enabled: bool = False

    git_author_name: str = "Multi-Agent Software Engineer"
    git_author_email: str = "agent@users.noreply.github.com"

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
