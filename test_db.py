from app.database import test_connection

result = test_connection()
print("PostgreSQL connection successful:", result)