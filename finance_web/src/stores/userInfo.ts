import { defineStore } from 'pinia'
import { ref, computed } from 'vue' // 可以直接用 Vue 的响应式 API

// 定义并导出 Store，第一个参数是唯一 ID（必须）
export const useUserStore = defineStore('counter', () => {
    // 1. 状态 State：直接用 ref/reactive 声明（和组件内写法一致）
    const userInfo = ref({
        name: "张三",
        age: 20
    })

    // 2. 派生状态 Getter：直接用 computed 声明（有缓存）
    const userName = computed(() => userInfo.value.name)


    const updateUser = (newUser:any) => {
        userInfo.value = newUser
    }

    // 必须返回需要暴露的属性和方法
    return {
        userInfo,
        userName,
        updateUser
    }
})
