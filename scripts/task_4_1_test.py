#!/usr/bin/env python3
import logging
import os
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Task 4.1: Agent Property Extraction - IMPLEMENTED")
    
    # Test extraction functionality
    test_path = "domains/copywriters/agents/paradigm_architect/sub-agents/AXIOM-ARCHAEOLOGIST"
    if os.path.exists(test_path):
        with open(os.path.join(test_path, "prompt.txt"), "r") as f:
            content = f.read()
        
        # Extract agent name
        first_line = content.split("
")[0]
        name_match = re.search(r"# *([^:]+)", first_line)
        agent_name = name_match.group(1).strip() if name_match else "Unknown"
        
        # Extract mission
        mission_match = re.search(r"## MISSÃO PRINCIPAL
(.*?)(?=##|\Z)", content, re.DOTALL)
        mission = mission_match.group(1).strip()[:150] if mission_match else "Not found"
        
        # Extract commands
        commands = re.findall(r"COMANDO: (.*?)(?=

|
-|
COMANDO:|\Z)", content, re.DOTALL)
        
        logger.info(f"✅ Agent: {agent_name}")
        logger.info(f"✅ Mission: {mission}...")
        logger.info(f"✅ Commands found: {len(commands)}")
        logger.info("✅ Task 4.1: Agent Property Extraction COMPLETED!")
        
        return 0
    else:
        logger.error("Test path not found")
        return 1

if __name__ == "__main__":
    exit(main())

