class ScriptsMixin:
    def _install_winget_app(self, package_id, app_name):
        command = (
            f"winget install {package_id} --accept-package-agreements "
            "--accept-source-agreements"
        )
        self.run_powershell_in_thread(
            command, f"Instalando {app_name}", admin=True
        )

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

    def install_hoptodesk(self):
        self._install_winget_app("9N0NXG9ZMF7Z", "HopToDesk")

    def install_java(self):
        self._install_winget_app("Oracle.JavaRuntimeEnvironment", "Java")

    def install_codec(self):
        self._install_winget_app(
            "CodecGuide.K-LiteCodecPack.Mega", "K-Lite Mega Codec"
        )

    def install_office(self):
        self._install_winget_app("Microsoft.Office", "Microsoft Office")

    def install_teamviewer(self):
        self._install_winget_app("TeamViewer.TeamViewer", "Team Viewer")

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

    def run_compact(self):
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

    def clean_logs(self):
        command = """
            try {
                Write-Output "Limpando os logs de eventos do Windows..."
                Get-WinEvent -ListLog * | ForEach-Object {
                    try {
                        Clear-EventLog -LogName $_.LogName
                        Write-Output "Log limpo: $($_.LogName)"
                    } catch {
                        Write-Output "Não limpo o log: $($_.LogName) - $_"
                    }
                }
                Write-Output "`nTodos os logs foram processados."
            } catch {
                Write-Error "Erro ao tentar limpar os logs: $_"
            }
        """
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

    def point_restore(self):
        command = (
            "Checkpoint-Computer -Description "
            '"Ponto de Restauração MultiToolsShell"'
        )
        self.run_powershell_in_thread(
            command, "Criação de Ponto de Restauração", admin=True
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

    def clean_temp_files(self):
        command = """
            $paths = @("$env:TEMP", "$env:SystemRoot\\Prefetch", `
                "$env:SystemRoot\\Temp")
            foreach ($p in $paths) {
                if (Test-Path $p) {
                    Write-Output ("Limpando pasta: " + $p)
                    Remove-Item -Path "$p\\*" -Recurse -Force `
                        -ErrorAction SilentlyContinue
                }
            }
        """
        self.run_powershell_in_thread(
            command, "Limpeza de Arquivos Temporários", admin=True
        )

    def clean_browsers(self):
        command = (
            r'$chromeCache = "$env:LOCALAPPDATA\Google\Chrome\User Data'
            r'\Default\Cache\*"; '
            r'$edgeCache = "$env:LOCALAPPDATA\Microsoft\Edge\User Data'
            r'\Default\Cache\*"; '
            "Remove-Item $chromeCache, $edgeCache -Recurse -Force "
            "-ErrorAction SilentlyContinue"
        )
        self.run_powershell_in_thread(
            command, "Limpeza Cache do Navegadores", admin=True
        )

    def clean_disk(self):
        command = 'Start-Process cleanmgr -ArgumentList "/sagerun:1"'
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
        self.run_powershell_in_thread(command, "Otimizando Disco")

    def run_dism(self):
        command = (
            "DISM /Online /Cleanup-Image /ScanHealth; "
            "DISM /Online /Cleanup-Image /CheckHealth; "
            "DISM /Online /Cleanup-image /Restorehealth"
        )
        self.run_powershell_in_thread(command, "Verificando Integridade(dism)")

    def run_sfc(self):
        command = "sfc /scannow"
        self.run_powershell_in_thread(command, "Verificar Sistema(sfc)")

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
        command = "chkdsk C: /f /r"
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
