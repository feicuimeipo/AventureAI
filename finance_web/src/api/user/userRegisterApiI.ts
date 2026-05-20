

import httpRequest from '@/api/httpRequest.ts';
import type { UserBaseInfoBO, UserProfileBO } from '@/types/userBO.ts';

export const sendAuthCodeByEmail = (email: string) => {
  return httpRequest.post('/user/register/send_code_by_email', { email: email });
}

export const sendAuthCodeByPhone = (phone: string) => {
  return httpRequest.post('/user/register/send_code_by_phone', { phone: phone });
}

export const doRegister = (param: UserBaseInfoBO) => {
  return httpRequest.post('/user/register/do', param);
};

export const doSaveRole = (param: any) => {
  return httpRequest.post('/user/register/doSaveRole', param);
};

export const getUserRole = (userId: string) => {
  return httpRequest.get('/user/register/getUserRoleByUserId', { userId: userId });
};

export const doSaveUserProfile = (param: UserProfileBO) => {
  return httpRequest.post('/user/register/doSaveUserProfile', param);
};



