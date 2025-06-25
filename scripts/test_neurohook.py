#!/usr/bin/env python3
"""
Test logic flow extraction on neurohook_ultra agent
"""

import os
import re

def test_neurohook_extraction():
    """Test the logic flow extraction on neurohook"""
    test_agent_path = "domains/copywriters/agents/neurohook_ultra/prompt.txt"
    
    if os.path.exists(test_agent_path):
        with open(test_agent_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        
        print(f"🧠 TESTING NEUROHOOK LOGIC FLOW EXTRACTION")
        print(f"📄 File: {test_agent_path}")
        print(f"📏 Content length: {len(prompt_text)} characters")
        
        # Extract phases
        phase_patterns = [
            r'\[PHASE\s+(\d+)\]\s*([^\[\n]+)',
            r'PHASE\s+(\d+)[\]\s]*([^\[\n]+)'
        ]
        
        all_phases = []
        for pattern in phase_patterns:
            phases = re.findall(pattern, prompt_text, re.IGNORECASE | re.MULTILINE)
            all_phases.extend(phases)
        
        print(f"🔍 Found {len(all_phases)} phases:")
        for i, (num, desc) in enumerate(all_phases):
            print(f"  - Phase {num}: {desc[:60]}...")
        
        # Extract sub-agents
        sub_agent_patterns = [
            r'<([A-Z_-]+)>',
            r'Delegue\s+ao\s+sub-agente\s+<([^>]+)>',
            r'→\s*Delegue\s+ao\s+sub-agente\s+<([^>]+)>'
        ]
        
        all_sub_agents = set()
        for pattern in sub_agent_patterns:
            sub_agents = re.findall(pattern, prompt_text, re.IGNORECASE)
            all_sub_agents.update(sub_agents)
        
        print(f"🤖 Found {len(all_sub_agents)} sub-agents:")
        for agent in sorted(all_sub_agents):
            print(f"  - {agent}")
        
        # Extract decision patterns
        decision_patterns = [
            r'Se\s+a\s+consulta\s+requer\s+▢\s*([^,\n]+)',
            r'AVALIE\s+A\s+CONSULTA\s+E\s+DETERMINE\s+([^\n]+)'
        ]
        
        all_decisions = []
        for pattern in decision_patterns:
            decisions = re.findall(pattern, prompt_text, re.IGNORECASE | re.MULTILINE)
            all_decisions.extend(decisions)
        
        print(f"🤔 Found {len(all_decisions)} decision points:")
        for i, decision in enumerate(all_decisions):
            print(f"  - Decision {i+1}: {decision[:60]}...")
        
        print("\n✅ NEUROHOOK EXTRACTION COMPLETED!")
        return True
    else:
        print(f"❌ Test file not found: {test_agent_path}")
        return False

if __name__ == "__main__":
    test_neurohook_extraction()
