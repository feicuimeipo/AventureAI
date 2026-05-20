import httpRequest from '@/api/httpRequest.ts';
import type { NeedVO } from '@/types/needBO.ts';

export const postNeeds = (param: NeedVO) => {
  return httpRequest.post('/needs/post', param);
};

export const editNeeds = (id: string, param: NeedVO) => {
  param.id = id;
  return httpRequest.post('/needs/edit', param);
};



export const getNeedList = () => {
  return httpRequest.get('/needs/list', {});
};

export const getNeedDetail = (id:string) => {
  return httpRequest.get('/needs/detail', {id:id});
};

