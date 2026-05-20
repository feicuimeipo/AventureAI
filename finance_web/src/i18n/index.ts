
import { createI18n } from 'vue-i18n'
import zh from './zh.json'
import en from './en.json'

const messages = {
    en,
    zh
}

const savedLocale = localStorage.getItem('locale') || 'zh'

const i18n = createI18n({
    legacy: false,
    locale: savedLocale,
    fallbackLocale: 'en',
    warnHtmlMessage: false,  // 关闭 HTML 检测警告
    messages
})


export function setLocale(lang: string) {
    i18n.global.locale.value = lang
    localStorage.setItem('locale', lang)
}

export default i18n
