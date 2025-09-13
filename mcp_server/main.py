from servidor import create_mcp_server
from utilidades.cache import init_cache_db

    
# Entry point to run the servercd 
if __name__ == "__main__":
    init_cache_db() # Initialize the cache database
    mcp=create_mcp_server()
    #mcp.run(transport="stdio")
    mcp.run(transport="http", host="127.0.0.1", port=8000)




