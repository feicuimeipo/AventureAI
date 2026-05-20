interface ImportMetaEnv {
    readonly VITE_API_BASE_URL: string
    readonly VITE_APP_TITLE: string
    // 添加更多自定义变量
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
