import { numeric } from '@vuelidate/validators';

declare module 'nprogress/nprogress.css';
declare module '@/styles/common.scss';
declare module '@/styles/*.scss';
declare module '@/styles/*.css';
declare module '@/styles/module-login-register.scss';
declare module '@@/styles/module_partner.scss';
declare module '@/styles/module-*.scss';
declare module  '@/styles/module_newsfeed.scss';

declare module '*.scss' {
  const content: Record<string, string>;
  export default content;
}

declare module '*.css' {
  const content: Record<string, string>;
  export default content;
}


export interface PageBO{
  page: number,
  perPage: number,
  total: number,
  is_last_page: boolean,
}