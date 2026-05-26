import httpRequest from '@/api/httpRequest.ts';
import type { PartnerSearchDTO } from '@/types/needBO.ts';

export const findMatchResultByParams = (param: PartnerSearchDTO) => {
  return httpRequest.get('/api/partner/list', param);
};

export const getCandidateDetail = (id: string) => {
  return httpRequest.get('/api/partner/detail/' + id, {});
};

export const getMatchScoreDetail = (id: string) => {
  return httpRequest.get('/api/partner/matchScore/' + id, {});
};


export const cancelAction = (param: any) => {
  return httpRequest.post('/api/partner/cancelAction', param);
};

export const addAction = (param: any) => {
  return httpRequest.post('/api/partner/addAction', param);
};

