# ingestion/metadata.py
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Mapeamento de domínios para agentes principais
DOMAIN_TO_AGENT = {
    'neurohook': 'NEUROHOOK-ULTRA',
    'retention': 'RETENTION-ARCHITECT',
    'pain': 'PAIN-DETECTOR',
    'paradigm': 'PARADIGM-ARCHITECT',
    'metaphor': 'METAPHOR-ARCHITECT',
    'conversion': 'CONVERSION-CATALYST'
}

# Mapeamento de subdomínios para sub-agentes do NEUROHOOK-ULTRA
NEUROHOOK_SUBDOMAIN_TO_SUBAGENT = {
    'core_foundations/neuroscience_of_attention': 'Cognition-Scanner',
    'core_foundations/cognitive_biases': 'Cognition-Scanner',
    'hook_techniques/headline_formulas': 'Relevance-Engineer',
    'hook_techniques/pattern_interruption': 'Dissonance-Architect',
    'audience_psychology': 'Credibility-Calibrator',
    'linguistic_engineering': 'Relevance-Engineer',
    'implementation_guides': 'Urgency-Programmer'
}

# Mapeamento de subdomínios para sub-agentes do RETENTION-ARCHITECT
RETENTION_SUBDOMAIN_TO_SUBAGENT = {
    'cognitive_foundations/attention_psychology': 'TENSION-ENGINEER',
    'retention_techniques/tension_structures': 'TENSION-ENGINEER',
    'retention_techniques/rhythm_and_pacing': 'RHYTHM-PROGRAMMER',
    'retention_techniques/transition_engineering': 'TRANSITION-SPECIALIST',
    'retention_techniques/immersion_patterns': 'IMMERSION-ARCHITECT',
    'master_examples': 'JOURNEY-CARTOGRAPHER'
}

# Mapeamento de subdomínios para sub-agentes do PAIN-DETECTOR
PAIN_SUBDOMAIN_TO_SUBAGENT = {
    'foundational_psychology/emotional_frameworks': 'DIGITAL-ETHNOGRAPHER',
    'pain_taxonomy/domains_of_suffering/financial_pains': 'CONTEXT-CARTOGRAPHER',
    'pain_taxonomy/domains_of_suffering/relationship_pains': 'CONTEXT-CARTOGRAPHER',
    'pain_taxonomy/domains_of_suffering/career_pains': 'CONTEXT-CARTOGRAPHER',
    'pain_taxonomy/domains_of_suffering/health_pains': 'CONTEXT-CARTOGRAPHER',
    'pain_taxonomy/detection_frameworks': 'SYMPTOM-TRANSLATOR',
    'pain_taxonomy/application_frameworks': 'CONSEQUENCE-AMPLIFIER',
    'agent_architecture': 'IMPACT-PRIORITIZER'
}

# Mapeamento para os outros 3 agentes principais seguindo o mesmo padrão

def extract_metadata_from_path(file_path, base_dir):
    """
    Extrai metadados relevantes do caminho do arquivo,
    incluindo domínio, agente principal, sub-agente, etc.
    """
    rel_path = os.path.relpath(file_path, base_dir)
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1]
    
    # Extrair domínio do primeiro nível de pasta
    parts = rel_path.split(os.sep)
    domain = parts[0].replace('_knowledge', '') if len(parts) > 0 else None
    
    # Subdomínio é o resto do caminho sem o arquivo
    subdomain = os.path.dirname(rel_path).replace(parts[0] + os.sep, '') if len(parts) > 1 else None
    
    # Determinar agente principal com base no domínio
    agent_principal = DOMAIN_TO_AGENT.get(domain, domain)
    
    # Determinar sub-agente com base no subdomínio (varia por agente principal)
    sub_agent = None
    if agent_principal == 'NEUROHOOK-ULTRA' and subdomain:
        # Tenta encontrar o subdomínio mais específico que corresponda
        matching_subdomains = [sd for sd in NEUROHOOK_SUBDOMAIN_TO_SUBAGENT if subdomain.startswith(sd)]
        if matching_subdomains:
            # Usar o mais específico (maior comprimento)
            best_match = max(matching_subdomains, key=len)
            sub_agent = NEUROHOOK_SUBDOMAIN_TO_SUBAGENT[best_match]
    elif agent_principal == 'RETENTION-ARCHITECT' and subdomain:
        matching_subdomains = [sd for sd in RETENTION_SUBDOMAIN_TO_SUBAGENT if subdomain.startswith(sd)]
        if matching_subdomains:
            best_match = max(matching_subdomains, key=len)
            sub_agent = RETENTION_SUBDOMAIN_TO_SUBAGENT[best_match]
    elif agent_principal == 'PAIN-DETECTOR' and subdomain:
        matching_subdomains = [sd for sd in PAIN_SUBDOMAIN_TO_SUBAGENT if subdomain.startswith(sd)]
        if matching_subdomains:
            best_match = max(matching_subdomains, key=len)
            sub_agent = PAIN_SUBDOMAIN_TO_SUBAGENT[best_match]
    
    # Determinar tipo de documentação
    doc_type = None
    if 'summaries' in rel_path:
        doc_type = 'summary'
    elif 'papers' in rel_path:
        doc_type = 'paper'
    elif 'books' in rel_path:
        doc_type = 'book'
    elif 'templates' in rel_path or 'proven_templates' in rel_path:
        doc_type = 'template'
    elif 'frameworks' in rel_path:
        doc_type = 'framework'
    elif 'profiles' in rel_path:
        doc_type = 'profile'
    elif 'patterns' in rel_path:
        doc_type = 'pattern'
    elif 'guides' in rel_path:
        doc_type = 'guide'
    elif 'examples' in rel_path or 'masterpieces' in rel_path:
        doc_type = 'example'
    
    # Montar o conjunto completo de metadados
    metadata = {
        'file_name': file_name,
        'file_path': rel_path,
        'file_type': file_ext[1:] if file_ext else None,
        'domain': domain,
        'subdomain': subdomain,
        'agent_id': agent_principal,
        'sub_agent_id': sub_agent,
        'doc_type': doc_type,
        'source_type': 'internal_knowledge',
        'created_at': os.path.getctime(file_path),
        'updated_at': os.path.getmtime(file_path)
    }
    
    return metadata

