

        const uploadZone = document.getElementById('uploadZone');
        if (uploadZone) {
                       const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            function playSciFiSound(type) {
                if(audioCtx.state === 'suspended') audioCtx.resume();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                if (type === 'hover') {
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.1);
                    gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.1);
                } else if (type === 'success') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(440, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(660, audioCtx.currentTime + 0.1);
                    osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.2);
                    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.5);
                } else if (type === 'error') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.3);
                    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.3);
                }
            }

            console.log('✅ Zona de transferencia Modo Dios activada');
        }
        
        document.getElementById('openUploadBtn')?.addEventListener('click', () => document.getElementById('folderInput').click());
        document.getElementById('ctaUploadBtn')?.addEventListener('click', () => document.getElementById('folderInput').click());
        
        function init() {
            if (featuresGrid) {
                featuresGrid.innerHTML = [
                    { icon: '💻', title: 'Código Puro', ext: '.js .py .java .ts...', desc: 'Extrae solo el texto útil para la IA' },
                    { icon: '🧹', title: 'Filtro Inteligente', ext: 'NO venv NO node_modules', desc: 'Ignora basura y dependencias pesadas' },
                    { icon: '🔒', title: '100% Privado', ext: 'PROCESAMIENTO LOCAL', desc: 'El archivo se genera directo en tu PC' },
                    { icon: '⚡', title: 'Velocidad Absoluta', ext: 'DRAG & DROP', desc: 'Arrastra tu proyecto crudo sin comprimir' }
                ].map(f => `<div class="feature-card-cyber"><div class="feature-icon-cyber">${f.icon}</div><h3 class="feature-title-cyber">${f.title}</h3><div class="feature-ext-cyber">${f.ext}</div><p class="feature-desc-cyber">${f.desc}</p></div>`).join('');
            }
            const matrixToggle = document.getElementById('matrixToggle');
            if (matrixToggle) {
                matrixToggle.onclick = () => {
                    document.body.classList.toggle('matrix-mode');
                    matrixToggle.classList.toggle('active');
                    localStorage.setItem('matrix-mode', document.body.classList.contains('matrix-mode'));
                };
                if (localStorage.getItem('matrix-mode') === 'true') { document.body.classList.add('matrix-mode'); matrixToggle.classList.add('active'); }
            }
            for (let i = 0; i < 100; i++) { let p = document.createElement('div'); p.classList.add('particle'); p.style.left = Math.random() * 100 + '%'; p.style.animationDelay = Math.random() * 10 + 's'; p.style.animationDuration = 5 + Math.random() * 10 + 's'; document.getElementById('particles')?.appendChild(p); }
            const canvas = document.getElementById('matrix-canvas');
            if (canvas) {
                let ctx = canvas.getContext('2d');
                canvas.width = window.innerWidth; canvas.height = window.innerHeight;
                let chars = "01";
                let fontSize = 14, cols = canvas.width / fontSize, drops = Array(Math.floor(cols)).fill(0).map(() => Math.floor(Math.random() * -canvas.height));
                function draw() { ctx.fillStyle = 'rgba(0,0,0,0.05)'; ctx.fillRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#0f0'; ctx.font = fontSize + 'px monospace'; for (let i = 0; i < drops.length; i++) { let char = chars[Math.floor(Math.random() * chars.length)]; ctx.fillText(char, i * fontSize, drops[i] * fontSize); if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0; drops[i]++; } }
                setInterval(draw, 35);
                window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; drops = Array(Math.floor(canvas.width / fontSize)).fill(0).map(() => Math.floor(Math.random() * -canvas.height)); });
            }
        }
        init();
        
        window.copyLink = () => { navigator.clipboard.writeText(document.getElementById('generatedLink')?.innerText.replace('🔒 ', '') || ''); alert('Enlace copiado'); };
   
// (Input movido al inicio del script)
let pendingUploadFiles = [];

function prepareUpload(files) {
    if (!files.length) return;
    pendingUploadFiles = files;
    document.getElementById('uploadZone').style.display = 'none';
    document.getElementById('confirmZone').style.display = 'block';
    const statusDiv = document.getElementById('uploadStatus');
    if (statusDiv) statusDiv.innerHTML = '';
}

window.cancelUpload = function() {
    pendingUploadFiles = [];
    document.getElementById('confirmZone').style.display = 'none';
    document.getElementById('uploadZone').style.display = 'block';
    folderInput.value = '';
};

window.confirmUpload = function() {
    document.getElementById('confirmZone').style.display = 'none';
    document.getElementById('uploadZone').style.display = 'block';
    uploadFolder(pendingUploadFiles);
};

// (Removed leftover code)
    
// Función para procesar carpeta 100% LOCALMENTE en el navegador
async function uploadFolder(files) {
    if (!files.length) return;
    
    let projectName = "cerbero_proyecto";
    if (files.length > 0 && files[0].webkitRelativePath) {
        const parts = files[0].webkitRelativePath.split('/');
        if (parts.length > 0 && parts[0]) {
            projectName = parts[0];
        }
    }
    
    // Lista básica de carpetas y archivos a ignorar en el frontend para no saturar el servidor
    const ignorePatterns = [
        '/node_modules/', '\\node_modules\\', '/venv/', '/.venv/', '/env/', '/.env',
        '/.git/', '/__pycache__/', '/.idea/', '/.vscode/', '/.next/', '/.nuxt/',
        '/dist/', '/build/', '/out/', '/target/', '/bin/', '/obj/',
        '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo', '.pyd',
        '.jpg', '.jpeg', '.png', '.gif', '.ico', '.webp', '.mp4', '.mp3', '.pdf', '.zip', '.rar', '.tar', '.gz'
    ];
    
    let validFiles = [];
    let ignoredCount = 0;
    
    for (let file of files) {
        const relativePath = file.webkitRelativePath || file.name;
        
        let shouldIgnore = false;
        for (let pattern of ignorePatterns) {
            if (relativePath.includes(pattern) || relativePath.endsWith(pattern)) {
                shouldIgnore = true;
                break;
            }
        }
        
        if (!shouldIgnore) {
            validFiles.push(file);
        } else {
            ignoredCount++;
        }
    }
    
    const statusDiv = document.getElementById('uploadStatus');
    
    if (validFiles.length === 0) {
        if (statusDiv) statusDiv.innerHTML = `❌ Error: No se encontraron archivos útiles o todos fueron ignorados.`;
        return;
    }
    
    const exportFormat = document.querySelector('input[name="exportFormat"]:checked')?.value || 'txt';
    const formatName = exportFormat === 'md' ? 'MARKDOWN' : 'TXT';
    
    if (statusDiv) {
        statusDiv.style.background = '#050508';
        statusDiv.style.border = '1px solid #00f3ff';
        statusDiv.style.padding = '15px';
        statusDiv.style.borderRadius = '8px';
        statusDiv.style.textAlign = 'left';
        statusDiv.style.color = '#00f3ff';
        statusDiv.style.fontFamily = 'monospace';
        statusDiv.style.boxShadow = '0 0 15px rgba(0, 243, 255, 0.2)';
        statusDiv.innerHTML = `> Iniciando protocolo de extracción 100% LOCAL...<br>> Analizando ${files.length} archivos en total...<br>> Ignorando dependencias y binarios (${ignoredCount} ignorados)...<br>> Procesando ${validFiles.length} archivos de código fuente en RAM...<br><span style="color:#b026ff; animation: blackHolePulse 1s infinite;">> Generando archivo ${formatName}...</span>`;
    }

    try {
        let outputLines = [];
        outputLines.push("=".repeat(60));
        outputLines.push("SYSTEM INITIALIZATION: CERBERUS PROTOCOL ENGAGED");
        outputLines.push("=".repeat(60));
        outputLines.push("The following is the complete, raw source code of a software project.");
        outputLines.push("As an advanced AI assistant, your directive is to thoroughly analyze");
        outputLines.push("the architecture, logic, and dependencies of this codebase.");
        outputLines.push("Please assume the role of a Principal Software Engineer.");
        outputLines.push("All your subsequent responses must be in SPANISH (Español), highly");
        outputLines.push("technical, concise, and directly address the context provided below.");
        outputLines.push("");
        outputLines.push(`Archivos de código procesados localmente: ${validFiles.length}`);
        outputLines.push("=".repeat(60) + "\n");

        for (let file of validFiles) {
            const path = file.webkitRelativePath || file.name;
            outputLines.push(`## ${path}`);
            outputLines.push("-".repeat(40));
            
            try {
                let content = await file.text();
                // Truncar archivos gigantes (25,000 caracteres)
                if (content.length > 25000) {
                    content = content.substring(0, 25000) + "\n... [CONTENIDO TRUNCADO]";
                }
                
                // Intentar sacar el lenguaje
                let ext = path.split('.').pop().toLowerCase();
                if (ext === path.toLowerCase()) ext = 'text'; // Sin extensión
                
                outputLines.push("```" + ext);
                outputLines.push(content);
                outputLines.push("```");
            } catch (e) {
                outputLines.push("[ARCHIVO BINARIO O ILEGIBLE - Ignorado]");
            }
            outputLines.push("\n" + "=".repeat(60) + "\n");
        }

        const blobContent = outputLines.join("\n");
        const blobType = exportFormat === 'md' ? 'text/markdown;charset=utf-8' : 'text/plain;charset=utf-8';
        const blob = new Blob([blobContent], { type: blobType });
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${projectName}.${exportFormat}`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        
        if (typeof playSciFiSound !== 'undefined') playSciFiSound('success');
        if (statusDiv) statusDiv.innerHTML = `<span style="color:#00ff9d;">> [ÉXITO]</span> Proyecto procesado LOCALMENTE de forma ultra-rápida y descargado.`;

        // Actualizar el contador del servidor en segundo plano
        fetch('/p/api/upload-folder/', { method: 'POST', body: new FormData() }).catch(()=>console.log("Stats ping"));

    } catch(error) {
        if (typeof playSciFiSound !== 'undefined') playSciFiSound('error');
        if (statusDiv) statusDiv.innerHTML = `<span style="color:#ff4444;">> [ERROR]</span> Ocurrió un error leyendo los archivos: ${error.message}`;
    }
}

// (Eliminado onchange duplicado)

// Arrastrar carpeta
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--neon-blue)';
    uploadZone.style.background = 'rgba(0, 243, 255, 0.1)';
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.borderColor = 'rgba(0, 243, 255, 0.3)';
    uploadZone.style.background = 'var(--dark-3)';
});

uploadZone.addEventListener('drop', async (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'rgba(0, 243, 255, 0.3)';
    uploadZone.style.background = 'var(--dark-3)';
    uploadZone.classList.remove('black-hole-active');
    
    if (typeof playSciFiSound !== 'undefined') playSciFiSound('hover');

    const items = e.dataTransfer.items;
    const files = [];
    
    for (let item of items) {
        const entry = item.webkitGetAsEntry();
        if (entry) {
            const allFiles = await getAllFilesFromEntry(entry);
            files.push(...allFiles);
        }
    }
    
    if (files.length > 0) {
        prepareUpload(files); // <= AQUÍ ESTABA EL CONFLICTO
    } else {
        // Fallback si no soporta webkitGetAsEntry
        prepareUpload(Array.from(e.dataTransfer.files));
    }
});

// Función recursiva para leer carpetas
async function getAllFilesFromEntry(entry) {
    const files = [];
    if (entry.isFile) {
        return new Promise((resolve) => {
            entry.file(file => {
                file.webkitRelativePath = entry.fullPath.slice(1);
                resolve([file]);
            });
        });
    } else if (entry.isDirectory) {
        const reader = entry.createReader();
        return new Promise((resolve) => {
            reader.readEntries(async (entries) => {
                let allFiles = [];
                for (let ent of entries) {
                    const subFiles = await getAllFilesFromEntry(ent);
                    allFiles = allFiles.concat(subFiles);
                }
                resolve(allFiles);
            });
        });
    }
    return files;
}
document.getElementById('docsBtn')?.addEventListener('click', () => {
    window.location.href = '/docs/';
});


// ==================== GUÍA DE FRAMEWORKS ====================
const frameworkData = {
    django: { name: 'Django', files: ['tu_app/', 'templates/', 'static/', 'manage.py', 'requirements.txt'], desc: 'Framework web Python' },
    flutter: { name: 'Flutter', files: ['lib/', 'assets/', 'pubspec.yaml'], desc: 'Framework móvil Dart' },
    react: { name: 'React', files: ['src/', 'public/', 'package.json'], desc: 'Biblioteca JavaScript' },
    angular: { name: 'Angular', files: ['src/app/', 'angular.json', 'package.json'], desc: 'Framework TypeScript' },
    vue: { name: 'Vue.js', files: ['src/', 'public/', 'package.json'], desc: 'Framework progresivo JavaScript' },
    node: { name: 'Node.js', files: ['src/', 'routes/', 'package.json', 'server.js'], desc: 'Entorno JavaScript' },
    spring: { name: 'Spring Boot', files: ['src/main/java/', 'pom.xml'], desc: 'Framework Java' },
    laravel: { name: 'Laravel', files: ['app/', 'routes/', 'resources/views/', 'composer.json'], desc: 'Framework PHP' },
    html: { name: 'HTML/CSS/JS', files: ['index.html', 'css/', 'js/', 'assets/'], desc: 'Web estática' }
};

function showFrameworkGuide(framework) {
    const data = frameworkData[framework];
    const guideDiv = document.getElementById('frameworkGuideContent');
    const contentDiv = document.getElementById('frameworkGuideContent');
    
    if (data) {
        const filesList = data.files.map(f => `<li style="margin-bottom: 8px;">📁 <strong>${f}</strong></li>`).join('');
        
        guideDiv.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p style="color: #00ff9d; margin-bottom: 10px;">✅ <strong>${data.name}</strong> - ${data.desc}</p>
                    <p style="color: #00f3ff; margin-bottom: 10px;">📁 Archivos que debes subir:</p>
                    <ul style="list-style: none; padding: 0;">
                        ${filesList}
                    </ul>
                </div>
                <div>
                    <p style="color: #ffdd59; margin-bottom: 10px;">💡 Consejo:</p>
                    <p style="color: #888;">No subas carpetas como <strong>venv/</strong>, <strong>node_modules/</strong>, <strong>__pycache__/</strong> o <strong>.git/</strong></p>
                    <button onclick="copyFrameworkPrompt('${framework}')" class="btn-cyber btn-cyber-outline" style="margin-top: 15px;">📋 Copiar prompt para IA</button>
                </div>
            </div>
        `;
        guideDiv.style.display = 'block';
    }
}

function copyFrameworkPrompt(framework) {
    const data = frameworkData[framework];
    const prompt = `🎯 Tengo un proyecto en ${data.name}. Quiero que actúes como mi tutor de programación.

Mi proyecto usa estos archivos principales: ${data.files.join(', ')}

Por favor:
1. Explícame para qué sirve cada carpeta
2. Enséñame cómo funciona la estructura
3. Guíame paso a paso para entender el código

No asumas que sé programar. Quiero aprender.`;
    
    navigator.clipboard.writeText(prompt);
    alert('✅ Prompt copiado. Pégalo en la IA');
}

// ==================== SELECCIÓN DE LENGUAJE ====================
let currentLanguage = '';

function selectLanguage(lang) {
    const langNames = {
        python: 'Python', javascript: 'JavaScript', typescript: 'TypeScript',
        java: 'Java', dart: 'Dart', php: 'PHP', csharp: 'C#',
        go: 'Go', rust: 'Rust', ruby: 'Ruby'
    };
    
    currentLanguage = lang;
    document.getElementById('selectedLanguage').style.display = 'block';
    document.getElementById('langDisplay').innerHTML = `${langNames[lang]} (${lang})`;
    
    // Marcar el botón seleccionado
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.style.opacity = '0.6';
        btn.style.borderColor = '#00f3ff';
    });
    event.target.style.opacity = '1';
    event.target.style.borderColor = '#00ff9d';
}

function copyLanguagePrompt() {
    if (!currentLanguage) {
        alert('⚠️ Primero selecciona un lenguaje');
        return;
    }
    
    const prompt = `📝 Mi proyecto está escrito en ${currentLanguage.toUpperCase()}. 
    
Quiero que actúes como mi tutor. Explícame los conceptos clave de este lenguaje que necesito saber para entender mi proyecto.

No asumas que sé nada. Voy empezando.`;
    
    navigator.clipboard.writeText(prompt);
    alert('✅ Prompt de lenguaje copiado. Pégalo en la IA');
}
    