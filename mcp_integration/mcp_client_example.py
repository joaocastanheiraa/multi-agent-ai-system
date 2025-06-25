#!/usr/bin/env python3
"""
Cliente MCP exemplo
"""

import asyncio
import aiohttp
import json

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    async def list_agents(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/agents") as response:
                return await response.json()
    
    async def call_agent(self, agent_name, method, payload):
        data = {"agent_name": agent_name, "method": method, "payload": payload}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/agent/process", json=data) as response:
                return await response.json()

async def example():
    client = MCPClient()
    agents = await client.list_agents()
    print("Agentes:", json.dumps(agents, indent=2))

if __name__ == "__main__":
    asyncio.run(example())
