import httpRequest from '@/api/httpRequest.ts';

export const getCurrentUserInfo = () => {
  return httpRequest.get('/api/user/currentUser/info', {});
};

export const doLoginState = () => {
  return httpRequest.get('/api/user/currentUser/loginState', {});
};

export const getCurrentUserDetail = () => {
  return httpRequest.get('/api/user/currentUser/info', {});
};