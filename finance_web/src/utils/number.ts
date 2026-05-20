/**
 * 宽松判断：尝试将值转换为数字，并检查是否有效
 * @param {*} value - 待检查的值
 * @returns {boolean}
 */
export function isValidNumber(value:any) {
  // 排除 null 和空字符串，因为 Number(null) 为 0, Number("") 为 0
  if (value === null || value === '') return false;

  const num = Number(value);
  return !isNaN(num) && isFinite(num);
}
