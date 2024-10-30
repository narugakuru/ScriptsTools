<!-- def copy_files_with_structure(origin_path, copy_path, file_list):
我希望给fileList设置一个默认值，但这好像会出错，修复它
后端的api是/file/copy_list
参数是封装成字典或者json的origin_path, copy_path, file_list -->
<template>
    <Logos />
    <el-form label-width="120px">
        <el-form-item label="源文件夹路径">
            <el-input v-model="origin_path" placeholder="请输入源文件夹路径"></el-input>
        </el-form-item>

        <el-form-item label="目标文件夹路径">
            <el-input v-model="copy_path" placeholder="请输入目标文件夹路径"></el-input>
        </el-form-item>

        <el-form-item label="文件列表">
            <el-input type="textarea" v-model="file_list" placeholder="请输入文件列表，每行一个文件路径" rows="10"></el-input>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="executeTask">执行</el-button>
        </el-form-item>

        <!-- 添加日志显示区域 -->
        <el-form-item label="执行日志">
            <div class="log-container">
                <el-input type="textarea" v-model="logContent" readonly rows="15" class="log-area"></el-input>
                <div class="log-status" v-if="isConnected">
                    <el-tag type="success">已连接</el-tag>
                </div>
            </div>
        </el-form-item>
    </el-form>
</template>

<script>
import axios from '../axios';  // 使用已经创建的 axios 实例
import { ElMessage, ElMessageBox } from 'element-plus'


export default {
    data() {
        return {
            origin_path: 'E:/WorkSpace/WebKaisyu/ssl-htdocs-local',
            copy_path: 'E:/WorkSpace/WebKaisyu/html_1020',
            file_list: `recruit/msg01.html
recruit/way.html
recruit/carrerPath.html
recruit/training.html
recruit/other.html
common/template/footer.php
common2/tmp/footer.php`,
            isConnected: false,
            isExecuting: false,
        };
    },
    methods: {
        async executeTask() {
            try {
                // 1. 先建立WebSocket连接
                await this.setupWebSocket('copy_list');

                // 2. 确认WebSocket连接成功后再发送HTTP请求
                const payload = {
                    origin_path: this.origin_path,
                    copy_path: this.copy_path,
                    file_list: this.file_list.split('\n').filter(line => line.trim())
                };

                const response = await axios.post('/run_script/copy_list', payload);
                const { code, message, data } = response.data;
                console.log(code, message, data)
                // 显示响应结果为弹窗
                ElMessageBox.alert(`${JSON.stringify(data)}`, 'Response', {
                    confirmButtonText: '关闭',
                    callback: (action) => {
                        ElMessage({
                            type: 'info',
                            message: `action: ${action}`,
                        })
                    }
                });
            } catch (error) {
                console.error('执行任务失败:', error);
                ElMessageBox.alert('执行任务失败\nCode: ${code}\nMessage: ${message}\nData: ${JSON.stringify(data)}', '错误', {
                    confirmButtonText: '关闭',
                    callback: (action) => {
                        ElMessage({
                            type: 'error',
                            message: `action: ${action}`,
                        })
                    }
                });
            }
        },

        // 改进的WebSocket连接方法
        async setupWebSocket(scriptName) {
            return new Promise((resolve, reject) => {
                this.socket = new WebSocket(`ws://localhost:8000/api/run_script/ws/${scriptName}`);

                this.socket.onopen = () => {
                    console.log("WebSocket connected");
                    resolve();
                };

                this.socket.onerror = (error) => {
                    console.error("WebSocket connection failed:", error);
                    reject(error);
                };

                this.socket.onmessage = (event) => {
                    const logMessage = event.data;
                    this.appendLog(logMessage);
                };

                this.socket.onclose = () => {
                    console.log("WebSocket connection closed");
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
        }


    }
};
</script>



<!-- 
<style scoped>
el-form-item div.log-container {
    width: 100%;
    min-width: 300px;
    position: relative;
}

.log-area {
    width: 100%;
    font-family: monospace;
    background-color: #1e1e1e;
    color: #d4d4d4;
    line-height: 1.6;
}

.log-status {
    width: 100%;
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1;
}

:deep(.el-input__inner) {
    font-family: monospace !important;
}
</style> -->