import httpRequest from '@/api/httpRequest.ts';


export const updateLastActive = (param: any) => {
  return httpRequest.post('/api/user//currentUser/stat/behaviorLog', param);
};

