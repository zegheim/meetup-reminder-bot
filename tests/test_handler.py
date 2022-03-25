from src.handler import lambda_handler


def test_lambda_handler():
    assert lambda_handler({}, {}) == "Hello from Terraform!"
