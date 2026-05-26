interface ImportMetaEnv {
    readonly VITE_API_BASE_URL: string
    readonly VITE_APP_HOST: string
    readonly VITE_APP_TITLE: string
    // 添加更多自定义变量
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}

declare global {
    const defineProps: typeof import('vue').defineProps
    const defineEmits: typeof import('vue').defineEmits
    const defineExpose: typeof import('vue').defineExpose
    const withDefaults: typeof import('vue').withDefaults
}
export {}