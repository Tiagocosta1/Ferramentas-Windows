def MenuMain(self):
    return {
        "Rede e Conectividade": lambda: self.show_menu("network"),
        "Sistema e Hardware": self.get_system_info,
        "Usuários e Segurança": self.get_user_info,
        "Monitoramento e Logs": self.get_logs,
        "Otimização e Performance": lambda: self.show_menu("otimization"),
        "Assistente de Diagnóstico": lambda: self.show_menu("diagnostic"),
        "Manutenção Avançada": lambda: self.show_menu("fix"),
        "Ajuda e Documentação": self.show_help,
    }


def MenuNetwork(self):
    return {
        "Mostrar Configuração IP": self.get_network_info,
        "Ping google.com": self.ping_google,
        "Limpar Cache DNS": self.limpar_cache_dns,
        "Redefinir TCP/IP": self.redefinir_tcpip,
    }


def MenuOtimization(self):
    return {
        "Limpar Arquivos Temporários": self.clear_temp_files,
        "Listar Programas na Inicialização": self.listar_programas_startup,
    }


def MenuDiagnostic(self):
    return {
        "Verificar Disco (CHKDSK)": self.verificar_disco_chkdsk,
        "Verificar Arquivos (SFC)": self.verificar_arquivos_sfc,
        "Verificar Imagem (DISM)": self.verificar_imagem_dism,
        "Diagnóstico Completo": self.diagnostico_completo,
    }


def MenuFix(self):
    return {
        "Atualizar Programas (Winget)": self.atualizar_programas_winget,
        "Criar Ponto de Restauração": self.criar_ponto_restauracao,
    }
