"""敏感信息脱敏测试（以下均为伪造值，不是真实凭据）。"""
API_KEY = "sk-fake-1234567890abcdef"
GITHUB_TOKEN = "ghp_FAKE1234567890abcdefghijklmnopqrstuv"
DB_PASSWORD = "SuperSecret123!"
DATABASE_URL = "postgresql://admin:SuperSecret123!@db.example.com:5432/app"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
FAKEKEYMATERIAL1234567890
-----END RSA PRIVATE KEY-----"""


def connect():
    return {"Authorization": f"Bearer {GITHUB_TOKEN}", "url": DATABASE_URL}
