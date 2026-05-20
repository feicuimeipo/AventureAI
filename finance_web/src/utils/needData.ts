interface NeedItem {
  tag: string;
  name: string;
  icon: string;
  class: string;
}

export interface RoleTypeItem {
  tag: string;
  name: string;
  icon: string;
  class: string;
  roleWanted: string;
  skillReq: string;
}

export const NeedRoleItems: NeedItem[] = [
  { tag: 'CEO', name: 'CEO/首席运营官', icon: '', class: 'stag' },
  { tag: 'CTO', name: 'CTO/技术负责人', icon: '', class: 'stag' },
  { tag: 'COO', name: 'COO/运营负责人', icon: '', class: 'stag' },
  { tag: 'CML', name: 'CMO/市场负责人', icon: '', class: 'stag' },
  { tag: 'CFO', name: 'CFO/财务顾问', icon: '', class: 'stag' },
  { tag: 'CoreEngineer', name: '核心工程师', icon: '', class: 'stag' },
  { tag: 'Investor', name: '投资人', icon: '', class: 'stag' },
  { tag: 'FinancialConsultant', name: '财务顾问', icon: '', class: 'stag' },
  { tag: 'NewProject', name: '新项目', icon: '', class: 'stag' },
  { tag: 'ResourceProvider', name: '资源方', icon: '', class: 'stag' },
];

export const SearchTagRoleWanted: RoleTypeItem[] = [
  {
    tag: 'CEO',
    name: 'CEO',
    icon: '',
    class: 'ftag',
    roleWanted: 'CEO,COO,CMO,founder',
    skillReq: '全部',
  },
  {
    tag: 'technology',
    name: '技术',
    icon: '',
    class: 'ftag',
    roleWanted: 'CTO,CoreEngineer',
    skillReq: '全栈开发,AI/ML工程师,产品设计,系统架构',
  },
  {
    tag: 'operator',
    name: '运营',
    icon: '',
    class: 'ftag',
    roleWanted: 'COO,CMO',
    skillReq: '增长运营,B2B销售,市场营销,供应链管理',
  },
  {
    tag: 'consultant',
    name: '顾问',
    icon: '',
    class: 'ftag',
    roleWanted: 'Consultant,CFO',
    skillReq: '财务融资,供应链管理,自定义',
  },
  {
    tag: 'investor',
    name: '投资人',
    icon: '',
    class: 'ftag',
    roleWanted: 'investor,gov,corp',
    skillReq: '财务融资,供应链管理,自定义',
  },
  {
    tag: 'resource',
    name: '资源方',
    icon: '',
    class: 'ftag',
    roleWanted: 'gov,corp',
    skillReq: '供应链管理,自定义',
  },
  {
    tag: 'NewProject',
    name: '新项目',
    icon: '',
    class: 'ftag',
    roleWanted: 'founder,CEO',
    skillReq: '供应链管理,自定义',
  },
];


export const SkillsTagsItems: NeedItem[] = [
  { tag: 'FullStackDevelopment',name: '全栈开发', icon: '', class: 'stag' },
  { tag: 'AI_ML_Engineer',name: 'AI/ML工程师', icon: '', class: 'stag' },
  { tag: 'ProductDesign',name: '产品设计', icon: '', class: 'stag' },
  { tag: 'Architecture',name: '系统架构', icon: '', class: 'stag' },
  { tag: 'GrowthOperation',name: '增长运营', icon: '', class: 'stag' },
  { tag: 'B2B_Sales',name: 'B2B销售', icon: '', class: 'stag' },
  { tag: 'Marketing',name: '市场营销', icon: '', class: 'stag' },
  { tag: 'Financing',name: '财务融资', icon: '', class: 'stag' },
  { tag: 'SupplyChainManagement',name: '供应链管理', icon: '', class: 'stag' },
  // { tag: '自定义', icon: '', class: 'stag'},
];



export const SearchTagCities: NeedItem[] = [
  { tag: 'All_RemoteCapability',name: '全部(可远程)', icon: '', class: 'ftag' },
  { tag: 'Beijing',name: '北京', icon: '', class: 'ftag' },
  { tag: 'Shanghai',name: '上海', icon: '', class: 'ftag' },
  { tag: 'Shenzhen',name: '深圳', icon: '', class: 'ftag' },
  { tag: 'OtherCities',name: '其他', icon: '', class: 'ftag' },
];

export const ParticipationItems: NeedItem[] = [
  { tag: 'FullTime', name: '全职', icon: '', class: 'stag' },
  { tag: 'PartTime', name: '兼职', icon: '', class: 'stag' },
  { tag: 'Consultant', name: '顾问', icon: '', class: 'stag' },
];

export const NeedStatusItem = [
  { value: 'active', name: '活跃' },
  { value: 'paused', name: '暂停' },
  { value: 'filled', name: '已招满' },
];


export const CitiesItems = SearchTagCities


