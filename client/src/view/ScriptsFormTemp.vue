<template>
    <div>
        <Logos />
        <el-form :model="formData" label-width="120px">
            <el-form-item v-for="field in formFields" :key="field.model" :label="field.label">
                <component :is="getComponentType(field.type)" v-model="formData[field.model]"
                    v-bind="getComponentProps(field)"></component>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="executeTask" :loading="isRunning">
                    {{ isRunning ? '执行中...' : '执行' }}
                </el-button>
                <el-button type="danger" @click="clearLog" :disabled="isRunning">
                    清空日志
                </el-button>
            </el-form-item>

            <!-- 添加日志显示区域 -->
            <el-form-item label="执行日志">
                <div class="log-container">
                    <el-input type="textarea" v-model="logContent" readonly :rows="Number(15)"
                        class="log-area"></el-input>
                    <div class="log-status" v-if="isConnected">
                        <el-tag type="success">已连接</el-tag>
                    </div>
                </div>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import axios from '../axios';  // 使用已经创建的 axios 实例
import { openDB } from 'idb';

export default {
    props: {
        scriptName: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            formFields: [],
            formData: {},
            logContent: '',  // 初始化日志内容
            isConnected: false,
            isRunning: false,
        };
    },
    watch: {
        scriptName: {
            immediate: true,
            handler(newScriptName) {
                this.loadFormConfig(newScriptName);
                this.loadFormData(newScriptName);  // 确保在 scriptName 变化时加载数据
            }
        }
    },
    async created() {
        await this.loadFormConfig(this.scriptName);
        await this.loadFormData(this.scriptName);  // 加载存储的表单数据
    },
    methods: {
        async loadFormConfig(scriptName) {
            try {
                const response = await axios.get('/static/formConfig.json');
                const formConfig = response.data.script_list;  // 先获取 script_list
                const viewFormConfig = formConfig[scriptName];  // 然后再获取特定的配置
                console.log('scriptName:', scriptName)
                console.log('script_list:', formConfig);  // 查看 script_list 的内容
                console.log('获取的配置:', response.data);  // 添加调试信息
                console.log('viewFormConfig:', viewFormConfig);  // 查看特定配置

                if (viewFormConfig) {
                    this.formFields = viewFormConfig.form_fields;
                    this.formFields.forEach(field => {
                        this.formData[field.model] = field.default; // 给参数设置default默认值
                    });
                } else {
                    throw new Error(`未找到 script_name 为 ${scriptName} 的表单配置`);
                }
            } catch (error) {
                console.error('加载表单配置失败:', error);
                ElMessage({
                    message: `加载表单配置失败: ${error.message}`,
                    type: 'error',
                    duration: 5000
                });
            }
        },
        getComponentType(type) {
            const componentMap = {
                input: 'el-input',
                textarea: 'el-input',
                // 你可以根据需要添加更多组件类型
            };
            return componentMap[type] || 'el-input';
        },
        getComponentProps(field) {
            const props = { placeholder: field.placeholder };
            if (field.type === 'textarea') {
                props.type = 'textarea';
                props.rows = field.rows || 5;
            }
            return props;
        },
        async executeTask() {
            this.isRunning = true;
            try {
                // 1. 先建立WebSocket连接
                await this.setupWebSocket(this.scriptName);

                // 2. 确认WebSocket连接成功后再发送HTTP请求
                const payload = { ...this.formData };
                console.log('发送的参数:', payload);
                const response = await axios.post(`/script/${this.scriptName}`, payload);

                const { code, message, data } = response.data;
                console.log(code, message, data)

                ElMessage({
                    message: `响应数据: ${JSON.stringify(data)}`,
                    type: 'success',
                    duration: 5000
                });

                // 执行成功后存储表单数据
                await this.saveFormData(this.scriptName);

            } catch (error) {
                console.error('执行任务失败:', error);
                ElMessage({
                    message: `执行任务失败: ${error.message}`,
                    type: 'error',
                    duration: 5000
                });
            } finally {
                this.isRunning = false;
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

        async saveFormData(scriptName) {
            const db = await openDB('formDataDB', 1, {
                upgrade(db) {
                    db.createObjectStore('formDataStore');
                }
            });
            // 深拷贝 formData 以确保没有不可克隆的内容
            const formDataCopy = JSON.parse(JSON.stringify(this.formData));
            await db.put('formDataStore', formDataCopy, scriptName);
        },

        async loadFormData(scriptName) {
            const db = await openDB('formDataDB', 1, {
                upgrade(db) {
                    db.createObjectStore('formDataStore');
                }
            });

            const storedData = await db.get('formDataStore', scriptName);
            if (storedData) {
                this.formData = storedData;
            }
        },
    }
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