#!/usr/bin/env python3
"""
Send a task_status notification to the notification_server MCP server.
"""

import asyncio

from fastmcp import Client

async def main() -> None:
    client = Client("server.py")
    payload = {'status': 'success'}
    # payload = {'status': 'start', 'title': 'Batch Job', 'message': 'Job has started'}
    # payload = {'status': 'start', 'title': 'Batch Job', 'message': 'Job has started', 'sound': 'Glass'}

    async with client:
        result = await client.call_tool("task_status", payload)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
