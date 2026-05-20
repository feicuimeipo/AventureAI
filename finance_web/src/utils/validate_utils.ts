import { helpers } from '@vuelidate/validators';

export const validEmail = (email: string) => {
  // # 定义邮箱的正则表达式
  const pattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;

  if (!email) return false;
  // # 使用 re.match 方法进行匹配
  return pattern.test(email);
};

/**
 * 手机号验证
 * @param phone
 */
export const validMobilePhone = (phone: string) => {
  const phoneRegex = /^1[3-9]\d{9}$/;

  if (phone.length <= 1) {
    return false;
  }

  // 去除可能的空格和特殊字符
  const cleanedPhone = phone.replace(/\s+/g, '').replace(/-/g, '');

  // 验证格式
  return phoneRegex.test(cleanedPhone);
};


export const validPassword = (value: string) => {
  if (!value) return false;
  const strictPasswordRegex = /^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[_])[0-9a-zA-Z_]{6,20}$/;
  return strictPasswordRegex.test(value);
};

export const validUrl = (value: string) => {
  if (!helpers.req(value)) return true; // 如果字段为空，跳过验证（可选）
  let processedValue = value;
  if (value.includes('www.')) {
    processedValue = value.replaceAll('www.', '');
  }

  const regex = /^(?:[a-zA-Z0-9](?:[-.][a-zA-Z0-9])?)+(?:\.[a-z]{2,6})+$/i;
  return regex.test(processedValue);
};

/**
 * 手机号脱敏处理
 * @param phone
 */
export const maskPhoneNumber = (phone: string) => {
  if (phone.length <= 3) {
    return phone;
  }
  if (phone.length < 11) {
    return phone.substring(0,2) + "***"
  }
  // 脱敏：保留前3位和后4位，中间用*替换
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
};

