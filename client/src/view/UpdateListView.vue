<template>
    <Logos />
    <el-form label-width="120px">
        <el-form-item label="源文件夹路径">
            <el-input v-model="origin_path" placeholder="请输入源文件夹路径" class="input-params"></el-input>
        </el-form-item>

        <el-form-item label="目标文件夹路径">
            <el-input v-model="copy_path" placeholder="请输入目标文件夹路径" class="input-params"></el-input>
        </el-form-item>

        <el-form-item label="文件列表">
            <el-input type="textarea" v-model="file_list" placeholder="请输入文件列表，每行一个文件路径" :rows="Number(10)"
                class="input-params"></el-input>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="executeTask" :loading="isRunning">
                {{ isRunning ? '执行中...' : '执行' }}
            </el-button>
            <!-- 添加清空日志按钮 -->
            <el-button type="danger" @click="clearLog" :disabled="isRunning">
                清空日志
            </el-button>
        </el-form-item>

        <!-- 添加日志显示区域 -->
        <el-form-item label="执行日志">
            <div class="log-container">
                <el-input type="textarea" v-model="logContent" readonly :rows="Number(15)" class="log-area"></el-input>
                <div class="log-status" v-if="isConnected">
                    <el-tag type="success">已连接</el-tag>
                </div>
            </div>
        </el-form-item>
    </el-form>
</template>

<script>
import axios from '../axios';  // 使用已经创建的 axios 实例
import { ElMessage } from 'element-plus'
import { openDB } from 'idb';

export default {
    data() {
        return {
            script_name: 'copy_list',
            origin_path: '',
            copy_path: '',
            file_list: '',
            logContent: '',  // 初始化日志内容
            isConnected: false,
            isExecuting: false,
            isRunning: false,
        };
    },
    async created() {
        // 在组件创建时加载 IndexedDB 中的数据
        const db = await openDB('app', 1, {
            upgrade(db) {
                db.createObjectStore('params', { keyPath: 'script_name' });
            },
        });

        const entry = await db.get('params', this.script_name);

        if (entry) {
            this.origin_path = entry.origin_path;
            this.copy_path = entry.copy_path;
            this.file_list = entry.file_list;
        } else {
            this.origin_path = 'Z:/ssl-htdocs';
            this.copy_path = 'E:/WorkSpace/WebKaisyu/html_11';
            this.file_list = 'effort/content.html';
        }
    },
    methods: {
        async executeTask() {
            this.isRunning = true;  // 开始执行任务，设置为执行中
            try {
                // 保存参数到 IndexedDB
                const db = await openDB('app', 1);
                await db.put('params', {
                    script_name: this.script_name,
                    origin_path: this.origin_path,
                    copy_path: this.copy_path,
                    file_list: this.file_list
                });

                // 1. 先建立WebSocket连接
                await this.setupWebSocket(this.script_name);

                // 2. 确认WebSocket连接成功后再发送HTTP请求
                const payload = {
                    origin_path: this.origin_path,
                    copy_path: this.copy_path,
                    file_list: this.file_list.split('\n').filter(line => line.trim())
                };

                const response = await axios.post(`/script/${this.script_name}`, payload);
                console.log('发送的参数:', payload);
                const { code, message, data } = response.data;
                console.log(code, message, data)

                // 显示响应结果为消息提醒
                ElMessage({
                    message: `响应数据: ${JSON.stringify(data)}`,
                    type: 'success',
                    duration: 5000
                });

                // // 可以设置一个定时器，在特定时间后主动关闭连接
                // setTimeout(() => {
                //     if (this.socket.readyState === WebSocket.OPEN) {
                //         console.log('主动关闭连接');
                //         this.socket.close();
                //     }
                // }, 3000); // 10秒后关闭

            } catch (error) {
                console.error('执行任务失败:', error);
                ElMessage({
                    message: `执行任务失败\nCode: ${error.response?.data?.code}\nMessage: ${error.response?.data?.message}\nData: ${JSON.stringify(error.response?.data?.data)}`,
                    type: 'error',
                    duration: 5000
                });
            } finally {
                this.isRunning = false;  // 任务执行完毕，设置为未执行

            }
        },
        // 改进的WebSocket连接方法
        async setupWebSocket(scriptName) {
            return new Promise((resolve, reject) => {
                this.socket = new WebSocket(`ws://localhost:8000/api/script/ws/${scriptName}`);

                this.socket.onopen = () => {
                    console.log("WebSocket connected");
                    this.isConnected = true;  // 更新连接状态
                    resolve();
                };

                this.socket.onerror = (error) => {
                    console.error("WebSocket connection failed:", error);
                    this.isConnected = false;  // 更新连接状态
                    reject(error);
                };

                this.socket.onmessage = (event) => {
                    const logMessage = event.data;
                    this.appendLog(logMessage);
                    console.log("Received message:", logMessage);  // 实时打印消息到控制台
                };

                this.socket.onclose = () => {
                    console.log("WebSocket connection closed");
                    this.isConnected = false;  // 更新连接状态
                    this.appendLog("\n=== 连接已关闭 ===\n");
                };
            });
        },

        // 改进的日志追加方法
        appendLog(message) {
            this.logContent += message + "\n";
            // 自动滚动到底部
            this.$nextTick(() => {
                const textarea = document.querySelector('.log-area textarea');
                if (textarea) {
                    textarea.scrollTop = textarea.scrollHeight;
                }
            });
        },

        clearLog() {
            this.logContent = '';
        },

        async saveLog() {
            try {
                const parentPath = this.copy_path.substring(0, this.copy_path.lastIndexOf('/'));
                const logFilePath = `${parentPath}/copy_list.log`;

                const payload = {
                    logContent: this.logContent,
                    logFilePath: logFilePath
                };

                const response = await axios.post('/save-log', payload);
                const { code, message } = response.data;

                if (code === 200) {
                    ElMessage({
                        message: '日志保存成功',
                        type: 'success',
                        duration: 5000
                    });
                } else {
                    throw new Error(message);
                }
            } catch (error) {
                console.error('保存日志失败:', error);
                ElMessage({
                    message: `保存日志失败: ${error.message}`,
                    type: 'error',
                    duration: 5000
                });
            }
        }


    },

};
</script>


<style scoped>
.log-container {
    width: 100%;
    max-width: 1200px;
}

.input-params {
    max-width: 1200px;
}
</style>