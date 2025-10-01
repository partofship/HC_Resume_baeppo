from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EMAIL_PROVIDER: str = "gmail"

    EMAIL_USER: str
    EMAIL_PASS: str

    CONTACT_EMAIL: str = "hanyul0417@gmail.com"

    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        if self.EMAIL_PROVIDER == "naver":
            self.EMAIL_HOST = "smtp.naver.com"
            self.EMAIL_PORT = 587
        elif self.EMAIL_PROVIDER == "gmail":
            self.EMAIL_HOST = "smtp.gmail.com"
            self.EMAIL_PORT = 587
        else:
            raise ValueError(
                "지원하지 않는 메일 서비스입니다. (naver/gmail만 사용 가능)"
            )


settings = Settings()
