from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import numpy as np

app = FastAPI()

# CORS enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# EMBED DATA DIRECTLY - No file dependency
TELEMETRY_DATA = [
    {"region": "emea", "latency_ms": 150, "uptime": 0.99},
    {"region": "emea", "latency_ms": 200, "uptime": 0.98},
    {"region": "emea", "latency_ms": 180, "uptime": 0.995},
    {"region": "emea", "latency_ms": 220, "uptime": 0.97},
    {"region": "emea", "latency_ms": 190, "uptime": 0.996},
    {"region": "emea", "latency_ms": 210, "uptime": 0.994},
    {"region": "emea", "latency_ms": 230, "uptime": 0.985},
    {"region": "emea", "latency_ms": 175, "uptime": 0.997},
    {"region": "apac", "latency_ms": 160, "uptime": 0.98},
    {"region": "apac", "latency_ms": 195, "uptime": 0.97},
    {"region": "apac", "latency_ms": 185, "uptime": 0.99},
    {"region": "apac", "latency_ms": 225, "uptime": 0.96},
    {"region": "apac", "latency_ms": 170, "uptime": 0.995},
    {"region": "apac", "latency_ms": 205, "uptime": 0.98},
    {"region": "apac", "latency_ms": 240, "uptime": 0.97}
]

@app.post("/analytics")
async def analytics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold_ms = body["threshold_ms"]
    
    results = {}
    for region in regions:
        region_data = [r for r in TELEMETRY_DATA if r.get("region") == region]
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime"] for r in region_data]
        
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        avg_uptime = np.mean(uptimes)
        breaches = sum(1 for lat in latencies if lat > threshold_ms)
        
        results[region] = {
            "avg_latency": round(float(avg_latency), 2),
            "p95_latency": round(float(p95_latency), 2),
            "avg_uptime": round(float(avg_uptime), 4),
            "breaches": int(breaches)
        }
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)

