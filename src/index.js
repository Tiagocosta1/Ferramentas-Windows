const terminalOutput = document.getElementById('terminal-output');
const menuContainer = document.getElementById('menu-buttons');
let allMenuData = {};
let logContent = '';

const ICON_MAP = {
  'main': 'fas fa-home',
  'info_diag': 'fas fa-chart-line',
  'manut_otim': 'fas fa-wrench',
  'fix_sistem': 'fas fa-shield-alt',
  'network': 'fas fa-wifi',
  'security': 'fas fa-lock',
  'admin_system': 'fas fa-user-tie',
  'soft_app': 'fas fa-toolbox',
  'install_programs': 'fas fa-download',
  'clean_archives': 'fas fa-trash-alt',
  'otim_disk': 'fas fa-hdd',
  'firewall': 'fas fa-fire-extinguisher',
  'default_submenu': 'fas fa-folder',
  'default_command': 'fas fa-terminal',
};

const terminal_log = {
  showOnTerminal: function(text, tag = 'info') {
    const safeText = document.createTextNode(text + '\n');
    const span = document.createElement('span');
    logContent += `[${tag.toUpperCase()}] ${text}\n`;

    if (tag === 'title') span.className = 'tag-title';
    if (tag === 'error') span.className = 'tag-error';
    span.appendChild(safeText);
    terminalOutput.appendChild(span);
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
  },

  showHeader: function(taskName, admin) {
    const adminMsg = admin ? ' (Requer Admin)' : '';
    const header = `\n--- INICIANDO: ${taskName}${adminMsg} ---`;
    logContent += `[TITLE] ${header.trim()}\n`;
    this.showOnTerminal(header, 'title');
  },

  showErrors: function(message) {
    const escapedMessage = message.replace(/\\"/g, '"').replace(/\\n/g, '\n');
    this.showOnTerminal(escapedMessage, 'error');
  },

  showFooter: function(taskName) {
    const footer = `--- CONCLUÍDO: ${taskName} ---`;
    this.showOnTerminal(footer, 'title');
  }
};

function getIcon(menuName) {
    return ICON_MAP[menuName.split('_')[0]] || ICON_MAP[menuName] || ICON_MAP['default_command'];
}

function renderMenuLevel(menuData, menuName, level = 0) {
    const ul = document.createElement('ul');
    ul.className = 'submenu-list';
    if (level > 0) ul.classList.add('submenu');

    ul.setAttribute('data-menu-name', menuName);

    for (const [text, funcName] of Object.entries(menuData)) {
        const isSubMenu = funcName.startsWith('show_menu_');
        const nextMenuName = isSubMenu ? funcName.replace('show_menu_', '') : null;

        const li = document.createElement('li');

        const item = document.createElement('div');
        item.className = 'menu-item ' + (isSubMenu ? 'is-menu' : 'is-command');
        item.style.paddingLeft = `${20 + (level * 20)}px`;
        item.setAttribute('data-func-name', funcName);

        const iconClass = isSubMenu ? ICON_MAP['default_submenu'] : getIcon(funcName);
        item.innerHTML = `<i class="${iconClass}"></i><span>${text}</span>`;

        if (isSubMenu) {
            item.innerHTML += '<i class="fas fa-chevron-right dropdown-arrow"></i>';
            item.onclick = (e) => handleToggle(e, item, nextMenuName);
        } else {
            item.onclick = (e) => handleCommandClick(e, funcName);
        }

        li.appendChild(item);

        if (isSubMenu && allMenuData[nextMenuName]) {
            const submenuElement = renderMenuLevel(allMenuData[nextMenuName], nextMenuName, level + 1);
            li.appendChild(submenuElement);
        }

        ul.appendChild(li);
    }
    return ul;
}

function handleToggle(event, item, targetMenuName) {
    const submenuElement = item.nextElementSibling;

    if (submenuElement && submenuElement.classList.contains('submenu')) {
        document.querySelectorAll(`.submenu-list[data-menu-name="${item.parentElement.parentElement.getAttribute('data-menu-name')}"] > li > .menu-item.expanded`).forEach(el => {
            if (el !== item) {
                el.classList.remove('expanded');
                el.nextElementSibling.classList.remove('expanded');
            }
        });

        submenuElement.classList.toggle('expanded');
        item.classList.toggle('expanded');
    }
}

function handleCommandClick(event, funcName) {
    const clickedItem = event.currentTarget;
    try {
        if (window.pywebview.api[funcName]) {
            document.querySelectorAll('.menu-item.active').forEach(el => el.classList.remove('active'));
            clickedItem.classList.add('active');

            window.pywebview.api[funcName]();
        } else {
            terminal_log.showErrors(`Erro: Método Python "${funcName}" não encontrado na API.`);
        }
    } catch (e) {
        terminal_log.showErrors(`Erro ao chamar o método Python "${funcName}": ${e.message}`);
    }
}

function renderMenuStructure() {
    menuContainer.innerHTML = '';

    const logoDiv = document.createElement('div');
    logoDiv.id = 'menu-logo-header';
    logoDiv.innerHTML = '<i class="fas fa-tools"></i> Ferramentas';
    menuContainer.appendChild(logoDiv);

    const menuContentContainer = document.createElement('div');
    menuContentContainer.id = 'menu-content';
    menuContentContainer.style.flexGrow = '1';

    const menuElement = renderMenuLevel(allMenuData['main'], 'main', 0);
    menuContentContainer.appendChild(menuElement);
    menuContainer.appendChild(menuContentContainer);

    const exitItem = document.createElement('div');
    exitItem.className = 'menu-item back-button';
    exitItem.style.paddingLeft = '20px';
    exitItem.innerHTML = '<i class="fas fa-power-off"></i><span>Sair do Aplicativo</span>';
    exitItem.onclick = handleExit;
    menuContainer.appendChild(exitItem);
}

function startApp() {
  const date_now = new Date().toLocaleString('pt-BR');
  const init_text = `====== Ferramentas - Windows (Web) ======\nData: ${date_now}\n===========================\nSelecione uma opção no menu à esquerda`;
  logContent = `\n[TITLE] ${init_text.split('\n').join('\n[TITLE] ')}\n`;
  terminal_log.showOnTerminal(init_text, 'title');
}

window.addEventListener('pywebviewready', async function() {
  try {
    allMenuData = await window.pywebview.api.get_menu_structure();
    renderMenuStructure();
    startApp();
  } catch(e) {
    terminal_log.showErrors(`ERRO FATAL ao carregar a API Python: ${e.message}`);
  }
});

function handleExit() {
    window.pywebview.api.save_terminal_log(logContent)
        .then(() => {
            window.pywebview.api.quit();
        })
        .catch(error => {
            console.error("Erro ao tentar salvar o log:", error);
            window.pywebview.api.quit();
        });
}