<template>
    <div>
        <el-container>
            <el-header>
                <h2>选择脚本</h2>
            </el-header>
            <el-main>
                <el-row :gutter="20">
                    <el-col :span="8" v-for="(value, key) in scriptList" :key="key">
                        <el-card @click="selectScript(key)" class="script-card">
                            <div>{{ key }}</div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import axios from '../axios'; // 使用已经创建的 axios 实例

export default {
    data() {
        return {
            scriptList: {}
        };
    },
    async created() {
        await this.loadScriptList();
    },
    methods: {
        async loadScriptList() {
            try {
                const response = await axios.get('/static/formConfig.json');
                this.scriptList = response.data.script_list;
            } catch (error) {
                console.error('加载脚本列表失败:', error);
                this.$message.error(`加载脚本列表失败: ${error.message}`);
            }
        },
        selectScript(scriptName) {
            console.log('Selected script:', scriptName);
            this.$router.push({ name: 'ScriptsFormTemp', params: { scriptName } }); // 确保传递 scriptName 参数
        }
    }
};
</script>

<style scoped>
.script-card {
    cursor: pointer;
    text-align: center;
    padding: 20px;
    transition: transform 0.3s;
}

.script-card:hover {
    transform: scale(1.05);
}
</style>