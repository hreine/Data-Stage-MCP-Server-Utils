from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def process_data(input: str) -> str:
    """Process data on the server"""
    return f"Processed: {input}"

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
