export function userQueryParam() {
  // 辅助函数：安全获取字符串，避免 undefined
  const getStr = (val: any): string => val ?? '';

  // 辅助函数：安全获取数字
  const getNum = (val: any): number | undefined => {
    if (val === undefined || val === null || val === '') return undefined;
    const num = Number(val);
    return isNaN(num) ? undefined : num;
  };

  // 辅助函数：处理可能的数组或逗号分隔字符串
   const getArray = (val: any): string[] | undefined => {
    if (!val) return undefined;
    if (Array.isArray(val)) return val;
    // 如果是逗号分隔的字符串，分割成数组
    if (typeof val === 'string') return val.split(',').filter(item => item.trim() !== '');
    return [String(val)];
  };

   return{
     getArray,
     getStr,
     getNum
   }
}