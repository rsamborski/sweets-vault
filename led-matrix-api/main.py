import uvicorn
import os

def main():
    # Allow configuring host/port via env vars if needed
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    # Run the app
    # reload=True is useful for dev, but we can make it conditional or just default for now
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
