export interface WebSocketOptions {
    onOpen?: () => void;
    onError?: (error: Event) => void;
    onMessage?: (message: string) => void;
    onClose?: () => void;
}

export function setupWebSocket(url: string, options: WebSocketOptions) {
    return new Promise<WebSocket>((resolve, reject) => {
        const socket = new WebSocket(url);

        socket.onopen = () => {
            console.log("WebSocket connected");
            if (options.onOpen) options.onOpen();
            resolve(socket);
        };

        socket.onerror = (error) => {
            console.error("WebSocket connection failed:", error);
            if (options.onError) options.onError(error);
            reject(error);
        };

        socket.onmessage = (event) => {
            const logMessage = event.data;
            if (options.onMessage) options.onMessage(logMessage);
            console.log("Received message:", logMessage);
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed");
            if (options.onClose) options.onClose();
        };
    });
}


/* async setupWebSocketConnection(scriptName) {
    try {
        const url = `ws://localhost:8000/api/script/ws/${scriptName}`;
        await setupWebSocket(url, {
            onOpen: () => {
                this.isConnected = true;  // 更新连接状态
            },
            onError: (error) => {
                this.isConnected = false;  // 更新连接状态
            },
            onMessage: (logMessage) => {
                this.appendLog(logMessage);
            },
            onClose: () => {
                this.isConnected = false;  // 更新连接状态
                this.appendLog("\n=== 连接已关闭 ===\n");
            }
        });
    } catch (error) {
        console.error("WebSocket connection failed:", error);
    }
}, */