import sys
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crawler import crawl_fare_data

app = FastAPI(title="crawl-surff API")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/fares")
def get_fares(cntr_type: str, pol: str, pod: str, period: str = "6개월"):
    """
    Endpoint to retrieve fare data using the crawler.
    By using 'def' instead of 'async def', FastAPI assigns this to a background thread.
    This prevents Uvicorn's SelectorEventLoop policy on Windows from colliding with Playwright,
    which strictly requires a ProactorEventLoop to manage Chromium subprocesses.
    """
    try:
        print(f"Received request for {cntr_type}, {pol} to {pod} for {period}")
        
        # Instantiate a proper event loop for this thread based on OS
        if sys.platform == "win32":
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()
            
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(crawl_fare_data(cntr_type, pol, pod, period))
        finally:
            loop.close()
            
        if result["status"] == "success" and result.get("data"):
            return result
        else:
            raise HTTPException(status_code=404, detail="Fare data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files from the React build
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

@app.exception_handler(404)
async def custom_404_handler(request, exc):
    # For SPA routing, serve index.html for 404s if it's not an API route
    if request.url.path.startswith("/api/"):
        return {"detail": exc.detail}
    index_path = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Not Found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
