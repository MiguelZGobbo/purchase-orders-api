from scripts import smoke_compose


def test_wait_for_api_retries_connection_reset(monkeypatch):
    attempts = 0

    def request(method, path):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ConnectionResetError('API ainda está iniciando')
        return 200, {'status': 'healthy'}

    monkeypatch.setattr(smoke_compose, 'request', request)
    monkeypatch.setattr(smoke_compose.time, 'sleep', lambda _: None)

    smoke_compose.wait_for_api()

    assert attempts == 2
