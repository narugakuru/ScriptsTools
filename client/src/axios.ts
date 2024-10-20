// src/axios.js 或 src/axios.ts
import axios from 'axios';

// 创建一个 Axios 实例
const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api', // 设置后端 API 地址
    timeout: 10000, // 请求超时设置（可选）
});


export default instance;
