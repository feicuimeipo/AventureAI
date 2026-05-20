import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios';
// 引入NProgress, 引入nprogress样式文件
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import MessageBox from '@/utils/MessageBox.ts';
import { getAuthToken } from '@/stores/token.ts';


const createInstance = (baseURL: string) => {
  return axios.create({
    baseURL: baseURL,
    timeout: 80000,
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

// 创建实例
const service: AxiosInstance = createInstance(import.meta.env.VITE_API_BASE_URL);
// 添加请求拦截器
service.interceptors.request.use(
  config => {
    NProgress.start();

    // console.log("api"+import.meta.env.VITE_API_BASE_URL);
    // 在发送请求之前做些什么，例如设置token等
    const token = getAuthToken();
    // console.log("token="+token)
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    config.headers['content-type'] = 'application/json';
    // 展示进度条
    return config;
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);


// 添加响应拦截器
//响应拦截
service.interceptors.response.use(
  (res => {
    //返回数据
    // 关闭进度条
    NProgress.done();
    //console.log('返回数据：' + JSON.stringify(res) + "\n\n [请求URL] "+ res.config.url+" Status: "+ res.status);

    const { data } = res; //data = res.data

    if (res.status === 200) {
      return data;
    } else {
      const message = showMessage(res.status);
      console.error(message);
      MessageBox.Error(message || 'Error');
      return Promise.reject(new Error(message || 'Error'));
    }
  }),
    (error: any) => {
        // 关闭进度条
        NProgress.done();

        let message = '网络错误！';
        if (error.response) {
          message = showMessage(error.response.status);
        } else if (error.code === 'ECONNABORTED') {
          message = '请求超时';
        }

        console.error('error=>', error.message, ',msg=' + message);
        MessageBox.Error(message || 'Error');
        return Promise.reject(error);
    }
)

//添加request 类
class HttpRequest {
  // get 请求
  public get(url: any, params: any) {
    const config: AxiosRequestConfig = {
      method: 'get',
      params: params,
      url: url,
    };
    return service(config);
  }
  // post 请求
  public post(url: any, params: any) {
    const config: AxiosRequestConfig = {
      method: 'post',
      data: params,
      url: url,
    };
    return service(config);
  }

}


const showMessage = (status: number | string): string => {
  let message: string = '';
  switch (status) {
    case 400:
      message = '请求错误(400)';
      break;
    case 401:
      message = '未授权，请重新登录(401)';
      break;
    case 403:
      message = '拒绝访问(403)';
      break;
    case 404:
      message = '请求出错(404)';
      break;
    case 408:
      message = '请求超时(408)';
      break;
    case 500:
      message = '服务器错误(500)';
      break;
    case 501:
      message = '服务未实现(501)';
      break;
    case 502:
      message = '网络错误(502)';
      break;
    case 503:
      message = '服务不可用(503)';
      break;
    case 504:
      message = '网络超时(504)';
      break;
    case 505:
      message = 'HTTP版本不受支持(505)';
      break;
    default:
      message = `连接出错(${status})!`;
  }
  return `${message}，请检查网络或联系管理员！`;
};

const httpRequest = new HttpRequest()
export default httpRequest;