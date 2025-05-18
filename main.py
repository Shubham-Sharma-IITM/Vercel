from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

app = FastAPI()

# Enable CORS: Allow all origins for GET requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow any origin
    allow_methods=["GET"],      # Allow only GET requests
    allow_headers=["*"],        # Allow any headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/api")
def get_marks(name: List[str] = Query(...)):
    try:
        with open("q-vercel-python.json") as f:
            data = json.load(f)

        # Create a mapping from name to marks
        name_to_marks = {entry["name"]: entry["marks"] for entry in data}

        # Retrieve marks in the order names were provided
        marks = [name_to_marks.get(n, None) for n in name]

        return {"marks": marks}

    except FileNotFoundError:
        return {"error": "q-vercel-python.json not found"}
    except Exception as e:
        return {"error": str(e)}
