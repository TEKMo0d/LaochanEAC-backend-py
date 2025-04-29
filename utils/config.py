import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @property
    def port(self) -> int:
        return int(os.environ.get("PORT", 25730))

    @property
    def self_url(self) -> str:
        return os.environ.get("SELF_URL", "http://localhost:25730")

    @property
    def ntp_url(self) -> str:
        return os.environ.get("NTP_URL", "ntp://pool.ntp.org")

    @property
    def mongo_url(self) -> str:
        return os.environ.get("MONGO_URL", "mongodb://localhost:27017")

    @property
    def db_name(self) -> str:
        return os.environ.get("DB_NAME", "laochan-eacnet")

    @property
    def is_dev(self) -> bool:
        return os.environ.get("NODE_ENV") != "production"

config = Config()
default_config = config
