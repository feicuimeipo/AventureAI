import { UserRoleEnum } from '@/types/userBO.ts';

interface Role{
  tag: string;
  name: string;
  intro: string;
  icon: string;
  personalCount: number;
  class: string
}

export const getRoleDesc = (role: string) => {
  for (let i = 0; i < RoleItems.length; i++) {
    if (RoleItems[i].tag === role) {
      return RoleItems[i].name;
    }
  }
};


export const RoleItems: Role[] = [
  {
    tag: UserRoleEnum.FOUNDER,
    name: '创业者',
    intro: '寻找资源与连接',
    icon: '🚀',
    personalCount: 1243,
    class: 'rc role-card',
  },
  {
    tag: UserRoleEnum.INVESTOR,
    name: '投资人',
    intro: '发现优质项目',
    icon: '💼',
    personalCount: 387,
    class: 'rc role-card',
  },
  {
    tag: UserRoleEnum.EXPERT,
    name: '行业专家',
    intro: '分享知识，建立品牌',
    icon: '🎓',
    personalCount: 842,
    class: 'rc role-card',
  },
  {
    tag: UserRoleEnum.FA,
    name: '顾问',
    intro: '提供专业咨询',
    icon: '📌',
    personalCount: 900,
    class: 'rc role-card',
  },
  {
    tag: UserRoleEnum.CORP,
    name: '企业方',
    intro: '寻找创新供应商',
    icon: '🏢',
    personalCount: 328,
    class: 'rc role-card',
  },
  {
    tag: UserRoleEnum.GOV,
    name: '政府',
    intro: '寻找资源合答',
    icon: '🏫',
    personalCount: 500,
    class: 'rc role-card',
  },
];


interface Items {
  tag: string;
  name: string;
  icon: string;
  class: string;
}

export const UserTitles: Items[] = [
  { tag: 'CEO', name: 'CEO/首席运营官', icon: '', class: 't-chip' },
  { tag: 'CTO', name: 'CTO/技术负责人', icon: '', class: 't-chip' },
  { tag: 'COO', name: 'COO/运营负责人', icon: '', class: 't-chip' },
  { tag: 'CMO', name: 'CMO/市场负责人', icon: '', class: 't-chip' },
  { tag: 'CFO', name: 'CFO/财务顾问', icon: '', class: 't-chip' },
  { tag: 'CoreEngineer', name: '核心工程师', icon: '', class: 't-chip' },
  { tag: 'Consultant', name: '行业顾问', icon: '', class: 't-chip' },
];

export const IndustryItems: Items[] = [
  { tag: 'AL_ML', name: 'AI/大模型', icon: '🤖 ', class: 't-chip' },
  { tag: 'SAAS', name: '企业SAAS', icon: '📦 ', class: 't-chip' },
  { tag: 'ConsumerGoods', name: '消费品', icon: '🛒 ', class: 't-chip' },
  { tag: 'NewEnergy', name: '新能源', icon: '🔌 ', class: 't-chip' },
  { tag: 'HealthCare', name: '医疗健康', icon: '💊 ', class: 't-chip' },
  { tag: 'HardwareRobot', name: '硬件机器人', icon: '🏭 ', class: 't-chip' },
  { tag: 'CrossBorderEcommerce', name: '跨境电商', icon: '🛩 ', class: 't-chip' },
  { tag: 'EducationalTechnology', name: '教育科技', icon: '📗 ', class: 't-chip' },
  { tag: 'FinTech', name: '金融科技', icon: '🏦 ', class: 't-chip' },
];

export const ProjectStageItems: Items[] = [
  { tag: 'IdeaPeriod', name: '想法期', icon: '💡 ', class: 't-chip' },
  { tag: 'ProductDeveloping', name: '产品研发', icon: '🔧 ', class: 't-chip' },
  { tag: 'Incoming', name: '已有收入', icon: '📈 ', class: 't-chip' },
  { tag: 'FinancingInProgress', name: '融资中', icon: '💰 ', class: 't-chip' },
];


export const NeedTagsItems: Items[] = [
  { tag: 'seeking_cofounder', name: '找联合创始人', icon: '🤝 ', class: 't-chip' },
  { tag: 'seeking_angelInvestor', name: '寻找天使投资', icon: '💰 ', class: 't-chip' },
  { tag: 'recruiting_coreTeam', name: '招核心团队', icon: '👥 ', class: 't-chip' },
  { tag: 'hunting_customers', name: '找早期客户', icon: '🛒 ', class: 't-chip' },
  { tag: 'connecting_resource', name: '对接产业资源', icon: '🏢 ', class: 't-chip' },
];

export const WorkTypeItems: Items[] = [
  // {tag: 'CEO/创始人', name: '不限', icon: '', class: 'stag' },
  { tag: 'FullTime', name: '全职', icon: '', class: 't-chip' },
  { tag: 'PartTime', name: '兼职', icon: '', class: 't-chip' },
  { tag: 'Consultant', name: '顾问', icon: '', class: 't-chip' },
];

export const SkillTagsItems: Items[] = [
  { tag: 'ProductDesigner', name: '产品设计', icon: '🤝 ', class: 'stg' },
  { tag: 'FullStackDevelopment', name: '全栈开发', icon: '💰 ', class: 'stg' },
  { tag: 'AL_ML', name: 'AI/ML', icon: '👥 ', class: 'stg' },
  { tag: 'Marketing', name: '市场营销', icon: '🛒 ', class: 'stg' },
  { tag: 'BusinessNegotiation', name: '商业谈判', icon: '🏢 ', class: 'stg' },
  { tag: 'Financing', name: '财务融资', icon: '🏢 ', class: 'stg' },
  { tag: 'SupplyChainManagement', name: '供应链', icon: '🏢 ', class: 'stg' },
];

export const FundingStageItems: Items[] = [
  { tag: 'Seed', name: '种子轮', icon: '🤝 ', class: 't-chip' },
  { tag: 'Angel', name: '天使轮', icon: '💰 ', class: 't-chip' },
  { tag: 'PreA', name: 'Pre-A轮', icon: '👥 ', class: 't-chip' },
  { tag: 'A', name: 'A轮', icon: '🛒 ', class: 't-chip' },
  { tag: 'B_B+', name: 'B轮及以后', icon: '📈 ', class: 't-chip' },
  { tag: 'Unfunded', name: '未融资', icon: '🏢 ', class: 't-chip' },
];


export const InvestmentTagsItems: Items[] = [
  { tag: 'Seed', name: '种子轮', icon: '🤝 ', class: 'stg' },
  { tag: 'Angel', name: '天使轮', icon: '💰 ', class: 'stg' },
  { tag: 'PreA', name: 'Pre-A轮', icon: '👥 ', class: 'stg' },
  { tag: 'A', name: 'A轮', icon: '🛒 ', class: 'stg' },
  { tag: 'B_B+', name: 'B轮及以后', icon: '🏢 ', class: 'stg' },
];
