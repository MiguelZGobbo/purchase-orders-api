import os
import subprocess
import sys
from pathlib import Path


def test_seed_script_loads_dotenv_when_invoked_directly(tmp_path):
    database = tmp_path / 'seed.db'
    (tmp_path / '.env').write_text(
        f'DB_URI=sqlite:///{database.as_posix()}\nJWT_SECRET_KEY=seed-test-secret\n',
        encoding='utf-8',
    )
    environment = os.environ.copy()
    environment.pop('DB_URI', None)
    environment.pop('JWT_SECRET_KEY', None)
    script = Path(__file__).resolve().parents[1] / 'scripts' / 'seed.py'

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert 'Banco populado com sucesso!' in result.stdout
    assert database.exists()
