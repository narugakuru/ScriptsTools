client/src/components/LogsComponent.vue (6-20新增代码)
<template>
  <div>
    <h2>实时日志</h2>
    <div v-if="error">{{ error }}</div>
    <div v-else>
      <div v-for="log in logs" :key="log">{{ log }}</div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue'
import { useWebSocket } from 'vue-native-websocket-vue3'

export default defineComponent({
  name: 'LogViewer',
  props: {
    apiPath: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const logs = ref([]);
    const error = ref(null);
    const wsUrl = `ws://${window.location.host}/ws/${props.apiPath}`;

    const { connect, disconnect } = useWebSocket(wsUrl, {
      onmessage: (e) => logs.value.push(e.data),
      onopen: () => console.log('WebSocket connected'),
      onclose: () => {
        console.log('WebSocket disconnected');
        error.value = '后端api不可用';
      },
      onerror: (e) => {
        console.log('WebSocket error:', e)
        error.value = '后端api不可用';
      }
    });

    onMounted(() => connect());
    onBeforeUnmount(() => disconnect());

    return {
      logs,
      error
    }
  }
})
</script>

<style scoped>
/* 样式 */
</style>
