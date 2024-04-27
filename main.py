import time
import numpy as np
import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

activity_state = "normal"
state_change_time = time.time()  # Track when the last state change occurred

def get_next_state():
    global activity_state, state_change_time
    now = time.time()
    time_in_current_state = now - state_change_time
    
    durations = {"normal": 300, "high_activity": 60, "rest": 600, "cooldown": 120}
    
    if activity_state == "normal" and time_in_current_state > durations["normal"]:
        if random.random() < 0.2:
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
        
        if activity_state == "normal":
            heart_rate = int(np.random.normal(loc=80, scale=10))
            steps = random.randint(0, 20)
            temperature = float(np.random.normal(loc=38.5, scale=0.5))
        elif activity_state == "high_activity":
            heart_rate = int(np.random.normal(loc=140, scale=20))
            steps = random.randint(20, 60)
            temperature = float(np.random.normal(loc=39.5, scale=0.7))
        elif activity_state == "rest":
            heart_rate = int(np.random.normal(loc=60, scale=5))
            steps = random.randint(0, 2)
            temperature = float(np.random.normal(loc=37.5, scale=0.3))
        elif activity_state == "cooldown":
            heart_rate = int(np.random.normal(loc=100, scale=10))
            steps = random.randint(10, 20)
            temperature = float(np.random.normal(loc=38.0, scale=0.4))
        
        timestamp = datetime.now().isoformat()
        data = f"{steps} | {temperature:.2f} | {heart_rate} | {timestamp}\n"
        yield data.encode()
        time.sleep(5)

def get_next_state_sick():
    global activity_state, state_change_time
    now = time.time()
    time_in_current_state = now - state_change_time

    durations = {"normal": 600, "high_activity": 30, "rest": 1200, "cooldown": 180}
    
    if activity_state == "normal" and time_in_current_state > durations["normal"]:
        if random.random() < 0.05:
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

        activity_state = "high_activity"
        
        # Data generation with variability suited to a sick dog
        if activity_state == "normal":
            heart_rate = int(np.random.normal(loc=80, scale=20))
            steps = random.randint(0, 10)
            temperature = float(np.random.normal(loc=38.7, scale=0.6))
        elif activity_state == "high_activity":
            heart_rate = int(np.random.normal(loc=140, scale=30))
            steps = random.randint(0, 10)
            temperature = float(np.random.normal(loc=39.7, scale=0.8))
        elif activity_state == "rest":
            heart_rate = int(np.random.normal(loc=60, scale=7))
            steps = random.randint(0, 5)
            temperature = float(np.random.normal(loc=37.8, scale=0.5))
        elif activity_state == "cooldown":
            heart_rate = int(np.random.normal(loc=100, scale=15))
            steps = random.randint(5, 15)
            temperature = float(np.random.normal(loc=38.3, scale=0.5))
        
        timestamp = datetime.now().isoformat()
        data = f"{steps} | {temperature:.2f} | {heart_rate} | {timestamp}\n"
        yield data.encode()
        time.sleep(5)

@app.get("/data/stream")
async def stream_data():
    return StreamingResponse(fake_sensor_data(), media_type="text/event-stream")

@app.get("/data/sick/stream")
async def stream_data():
    return StreamingResponse(fake_sensor_data_sick(), media_type="text/event-stream")
