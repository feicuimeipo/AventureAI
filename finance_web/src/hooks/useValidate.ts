import { isReactive, reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';


// 自定义验证钩子
export function useValidate<T extends Record<string, any>>(initialFormData: any, rules: any) {
  // 创建响应式表单状态
  let formData = initialFormData;
  if (!isReactive(initialFormData)) {
    formData = reactive<T>(initialFormData);
  }


  const validateConfig = {
    $lazy: true,
  };

  // 使用vuelidate进行验证
  const v$ = useVuelidate(rules, formData, validateConfig);

  // 重置验证状态
  const resetValidation = () => {
    v$.value.$reset();
  };

  // 触发所有字段验证
  const doValidateForm = () => {
    v$.value.$touch();
    return !v$.value.$invalid;
  };

  // 获取验证错误信息
  const getErrors = () => {
    const errors: Record<string, string[]> = {};
    Object.keys(v$.value).forEach(key => {
      if (
        key !== '$invalid' &&
        key !== '$dirty' &&
        key !== '$error' &&
        key !== '$pending' &&
        v$.value[key].$errors
      ) {
        const fieldErrors = v$.value[key].$errors;
        if (fieldErrors && fieldErrors.length > 0) {
          errors[key] = fieldErrors.map((error: any) => {
            console.log(key + '=' + error.$message);
          });
        }
      }
    });


    return errors;
  };

  // 获取特定字段的错误信息
  const getFieldError = (field: string) => {
    if (!v$.value[field].$invalid && v$.value[field].$error) {
      v$.value[field].$errors.$message;
    }
    return '';
  };

  // 检查字段是否无效
  const doValidateField = (field: string) => {
    v$.value[field].$touch();
    return !v$.value[field].$invalid;
  };




  // 返回所有需要的响应式数据和方法
  return {
    formData,
    v$,
    resetValidation,
    doValidateForm,
    getErrors,
    getFieldError,
    doValidateField,
  };
}
