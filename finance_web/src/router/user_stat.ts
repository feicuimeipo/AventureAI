// 模拟获取用户ID
import { getAuthToken } from '@/stores/token.ts';


// 行为日志接口
interface BehaviorLog {
  authToken: string;
  route: string;
  duration: number; // 毫秒
  lastActiveTime: number;
  type: 'page_stay' | 'active_heartbeat';
}

// 本地存储队列
let logQueue: BehaviorLog[] = [];

// 上传配置
const UPLOAD_INTERVAL = 30000; // 30秒上传一次
const API_URL = import.meta.env.VITE_APP_HOST + '/api/user/currentUser/stat/behaviorLog';

// 发送数据函数
export const sendLogs = async (isBeacon: boolean = false) => {
  if (logQueue.length === 0) return;

  const dataToSend = [...logQueue];
  logQueue = []; // 清空队列

  console.log('Uploading logs:', dataToSend);

  if (isBeacon) {
    // 页面卸载时使用 sendBeacon
    const blob = new Blob([JSON.stringify(dataToSend)], { type: 'application/json' });
    navigator.sendBeacon(API_URL, blob);
  } else {
    // 定时上传使用 fetch
    try {
      await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend),
      });
    } catch (e) {
      console.error('Upload failed, pushing back to queue', e);
      logQueue.unshift(...dataToSend); // 失败则放回队列
    }
  }
};

// 记录页面离开
export const recordPageLeave = (toRoute: string, pageEnterTime: number, currentRouteName:string) => {
  const now = Date.now();

  const duration = now - pageEnterTime;

  // 忽略极短时间的误触 (< 500ms)
  if (duration < 500 && currentRouteName === toRoute) return;

  const log: BehaviorLog = {
    authToken: getAuthToken() || "",
    route: currentRouteName,
    duration: duration,
    lastActiveTime: now,
    type: 'page_stay',
  };

  logQueue.push(log);
  console.log(`Left ${currentRouteName}, stayed for ${duration}ms`);

  // 重置进入时间
  pageEnterTime = now;
  currentRouteName = toRoute;
};

// 启动定时上传
export const startUploadTimer = (uploadTimer:number | null) => {
  if (uploadTimer) clearInterval(uploadTimer);
  uploadTimer = window.setInterval(() => {
    sendLogs(false);
  }, UPLOAD_INTERVAL);
};



