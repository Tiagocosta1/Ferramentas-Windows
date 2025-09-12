def MenuMain(self):
    return {
        "Programas(winget)": lambda: self.show_menu("softwares"),
        "Úteis": lambda: self.show_menu("utility"),
        "Otimização e Manutenção": lambda: self.show_menu("otimization"),
        "Diagnóstico": lambda: self.show_menu("diagnostic"),
        "Rede": lambda: self.show_menu("network"),
        "Informações do Sistema": self.get_system_info,
        "Lista de Usuários": self.get_user_info,
        "Logs(10 últimos)": self.logs_windows,
    }


def MenuSoftwares(self):
    return {
        "7zip": self.install_7zip,
        "Adobe Reader": self.install_adobe_reader,
        "AnyDesk": self.install_anydesk,
        "Chrome": self.install_chrome,
        "FastCopy": self.install_fastcopy,
        "Firefox": self.install_firefox,
        "Foxit Reader": self.install_foxit,
        "HopToDesk": self.install_hoptodesk,
        "Java": self.install_java,
        "K-Lite Codec": self.install_codec,
        "Microsoft Office": self.install_office,
        "Team Viewer": self.install_teamviewer,
        "WinRar": self.install_winrar,
    }


def MenuUtility(self):
    return {
        "Atalhos Desktop": self.ativ_shortcut,
        "Ativ(win-off)": self.ativ_win_off,
        "Compactar(ssd pequeno)": self.run_compact,
        "Configurar cores": self.ativ_color_theme,
        "Criar Usuário Impressora": self.create_user,
        "Data e Hora": self.config_date_time,
        "Desativar IPv6": self.disable_ipv6,
        "Limpar Logs": self.clean_logs,
        "Plano de Energia": self.config_energy,
        "Renovar Anydesk": self.renew_anydesk,
    }


def MenuOtimization(self):
    return {
        "Ativar Firewall": self.ativ_firewall,
        "Atualizar Programs(winget)": self.update_winget,
        "Backup de Drivers": self.backup_driver,
        "Criar Ponto de Restauração": self.point_restore,
        "Desativar Firewall": self.desativ_firewall,
        "Gerenciar Usuários(local)": self.manager_users,
        "Limpar Arquivos Temporários": self.clean_temp_files,
        "Limpar Cache(Navegadores)": self.clean_browsers,
        "Limpeza de Disco": self.clean_disk,
        "Lista Programas(logon)": self.list_startup_run,
        "Otimizar Disco": self.defrag_disk,
        "Verificar Integridade(dism)": self.run_dism,
        "Verificar Sistema(sfc)": self.run_sfc,
    }


def MenuDiagnostic(self):
    return {
        "Diagnóstico(memória)": self.diag_memory,
        "Log de Aplicativos": self.logs_app,
        "Log de Atualizações(windows)": self.logs_update,
        "Relatório de Energia": self.logs_energy,
        "Status Licença(windows)": self.status_windows,
        "Velocidade do Disco": self.speed_disk,
        "Verificar Disco(chkdsk)": self.run_chkdsk,
    }


def MenuNetwork(self):
    return {
        "IP Atual": self.get_network_info,
        "Limpar Cache DNS": self.clean_dns,
        "Listar Placas de Rede": self.list_networks,
        "Ratrear Rota(google.com)": self.get_routes,
        "Redefinir IP": self.clean_ip,
        "Redefinir Winsock": self.clean_winsock,
        "Teste Ping(8.8.8.8)": self.test_ping_dns,
        "Teste Ping(google.com)": self.test_ping_page,
    }
