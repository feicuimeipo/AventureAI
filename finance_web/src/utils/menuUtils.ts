import type { LocaleMessage, RemoveIndexSignature } from "@intlify/core-base"
import type { ComposerTranslation, VueMessageType, LocaleMessageValue } from "vue-i18n"

export const globalEnv = () => {
  return import.meta.env;
};


export interface MenuItem {
  key: string | number;
  name: string,
  path: string,
  icon: string | null;
  isHot: boolean | null;
  isBlankTarget: boolean;
}

export const getHomeMenus = (t: ComposerTranslation<{ [x: string]: LocaleMessage<VueMessageType> }, string, RemoveIndexSignature<{ [x: string]: LocaleMessageValue<VueMessageType> }>, never, never, never>) => {
    return ([
      { name: t('about_us'), path: '#about', key: 1 },
      { name: t('platform_value'), path: '#values', key: 2 },
      { name: t('our_team'), path: '#team', key: 3 },
      { name: t('download_app'), path: '#download_app', key: 4 },
      { name: t('contact_us'), path: '#contact', key: 5 },
    ] as MenuItem[]);
}


export const getPartnerMenus = () => {

    return [
      { name: '发现搭子', path: '/partner/discovery', icon: '🔍 ', key: 1 },
      { name: '详情', path: '/partner/detail/:id', icon: '👤 ', key: 2 },
      { name: '消息', path: '/partner/message', icon: '💬 ', key: 3 },
      // { name: '发布需求', path: '/partner/post_need', icon: '✏️', key: 4 },
    ] as MenuItem[];
}


export const getPlatformMenus = () => {
    return [
      {
        name: '完善个人资料',
        path: '/platform/profile',
        icon: '👤 ',
        key: 1,
        isHot: false,
        isBlankTarget: false,
      },
      {
        name: '匹配搭子',
        path: '/partner',
        icon: '🔍 ',
        key: 7,
        isHot: false,
        isBlankTarget: true,
      },
      {
        name: '我的联合创始人',
        path: '/platform/my_cofounder',
        icon: '⚤ ',
        key: 2,
        isHot: false,
        isBlankTarget: false,
      },
      {
        name: '我的投意人',
        path: '/platform/my_investor',
        icon: '🤝 ',
        key: 3,
        isHot: false,
        isBlankTarget: false,
      },
      {
        name: 'BP管理',
        path: '/platform/my_bp',
        icon: '👨‍👩‍👧 ',
        key: 5,
        isHot: false,
        isBlankTarget: false,
      },
      {
        name: '我的资源',
        path: '/platform/my_resource',
        icon: '🤝 ',
        key: 3,
        isHot: false,
        isBlankTarget: false,
      },
      {
        name: '行业动态',
        path: '/platform/my_newsfeed',
        icon: '💬 ',
        key: 4,
        isHot: false,
        isBlankTarget: false,
      },
      {
        name: '站内消息',
        path: '/partner/message',
        icon: '💬 ',
        key: 3,
        isHot: false,
        isBlankTarget: true,
      },
    ] as MenuItem[];
}


export const getNeedsMenus = () => {
    return [
        { name: "发布需求", path: 'post_need',icon: "🔍 " ,key: 1},
        { name: "需求广场", path: 'needs_square' ,icon: "👤 ",key: 2},
       ]  as MenuItem[]
}



export const getNewsFeedMenus = () => {
  return [
    { name: 'AI行业', path: 'detail/:id', icon: '🔥 ', key: 'ai', isHot: true },
    { name: '企业SaaS', path: 'message', icon: '💬 ', key: 'saas' },
    { name: '融资动态', path: 'need', icon: '✏️', key: 'finance' },
    { name: '政策法规', path: 'message', icon: '💬 ', key: 'policy' },
    { name: '人事变动', path: 'need', icon: '✏️', key: 'hr' },
    { name: '产品发布', path: 'message', icon: '💬 ', key: 'newproduct' },
  ] as MenuItem[];
};



export const togleElementById = (elementId:string, display:boolean) =>{
    const obj = document.getElementById(elementId)
    if (obj){
        display? obj.style.display='block': obj.style.display='none'
    }
}


const getModuleStyle = (module:string) =>{
    switch (module){
        case "newsfeed":
        case "token":
        case "partner":
        case "platform":
            return "module-"+ module;
            break;
        default:
            return "module-default";
            break;
    }
}


export const getPlatformSyleClass = () => {
    return getModuleStyle("platform")
}

export const getPartnerStyleClass = () => {
    return getModuleStyle("partner")
}

export const getNeedsStyleClass = () => {
    return getModuleStyle("partner")
}

export const getNewsFeedStyle = () => {
    return getModuleStyle("newsfeed")
}

export const getHomeModuleStyle = () => {
  return getModuleStyle('default');
};

export const getDefaultModuleStyle = () => {
  return getModuleStyle('default');
};

