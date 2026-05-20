import httpRequest from '@/api/httpRequest.ts';

export const getCurrentUserInfo = () => {
  return httpRequest.get('/user/currentUser/info', {});
};

export const doLoginState = () => {
  return httpRequest.get('/user/currentUser/loginState', {});
};

export const getCurrentUserDetail = () => {
  return httpRequest.get('/user/currentUser/info', {});
};

