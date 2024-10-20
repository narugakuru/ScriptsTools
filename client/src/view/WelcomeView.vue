
<script>

</script>

<template>

    <Logos/>
    <el-form label-width="120px">
        <el-form-item label="源文件夹路径">

            <el-input placeholder="请输入源文件夹路径"></el-input>

        </el-form-item>


        <el-form-item label="目标文件夹路径">

            <el-input placeholder="请输入目标文件夹路径"></el-input>

        </el-form-item>


        <el-form-item label="排除文件扩展名">

            <el-input placeholder="请输入排除的文件扩展名，以逗号分隔"></el-input>

        </el-form-item>

        <el-form-item label="排除文件夹">

            <el-input placeholder="请输入排除的文件夹，以逗号分隔"></el-input>

        </el-form-item>


        <el-form-item label="强制更新所有文件">

            <el-switch></el-switch>

        </el-form-item>

        <el-form-item>

            <el-button type="primary">执行</el-button>

        </el-form-item>

    </el-form>

</template>
