<template>
    <div class="common-layout">
        <el-container>
            <BaseSide />
            <el-container class="header-main">
                <base-header/>
                <el-main>
                    <router-view />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script lang="ts" setup>

</script>

<style lang="less" scoped>
.common-layout {
    height: 100vh;
}

.header-main{
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0;
}
</style>