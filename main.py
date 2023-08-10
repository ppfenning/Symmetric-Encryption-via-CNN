from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
from audio_encrypter.verify import compare_files, run_folder_stats

config = Path("config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
PLAIN_FILES = DATADIR.joinpath("plaintext")
ENCRYPTED_FILES = DATADIR.joinpath("encrypted")
DECRYPTED_FILES = DATADIR.joinpath("decrypted")
KEYPATH = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))

DATADIR.mkdir(exist_ok=True)
PLAIN_FILES.mkdir(exist_ok=True)
ENCRYPTED_FILES.mkdir(exist_ok=True)
DECRYPTED_FILES.mkdir(exist_ok=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_folder_stats(ENCRYPTED_FILES, DECRYPTED_FILES, "", 1, KEYPATH)
