import httpRequest from '@/api/httpRequest.ts';
import type { PartnerSearchDTO } from '@/types/needBO.ts';

export const findMatchResultByParams = (param: PartnerSearchDTO) => {
  return httpRequest.get('/partner/list', param);
};

export const getCandidateDetail = (id: string) => {
  return httpRequest.get('/partner/detail/' + id, {});
};

export const getMatchScoreDetail = (id: string) => {
  return httpRequest.get('/partner/matchScore/' + id, {});
};


export const cancelAction = (param: any) => {
  return httpRequest.post('/partner/cancelAction', param);
};

export const addAction = (param: any) => {
  return httpRequest.post('/partner/addAction', param);
};

