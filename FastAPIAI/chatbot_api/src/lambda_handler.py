from mangum import Mangum
from main import app

# Mangum adapter for FastAPI
handler = Mangum(app)