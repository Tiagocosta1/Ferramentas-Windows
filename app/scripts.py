class ScriptsMixin:
    """
    Mixin que contém todos os métodos que executam scripts PowerShell.
    """

    # scripts.py (método get_network_info corrigido)

    def get_network_info(self):
        command = """
        Write-Output "=== CONFIGURAÇÃO DE REDE ==="
        $ipConfig = Get-NetIPConfiguration | `
            Where-Object { $_.IPv4DefaultGateway -ne $null }
        $ipLocal = $ipConfig.IPv4Address.IPAddress
        Write-Output ("IP Local: " + $ipLocal)
        try {
            $publicInfo = Invoke-RestMethod -Uri "https://ipinfo.io/json" `
                -TimeoutSec 5
            Write-Output ("IP Público: " + $publicInfo.ip)
            Write-Output ("Localização: " + $publicInfo.city + ", " `
                + $publicInfo.region + ", " + $publicInfo.country)
        } catch {
            Write-Output "IP Público: Não foi possível obter"
        }
        """
        self.executar_powershell_em_thread(command, "Configuração de Rede")

    def get_system_info(self):
        command = """
        Write-Output "=== INFORMAÇÕES DO SISTEMA ==="
        Write-Output "Computador: $env:COMPUTERNAME"
        Write-Output "Usuário: $env:USERNAME"
        $os = Get-CimInstance Win32_OperatingSystem
        $cpu = Get-CimInstance Win32_Processor
        $cs = Get-CimInstance Win32_ComputerSystem
        Write-Output ("SO: " + $os.Caption)
        Write-Output ("Processador: " + $cpu.Name)
        $memGB = [math]::Round(($cs.TotalPhysicalMemory / 1GB), 2)
        Write-Output ("Memória Total: " + $memGB + " GB")
        """
        self.executar_powershell_em_thread(command, "Informações do Sistema")

    def get_user_info(self):
        command = (
            "Get-LocalUser | Select-Object Name, Enabled, LastLogon | "
            "Format-Table -AutoSize"
        )
        self.executar_powershell_em_thread(command, "Informações de Usuários")

    def get_logs(self):
        command = (
            "Get-WinEvent -FilterHashtable @{LogName='System'; Level=2} "
            "-MaxEvents 10 | Format-Table TimeCreated, Message -Wrap -AutoSize"
        )
        self.executar_powershell_em_thread(
            command, "Logs de Eventos do Sistema"
        )

    def clear_temp_files(self):
        command = """
        $paths = @("$env:TEMP", "$env:SystemRoot\\Prefetch")
        foreach ($p in $paths) {
            if (Test-Path $p) {
                Write-Output ("Limpando pasta: " + $p)
                Remove-Item -Path "$p\\*" -Recurse -Force `
                    -ErrorAction SilentlyContinue
            }
        }
        Write-Output "Limpeza de arquivos temporários concluída."
        """
        self.executar_powershell_em_thread(
            command, "Limpeza de Arquivos Temporários", admin=True
        )

    def ping_google(self):
        command = "Test-Connection google.com -Count 4"
        self.executar_powershell_em_thread(command, "Ping Google")

    def limpar_cache_dns(self):
        command = "ipconfig /flushdns"
        self.executar_powershell_em_thread(command, "Limpeza de Cache DNS")

    def redefinir_tcpip(self):
        command = "netsh int ip reset"
        self.executar_powershell_em_thread(
            command, "Redefinição de TCP/IP", admin=True
        )

    def listar_programas_startup(self):
        command = (
            "Get-CimInstance Win32_StartupCommand | "
            "Select-Object Name, Command, Location | Format-Table -AutoSize"
        )
        self.executar_powershell_em_thread(
            command, "Programas na Inicialização"
        )

    def verificar_disco_chkdsk(self):
        command = "chkdsk C: /f /r"
        self.executar_powershell_em_thread(
            command, "Verificação de Disco (CHKDSK)", admin=True
        )

    def verificar_arquivos_sfc(self):
        command = "sfc /scannow"
        self.executar_powershell_em_thread(
            command, "Verificação de Arquivos de Sistema (SFC)", admin=True
        )

    def verificar_imagem_dism(self):
        command = """
        DISM /Online /Cleanup-Image /ScanHealth
        DISM /Online /Cleanup-Image /CheckHealth
        """
        self.executar_powershell_em_thread(
            command, "Verificação de Imagem do Sistema (DISM)", admin=True
        )

    def diagnostico_completo(self):
        command = """
        DISM /Online /Cleanup-Image /RestoreHealth
        sfc /scannow
        """
        self.executar_powershell_em_thread(
            command, "Diagnóstico Completo do Sistema", admin=True
        )

    def atualizar_programas_winget(self):
        command = (
            "winget upgrade --all --accept-package-agreements "
            "--accept-source-agreements"
        )
        self.executar_powershell_em_thread(
            command, "Atualizando Apps com Winget", admin=True
        )

    def criar_ponto_restauracao(self):
        command = (
            "Checkpoint-Computer -Description "
            '"Ponto de Restauração MultiToolsShell"'
        )
        self.executar_powershell_em_thread(
            command, "Criação de Ponto de Restauração", admin=True
        )

    def show_help(self):
        texto_ajuda = """
    === AJUDA E DOCUMENTAÇÃO ===
    - Selecione uma categoria no menu à esquerda.
    - Os resultados aparecerão neste terminal.
    - Comandos demorados rodam em segundo plano.
    - IMPORTANTE: Execute como Administrador.
    """
        self.show_on_terminal(texto_ajuda)
