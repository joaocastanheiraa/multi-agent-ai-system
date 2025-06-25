
from mcp.server.fastmcp import FastMCP
import json
from datetime import datetime

mcp = FastMCP("CustomTools")

@mcp.tool()
def get_system_info() -> str:
    """Obter informações do sistema"""
    import platform
    return json.dumps({
        "system": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat()
    })

@mcp.tool()
def calculate_fibonacci(n: int) -> str:
    """Calcular sequência de Fibonacci até n"""
    if n <= 0:
        return "[]"
    elif n == 1:
        return "[0]"
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return json.dumps(fib)

if __name__ == "__main__":
    mcp.run(transport="stdio")
