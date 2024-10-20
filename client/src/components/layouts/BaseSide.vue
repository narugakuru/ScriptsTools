<script lang="ts" setup>

import { isCollapse } from './layouts'


</script>

<template>
  <el-aside width="200px">
    <router-link to="/">
      <h1>Home</h1>
    </router-link>
    <el-scrollbar max-height="800">
      <el-menu router default-active="1" unique-opened :collapse="isCollapse">
        <el-menu-item index="/welcome">
          <el-icon>
            <setting />
          </el-icon>
          <!-- <router-link to="/">比对复制文件夹</router-link> -->
          <span>比对复制文件夹</span>
        </el-menu-item>
        <el-menu-item index="/updateList">
          <el-icon>
            <setting />
          </el-icon>
          <!-- <router-link to="/welcome">批量复制文件列表</router-link> -->
          <span>批量复制文件列表</span>
        </el-menu-item>
        <el-menu-item index="/logs">
          <el-icon>
            <document />
          </el-icon>
          <!-- <router-link to="/logs">日志</router-link> -->
          <span>日志</span>
        </el-menu-item>

      </el-menu>
    </el-scrollbar>
  </el-aside>
</template>



<style lang="scss" scoped>
h1 {
  text-align: center;
}

.el-aside {
  height: 100vh;
  width: auto;
  padding: 0;
}

.el-menu {
  width: 200px;
  height: 100vh;
  border-right: none;
  padding: 0;

  &.el-menu--collapse {
    width: 60px;

    &h1 {
      display: none;
    }
  }
}

.el-icon {
  width: 20px;
}



.el-scrollbar {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>