
// @ts-ignore
export const enum UserRoleEnum {
  FOUNDER = 'founder',
  INVESTOR = 'investor',
  FA = 'fa',
  EXPERT = 'expert',
  CORP = 'corp',
  GOV = 'gov'
}

export interface PasswordLoginBO {
  phoneOrEmail: string;
  password: string;
}

export interface ForgetPasswordBO {
  phoneOrEmail: string;
  certificationCode: string;
  password: string;
  confirmPassword: string;
  isVerified: boolean;
  userId: string;
}

export interface CurrentUserBO {
  userId: string | null;
  phone: string | null;
  email: string | null;
  role: string;
  title: '',
  displayName: string;
  industryTags: string;
  skillTags: string;
  projectName: string;
  projectStage: string;
  fundingStage: string;
  needTags: string;
  teamSize: number | '';
  investmentTags: string;
  completeness: number | '';
  firstName: string;
}

// 用户基本信息BO

export interface UserBaseInfoBO {
  phoneOrEmail: string;
  password: string;
  confirmPassword: string;
  verificationCode: string;
  isAgreement: boolean | false;
}


export interface UserProfileBO {
  userId: string;
  role: string;
  title: string;
  avatarUrl: string;
  displayName: string;
  bio: string;
  city: string;
  skillTags: string;
  industryTags: string;
  projectName: string;
  projectStage: string;
  teamSize: string;
  fundingStage: string;
  needTags: string;
  investmentTags: string;
  workType: string;
}


export interface RoleBO {
  userId: string;
  role: string;
}

export interface UserBehaviorBO {
  accessToken: string,
  action: string
  subAction: string,
}