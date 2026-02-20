from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import numpy as np
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    try:
        body = await request.json()
        regions = body["regions"]
        threshold_ms = body["threshold_ms"]
        
        # Vercel-safe file read (handles serverless paths)
        file_path = os.path.join(os.path.dirname(__file__), "q-vercel-latency.json")
        with open(file_path, "r") as f:
            data = json.load(f)
        
        results = {}
        for region in regions:
            region_data = [r for r in data if r.get("region") == region]
            latencies = [r["latency_ms"] for r in region_data if "latency_ms" in r]
            uptimes = [r["uptime"] for r in region_data if "uptime" in r]
            
            avg_latency = np.mean(latencies) if latencies else 0
            p95_latency = np.percentile(latencies, 95) if latencies else 0
            avg_uptime = np.mean(uptimes) if uptimes else 0
            breaches = sum(1 for lat in latencies if lat > threshold_ms)
            
            results[region] = {
                "avg_latency": round(float(avg_latency), 2),
                "p95_latency": round(float(p95_latency), 2),
                "avg_uptime": round(float(avg_uptime), 4),
                "breaches": int(breaches)
            }
        return results
        
    except Exception as e:
        return {"error": str(e)}  # Debug info

# Local runner (remove for Vercel)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
