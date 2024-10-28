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
common2/tmp/footer.php` // 默认值，需要换行符'\n'
        };
    },
    methods: {
        async executeTask() {
            const payload = {
                origin_path: this.origin_path,
                copy_path: this.copy_path,
                file_list: this.file_list // 将每一行作为一个文件路径
            };

            try {
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
        }

    }
};
</script>
