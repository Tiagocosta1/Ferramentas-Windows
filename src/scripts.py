import threading
import subprocess
import os
import re
import logging
from src.interface import InterfaceMixin

class ScriptsMixin:
    def __init__(self, window=None):
        self.interface_utils = InterfaceMixin()
        self.window = window

    def run_powershell_in_thread(self, command, task_name, admin=False):
        admin_flag = 'true' if admin else 'false'
        if self.window:
            self.window.evaluate_js(f'terminal_log.showHeader("{task_name}", {admin_flag})')

        def _threaded_task_runner():
            process = None
            try:
                full_command = self._prepare_powershell_command(command)

                process = self._execute_subprocess_realtime(full_command)

                self._read_stream_and_update_js(process.stdout)

            except FileNotFoundError:
                logging.error("O PowerShell não foi encontrado.")
                if self.window:
                    self.window.evaluate_js('terminal_log.showErrors("ERRO: O PowerShell não foi encontrado.")')
            except Exception as exc:
                error_msg = str(exc).replace('\\', '\\\\').replace('"', '\\"')
                logging.error(f"Ocorreu um erro inesperado: {error_msg}")
                if self.window:
                    self.window.evaluate_js(f'terminal_log.showErrors("Ocorreu um erro inesperado: {error_msg}")')
            finally:
                if process:
                    self._handle_process_completion(process, task_name)

        self._run_thread(_threaded_task_runner)

    def _read_stream_and_update_js(self, stream):
        for line_bytes in iter(stream.readline, b""):
            decoded_line = self.interface_utils._decode_output(line_bytes)

            js_safe_line = decoded_line.replace('\\', '\\\\').replace('"', '\\"')

            js_safe_line = js_safe_line.replace('\r', '').replace('\n', '')

            js_safe_line = re.sub(r'(\b(http|https)://\S+)', r'\\1', js_safe_line)

            if self.window:
                self.window.evaluate_js(f'terminal_log.showOnTerminal("{js_safe_line}")')

    def _prepare_powershell_command(self, command):
        ps_script = f"""
        $PSDefaultParameterValues['Out-File:Encoding'] = 'UTF8'
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        chcp 65001 > $null
        {command}
        """
        return [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
            "-Command",
            ps_script,
        ]

    def _execute_subprocess_realtime(self, full_command):
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                startupinfo=startupinfo,
            )
            return process
        except Exception as e:
            logging.error(f"Erro ao executar subprocesso: {e}")
            raise

    def _run_thread(self, target):
        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    def _handle_process_completion(self, process, task_name):
        process.wait()
        error_output = self.interface_utils._decode_output(process.stderr.read())
        if error_output:
            error_msg = error_output.replace('\\', '\\\\').replace('"', '\\"')
            logging.warning(f"Erro no processo: {error_msg}")
            if self.window:
                self.window.evaluate_js(f'terminal_log.showErrors("ERRO:\\n{error_msg}")')

        if self.window:
            self.window.evaluate_js(f'terminal_log.showFooter("{task_name}")')

    def _install_winget_app(self, package_id, app_name):
        command = (
            f"winget install {package_id} --accept-package-agreements --accept-source-agreements"
        )
        self.run_powershell_in_thread(command, f"Instalando {app_name}", admin=True)

    def install_app(self, package_id, app_name):
        self._install_winget_app(package_id, app_name)

    def install_7zip(self):
        self._install_winget_app("7zip.7zip", "7Zip")

    def install_adobe_reader(self):
        self._install_winget_app("Adobe.Acrobat.Reader.64-bit", "Adobe Reader")

    def install_anydesk(self):
        self._install_winget_app("AnyDesk.AnyDesk", "AnyDesk")

    def install_chrome(self):
        self._install_winget_app("Google.Chrome", "Google Chrome")

    def install_fastcopy(self):
        self._install_winget_app("FastCopy.FastCopy", "FastCopy")

    def install_firefox(self):
        self._install_winget_app("Mozilla.Firefox.pt-BR", "Mozilla Firefox")

    def install_foxit(self):
        self._install_winget_app("Foxit.FoxitReader", "Foxit Reader")

    def install_rustdesk(self):
        command = '''
            $url = "https://visaoinformaticapb.com.br/downloads/rustdesk.exe"
            $destino = Join-Path $env:TEMP "rustdesk.exe"
            $argumentos = "/VERYSILENT"

            Write-Host "Baixando o RustDesk..."
            Invoke-WebRequest -Uri $url -OutFile $destino

            Write-Host "Instalando... (Aguardando o término)"
            Start-Process -FilePath $destino -ArgumentList $argumentos -Wait

            Write-Host "Instalação concluída."

            Remove-Item $destino -Force
            Write-Host "Instalador removido."
        '''
        self.run_powershell_in_thread(
            command, "Instalando RustDesk", admin=True
        )

    def install_java(self):
        self._install_winget_app("Oracle.JavaRuntimeEnvironment", "Java")

    def install_codec(self):
        self._install_winget_app(
            "CodecGuide.K-LiteCodecPack.Mega", "K-Lite Mega Codec"
        )

    def install_office(self):
        self._install_winget_app("Microsoft.Office", "Microsoft Office")

    def install_teamviewer(self):
        command = '''
            $url = "https://visaoinformaticapb.com.br/downloads/teamviewer.exe"
            $destino = Join-Path $env:TEMP "teamviewer.exe"
            $argumentos = "/VERYSILENT"

            Write-Host "Baixando o TeamViewer..."
            Invoke-WebRequest -Uri $url -OutFile $destino

            Write-Host "Instalando... (Aguardando o término)"
            Start-Process -FilePath $destino -ArgumentList $argumentos -Wait

            Write-Host "Instalação concluída."

            Remove-Item $destino -Force
            Write-Host "Instalador removido."
        '''
        self.run_powershell_in_thread(
            command, "Instalando TeamViewer", admin=True
        )

    def install_winrar(self):
        self._install_winget_app("RARLab.WinRAR", "WinRar")

    def ativ_shortcut(self):
        command = (
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\ClassicStartMenu" '
            '-Name "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\NewStartPanel" '
            '-Name "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\ClassicStartMenu" '
            '-Name "{59031a47-3f72-44a7-89c5-5595fe6b30ee}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\NewStartPanel" '
            '-Name "{59031a47-3f72-44a7-89c5-5595fe6b30ee}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\ClassicStartMenu" '
            '-Name "{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\NewStartPanel" '
            '-Name "{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\ClassicStartMenu" '
            '-Name "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}" '
            "-Value 0 -PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\'
            'HideDesktopIcons\\NewStartPanel" '
            '-Name "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}" '
            "-Value 0 -PropertyType DWORD -Force;"
        )
        self.run_powershell_in_thread(
            command, "Colocando Atalhos no Desktop", admin=True
        )

    def ativ_win_off(self):
        command = "irm https://get.activated.win | iex"
        self.run_powershell_in_thread(
            command, "Ativando o Windows e Office", admin=True
        )

    def compact_os(self):
        command = (
            "powercfg /hibernate off;"
            "Set-ItemProperty -Path "
            '"HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\'
            'ReserveManager" -Name "ShippedWithReserves" -Value 0 '
            "-PropertyType DWORD -Force;"
            "compact.exe /CompactOS:always;"
        )
        self.run_powershell_in_thread(
            command, "Compactando Sistema(ssd pequeno)", admin=True
        )

    def ativ_color_theme(self):
        command = (
            "New-ItemProperty -Path "
            '"HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\'
            'Personalize" -Name AppsUseLightTheme -Value 1 -PropertyType'
            " DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\'
            'Personalize" -Name SystemUsesLightTheme -Value 0 -PropertyType'
            " DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\'
            'Personalize" -Name EnableTransparency -Value 0 -PropertyType'
            " DWORD -Force;"
        )
        self.run_powershell_in_thread(
            command, "Definindo Padrão de Cores do Windows", admin=True
        )

    def create_user(self):
        command = """
            $Username = "impressora"
            $Password = "123"
            $Description = "Novo usuario Impressora"
            $UserExists = Get-LocalUser -Name $Username -ErrorAction `
                SilentlyContinue
            if ($UserExists) {
                Write-Output "O usuário '$Username' já existe. Redefinindo..."
                $SecurePassword = ConvertTo-SecureString $Password `
                    -AsPlainText -Force
                Set-LocalUser -Name $Username -Password $SecurePassword
                if (-not (Get-LocalGroupMember -Group "Administradores" `
                    -Member $Username -ErrorAction SilentlyContinue)) {
                    Add-LocalGroupMember -Group "Administradores" `
                        -Member $Username
                }
                Set-LocalUser -Name $Username -PasswordNeverExpires $true
            }
            else {
                Write-Output "Criando o usuário '$Username'..."
                $SecurePassword = ConvertTo-SecureString $Password `
                    -AsPlainText -Force
                New-LocalUser -Name $Username -Password $SecurePassword `
                    -FullName $Description -Description $Description `
                    -PasswordNeverExpires
                Add-LocalGroupMember -Group "Administradores" -Member $Username
                Set-LocalUser -Name $Username -PasswordNeverExpires $true
                Write-Output "Usuário '$Username' criado com sucesso."
            }
        """
        self.run_powershell_in_thread(
            command, "Criando Usuário Impressora", admin=True
        )

    def config_date_time(self):
        command = (
            'tzutil /s "SA Western Standard Time"; '
            "net stop w32time; "
            "w32tm /unregister; "
            "w32tm /register; "
            "net start w32time; "
            "w32tm /resync;"
        )
        self.run_powershell_in_thread(
            command, "Configurando Data e Hora", admin=True
        )

    def disable_ipv6(self):
        command = (
            "New-ItemProperty -Path "
            '"HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters"'
            ' -Name "DisabledComponents" -Value 0xFF -PropertyType'
            " DWORD -Force"
        )
        self.run_powershell_in_thread(command, "Desativando IPv6", admin=True)

    def command_clean_logs(self):
        return (
            'Write-Output "--- Iniciando Limpeza de Logs do Windows ---";\n'
            '$logs = @("Application", "Security", "System", "Setup",'
            ' "ForwardedEvents");\n'
            'Write-Output "Limpando os principais logs de eventos...";\n'
            "foreach ($log in $logs) {\n"
            '    Write-Output "Processando log: $log";\n'
            "    try {\n"
            "        # Verifica se o log existe antes de tentar limpar\n"
            "        if (Get-WinEvent -ListLog $log"
            " -ErrorAction SilentlyContinue) {\n"
            "            wevtutil cl $log;\n"  # Adicionado ; por segurança
            '            Write-Output "Log $($log) limpo com sucesso."\n'
            "        } else {\n"
            '            Write-Output "Log $($log) não encontrado."\n'
            "        }\n"
            "    } catch {\n"
            '        Write-Output "ERRO ao limpar o log $($log): $_"\n'
            "    }\n"
            "}\n"
            'Write-Output "--- Limpeza de Logs do Windows Concluída ---";'
        )

    def clean_logs(self):
        command = self.command_clean_logs()
        self.run_powershell_in_thread(
            command, "Limpando Logs do Windows", admin=True
        )

    def config_energy(self):
        command = (
            "powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c; "
            "powercfg -change -standby-timeout-ac 0; "
            "powercfg -change -standby-timeout-dc 0; "
            "powercfg -change -monitor-timeout-ac 0; "
            "powercfg -change -monitor-timeout-dc 0; "
            "powercfg -change -disk-timeout-ac 0; "
            "powercfg -change -disk-timeout-dc 0; "
            "powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS"
            " PBUTTONACTION 2; "
            "powercfg -setdcvalueindex SCHEME_CURRENT SUB_BUTTONS"
            " PBUTTONACTION 2; "
            "powercfg -setactive SCHEME_CURRENT;"
        )
        self.run_powershell_in_thread(
            command, "Configurando Plano de Energia", admin=True
        )

    def renew_anydesk(self):
        command = (
            'taskkill /f /im "AnyDesk.exe";'
            'Remove-Item "$env:ALLUSERSPROFILE\\AnyDesk\\service.conf" -Force'
            " -ErrorAction SilentlyContinue;"
            'Remove-Item "$env:APPDATA\\AnyDesk\\service.conf" -Force'
            " -ErrorAction SilentlyContinue;"
            'Remove-Item "$env:ALLUSERSPROFILE\\AnyDesk*" -Force -Recurse'
            " -ErrorAction SilentlyContinue;"
            'Remove-Item "$env:APPDATA\\AnyDesk\\*" -Force -Recurse'
            " -ErrorAction SilentlyContinue;"
        )
        self.run_powershell_in_thread(
            command, "Resetando ID do AnyDesk", admin=True
        )

    def ativ_firewall(self):
        command = "netsh advfirewall set allprofiles state on"
        self.run_powershell_in_thread(command, "Ativando Firewall", admin=True)

    def update_winget(self):
        command = (
            "winget upgrade --all --accept-package-agreements "
            "--accept-source-agreements"
        )
        self.run_powershell_in_thread(
            command, "Atualizando Apps com Winget", admin=True
        )

    def backup_driver(self):
        command = r"""
            $desktop = [Environment]::GetFolderPath("Desktop")
            mkdir "$desktop\DriverBackup"
            Export-WindowsDriver -Online -Destination "$desktop\DriverBackup" `
                | Select-Object ClassName, ProviderName, Date, Version `
                | Sort-Object ClassName `
                | Export-Csv -Path "$desktop\DriverBackup\Exportado.csv" `
                    -NoTypeInformation -Encoding UTF8;
        """
        self.run_powershell_in_thread(
            command, "Realizando Backup dos Drivers", admin=True
        )

    def desativ_firewall(self):
        command = "netsh advfirewall set allprofiles state off"
        self.run_powershell_in_thread(
            command, "Desativando Firewall", admin=True
        )

    def manager_users(self):
        command = "Start-Process lusrmgr.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Gerenciador de usuários", admin=True
        )

    def comand_temp_files(self):
        return """
            Write-Output "--- Iniciando Limpeza de Arquivos Temporários ---;"
            $paths = @("$env:TEMP", "$env:SystemRoot\\Prefetch", `
                "$env:SystemRoot\\Temp");
            foreach ($p in $paths) {
                if (Test-Path $p) {
                    Write-Output ("Limpando pasta: " + $p);
                    Remove-Item -Path "$p\\*" -Recurse -Force `
                        -ErrorAction SilentlyContinue;
                }
            }
            Write-Output "--- Limpeza de Arquivos Temporários Concluída ---;"
        """

    def clean_temp_files(self):
        command = self.comand_temp_files()
        self.run_powershell_in_thread(
            command, "Limpeza de Arquivos Temporários", admin=True
        )

    def command_browser_cache(self):
        return (
            'Write-Output "--- Limpeza de Cache - Navegadores ---";'
            '$chromeCache = "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\'
            'Default\\Cache\\*";'
            '$edgeCache = "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\'
            'Default\\Cache\\*";'
            "Remove-Item $chromeCache, $edgeCache -Recurse -Force "
            "-ErrorAction SilentlyContinue;"
            '$firefoxProfilesPath = "$env:APPDATA\\Mozilla\\Firefox\\'
            'Profiles";'
            "$profileDirs = Get-ChildItem -Path $firefoxProfilesPath"
            " -Directory -ErrorAction SilentlyContinue;"
            "foreach ($profile in $profileDirs) {"
            '    $cachePath = Join-Path $profile.FullName "cache2";'
            "    if (Test-Path $cachePath) {"
            "        try {"
            "            Remove-Item -Path $cachePath -Recurse -Force"
            "             -ErrorAction Stop;"
            '            Write-Output "Cache limpo: $($profile.Name)";'
            "        }"
            "        catch {"
            '            Write-Output "Erro perfil $($profile.Name): $_;"'
            "        }"
            "    } else {"
            '        Write-Output "Nenhum cache perfil: $($profile.Name);"'
            "    }"
            "}"
            'Write-Output "--- Limpeza Cache - Navegadores Concluída ---;"'
        )

    def clean_browsers(self):
        command = self.command_browser_cache()
        self.run_powershell_in_thread(
            command, "Limpeza Cache do Navegadores", admin=True
        )

    def command_clean_disk(self):
        return (
            'Write-Output "--- Iniciando Limpeza de Disco ---";'
            'Start-Process cleanmgr -ArgumentList "/sagerun:1" -Wait;'
            'Write-Output "--- Limpeza de Disco Concluída ---";'
        )

    def clean_disk(self):
        command = self.command_clean_disk()
        self.run_powershell_in_thread(
            command, "Executando Limpeza de Disco", admin=True
        )

    def list_startup_run(self):
        command = (
            "Get-CimInstance Win32_StartupCommand | "
            "Select-Object Name, Command, Location | Format-Table -AutoSize"
        )
        self.run_powershell_in_thread(command, "Programas na Inicialização")

    def defrag_disk(self):
        command = r"""
            $disk = Get-PhysicalDisk | Where-Object { $_.DeviceID `
                -eq (Get-Partition -DriveLetter C).DiskNumber }
            if ($disk.MediaType -eq "SSD") {
                Write-Output "Disco C: é SSD. Executando TRIM..."
                defrag C: /L
                Write-Output "TRIM executado com sucesso."
            } else {
                Write-Output "Disco C: é HDD. Executando desfragmentação..."
                defrag C:
                Write-Output "Desfragmentação concluída."
            }
        """
        self.run_powershell_in_thread(command, "Otimizando Disco", admin=True)

    def run_dism(self):
        command = (
            "DISM /Online /Cleanup-Image /ScanHealth; "
            "DISM /Online /Cleanup-Image /CheckHealth; "
            "DISM /Online /Cleanup-image /Restorehealth"
        )
        self.run_powershell_in_thread(
            command, "Verificando Integridade(dism)", admin=True
        )

    def run_sfc(self):
        command = "sfc /scannow"
        self.run_powershell_in_thread(
            command, "Verificar Sistema(sfc)", admin=True
        )

    def diag_memory(self):
        command = "Start-Process mdsched"
        self.run_powershell_in_thread(command, "Diagnóstico(memória)")

    def logs_app(self):
        command = """
            Write-Output "=== LOGS DE APLICATIVOS ==="
            Get-EventLog -LogName Application -Newest 10 `
                | Format-Table TimeGenerated, EntryType, Source, Message `
                    -AutoSize -Wrap
        """
        self.run_powershell_in_thread(command, "Log de Aplicativos")

    def logs_update(self):
        command = """
            Write-Output "Verificando atualizações do Windows..."
            Get-WindowsUpdateLog
            Write-Output "Logs gerados com Sucesso no Desktop"
        """
        self.run_powershell_in_thread(command, "Log de Atualizações(windows)")

    def logs_energy(self):
        command = """
            $desktop = [Environment]::GetFolderPath("Desktop")
            cd $desktop
            powercfg /energy
        """
        self.run_powershell_in_thread(command, "Diagnóstico de Energia")

    def status_windows(self):
        command = "slmgr /xpr"
        self.run_powershell_in_thread(command, "Status Licença(windows)")

    def speed_disk(self):
        command = "winsat disk"
        self.run_powershell_in_thread(command, "Avaliando Desempenho do Disco")

    def run_chkdsk(self):
        command = """
            Write-Output "AGENDANDO CHKDSK NA PRÓXIMA REINICIALIZAÇÃO..."
            echo S | chkdsk C: /f /r
            Write-Output "CHKDSK foi agendado."
            Write-Output "VOCÊ PRECISA REINICIAR O COMPUTADOR para que a
             verificação ocorra."
        """
        self.run_powershell_in_thread(
            command, "Verificação de Disco (CHKDSK)", admin=True
        )

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
        self.run_powershell_in_thread(command, "Configuração de Rede")

    def clean_dns(self):
        command = "ipconfig /flushdns"
        self.run_powershell_in_thread(command, "Limpeza de Cache DNS")

    def list_networks(self):
        command = (
            'Write-Output "=== ADAPTADORES DE REDE ==="; '
            "Get-NetAdapter | Select-Object Name, Status, MacAddress | "
            "Format-Table -AutoSize"
        )
        self.run_powershell_in_thread(command, "Placas de Rede")

    def get_routes(self):
        command = "tracert google.com"
        self.run_powershell_in_thread(command, "Rota(google.com)")

    def clean_ip(self):
        command = "netsh int ip reset"
        self.run_powershell_in_thread(
            command, "Redefinição de TCP/IP", admin=True
        )

    def clean_winsock(self):
        command = "netsh winsock reset"
        self.run_powershell_in_thread(
            command, "Redefinição do Catálogo Winsock", admin=True
        )

    def test_ping_dns(self):
        command = "Test-Connection 8.8.8.8 -Count 4"
        self.run_powershell_in_thread(command, "Ping DNS")

    def test_ping_page(self):
        command = "Test-Connection google.com -Count 4"
        self.run_powershell_in_thread(command, "Ping Pagina")

    def get_system_info(self):
        command = """
            Write-Output "=== INFORMAÇÕES DO SISTEMA ==="
            Write-Output "Computador: $env:COMPUTERNAME"
            Write-Output "Usuário: $env:USERNAME"
            $os = Get-CimInstance Win32_OperatingSystem
            Write-Output "SO: $($os.Caption)"
            $cpu = Get-CimInstance Win32_Processor
            Write-Output "Processador: $($cpu.Name)"
            $cs = Get-CimInstance Win32_ComputerSystem
            $memGB = [math]::Round(($cs.TotalPhysicalMemory / 1GB), 2)
            Write-Output "Memória Total: $memGB GB"
            $ramFreeMB = [math]::Round(($os.FreePhysicalMemory / 1KB), 2)
            Write-Output "RAM Livre: $ramFreeMB MB"
            $disk = Get-PSDrive C -ErrorAction SilentlyContinue
            if ($disk) {
                $freeGB = [math]::Round(($disk.Free / 1GB), 2)
                $totalGB = [math]::Round(($disk.Used + $disk.Free) / 1GB, 2)
                Write-Output "Disco C: $freeGB GB livres / $totalGB GB total"
            }
        """
        self.run_powershell_in_thread(command, "Informações do Sistema")

    def get_user_info(self):
        command = (
            "Get-LocalUser | Select-Object Name, Enabled, LastLogon | "
            "Format-Table -AutoSize"
        )
        self.run_powershell_in_thread(command, "Informações de Usuários")

    def logs_windows(self):
        command = (
            "Get-WinEvent -FilterHashtable @{LogName='System'; Level=2} "
            "-MaxEvents 10 | Format-Table TimeCreated, Message -Wrap -AutoSize"
        )
        self.run_powershell_in_thread(command, "Logs de Eventos do Sistema")

    def clean_full(self):
        command = self.comand_temp_files()
        command += self.command_browser_cache()
        command += self.command_clean_logs()
        command += self.command_clean_disk()
        self.run_powershell_in_thread(command, "Limpeza Completa", admin=True)

    def fix_full(self):
        command = """
            Write-Output "--- Iniciando Reparo DISM ---"
            DISM /Online /Cleanup-Image /ScanHealth
            DISM /Online /Cleanup-Image /CheckHealth
            DISM /Online /Cleanup-image /Restorehealth

            Write-Output "--- Iniciando Verificação SFC ---"
            sfc /scannow

            Write-Output "--- REPARO COMPLETO CONCLUÍDO ---"
        """
        self.run_powershell_in_thread(
            command, "Rotina de Reparo de Sistema", admin=True
        )

    def fix_windows_update(self):
        command = (
            "Stop-Service -Name wuauserv -Force; "
            "Stop-Service -Name bits -Force; "
            "Stop-Service -Name cryptsvc -Force; "
            "Stop-Service -Name msiserver -Force; "
            r'Rename-Item -Path "C:\\Windows\\SoftwareDistribution" '
            r'-NewName "SoftwareDistribution.old" '
            "-ErrorAction SilentlyContinue; "
            r'Rename-Item -Path "C:\\Windows\\System32\\catroot2" '
            r'-NewName "catroot2.old" -ErrorAction SilentlyContinue; '
            r"""
                $dlls = @(
                    "atl.dll","urlmon.dll","mshtml.dll","shdocvw.dll"
                    ,"browseui.dll","jscript.dll","vbscript.dll","scrrun.dll",
                    "msxml.dll","msxml3.dll","msxml6.dll","actxprxy.dll",
                    "softpub.dll","wintrust.dll","dssenh.dll","rsaenh.dll",
                    "gpkcsp.dll","sccbase.dll","slbcsp.dll","cryptdlg.dll",
                    "oleaut32.dll","ole32.dll","shell32.dll","initpki.dll",
                    "wuapi.dll","wuaueng.dll","wuaueng1.dll","wucltui.dll",
                    "wups.dll","wups2.dll","wuweb.dll","qmgr.dll",
                    "qmgrprxy.dll","wucltux.dll","muweb.dll","wuwebv.dll"
                )
                foreach ($dll in $dlls) {
                    regsvr32.exe /s $dll
                }
            """
            "Start-Service -Name wuauserv; "
            "Start-Service -Name bits; "
            "Start-Service -Name cryptsvc; "
            "Start-Service -Name msiserver;"
        )
        self.run_powershell_in_thread(
            command, "Reparando Windows Update", admin=True
        )

    def fix_microsoft_store(self):
        command = (
            "wsreset.exe; "
            "Get-AppxPackage -AllUsers *WindowsStore* | "
            "Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "
            "'$($_.InstallLocation)\\AppXManifest.xml'}"
        )
        self.run_powershell_in_thread(
            command, "Reparando Microsoft Store", admin=True
        )

    def re_register_store_apps(self):
        command = (
            "Get-AppxPackage -AllUsers | "
            "ForEach-Object { Add-AppxPackage -DisableDevelopmentMode "
            '-Register "$($_.InstallLocation)\\AppXManifest.xml" '
            "-ErrorAction SilentlyContinue}"
        )
        self.run_powershell_in_thread(
            command, "Re-registrando Apps da Store", admin=True
        )

    def fix_firewall(self):
        command = (
            "netsh advfirewall reset; "
            "netsh advfirewall set allprofiles state on; "
            "Set-Service mpssvc -StartupType Automatic; "
            "Start-Service mpssvc"
        )
        self.run_powershell_in_thread(
            command, "Reparando Firewall do Windows", admin=True
        )

    def fix_network(self):
        command = """
            Write-Output "--- Iniciando Reparo de Rede ---"
            Write-Output "Limpando Cache DNS..."
            ipconfig /flushdns
            Write-Output "Redefinindo TCP/IP..."
            netsh int ip reset
            Write-Output "Redefinindo Catálogo Winsock..."
            netsh winsock reset
            Write-Output "--- Reparo de Rede Concluído ---"
        """
        self.run_powershell_in_thread(
            command, "Reparando Rede (DNS, IP, Winsock)", admin=True
        )

    def fix_icons(self):
        command = (
            "ie4uinit.exe -ClearIconCache; "
            "Stop-Process -Name explorer -Force; "
            "Start-Process explorer;"
        )
        self.run_powershell_in_thread(
            command, "Reparando Ícones do Sistema", admin=True
        )

    def fix_start_menu(self):
        command = (
            "Get-AppxPackage "
            "-AllUsers Microsoft.Windows.StartMenuExperienceHost | "
            "Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "
            "'$($_.InstallLocation)\\AppXManifest.xml'}; "
            "Stop-Process -Name StartMenuExperienceHost -Force;"
        )
        self.run_powershell_in_thread(
            command, "Reparando Menu Iniciar", admin=True
        )

    def fix_taskbar(self):
        command = (
            "Get-AppxPackage -AllUsers Microsoft.Windows.ShellExperienceHost |"
            " Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "
            "'$($_.InstallLocation)\\AppXManifest.xml'}; "
            "Stop-Process -Name ShellExperienceHost -Force;"
        )
        self.run_powershell_in_thread(
            command, "Reparando Barra de Tarefas", admin=True
        )

    def clear_print_queue(self):
        command = (
            "Stop-Service -Name Spooler -Force; "
            "Remove-Item -Path 'C:\\Windows\\System32\\spool\\PRINTERS\\*' "
            "-Recurse -Force -ErrorAction SilentlyContinue; "
            "Start-Service -Name Spooler;"
        )
        self.run_powershell_in_thread(
            command, "Limpando Fila de Impressão", admin=True
        )

    def enable_system_restore(self):
        command = (
            "Enable-ComputerRestore -Drive 'C:'; "
            'Write-Output "Restauração do Sistema Ativada";'
        )
        self.run_powershell_in_thread(
            command, "Ativando Restauração do Sistema", admin=True
        )

    def disable_system_restore(self):
        command = (
            "Disable-ComputerRestore -Drive 'C:'; "
            'Write-Output "Restauração do Sistema Desativada";'
        )
        self.run_powershell_in_thread(
            command, "Desativando Restauração do Sistema", admin=True
        )

    def point_restore(self):
        command = (
            'Checkpoint-Computer -Description "Ponto de Restauração Manual";'
        )
        self.run_powershell_in_thread(
            command, "Criando Ponto de Restauração", admin=True
        )

    def restore_system(self):
        command = "rstrui.exe"
        self.run_powershell_in_thread(command, "Restaurar Sistema", admin=True)

    def status_firewall(self):
        command = "netsh advfirewall show allprofiles"
        self.run_powershell_in_thread(command, "Status do Firewall")

    def status_protection(self):
        command = "Get-MpComputerStatus | Format-List"
        self.run_powershell_in_thread(command, "Status do Windows Defender")

    def update_definitions(self):
        command = "Update-MpSignature"
        self.run_powershell_in_thread(
            command, "Atualizando Definições do Windows Defender", admin=True
        )

    def scan_threats(self):
        command = "Start-MpScan -ScanType QuickScan"
        self.run_powershell_in_thread(
            command, "Verificando Ameaças(Defender)", admin=True
        )

    def status_bitlocker(self):
        command = "Get-BitLockerVolume | Format-List"
        self.run_powershell_in_thread(command, "Status do BitLocker")

    def device_manager(self):
        command = "Start-Process devmgmt.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Gerenciador de Dispositivos", admin=True
        )

    def disk_management(self):
        command = "Start-Process diskmgmt.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Gerenciamento de Disco", admin=True
        )

    def printer_management(self):
        command = (
            'Start-Process "explorer.exe"'
            ' "shell:::{A8A91A66-3A7D-4424-8D24-04E180695C7A}";'
        )
        self.run_powershell_in_thread(
            command, "Abrindo Gerenciamento de Impressoras", admin=True
        )

    def event_viewer(self):
        command = "Start-Process eventvwr.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Visualizador de Eventos", admin=True
        )

    def task_scheduler(self):
        command = "Start-Process taskschd.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Agendador de Tarefas", admin=True
        )

    def system_services(self):
        command = "Start-Process services.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Gerenciador de Serviços", admin=True
        )

    def group_policy_editor(self):
        command = "Start-Process gpedit.msc"
        self.run_powershell_in_thread(
            command, "Abrindo Editor de Política de Grupo", admin=True
        )

    def registry_editor(self):
        command = "Start-Process regedit"
        self.run_powershell_in_thread(
            command, "Abrindo Editor do Registro", admin=True
        )

    def config_file_explorer(self):
        command = (
            "Write-Host 'Configurando o Explorador de Arquivos...';"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "HideFileExt" -Value 0 '
            "-PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "Start_TrackDocs" -Value 0 '
            "-PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "Start_TrackProgs" -Value 0 '
            "-PropertyType DWORD -Force;"
            '$path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\CloudStorage\\Accounts";'
            "if (Test-Path $path) { "
            'New-ItemProperty -Path $path -Name "OfficeOnline" -Value 0 '
            "-PropertyType DWORD -Force };"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "LaunchTo" -Value 1 '
            "-PropertyType DWORD -Force;"
            "Write-Host 'Configurações aplicadas. Reiniciando o Explorer...';"
            "Stop-Process -Name explorer -Force"
        )
        self.run_powershell_in_thread(
            command, "Configurando Explorador de Arquivos", admin=True
        )

    def show_hidden_files(self):
        command = (
            'Write-Host "Mostrando arquivos ocultos e do sistema...";'
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "Hidden" -Value 1 '
            "-PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "ShowSuperHidden" -Value 1 '
            "-PropertyType DWORD -Force;"
            "Write-Host 'Reiniciando Explorer para aplicar...';"
            "Stop-Process -Name explorer -Force"
        )
        self.run_powershell_in_thread(
            command, "Mostrando Arquivos Ocultos", admin=True
        )

    def hide_hidden_files(self):
        command = (
            'Write-Host "Ocultando arquivos ocultos e do sistema...";'
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "Hidden" -Value 0 '
            "-PropertyType DWORD -Force;"
            "New-ItemProperty -Path "
            '"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'Explorer\\Advanced" -Name "ShowSuperHidden" -Value 0 '
            "-PropertyType DWORD -Force;"
            'Write-Host "Reiniciando Explorer para aplicar...";'
            "Stop-Process -Name explorer -Force"
        )
        self.run_powershell_in_thread(
            command, "Ocultando Arquivos Ocultos", admin=True
        )

    def shortcut_office(self):
        command = """
            $desktop = "$env:PUBLIC\\Desktop"
            $apps = @("Word", "Excel", "PowerPoint")
            $officePaths = @(
                "$env:ProgramFiles\\Microsoft Office\\root\\Office16",
                "$env:ProgramFiles(x86)\\Microsoft Office\\root\\Office16"
                "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
            )
            foreach ($app in $apps) {
                $found = $false
                foreach ($path in $officePaths) {
                    $appPath = "$path\\$app.lnk"
                    if (Test-Path $appPath) {
                        Write-Host "Atalho encontrado: $appPath"
                        Copy-Item -Path $appPath -Destination $desktop -Force
                        $found = $true
                        break
                    }
                }
                if (-not $found) {
                    Write-host "AVISO: Atalho para '$app' não encontrado."
                }
            }
            Write-Host "Criação de atalhos do Office concluída."
        """
        self.run_powershell_in_thread(
            command, "Criando Atalhos do Office no Desktop", admin=True
        )

    def config_visual_options(self):
        command = (
            "function Set-RegistryValue {"
            "    param ("
            "        [string]$path,"
            "        [string]$name,"
            "        [object]$value"
            "    )"
            "    if (Test-Path $path) {"
            "        Set-ItemProperty -Path $path -Name $name -Value $value"
            "    } else {"
            "        New-Item -Path $path -Force | Out-Null"
            "        Set-ItemProperty -Path $path -Name $name -Value $value"
            "    }"
            "}"
            '$performanceKey = "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\Explorer\\VisualEffects";'
            'Set-RegistryValue -path $performanceKey -name "VisualFX" '
            "-value 0;"
            'Set-RegistryValue -path $performanceKey -name "DragWindow" '
            "-value 1;"
            'Set-RegistryValue -path $performanceKey -name "IconCache" '
            "-value 1;"
            "Set-RegistryValue -path $performanceKey -name "
            '"ShadowUnderWindows" -value 1;'
            'Set-RegistryValue -path $performanceKey -name "ShadowUnderMouse" '
            "-value 1;"
            'Set-RegistryValue -path $performanceKey -name "SmoothScroll" '
            "-value 1;"
            'Set-RegistryValue -path $performanceKey -name "RoundFont" '
            "-value 1;"
            'Set-RegistryValue -path $performanceKey -name "ShadowLabels" '
            "-value 1;"
        )
        self.run_powershell_in_thread(
            command, "Configurando Opções Visuais", admin=True
        )

    def disable_notifications(self):
        command = (
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\PushNotifications" -Name "ToastEnabled" -Value 0 '
            "-Force;"
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\Notifications\\Settings" -Name '
            '"NOC_GLOBAL_SETTING_TOASTS_ENABLED" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\ContentDeliveryManager" '
            '-Name "SystemPaneSuggestionsEnabled" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\Explorer\\Advanced" '
            '-Name "ShowSyncProviderNotifications" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\ContentDeliveryManager" '
            '-Name "SubscribedContent-310093Enabled" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\ContentDeliveryManager" '
            '-Name "SubscribedContent-314563Enabled" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\ContentDeliveryManager" '
            '-Name "SubscribedContent-338387Enabled" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\UserProfileEngagement" '
            '-Name "ScoobeSystemSettingEnabled" -Value 0 -Force;'
            'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\ContentDeliveryManager" '
            '-Name "SoftLandingEnabled" -Value 0 -Force;'
        )
        self.run_powershell_in_thread(
            command, "Desativando Notificações", admin=True
        )

    def list_programs(self):
        command = (
            "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\"
            "Windows\\CurrentVersion\\Uninstall\\* | Select-Object "
            "DisplayName,"
            " DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize;"
            "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\"
            "CurrentVersion\\Uninstall\\* | Select-Object DisplayName, "
            "DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize;"
            "Get-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\"
            "CurrentVersion\\Uninstall\\* | Select-Object DisplayName, "
            "DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize;"
        )
        self.run_powershell_in_thread(command, "Programas Instalados")

    def remove_bloatware(self):
        command = (
            "Get-AppxPackage -AllUsers | Where-Object { $_.Name -notmatch "
            '"(Microsoft.WindowsStore|Microsoft.MSPaint|Microsoft.Windows'
            "Calculator|Microsoft.Windows.Photos|Microsoft.Windows.Alarm|"
            "Microsoft.Windows.Notepad|Microsoft.ScreenSketch|"
            'Microsoft.MicrosoftEdge)" } | '
            "Remove-AppxPackage -ErrorAction SilentlyContinue; "
            "Get-AppxPackage -AllUsers | Where-Object { $_.Name -notmatch "
            '"(Microsoft.WindowsStore|Microsoft.MSPaint|Microsoft.Windows'
            "Calculator|Microsoft.Windows.Photos|Microsoft.Windows.Alarm|"
            "Microsoft.Windows.Notepad|Microsoft.ScreenSketch|"
            'Microsoft.MicrosoftEdge)" } | '
            "Remove-AppxProvisionedPackage -Online -ErrorAction "
            "SilentlyContinue;"
        )
        self.run_powershell_in_thread(
            command, "Removendo Bloatware", admin=True
        )

    def remove_programs(self):
        command = "appwiz.cpl"
        self.run_powershell_in_thread(
            command, "Abrindo Adicionar ou Remover Programas", admin=True
        )

    def ativ_winrar(self):
        command = """
            $arquivo = "C:\\Program Files\\WinRAR\\rarreg.key"
            Remove-Item -Path $arquivo -Force -ErrorAction SilentlyContinue
            $caminho = "C:\\Program Files\\WinRAR\\rarreg.key"
            $conteudo = @"
RAR registration data
Federal Agency for Education
1000000 PC usage license
UID=b621cca9a84bc5deffbf
6412612250ffbf533df6db2dfe8ccc3aae5362c06d54762105357d
5e3b1489e751c76bf6e0640001014be50a52303fed29664b074145
7e567d04159ad8defc3fb6edf32831fd1966f72c21c0c53c02fbbb
2f91cfca671d9c482b11b8ac3281cb21378e85606494da349941fa
e9ee328f12dc73e90b6356b921fbfb8522d6562a6a4b97e8ef6c9f
fb866be1e3826b5aa126a4d2bfe9336ad63003fc0e71c307fc2c60
64416495d4c55a0cc82d402110498da970812063934815d81470829275
"@
            $conteudo | Set-Content -Path $caminho -Encoding ASCII
        """
        self.run_powershell_in_thread(command, "Ativando WinRAR", admin=True)
