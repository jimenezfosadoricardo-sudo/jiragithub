const exportarChatTabularInfallible = () => {
    // 1. Capturamos y filtramos los nodos principales de texto
    const todosLosNodos = Array.from(document.querySelectorAll('.copyable-text[data-testid="selectable-text"]'));
    const nodosPrincipales = todosLosNodos.filter(nodo => 
        !todosLosNodos.some(superior => superior !== nodo && superior.contains(nodo))
    );
    
    // 2. Procesamos el mapeo de datos
    let datosChat = nodosPrincipales.map((msg) => {
        // --- BARRERA ANTI-BASURA ---
        // Buscamos el contenedor de metadatos estricto.
        const contenedorMeta = msg.closest('[data-pre-plain-text]');
        
        // Si no tiene metadatos de mensaje (es el encabezado, una fecha, o un aviso de sistema), LO DESCARTAMOS.
        if (!contenedorMeta) {
            return null; 
        }

        const clon = msg.cloneNode(true);
        
        // Render de emojis nativos
        const emojis = clon.querySelectorAll('img[alt]');
        emojis.forEach(img => {
            const caracterEmoji = img.getAttribute('alt') || '';
            img.parentNode.replaceChild(document.createTextNode(caracterEmoji), img);
        });
        
        // Extracción de metadatos
        const metaText = contenedorMeta.getAttribute('data-pre-plain-text');
        let emisor = 'Desconocido';
        let fechaHora = 'Desconocida';
        
        const match = metaText.match(/\[(.*?)\]\s*(.*?):\s*$/);
        if (match) {
            fechaHora = match[1];
            emisor = match[2].trim();
        }
        
        // Normalización de tu emisor comercial
        if (emisor === "Padmi Soporte") {
            emisor = "Yo (Padmi Soporte)";
        }
        
        return {
            fecha_hora: fechaHora,
            emisor: emisor,
            mensaje: clon.innerText.trim()
        };
    });

    // 3. Limpiamos los nulos (la basura) y reasignamos los IDs secuenciales limpios (1, 2, 3...)
    datosChat = datosChat
        .filter(item => item !== null && item.mensaje.length > 0)
        .map((item, index) => ({
            id: index + 1,
            ...item
        }));

    // --- EXTRACCIÓN BULLETPROOF DEL NOMBRE DEL ARCHIVO ---
    let nombreArchivo = "";
    const elementoHeader = document.querySelector('span[data-testid="conversation-info-header-chat-title"]');
    
    if (elementoHeader && elementoHeader.innerText) {
        nombreArchivo = elementoHeader.innerText.trim().replace(/\s+/g, '').replace(/[^a-zA-Z0-9+_-]/g, '');
    } 
    
    if (!nombreArchivo) {
        const objetoCliente = datosChat.find(item => item.emisor !== "Yo (Padmi Soporte)");
        if (objetoCliente) {
            nombreArchivo = objetoCliente.emisor.replace(/\s+/g, '').replace(/[^a-zA-Z0-9+_-]/g, '');
        } else {
            nombreArchivo = "chat_desconocido_" + Date.now();
        }
    }

    // 4. Trigger de descarga automática
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(datosChat, null, 2));
    const descargarAnchor = document.createElement('a');
    descargarAnchor.setAttribute("href", dataStr);
    descargarAnchor.setAttribute("download", `${nombreArchivo}.json`);
    document.body.appendChild(descargarAnchor);
    descargarAnchor.click();
    descargarAnchor.remove();
    
    console.log(`¡Éxito total! Archivo guardado correctamente como: ${nombreArchivo}.json (Libre de basura UI)`);
};

exportarChatTabularInfallible();