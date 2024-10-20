<template>

    <Logos/>
    <el-form :model="form" label-width="120px">
        <el-form-item label="源文件夹路径">
            <el-input v-model="form.origin_path" placeholder="请输入源文件夹路径"></el-input>
        </el-form-item>

        <el-form-item label="目标文件夹路径">
            <el-input v-model="form.copy_path" placeholder="请输入目标文件夹路径"></el-input>
        </el-form-item>

        <el-form-item label="排除文件扩展名">
            <el-input v-model="excludeExtsInput" placeholder="请输入排除的文件扩展名，以逗号分隔"></el-input>
        </el-form-item>

        <el-form-item label="排除文件夹">
            <el-input v-model="excludeDirsInput" placeholder="请输入排除的文件夹，以逗号分隔"></el-input>
        </el-form-item>

        <el-form-item label="强制更新所有文件">
            <el-switch v-model="form.all_copy"></el-switch>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="submitForm">执行</el-button>
        </el-form-item>
    </el-form>
</template>

<script>


export default {
    data() {
        return {

            form: {
                origin_path: "Z:/ssl-htdocs", // 直接初始化为默认值
                copy_path: "E:/WorkSpace/WebKaisyu/ssl-htdocs-local", // 直接初始化为默认值
                exclude_exts: ['.pdf', '.PDF'],
                exclude_dirs: ['.git', 'pdf'],
                all_copy: false,
            },
            excludeExtsInput: '.pdf, .PDF', // 直接设置默认值
            excludeDirsInput: '.git, pdf', // 直接设置默认值
        }
    },
    methods: {
        submitForm() {
            this.form.exclude_exts = this.parseInput(this.excludeExtsInput, '排除文件扩展名');
            if (!this.form.exclude_exts) return;

            this.form.exclude_dirs = this.parseInput(this.excludeDirsInput, '排除文件夹');
            if (!this.form.exclude_dirs) return;

            // 添加请求头
            const config = {
                headers: {
                    'Content-Type': 'application/json' // 设置内容类型为 JSON
                }
            };

            this.$axios.post('/file/copy_folders', this.form, config) // 传递配置
                .then(response => {
                    console.log('提交成功:', response.data);
                    this.$message.success('提交成功！');
                })
                .catch(error => {
                    console.error('提交失败:', error);
                    this.$message.error('提交失败，请检查输入！');
                });
        },
        parseInput(input, label) {
            const parsedArray = input.split(',').map(item => item.trim()).filter(item => item);
            if (parsedArray.length === 0) {
                this.$message.error(`${label}不能为空或无效的输入！`);
                return false;
            }
            return parsedArray;
        }
    },
    mounted() {
        console.log('Welcome 组件已挂载', this.form);

        const storedForm = JSON.parse(localStorage.getItem('formData'));
        if (storedForm) {
            this.form = storedForm;
            this.excludeExtsInput = storedForm.exclude_exts.join(', ');
            this.excludeDirsInput = storedForm.exclude_dirs.join(', ');
        }


    },
    beforeRouteEnter(to, from, next) {
        this.$axios.get('/api/get_folder_data')
            .then(response => {
                // 使用 response 数据或删除 response 参数
                console.log(response.data); // 示例：打印 response 数据
                next(); // 调用 next() 以解决未使用的警告
            })
            .catch(error => {
                console.error(error); // 打印错误信息以使用 error 变量
                next(); // 调用 next() 以解决未使用的警告
            });
    },

}

</script>