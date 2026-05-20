import { ref, onMounted, onUnmounted } from 'vue';
import { useCurrentUserStore } from '@/stores/currentUser';
import { updateLastActive } from '@/api/user/userStat.ts'; // 假设你有用户Store


// 配置项
const CONFIG = {
  UPLOAD_INTERVAL: 60 * 1000, // 每60秒上报一次
  EVENTS: ['mousedown', 'keydown', 'touchstart', 'scroll'], // 监听的事件
};

let uploadTimer: number | null = null

export function useActiveTracker() {
  const userStore = useCurrentUserStore();
  const lastActiveTime = ref(Date.now());

  // 更新活跃时间
  const updateActiveTime = () => {
    lastActiveTime.value = Date.now();
  };

  // 上报函数
  const reportActiveTime = async () => {
    if (!userStore.isLogin) return;

    try {
      await updateLastActive({
        lastActiveTime: lastActiveTime.value,
        timestamp: Date.now(),
        duration: 0
      });
    } catch (error) {
      console.error('活跃时间上报失败', error);
    }
  };

  // 使用 sendBeacon 进行兜底上报（页面关闭时）
  const beaconReport = () => {
    if (!userStore.isLogin) return;

    const data = JSON.stringify({
      last_active: lastActiveTime.value,
      timestamp: Date.now(),
      type: 'beacon',
    });

    // sendBeacon 是异步的，但会在页面卸载前尝试发送，不阻塞卸载
    navigator.sendBeacon('/api/user/currentUser/stat/behaviorLog', data);
  };

  // 初始化监听
  const initTracker = () => {
    // 1. 绑定交互事件
    CONFIG.EVENTS.forEach(event => {
      window.addEventListener(event, updateActiveTime, { passive: true });
    });

    // 2. 启动定时上报
    uploadTimer = setInterval(reportActiveTime, CONFIG.UPLOAD_INTERVAL);

    // 3. 绑定页面卸载事件（兜底）
    window.addEventListener('beforeunload', beaconReport);
  };

  // 清理监听
  const destroyTracker = () => {
    // 移除交互事件
    CONFIG.EVENTS.forEach(event => {
      window.removeEventListener(event, updateActiveTime);
    });

    // 清除定时器
    if (uploadTimer) {
      clearInterval(uploadTimer);
      uploadTimer = null;
    }

    // 移除卸载事件
    window.removeEventListener('beforeunload', beaconReport);

    // 销毁前再上报一次，确保最新数据
    reportActiveTime();
  };

  onMounted(() => {
    initTracker();
  });

  onUnmounted(() => {
    destroyTracker();
  });

  return {
    lastActiveTime,
  };
}
