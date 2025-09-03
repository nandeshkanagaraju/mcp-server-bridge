import logging

logger = logging.getLogger("MCPServer")
logger.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler("mcp_server.log")
fh.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Add handlers
logger.addHandler(ch)
logger.addHandler(fh)
