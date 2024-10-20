<script lang="ts" setup>

import { isCollapse } from './layouts'

</script>

<template>

  <el-header>

    <el-icon @click="isCollapse = !isCollapse" :size="25">

      <Expand v-show="isCollapse" />
      <Fold v-show="!isCollapse" />

    </el-icon>


    <el-breadcrumb separator="/">

      <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>

      <el-breadcrumb-item>

        <a href="/">promotion management</a>
      </el-breadcrumb-item>

      <el-breadcrumb-item>promotion list</el-breadcrumb-item>

      <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
    </el-breadcrumb>


  </el-header>

</template>

<style>
.el-header {
  display: flex;
  align-items: center;
}

.el-icon {
  /* margin-block: 10px; */
  margin-inline: 15px;
}
</style>