import os
import shutil

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

try:
    MISTRAL_API_KEY = os.environ['MISTRAL_API_KEY']
except:
    print('Environment variable `MISTRAL_API_KEY` not set - exiting')
    os._exit(1)

try:
    # Supprime la base de données initiale si nécessaire
    shutil.rmtree(f'{DATA_DIR}/qdrant_database')
except FileNotFoundError:
    pass

from .prompting import run_model