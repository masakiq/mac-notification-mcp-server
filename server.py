#!/usr/bin/env python3
# claude_notification_server.py
"""
Notify the Mac when the response is complete from the MCP server.
"""

import os
import subprocess
import time
from enum import Enum
from typing import Optional, Dict, Any

from fastmcp import FastMCP, Context

mcp = FastMCP("Notification Server",
              description="MCP server that notifies the processing status",
              dependencies=["fastmcp"])

class NotificationType(str, Enum):
    START = "start"
    COMPLETE = "complete"
    ERROR = "error"

DEFAULT_SOUNDS = {
    NotificationType.START: "Glass",
    NotificationType.COMPLETE: "Hero",
    NotificationType.ERROR: "Basso"
}

DEFAULT_TITLES = {
    NotificationType.START: "Processing started",
    NotificationType.COMPLETE: "Processing finished",
    NotificationType.ERROR: "Processing error"
}

DEFAULT_MESSAGES = {
    NotificationType.START: "Processing has started",
    NotificationType.COMPLETE: "Processing is complete",
    NotificationType.ERROR: "An error occurred during processing"
}

def send_mac_notification(title: str, message: str, sound_name: Optional[str] = None):
    """Send notifications to the macOS Notification Center"""
    try:
        script = f'display notification "{message}" with title "{title}"'

        if sound_name:
            if not sound_name.endswith(".aiff"):
                sound_name = f"{sound_name}.aiff"

            subprocess.run(["afplay", f"/System/Library/Sounds/{sound_name}"],
                          stderr=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL)

        subprocess.run(["osascript", "-e", script],
                      stderr=subprocess.DEVNULL,
                      stdout=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"Notification error: {e}")
        return False

def get_config(notification_type: NotificationType, config_type: str):
    # Creating environment variable names (e.g., CLAUDE_START_SOUND, CLAUDE_COMPLETE_TITLE)
    env_var = f"CLAUDE_{notification_type.upper()}_{config_type.upper()}"

    if config_type.lower() == "sound":
        defaults = DEFAULT_SOUNDS
    elif config_type.lower() == "title":
        defaults = DEFAULT_TITLES
    elif config_type.lower() == "message":
        defaults = DEFAULT_MESSAGES
    else:
        return None

    return os.environ.get(env_var, defaults.get(notification_type))

@mcp.tool()
async def task_status(status: str, ctx: Context, message: Optional[str] = None,
                     title: Optional[str] = None, sound: Optional[str] = None) -> Dict[str, Any]:
    """
    Notify the processing status of Claude

    Args:
        status: Type of notification ('start', 'complete', 'error')
        message: Custom notification message (optional)
        title: Custom notification title (optional)
        sound: Custom sound name (optional)
        ctx: MCP context

    Returns:
        A dictionary containing the result of the notification
    """
    try:
        try:
            notification_type = NotificationType(status.lower())
        except ValueError:
            await ctx.warning(f"Unknown notification type: {status}. Processing as ‘complete’.")
            notification_type = NotificationType.COMPLETE

        notification_title = title or get_config(notification_type, "title")
        notification_message = message or get_config(notification_type, "message")
        notification_sound = sound or get_config(notification_type, "sound")

        await ctx.info(f"Send notification: {notification_type} - {notification_title}")

        success = send_mac_notification(
            title=notification_title,
            message=notification_message,
            sound_name=notification_sound
        )

        return {
            "success": success,
            "type": notification_type,
            "title": notification_title,
            "message": notification_message,
            "timestamp": time.time()
        }

    except Exception as e:
        await ctx.error(f"Notification error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": time.time()
        }

@mcp.resource("config://notification-settings")
async def get_notification_settings() -> Dict[str, Any]:
    """
    Retrieve current notification settings
    """
    settings = {}

    for notification_type in NotificationType:
        settings[notification_type] = {
            "title": get_config(notification_type, "title"),
            "message": get_config(notification_type, "message"),
            "sound": get_config(notification_type, "sound")
        }

    system_sounds = [
        "Basso", "Blow", "Bottle", "Frog", "Funk",
        "Glass", "Hero", "Morse", "Ping", "Pop",
        "Purr", "Sosumi", "Submarine", "Tink"
    ]

    settings["available_sounds"] = system_sounds
    return settings

if __name__ == "__main__":
    mcp.run()
