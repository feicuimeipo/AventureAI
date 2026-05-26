import httpRequest from '@/api/httpRequest.ts';
import type { ForgetPasswordBO,  PasswordLoginBO } from '@/types/userBO.ts';

export const doPasswordLogin = (params: PasswordLoginBO) => {
  return httpRequest.post('/api/user/doLoginByPassword', params);
};

export const doLogout = () => {
  return httpRequest.get('/api/user/doLogout', {});
};

export const doConfirmPhoneOrMail = (params: ForgetPasswordBO) => {
  return httpRequest.get('/api/user/forgetPassword/doConfirmPhoneOrMail', params);
};

export const doResetPassword = (params: any) => {
  return httpRequest.post('/api/user/forgetPassword/doResetPassword', params);
};

export const sendForgetPasswordAuthCodeByEmail = (email: string) => {
  return httpRequest.post('/api/user/forgetPassword/send_code_by_email', { email: email });
};

export const sendForgetPasswordAuthCodeByPhone = (phone: string) => {
  return httpRequest.post('/api/user/forgetPassword/send_code_by_phone', { phone: phone });
};
