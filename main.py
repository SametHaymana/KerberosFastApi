import uvicorn
from dotenv import load_dotenv
import os
from src.app import app



if __name__ == '__main__':
    load_dotenv()
    
    port = int(os.getenv('PORT')) if os.getenv('PORT') else 5000
    
    uvicorn.run(app, host="0.0.0.0", port=port)