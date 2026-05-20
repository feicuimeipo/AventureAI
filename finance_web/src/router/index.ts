import {createRouter, createWebHistory} from "vue-router";
import NProgress from 'nprogress'
// @ts-ignore
import 'nprogress/nprogress.css'
import { recordPageLeave, sendLogs, startUploadTimer } from '@/router/user_stat.ts';


const routes = [
  {
    path: '/',
    name: 'index',
    component: () => import('@/views/home/IndexHomeView.vue'),
    meta: {
      title: '首页',
    },
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/home/IndexHomeView.vue'),
    meta: {
      title: '首页',
    },
  },
  {
    path: '/platform',
    name: 'platform',
    component: () => import('@/views/platform/IndexPlatform.vue'),
    redirect: '/platform/profile',
    meta: {
      title: '首页',
    },
    children: [
      {
        path: 'profile',
        name: 'personal_profile',
        component: () => import('@/views/platform/MyProfileView.vue'),
      },
      {
        path: 'my_cofounder',
        name: 'my_cofounder',
        component: () => import('@/views/platform/MyCofounderView.vue'),
        children: [
          {
            path: ':id',
            name: 'my_cofounder_detail',
            component: () => import('@/views/platform/common/MyCandidateDetailView.vue'),
          },
        ],
      },
      {
        path: 'my_investor',
        name: 'my_candidate',
        component: () => import('@/views/platform/MyInvestorView.vue'),
        children: [
          {
            path: ':id',
            name: 'my_investor_detail',
            component: () => import('@/views/platform/common/MyCandidateDetailView.vue'),
          },
        ],
      },
      {
        path: 'my_bp',
        name: 'my_business_plan',
        component: () => import('@/views/platform/MyBusinessPlanView.vue'),
      },
      {
        path: 'my_newsfeed',
        name: 'my_newsfeed',
        component: () => import('@/views/platform/MyNewsfeed.vue'),
      },
      {
        path: 'my_resource',
        name: 'my_resource',
        component: () => import('@/views/platform/MyOtherCandidateView.vue'),
        children: [
          {
            path: ':id',
            name: 'my_resource_detail',
            component: () => import('@/views/platform/common/MyCandidateDetailView.vue'),
          },
        ],
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/users/UserLoginView.vue'),
    meta: {
      title: '用户登录',
    },
  },
  {
    path: '/forgetpassword',
    name: 'forget_password',
    component: () => import('@/views/users/UserForgetPassowrdView.vue'),
    meta: {
      title: '用户登录',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/users/register/IndexRegisterView.vue'),
    redirect: '/register',
    meta: {
      title: '用户注册',
    },
    children: [
      {
        path: '',
        name: 'base',
        component: () => import('@/views/users/register/UserRegisterBaseInfoView.vue'),
      },
      {
        path: 'role',
        name: 'register_role',
        component: () => import('@/views/users/register/UserRegisterRoleView.vue'),
      },
      {
        path: 'profile',
        name: 'register_profile',
        component: () => import('@/views/users/register/UserRegisterProfileView.vue'),
      },
      {
        path: 'finish',
        name: 'register_finish',
        component: () => import('@/views/users/register/UserRegisterFinishView.vue'),
      },
    ],
  },
  {
    path: '/partner',
    name: 'partner',
    component: () => import('@/views/partner/IndexPartnerView.vue'),
    redirect: '/partner/discovery',
    meta: {
      title: '创业搭子',
    },
    children: [
      {
        path: 'discovery',
        name: 'partner_discovery',
        component: () => import('@/views/partner/PartnerDiscoveryView.vue'),
      },
      {
        path: 'detail/:id',
        name: 'partner_detail',
        component: () => import('@/views/partner/PartnerDetail.vue'),
      },
      {
        path: 'message',
        name: 'message',
        component: () => import('@/views/chat/WebChatView.vue'),
      },
      {
        path: 'post_need',
        name: 'post_need',
        component: () => import('@/views/partner/PostNeedView.vue'),
        props: true,
      },
    ],
  },
  {
    path: '/newsfeed',
    name: 'newsfeed',
    component: () => import('@/views/newsfeed/IndexNewsFeedView.vue'),
    meta: {
      title: '行业动态',
    },
    redirect: '/newsfeed',
    children: [
      {
        path: '',
        name: 'newsfeed_index',
        component: () => import('@/views/newsfeed/NewsFeedHomeView.vue'),
      },
      {
        path: 'list/:type',
        name: 'list/:type',
        component: () => import('@/views/newsfeed/NewsfeedListView.vue'),
      },
      {
        path: 'detail/:id',
        name: 'news_detail',
        component: () => import('@/views/newsfeed/NewsfeedDetailView.vue'),
      },
      {
        path: 'subscription',
        name: 'subscription',
        component: () => import('@/views/newsfeed/NewsfeedSubscriptionView.vue'),
      },
      {
        path: 'favorite',
        name: 'favorite',
        component: () => import('@/views/newsfeed/MyFavoriteViewNewsfeed.vue'),
      },
    ],
  },
  {
    path: '/token',
    name: 'token',
    component: () => import('@/views/token/IndexTokenView.vue'),
    meta: {
      title: '个人Token中心',
    },
    redirect: '/token',
    children: [
      {
        path: '',
        name: 'token_home',
        component: () => import('@/views/token/TokenHomeView.vue'),
      },
    ],
  },
  {
    // 404页面
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: {
      title: '页面未找到',
    },
  },
];


const router = createRouter({
  history: createWebHistory(), //这里指定基本的URL
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (to.hash && to.hash.startsWith('#')) {
      return savedPosition || { el: to.hash, behavior: 'smooth', top: 80 };
    } else {
      // 否则回到顶部
      return { top: 0 };
    }
  },
});
export default router;

// 全局变量用于存储进入时间
let currentRouteName: string = '';
let pageEnterTime: number = Date.now();
let uploadTimer: number | null = null;

/**
 * 路由守卫：记录离开页面时的停留时间
 */
router.beforeEach((to, from) => {
  // 开启进度条
  NProgress.start();

  if (from.name) {
    recordPageLeave((to.name as string) || 'unknown', pageEnterTime, currentRouteName);
  } else {
    // 首次进入
    currentRouteName = (to.name as string) || 'unknown';
    pageEnterTime = Date.now();
  }

  // 设置页面标题
  document.title = to.meta.title
    ? `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE || 'Venture AI'}`
    : import.meta.env.VITE_APP_TITLE || 'Venture AI';

  return true;
});

router.afterEach((to, _from) => {
  // 关闭进度条
  NProgress.done();

  currentRouteName = (to.name as string) || 'unknown';
  if (!uploadTimer) startUploadTimer(uploadTimer);

});


// 监听页面卸载
//(toRoute: string, pageEnterTime: number, currentRouteName:string)
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', () => {
    recordPageLeave('unload', pageEnterTime, currentRouteName);
    sendLogs(true);
  });

  // 监听可见性变化，处理后台挂机
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      // 页面隐藏，记录一段停留
      recordPageLeave(currentRouteName,pageEnterTime,currentRouteName);
    } else {
      // 页面重新可见，重置计时
      pageEnterTime = Date.now();
    }
  });
}
