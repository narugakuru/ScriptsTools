<script lang="ts" setup>

import { isCollapse } from './layouts'
import { ref } from 'vue';

const menuItems = ref([
  { index: '/welcome', icon: 'setting', label: '比对复制文件夹' },
  { index: '/updateList', icon: 'setting', label: '批量复制文件列表' },
  { index: '/logs', icon: 'document', label: '日志' },
  { index: '/scripts', icon: 'document', label: 'scripts' },
  { index: '/upload', icon: 'document', label: 'upload' },

]);

</script>


<template>
  <el-aside width="200px">
    <router-link to="/">
      <h1>Home</h1>
    </router-link>

    <el-scrollbar max-height="800">

      <el-menu router default-active="/updateList" unique-opened :collapse="isCollapse">
        
        <template v-for="item in menuItems" :key="item.index">
          <el-menu-item :index="item.index">
            <el-icon>
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.label }}</span>
          </el-menu-item>
        </template>

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