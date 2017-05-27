from sys import path
from os.path import abspath, join, dirname
from dotenv import load_dotenv, find_dotenv

base_path = abspath(dirname(dirname(__file__)))
source_path = join(base_path, "src")
path.append(source_path)

# Load .env files for local development
load_dotenv(find_dotenv())
