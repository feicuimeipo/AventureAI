import { computed, isReactive, reactive } from 'vue';
import {validEmail, validMobilePhone} from '@/utils/validate_utils.ts';
import {helpers, required} from '@vuelidate/validators';
import {useValidate} from '@/hooks/useValidate.ts';
import {type ForgetPasswordBO, type UserBaseInfoBO, type UserProfileBO, UserRoleEnum,} from '@/types/userBO.ts';


// 自定义验证钩子
export function useValidateUserRegister(initialFormData: UserBaseInfoBO) {
  // 创建响应式表单状态
  // 创建响应式表单状态
  const formData = reactive<UserBaseInfoBO>(initialFormData);

  const rules = computed(() => ({
    phoneOrEmail: {
      required: helpers.withMessage('邮箱不能为空', required),
      validatePhoneOrEmail: helpers.withMessage('手机号或邮件格式不正确', validatePhoneOrEmail),
    },
    password: {
      required: helpers.withMessage('密码不能为空', required),
      validatePassword: helpers.withMessage(
        '密码必须包含数字、字母和特殊字符中的至少两种',
        validatePassword
      ),
    },
    confirmPassword: {
      required: helpers.withMessage('请确认密码', required),
      sameAsPassword: helpers.withMessage('两次输入的密码不一致', confirmPassword),
    },
    verificationCode: {
      required: helpers.withMessage('验证码不能为空', required),
    },
    isAgreement: {
      required: helpers.withMessage('您必须同意服务条款和隐私政策才能继续', validateAgreement),
    },
  }));

  //验证手机号或邮件号
  const validatePhoneOrEmail = (value: string) => {
    if (value.includes('@')) {
      return validEmail(value);
    } else {
      return validMobilePhone(value);
    }
  };

  // 自定义验证函数：验证密码强度
  const validatePassword = (value: string) => {
    // 至少包含数字、字母、特殊字符中的两种
    const hasNumber = /\d/.test(value);
    const hasLetter = /[a-zA-Z]/.test(value);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);

    return (hasNumber && hasLetter) || (hasNumber && hasSpecial) || (hasLetter && hasSpecial);
  };

  // 自定义验证函数：检查两个字段是否相等
  // @ts-ignore
  const confirmPassword = (value: string) => {
    return value === formData.password;
  };

  const validateAgreement = (value: boolean) => {
    console.log('validateAgreement===', value);
    return value;
  };

  const { v$, resetValidation, doValidateForm, getErrors, getFieldError, doValidateField } =
    useValidate(formData, rules);

  // 返回所有需要的响应式数据和方法
  return {
    formData,
    v$,
    rules,
    validatePhoneOrEmail,
    validatePassword,
    confirmPassword,
    resetValidation,
    doValidateForm,
    getFieldError,
    doValidateField,
    getErrors,
  };
}

// 自定义验证钩子
export function useValidateUserProfile(initialFormData: any) {
  //const formData = reactive<UserProfileBO>(initialFormData);

  let formData = initialFormData;
  if (!isReactive(initialFormData)) {
    formData = reactive<UserProfileBO>(initialFormData);
  }

  const rules = computed(() => ({
    userId: {
      required: helpers.withMessage('用户编号不能为空', required),
    },
    role: {
      required: helpers.withMessage('用户角色色不能为空', required),
    },
    // avatarUr: {},
    displayName: {
      required: helpers.withMessage('真实名称不能为空', required),
    },
    city: {
      required: helpers.withMessage('所在城市不能为空', required),
    },
    title: {
      required: helpers.withMessage('请选择岗位', validateTitle),
    },
    bio: {
      required: helpers.withMessage('个人介绍不能为空', required),
    },
    industryTags: {
      required: helpers.withMessage('请选择至少一个行业标签', required),
    },
    skillTags: {
      required: helpers.withMessage('请选择至少一个技能标签', validateSkillTags),
    },
    projectName: {
      required: helpers.withMessage('项目名称不能为空', validateProjectName),
    },
    projectStage: {
      required: helpers.withMessage('项目阶段不能为空', validateProjectStage),
    },
    fundingStage: {
      required: helpers.withMessage('请选择当前资金阶段', validateFundingStage),
    },
    needTags: {
      required: helpers.withMessage('请选择至少一个需求', validateNeedsTags),
    },
    investmentTags: {
      required: helpers.withMessage('请选择投资偏好', validateInvestmentTags),
    },
    teamSize: {
      required: helpers.withMessage('请选择团队规模', validateTeamSize),
    },

    workType: {
      required: helpers.withMessage('请选择工作性质', validateWorkType),
    },
  }));

  const validateProjectName = (value: string) => {
    const role = formData.role;
    if (role == UserRoleEnum.FOUNDER && (value == null || value.trim() == '')) {
      return false;
    }
    return true;
  };

  const validateProjectStage = (value: string) => {
    const role = formData.role;
    if (role == UserRoleEnum.FOUNDER && (value == null || value.trim() == '')) {
      return false;
    }
    return true;
  };

  const validateFundingStage = (value: string) => {
    const role = formData.role;
    if (role == UserRoleEnum.FOUNDER && (value == null || value.trim() == '')) {
      return false;
    } else {
      return true;
    }
  };

  const validateNeedsTags = (value: string | null) => {
    const role = formData.role;
    if (role == UserRoleEnum.FOUNDER && (value == null || value.trim() == '')) {
      return false;
    } else {
      return true;
    }
  };

  const validateTeamSize = (value: null | string) => {
    if ((value == null || value.trim() == '') && formData.role == UserRoleEnum.FOUNDER) {
      return false;
    }
    return true;
  };

  const validateWorkType = (value: null | string) => {
    if ((value == null || value.trim() == '') && (formData.role == UserRoleEnum.EXPERT || formData.role == UserRoleEnum.FA)) {
      return false;
    }
    return true;
  };


  // 自定义验证函数：检查两个字段是否相等
  const validateSkillTags = (value: string) => {
    // const role = formData.role;
    if (
      // (role == UserRoleEnum.EXPERT || role == UserRoleEnum.FA) &&
      value == null ||
      value.trim() == ''
    ) {
      return false;
    } else {
      return true;
    }
  };

  // 自定义验证函数：检查两个字段是否相等
  const validateTitle = (value: string) => {
    const role = formData.role;
    if (
       (role != UserRoleEnum.EXPERT && role != UserRoleEnum.FA) &&
      value == null ||
      value.trim() == ''
    ) {
      return false;
    } else {
      return true;
    }
  };

  const validateInvestmentTags = (value: string) => {
    if (formData.role == UserRoleEnum.INVESTOR && (value == null || value.trim() == '')) {
      return false;
    } else {
      return true;
    }
  };

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
    getErrors,
    validateProjectName,
    validateProjectStage,
    validateFundingStage,
    validateNeedsTags,
    validateTeamSize,
    validateSkillTags,
    validateInvestmentTags
  };
}


// 自定义验证钩子
export function useValidateForgetPassword(initialFormData: ForgetPasswordBO) {
  // 创建响应式表单状态
  // 创建响应式表单状态
  const formData = reactive<ForgetPasswordBO>(initialFormData);

  const rules = computed(() => ({
    phoneOrEmail: {
      required: helpers.withMessage('手机号或邮箱不能为空', required),
      validatePhoneOrEmail: helpers.withMessage('手机号或邮件格式不正确', validatePhoneOrEmail),
    },
    verificationCode: {
      required: helpers.withMessage('验证码不能为空', requiredVerificationCode),
    },
    password: {
      required: helpers.withMessage('密码不能为空', requiredPassword),
    },
    confirmPassword: {
      required: helpers.withMessage('密码不能为空', requiredConfirmPassword),
    },
  }));

  //验证手机号或邮件号
  const validatePhoneOrEmail = (value: string) => {
    if (!formData.isVerified) {
      if (value.includes('@')) {
        return validEmail(value);
      } else {
        return validMobilePhone(value);
      }
    }else{
      return true;
    }
  };

  const requiredVerificationCode = (value: string) => {
    if (!formData.isVerified) {
      if (value == null || value.trim() == '') {
        return false;
      }
    }
    return true;
  };

  const requiredPassword = (value: string) => {
    if (formData.isVerified) {
      if (value == null || value.trim() == '') {
        return false;
      }
    }
    return true;
  };

  const requiredConfirmPassword = (value: string) => {
    if (formData.isVerified){
      if (value != formData.confirmPassword) {
        return false;
      }
    }
    return true;
  }


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
    getErrors,
  };
}
  // 自定义验证钩子
  export function useValidateResetPassword(initialFormData: ForgetPasswordBO) {
    // 创建响应式表单状态
    // 创建响应式表单状态
    const formData = reactive<ForgetPasswordBO>(initialFormData);

    const rules = computed(() => ({
      phoneOrEmail: {
        required: helpers.withMessage('邮箱不能为空', required),
      },
       password: {
        validatePassword: helpers.withMessage(
          '密码必须包含数字、字母和特殊字符中的至少两种',
          validatePassword
        ),
      },
      confirmPassword: {
        required: helpers.withMessage('请确认密码', required),
        sameAsPassword: helpers.withMessage('两次输入的密码不一致', confirmPassword),
      },
    }));


  // 自定义验证函数：验证密码强度
  const validatePassword = (value: string) => {
    // 至少包含数字、字母、特殊字符中的两种
    const hasNumber = /\d/.test(value);
    const hasLetter = /[a-zA-Z]/.test(value);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);

    return (hasNumber && hasLetter) || (hasNumber && hasSpecial) || (hasLetter && hasSpecial);
  };

  // 自定义验证函数：检查两个字段是否相等
  // @ts-ignore
  const confirmPassword = (value: string) => {
    return value === formData.password;
  };

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
    getErrors,
  };
}

