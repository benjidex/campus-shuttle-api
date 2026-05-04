from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Campus Shuttle API")

# In-memory database
rides = []

# Data model
class Ride(BaseModel):
    user: str
    pickup: str
    destination: str

# Helper function
def find_ride(ride_id: int):
    for ride in rides:
        if ride["id"] == ride_id:
            return ride
    return None

# Create ride
@app.post("/rides")
def create_ride(ride: Ride):
    new_ride = {
        "id": len(rides) + 1,
        "user": ride.user,
        "pickup": ride.pickup,
        "destination": ride.destination,
        "status": "pending"
    }
    rides.append(new_ride)
    return new_ride

# Get all rides
@app.get("/rides")
def get_rides():
    return rides

# Assign ride
@app.put("/rides/{ride_id}/assign")
def assign_ride(ride_id: int):
    ride = find_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    if ride["status"] != "pending":
        raise HTTPException(status_code=400, detail="Ride already assigned or completed")

    ride["status"] = "assigned"
    ride["shuttle"] = "Shuttle A"
    return ride

# Complete ride
@app.put("/rides/{ride_id}/complete")
def complete_ride(ride_id: int):
    ride = find_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    if ride["status"] != "assigned":
        raise HTTPException(status_code=400, detail="Ride must be assigned first")

    ride["status"] = "completed"
    return ride

# Delete ride
@app.delete("/rides/{ride_id}")
def delete_ride(ride_id: int):
    ride = find_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    rides.remove(ride)
    return {"message": "Ride deleted"}