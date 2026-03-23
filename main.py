from fastmcp import FastMCP
import random 
import json
#create mcp
mcp=FastMCP("Simple calculator Server")
#tool :Add Two Numbers
@mcp.tool()
def add(a:int,b:int)->int:
    """Add Two numbers together 
    Args 
    a:First Number 
    b:Second Number
    Returns 
    the sum of a and b 
    """
    return a+b
#tool generate a random number 
@mcp.tool()
def random_number(min_val:int=1,max_val:int=100)->int:
    """Generate a random number within a range 
    AGrs
    min_value:minimum value (default:1)
    max_value:maximum value (default:100)
    Returns 
    A Randon integer between min_val and max_value

    """
    return random.randint(min_val,max_val)
@mcp.resource("info://server")
def server_info()->str:
    """Get information about the server"""
    info={
        "name":"Simple Caluclator Server",
        "version":"1.0.0",
        "description":"A basic Mcp server with math tools",
        "tools":["add","random_number"],
        "author":"your name"

        }
    return json.dumps(info,indent=2)



if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)