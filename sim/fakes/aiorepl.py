# Fake aiorepl module for simulator
# This module provides an async REPL in MicroPython but is not needed in simulator

import asyncio

class REPL:
    def __init__(self):
        pass

async def task():
    """Fake async task for aiorepl - runs but doesn't interfere with simulator"""
    # Just await forever without doing anything
    # This keeps the task alive without consuming resources
    await asyncio.Event().wait()

def start():
    pass
