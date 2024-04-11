import time
import numpy as np
import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

activity_state = "normal"
state_change_time = time.time()  # Track when the last state change occurred

## Healthy Dog Data Simulation

def get_next_state():
    global activity_state, state_change_time
    now = time.time()
    time_in_current_state = now - state_change_time
    
    # Define average duration for each state in seconds
    durations = {"normal": 300, "high_activity": 60, "rest": 600, "cooldown": 120}
    
    # Transition conditions
    if activity_state == "normal" and time_in_current_state > durations["normal"]:
        if random.random() < 0.2:  # 20% chance to switch to high activity
            activity_state = "high_activity"
        else:
            activity_state = "rest"
        state_change_time = now
        
    elif activity_state == "high_activity" and time_in_current_state > durations["high_activity"]:
        activity_state = "cooldown"
        state_change_time = now
        
    elif activity_state == "cooldown" and time_in_current_state > durations["cooldown"]:
        activity_state = "normal"
        state_change_time = now
        
    elif activity_state == "rest" and time_in_current_state > durations["rest"]:
        activity_state = "normal"
        state_change_time = now

def fake_sensor_data():
    while True:
        get_next_state()
        
        # Generate data based on the current state
        if activity_state == "normal":
            heart_rate = int(np.random.normal(loc=80, scale=10))
            steps = random.randint(0, 20)
        elif activity_state == "high_activity":
            heart_rate = int(np.random.normal(loc=140, scale=20))
            steps = random.randint(20, 60)
        elif activity_state == "rest":
            heart_rate = int(np.random.normal(loc=60, scale=5))
            steps = random.randint(0, 2)
        elif activity_state == "cooldown":
            heart_rate = int(np.random.normal(loc=100, scale=10))
            steps = random.randint(10, 20)
        
        data = f"Timestamp: {datetime.now().isoformat()}, State: {activity_state}, Heart Rate: {heart_rate}, Steps: {steps}\n"
        yield data.encode()
        time.sleep(1)

## Sick Dog Data Simulation
def get_next_state_sick():
    global activity_state, state_change_time
    now = time.time()
    time_in_current_state = now - state_change_time

    # Adjusted durations for a sick dog
    durations = {"normal": 600, "high_activity": 30, "rest": 1200, "cooldown": 180}
    
    # Transition conditions adjusted for low activity
    if activity_state == "normal" and time_in_current_state > durations["normal"]:
        if random.random() < 0.05:  # Reduced chance for high activity
            activity_state = "high_activity"
        else:
            activity_state = "rest"
        state_change_time = now
        
    elif activity_state == "high_activity" and time_in_current_state > durations["high_activity"]:
        activity_state = "cooldown"
        state_change_time = now
        
    elif activity_state == "cooldown" and time_in_current_state > durations["cooldown"]:
        activity_state = "normal"
        state_change_time = now
        
    elif activity_state == "rest" and time_in_current_state > durations["rest"]:
        activity_state = "normal"
        state_change_time = now

def fake_sensor_data_sick():
    while True:
        get_next_state_sick()
        
        # Generate data based on the current state with added randomness for erratic behavior
        heart_rate = int(np.random.normal(loc=80, scale=20))
        steps = random.randint(0, 10)
        
        # Introduce erratic heart rate and steps
        if random.random() < 0.1:  # 10% chance for erratic heart rate
            heart_rate = heart_rate + random.randint(-40, 40)
        if random.random() < 0.05:  # 5% chance for very low steps
            steps = steps - random.randint(0, 5)
        
        data = f"Timestamp: {datetime.now().isoformat()}, State: {activity_state}, Heart Rate: {heart_rate}, Steps: {steps}\n"
        yield data.encode()
        time.sleep(1)

@app.get("/data/stream")
async def stream_data():
    return StreamingResponse(fake_sensor_data(), media_type="text/event-stream")

@app.get("/data/sick/stream")
async def stream_data():
    return StreamingResponse(fake_sensor_data_sick(), media_type="text/event-stream")