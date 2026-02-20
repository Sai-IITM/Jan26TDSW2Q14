from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Embedded sample data (serverless compatible)
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
        
        results[region] = {
            "avg_latency": round(np.mean(latencies), 2),
            "p95_latency": round(np.percentile(latencies, 95), 2),
            "avg_uptime": round(np.mean(uptimes), 4),
            "breaches": sum(1 for lat in latencies if lat > threshold_ms)
        }
    
    return results


