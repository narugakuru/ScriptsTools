import { createRouter, createWebHistory } from 'vue-router';


const routes = [

  {
    path: '/static',
    name: 'AppLayouts',
    component: () => import('../components/layouts/AppLayouts.vue'),
    children: [
      {
        path: '/static',
        redirect: '/scriptslist', // 默认重定向到 /index
      },
      {
        path: '/index',
        name: 'index',
        component: () => import('../view/IndexView.vue'),
      },
      {
        path: '/scriptslist',
        name: 'scriptslist',
        component: () => import('../view/ScriptsList.vue'),
      },
      {
        path: '/script/:scriptName',
        name: 'ScriptsFormTemp',
        component: () => import('../view/ScriptsFormTemp.vue'),
        props: true
      },
      {
        path: '/scripts',
        name: 'scripts',
        component: () => import('../view/ScriptsForm.vue'),
      },
      {
        path: '/upload',
        name: 'upload',
        component: () => import('../view/UploadView.vue'),
      },
      {
        path: '/welcome',
        name: 'welcome',  
        component: () => import('../view/WelcomeView.vue'),
      },
      {
        path: '/updateList',
        name: 'updateList',
        component: () => import('../view/UpdateListView.vue'),
      },
      {
        path: '/logs',
        name: 'logs',
        component: () => import('../view/LogsView.vue'),
      },
    ]
  },
  {
    path: '/:catchAll(.*)', // 捕获所有未匹配的路由
    redirect: '/welcome', // 或者重定向到一个404页面
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;