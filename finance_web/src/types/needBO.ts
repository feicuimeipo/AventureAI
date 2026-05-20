export interface NeedVO {
  id: string;
  title: string;
  roleWanted: string;
  workType: string;
  cityReqs: string;
  description: string;
  industry: string;
  skillReqs: string;
  equityRange: string;
  vesting: string;
}

export interface NeedDetailVO extends NeedVO {
  status: string,
  viewCount: number,
  expiredAt: string,
  createdAt: string,
}

export interface PartnerSearchDTO {
  needId?: string;
  myCandidateType?: string;
  rangeValue?: number;
}

export interface RadorValueVO {
  skill: number,
  industry: number,
  roleTitle: number,
  city: number,


}