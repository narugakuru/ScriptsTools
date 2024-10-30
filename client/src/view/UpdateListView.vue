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
            <el-input 
                type="textarea" 
                v-model="file_list" 
                placeholder="请输入文件列表，每行一个文件路径" 
                rows="10"
            ></el-input>
        </el-form-item>

        <el-form-item>
            <el-button 
                type="primary" 
                @click="executeTask" 
                :loading="isRunning"
            >
                {{ isRunning ? '执行中...' : '执行' }}
            </el-button>
        </el-form-item>
        
        <!-- 改进的日志显示区域 -->
        <el-form-item label="执行日志">
            <div class="log-container" ref="logContainer">
                <div 
                    v-for="(log, index) in logs" 
                    :key="index"
                    :class="getLogClass(log)"
                >
                    {{ log }}
                </div>
            </div>
        </el-form-item>
    </el-form>
</template>

<script>
import axios from '../axios';
import { ElMessage } from 'element-plus'
import { nextTick } from 'vue'

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
            logs: [],
            isRunning: false,
            ws: null,
            scriptName: 'copy_list' // 脚本名称
        };
    },
    methods: {
        initWebSocket() {
            // 关闭已存在的连接
            this.closeWebSocket();
            
            // 创建新的WebSocket连接
            this.ws = new WebSocket(`ws://localhost:8000/api/script/ws/${this.scriptName}`);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
            };
            
            this.ws.onmessage = (event) => {
                if (event.data === "Script execution completed") {
                    this.closeWebSocket();
                    this.isRunning = false;
                    ElMessage.success('任务执行完成');
                } else {
                    this.logs.push(event.data);
                    this.scrollToBottom();
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                ElMessage.error('WebSocket连接错误');
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.isRunning = false;
            };
        },

        closeWebSocket() {
            if (this.ws) {
                this.ws.close();
                this.ws = null;
            }
        },

        // 滚动到日志底部
        async scrollToBottom() {
            await nextTick();
            const container = this.$refs.logContainer;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        },

        // 获取日志样式
        getLogClass(log) {
            if (log.includes('ERROR')) return 'log-error';
            if (log.includes('WARNING')) return 'log-warning';
            if (log.includes('INFO')) return 'log-info';
            return 'log-default';
        },

        async executeTask() {
            if (this.isRunning) return;

            this.logs = []; // 清空之前的日志
            this.isRunning = true;

            // 准备参数
            const payload = {
                origin_path: this.origin_path,
                copy_path: this.copy_path,
                file_list: this.file_list.split('\n').filter(line => line.trim()) // 将文本转换为数组并过滤空行
            };

            try {
                // 先建立WebSocket连接
                this.initWebSocket();

                // 调用执行接口
                const response = await axios.post(`/script/${this.scriptName}`, payload);
                
                if (!response.data.status === 'success') {
                    throw new Error(response.data.message || '执行失败');
                }
            } catch (error) {
                console.error('执行任务失败:', error);
                ElMessage.error('执行任务失败: ' + error.message);
                this.closeWebSocket();
                this.isRunning = false;
            }
        }
    },

    // 组件销毁前关闭WebSocket连接
    beforeUnmount() {
        this.closeWebSocket();
    }
};
</script>

<style scoped>
.log-container {
    height: 300px;
    overflow-y: auto;
    border: 1px solid #dcdfe6;
    padding: 10px;
    background-color: #f5f7fa;
    font-family: monospace;
}

.log-error {
    color: #f56c6c;
}

.log-warning {
    color: #e6a23c;
}

.log-info {
    color: #409eff;
}

.log-default {
    color: #606266;
}

/* 自定义滚动条样式 */
.log-container::-webkit-scrollbar {
    width: 6px;
}

.log-container::-webkit-scrollbar-thumb {
    background-color: #909399;
    border-radius: 3px;
}

.log-container::-webkit-scrollbar-track {
    background-color: #f5f7fa;
}
</style>
