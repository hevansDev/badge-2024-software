# Fake aiorepl module for simulator
# This module is MicroPython-specific and not needed in the simulator

import asyncio

class REPL:
    def __init__(self):
        pass

async def task():
    """Fake async task for aiorepl - just sleeps forever in simulator"""
    while True:
        await asyncio.sleep(1)

def start():
    pass
