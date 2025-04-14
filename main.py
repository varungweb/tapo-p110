import os
import asyncio
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tapo import ApiClient
from tapo.requests import EnergyDataInterval

app = FastAPI()


def get_quarter_start_month(today: datetime) -> int:
    return 3 * ((today.month - 1) // 3) + 1


async def get_device():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("IP_ADDRESS")

    client = ApiClient(tapo_username, tapo_password)
    return await client.p110(ip_address)


@app.get("/")
async def status():
    return {"status": "Tapo Controller is running."}


@app.get("/on")
async def turn_on():
    device = await get_device()
    await device.on()
    return {"status": "Device turned on."}


@app.get("/off")
async def turn_off():
    device = await get_device()
    await device.off()
    return {"status": "Device turned off."}


@app.get("/info")
async def device_info():
    device = await get_device()
    info = await device.get_device_info()
    return JSONResponse(content=info.to_dict())


@app.get("/usage")
async def usage():
    device = await get_device()
    usage = await device.get_device_usage()
    return JSONResponse(content=usage.to_dict())


@app.get("/power")
async def power():
    device = await get_device()
    power = await device.get_current_power()
    return JSONResponse(content=power.to_dict())


@app.get("/energy/hourly")
async def energy_hourly():
    device = await get_device()
    today = datetime.today()
    energy = await device.get_energy_data(EnergyDataInterval.Hourly, today)
    return JSONResponse(content=energy.to_dict())


@app.get("/energy/daily")
async def energy_daily():
    device = await get_device()
    today = datetime.today()
    energy = await device.get_energy_data(
        EnergyDataInterval.Daily,
        datetime(today.year, get_quarter_start_month(today), 1)
    )
    return JSONResponse(content=energy.to_dict())


@app.get("/energy/monthly")
async def energy_monthly():
    device = await get_device()
    today = datetime.today()
    energy = await device.get_energy_data(
        EnergyDataInterval.Monthly,
        datetime(today.year, 1, 1)
    )
    return JSONResponse(content=energy.to_dict())
