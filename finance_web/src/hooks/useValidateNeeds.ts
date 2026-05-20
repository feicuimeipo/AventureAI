import { computed, isReactive, reactive } from 'vue';
import { helpers } from '@vuelidate/validators';
import { useValidate } from '@/hooks/useValidate.ts';
import type { NeedVO } from '@/types/needBO.ts';

// 自定义验证钩子
export function useValidatePostNeeds(initialFormData: any) {

  let formData = initialFormData;
  if (!isReactive(initialFormData)) {
    formData = reactive<NeedVO>(initialFormData);
  }

  const rules = computed(() => ({
    title: {
      required: helpers.withMessage('请输入需求标题', () => {
        return (formData.title && formData.status == 'active') || formData.status != 'active';
      }),
    },
    roleWanted: {
      required: helpers.withMessage('需要的岗位角色不能为空', () => {
        return (formData.roleWanted && formData.status == 'active') || formData.status != 'active';
      }),
    },
    workType: {
      required: helpers.withMessage('参与方式不能为空', () => {
        return (formData.workType && formData.status == 'active') || formData.status != 'active';
      }),
    },
    cityReqs: {
      required: helpers.withMessage('请选择所在城市', () => {
        return (formData.cityReqs && formData.status == 'active') || formData.status != 'active';
      }),
    },
    description: {
      required: helpers.withMessage('需求描述不能为空', () => {
        return (formData.description && formData.status == 'active') || formData.status != 'active';
      }),
    },
    industry: {
      required: helpers.withMessage('请选择所属赛道', () => true),
    },
    skillReqs: {
      required: helpers.withMessage('请选择至少一个技能标签', () => true),
    },
    equityRange: {
      required: helpers.withMessage('请输入激励方式', () => true),
    },
    vesting: {
      required: helpers.withMessage('请输入兑现方式', () => true),
    },
  }));


  const { v$, resetValidation, doValidateForm, getErrors, getFieldError, doValidateField } =
    useValidate(formData, rules);

  // 返回所有需要的响应式数据和方法
  return {
    formData,
    v$,
    rules,
    resetValidation,
    doValidateForm,
    getFieldError,
    doValidateField,
    getErrors
  };
}


