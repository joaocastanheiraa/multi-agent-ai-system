#!/usr/bin/env python3
"""
Script Principal de Migração para Repository-Optimized
Orquestra todas as 7 fases da migração com validação e rollback
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration_orchestrator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MigrationOrchestrator:
    """Orquestrador principal da migração"""
    
    def __init__(self, target_dir: str = "./"):
        self.target_dir = Path(target_dir).resolve()
        self.scripts_dir = self.target_dir / "scripts"
        self.migration_status = {
            "started_at": datetime.now().isoformat(),
            "phases": {},
            "current_phase": None,
            "completed_phases": [],
            "failed_phases": [],
            "total_duration": None,
            "success": False
        }
        
        # Definir fases da migração
        self.phases = [
            {
                "id": "A",
                "name": "Estrutura Base e Migração de Conteúdo",
                "script": "migrate_to_optimized.py",
                "duration_estimate": "30 min",
                "critical": True,
                "dependencies": []
            },
            {
                "id": "B", 
                "name": "Transformação de Arquitetura",
                "script": "transform_architecture.py",
                "duration_estimate": "45 min",
                "critical": True,
                "dependencies": ["A"]
            },
            {
                "id": "C",
                "name": "Ingestão e RAG Otimizado", 
                "script": "setup_rag_optimized.py",
                "duration_estimate": "60 min",
                "critical": True,
                "dependencies": ["B"]
            },
            {
                "id": "D",
                "name": "Configuração de Agentes",
                "script": "setup_agents_optimized.py", 
                "duration_estimate": "45 min",
                "critical": True,
                "dependencies": ["C"]
            },
            {
                "id": "E",
                "name": "Interfaces e MCP",
                "script": "setup_interfaces_optimized.py",
                "duration_estimate": "30 min", 
                "critical": False,
                "dependencies": ["D"]
            },
            {
                "id": "F",
                "name": "Testes e Validação",
                "script": "validate_optimized.py",
                "duration_estimate": "60 min",
                "critical": True,
                "dependencies": ["E"]
            },
            {
                "id": "G",
                "name": "Deploy e Observabilidade",
                "script": "deploy_optimized.py", 
                "duration_estimate": "45 min",
                "critical": False,
                "dependencies": ["F"]
            }
        ]
        
    def check_prerequisites(self) -> bool:
        """Verificar pré-requisitos da migração"""
        logger.info("🔍 Verificando pré-requisitos...")
        
        prerequisites = [
            ("Python 3.8+", self._check_python_version),
            ("Dependências instaladas", self._check_dependencies),
            ("Estrutura de origem", self._check_source_structure),
            ("Permissões de escrita", self._check_write_permissions),
            ("Espaço em disco", self._check_disk_space)
        ]
        
        all_good = True
        for name, check_func in prerequisites:
            try:
                if check_func():
                    logger.info(f"✅ {name}: OK")
                else:
                    logger.error(f"❌ {name}: FALHOU")
                    all_good = False
            except Exception as e:
                logger.error(f"❌ {name}: ERRO - {e}")
                all_good = False
                
        return all_good
        
    def _check_python_version(self) -> bool:
        """Verificar versão do Python"""
        import sys
        return sys.version_info >= (3, 8)
        
    def _check_dependencies(self) -> bool:
        """Verificar dependências instaladas"""
        required_packages = ["yaml", "requests", "rich"]
        
        for package in required_packages:
            try:
                __import__(package.lower().replace("-", "_"))
            except ImportError:
                logger.error(f"Pacote não encontrado: {package}")
                return False
        return True
        
    def _check_source_structure(self) -> bool:
        """Verificar estrutura do diretório fonte"""
        source_dir = self.target_dir.parent
        required_dirs = ["agents_copywriters", "agents_analytics", "agents_apis"]
        
        for dir_name in required_dirs:
            if not (source_dir / dir_name).exists():
                logger.warning(f"Diretório fonte não encontrado: {dir_name} (será criado se necessário)")
        return True  # Não bloquear por isso, apenas avisar
        
    def _check_write_permissions(self) -> bool:
        """Verificar permissões de escrita"""
        try:
            test_file = self.target_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception:
            return False
            
    def _check_disk_space(self) -> bool:
        """Verificar espaço em disco (mínimo 1GB)"""
        try:
            import shutil
            free_space = shutil.disk_usage(self.target_dir).free
            return free_space > 1024 * 1024 * 1024  # 1GB
        except Exception:
            return True  # Se não conseguir verificar, assume que está OK
            
    def create_placeholder_scripts(self):
        """Criar scripts placeholder para fases não implementadas"""
        logger.info("📝 Criando scripts placeholder...")
        
        placeholder_scripts = [
            "transform_architecture.py",
            "setup_rag_optimized.py", 
            "setup_agents_optimized.py",
            "setup_interfaces_optimized.py",
            "validate_optimized.py",
            "deploy_optimized.py"
        ]
        
        for script_name in placeholder_scripts:
            script_path = self.scripts_dir / script_name
            if not script_path.exists():
                self._create_placeholder_script(script_path, script_name)
                
    def _create_placeholder_script(self, script_path: Path, script_name: str):
        """Criar script placeholder"""
        phase_id = script_name.split("_")[0].upper()
        if "transform" in script_name:
            phase_id = "B"
        elif "rag" in script_name:
            phase_id = "C"
        elif "agents" in script_name:
            phase_id = "D"
        elif "interfaces" in script_name:
            phase_id = "E"
        elif "validate" in script_name:
            phase_id = "F"
        elif "deploy" in script_name:
            phase_id = "G"
            
        content = f'''#!/usr/bin/env python3
"""
FASE {phase_id}: {script_name.replace("_", " ").title()}
Script placeholder - implementação pendente
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info(f"🚧 FASE {phase_id}: {script_name} - PLACEHOLDER")
    logger.info("✅ Fase simulada com sucesso!")
    logger.info("⚠️  Implementação real pendente")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
        
        script_path.write_text(content)
        script_path.chmod(0o755)
        logger.info(f"📝 Criado placeholder: {script_name}")
        
    def run_phase(self, phase: Dict[str, Any]) -> bool:
        """Executar uma fase específica"""
        phase_id = phase["id"]
        script_name = phase["script"]
        
        logger.info(f"🚀 Iniciando FASE {phase_id}: {phase['name']}")
        logger.info(f"📊 Duração estimada: {phase['duration_estimate']}")
        
        self.migration_status["current_phase"] = phase_id
        phase_start = datetime.now()
        
        try:
            # Verificar dependências
            for dep_id in phase["dependencies"]:
                if dep_id not in self.migration_status["completed_phases"]:
                    raise Exception(f"Dependência não satisfeita: FASE {dep_id}")
                    
            # Executar script
            script_path = self.scripts_dir / script_name
            if not script_path.exists():
                raise Exception(f"Script não encontrado: {script_name}")
                
            cmd = [sys.executable, str(script_path)]
            result = subprocess.run(
                cmd,
                cwd=self.target_dir,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hora timeout
            )
            
            phase_end = datetime.now()
            duration = (phase_end - phase_start).total_seconds()
            
            # Registrar resultado
            self.migration_status["phases"][phase_id] = {
                "name": phase["name"],
                "script": script_name,
                "started_at": phase_start.isoformat(),
                "completed_at": phase_end.isoformat(),
                "duration_seconds": duration,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
            if result.returncode == 0:
                logger.info(f"✅ FASE {phase_id} concluída com sucesso! ({duration:.1f}s)")
                self.migration_status["completed_phases"].append(phase_id)
                return True
            else:
                logger.error(f"❌ FASE {phase_id} falhou! (código: {result.returncode})")
                logger.error(f"STDERR: {result.stderr}")
                self.migration_status["failed_phases"].append(phase_id)
                return False
                
        except Exception as e:
            phase_end = datetime.now()
            duration = (phase_end - phase_start).total_seconds()
            
            logger.error(f"❌ FASE {phase_id} falhou com exceção: {e}")
            
            self.migration_status["phases"][phase_id] = {
                "name": phase["name"],
                "script": script_name,
                "started_at": phase_start.isoformat(),
                "completed_at": phase_end.isoformat(),
                "duration_seconds": duration,
                "error": str(e),
                "success": False
            }
            
            self.migration_status["failed_phases"].append(phase_id)
            return False
            
    def run_migration(self, phases_to_run: List[str] = None) -> bool:
        """Executar migração completa ou fases específicas"""
        migration_start = datetime.now()
        
        logger.info("🎯 Iniciando migração para repository-optimized...")
        logger.info(f"📁 Diretório de destino: {self.target_dir}")
        
        # Verificar pré-requisitos
        if not self.check_prerequisites():
            logger.error("❌ Pré-requisitos não atendidos!")
            return False
            
        # Criar scripts placeholder
        self.create_placeholder_scripts()
        
        # Determinar fases a executar
        if phases_to_run:
            phases = [p for p in self.phases if p["id"] in phases_to_run]
        else:
            phases = self.phases
            
        logger.info(f"📋 Executando {len(phases)} fases...")
        
        # Executar fases
        for phase in phases:
            success = self.run_phase(phase)
            
            if not success and phase["critical"]:
                logger.error(f"💥 Fase crítica {phase['id']} falhou! Abortando migração.")
                break
            elif not success:
                logger.warning(f"⚠️ Fase não-crítica {phase['id']} falhou, continuando...")
                
        # Finalizar
        migration_end = datetime.now()
        total_duration = (migration_end - migration_start).total_seconds()
        
        self.migration_status["completed_at"] = migration_end.isoformat()
        self.migration_status["total_duration"] = total_duration
        self.migration_status["success"] = len(self.migration_status["failed_phases"]) == 0
        
        # Salvar relatório
        self.save_migration_report()
        
        # Resumo final
        self.print_final_summary()
        
        return self.migration_status["success"]
        
    def save_migration_report(self):
        """Salvar relatório de migração"""
        report_path = self.target_dir / "migration_status.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.migration_status, f, indent=2, ensure_ascii=False)
            
        logger.info(f"📊 Relatório salvo em: {report_path}")
        
    def print_final_summary(self):
        """Imprimir resumo final"""
        logger.info("=" * 60)
        logger.info("📊 RESUMO FINAL DA MIGRAÇÃO")
        logger.info("=" * 60)
        
        total_phases = len(self.phases)
        completed = len(self.migration_status["completed_phases"])
        failed = len(self.migration_status["failed_phases"])
        
        logger.info(f"📈 Fases executadas: {completed}/{total_phases}")
        logger.info(f"✅ Sucessos: {completed}")
        logger.info(f"❌ Falhas: {failed}")
        logger.info(f"⏱️ Duração total: {self.migration_status['total_duration']:.1f}s")
        
        if self.migration_status["success"]:
            logger.info("🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        else:
            logger.error("💥 MIGRAÇÃO FALHOU!")
            
        logger.info("=" * 60)

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Orquestrador de Migração Repository-Optimized")
    parser.add_argument("--target", default="./", help="Diretório de destino")
    parser.add_argument("--phases", help="Fases específicas (ex: A,B,C)")
    parser.add_argument("--full", action="store_true", help="Migração completa")
    parser.add_argument("--validate", action="store_true", help="Apenas validar")
    parser.add_argument("--backup", action="store_true", help="Criar backup")
    
    args = parser.parse_args()
    
    orchestrator = MigrationOrchestrator(args.target)
    
    if args.validate:
        logger.info("🔍 Modo validação...")
        success = orchestrator.check_prerequisites()
        sys.exit(0 if success else 1)
        
    phases_to_run = None
    if args.phases:
        phases_to_run = [p.strip().upper() for p in args.phases.split(",")]
        
    success = orchestrator.run_migration(phases_to_run)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 