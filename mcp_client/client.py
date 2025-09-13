import requests
import json

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

def send_mcp_request(method: str, params: dict, request_id: int = 1):
    """Sends a JSON-RPC 2.0 request to the MCP server."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }
    
    try:
        response = requests.post(MCP_SERVER_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        # Parse SSE format if present
        if "data: " in response.text:
            for line in response.text.splitlines():
                if line.startswith("data: "):
                    json_str = line[len("data: "):].strip()
                    return json.loads(json_str)
            # If data: line is not found after splitting, fall back to original json()
            return response.json()
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Server response: {e.response.text}")
        return None

def discover_mcp_tools():
    """Performs an mcp/discover request with a dummy session ID."""
        
    response = send_mcp_request("tools/list", {})
    if response:
        if "result" in response:
            print("Discovery successful! Available tools:")
            for tool in response["result"]["tools"]:
                print(f"  - Name: {tool.get('name')}, Description: {tool.get('description')}")
        elif "error" in response:
            print(f"Discovery failed with error: {response['error']['message']}")
            if "Missing session ID" in response['error']['message']:
                print("The server still reports a missing session ID, even with a dummy one provided.")
                print("This suggests the server is validating the session ID, not just checking for its presence.")
            elif "Invalid session ID" in response['error']['message']:
                print("The server reports an invalid session ID. This is expected as we provided a dummy one.")
                print("This confirms the server is validating the session ID.")
        else:
            print(f"Unexpected response format: {response}")
    else:
        print("No response received from the server for discovery.")

if __name__ == "__main__":
    discover_mcp_tools()