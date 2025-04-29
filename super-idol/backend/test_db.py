from database import get_db, engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """
    Test the database connection.
    
    This function will:
    1. Try to connect to the database
    2. Execute a simple query
    3. Print the result
    """
    try:
        # Test using engine directly
        logger.info("Testing connection using engine...")
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("Engine connection successful!")
            print("Engine connection test passed!")
        
        # Test using session
        logger.info("\nTesting connection using session...")
        db = next(get_db())
        try:
            result = db.execute("SELECT 1")
            logger.info("Session connection successful!")
            print("Session connection test passed!")
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        print(f"Connection test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_connection() 