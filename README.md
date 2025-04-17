# Mac Notification MCP Server

A tool that sets up an MCP server to send macOS notifications when tasks start and complete in applications like Claude for Desktop.

## Overview

This tool displays the status of AI assistants like Claude in the macOS Notification Center when they perform time-consuming tasks. You can configure different notifications and sounds for task start, completion, and error events.

## Features

- Displays notifications in macOS Notification Center when tasks start, complete, or encounter errors
- Configurable sounds for each notification type
- Customizable via environment variables
- Integrates as an MCP tool for easy invocation from Claude for Desktop and other clients

## Requirements

- macOS
- Python 3.6 or higher
- fastmcp library

## Installation

1. Clone the repository:

```bash
git clone https://github.com/masakiq/mac-notification-mcp-server.git
cd mac-notification-mcp-server
```

2. Install dependencies:

```bash
pip install fastmcp
```

## Client Configuration

Adding MCP config to your client:

```json
{
  "mcpServers": {
    "notification": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/{path}/mac-notification-mcp-server/server.py"
      ]
    }
  }
}
```

Replace `{path}` with the actual path to the cloned repository.

## Usage

### Starting the Server

```bash
python server.py
```

### Integration with Claude

You can invoke the tool from Claude for Desktop or other MCP clients as follows:

```python
# Notification at task start
task_status(status="start", message="Analysis started", title="Task Started")

# Processing content
# ...

# Notification at task completion
task_status(status="complete", message="Analysis completed", title="Task Completed")
```

### Customization

You can customize notification titles, messages, and sounds using environment variables:

- `CLAUDE_START_TITLE`: Notification title at start
- `CLAUDE_START_MESSAGE`: Message at start
- `CLAUDE_START_SOUND`: Sound at start
- `CLAUDE_COMPLETE_TITLE`: Notification title at completion
- `CLAUDE_COMPLETE_MESSAGE`: Message at completion
- `CLAUDE_COMPLETE_SOUND`: Sound at completion
- `CLAUDE_ERROR_TITLE`: Notification title on error
- `CLAUDE_ERROR_MESSAGE`: Message on error
- `CLAUDE_ERROR_SOUND`: Sound on error

Example:

```bash
export CLAUDE_START_SOUND="Glass"
export CLAUDE_COMPLETE_SOUND="Hero"
export CLAUDE_ERROR_SOUND="Basso"
```

### Available Sounds

macOS includes several built-in system sounds you can choose from:

- Basso
- Blow
- Bottle
- Frog
- Funk
- Glass
- Hero
- Morse
- Ping
- Pop
- Purr
- Sosumi
- Submarine
- Tink

## API Reference

### task_status

```python
task_status(status: str, message: Optional[str] = None, title: Optional[str] = None, sound: Optional[str] = None)
```

- `status`: Notification type ('start', 'complete', 'error')
- `message`: Notification message (optional)
- `title`: Notification title (optional)
- `sound`: Notification sound (optional)

Return value:

```json
{
  "success": true,
  "type": "complete",
  "title": "Processing Complete",
  "message": "Processing has completed",
  "timestamp": 1618278341.123
}
```

## Call Server

### Call the server via STDIN/OUT

You can call the server using the following command:

```bash
python server.py
```

Then, please execute the following as standard input:

```bash
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"manual-client","version":"0.1.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"task_status","arguments":{"status":"start"}}}
```

### Call the server via Python client

```python
python call_server.py
```

## License

MIT

## Contributing

Please report bugs and feature requests via GitHub Issues. Pull requests are welcome.
