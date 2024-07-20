import dotenv
import os


dotenv.load_dotenv()

# Access environment variables as if they came from the actual environment
SECRET_KEY = os.getenv('kustikov')

# Example usage
print(f'SECRET_KEY: {SECRET_KEY}')