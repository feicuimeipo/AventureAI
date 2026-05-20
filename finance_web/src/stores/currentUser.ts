import {defineStore} from 'pinia';
import type {CurrentUserBO, PasswordLoginBO} from '@/types/userBO.ts';
import {doLogout, doPasswordLogin} from '@/api/user/userLoginApiI.ts';
import MessageBox from '@/utils/MessageBox.ts';
import {cleanAuthToken, setAuthToken} from '@/stores/token.ts';
import {doLoginState, getCurrentUserInfo} from '@/api/user/currentUserApi.ts';
import {useRouter} from 'vue-router';
import { reactive, ref } from 'vue';
import {maskPhoneNumber} from '@/utils/validate_utils.ts';

export const useCurrentUserStore = defineStore('currentUser', () => {
    const userInfo = reactive<CurrentUserBO>({
      userId: null,
      email: null,
      phone: null,
      role: '',
      title: '',
      displayName: '',
      industryTags: '',
      skillTags: '',
      projectName: '',
      projectStage: '',
      fundingStage: '',
      needTags: '',
      teamSize: '',
      investmentTags: '',
      completeness: '',
      firstName: '',
    });

  const isLogin =ref<boolean>(false);
  const loginState = async ():Promise<any> => {
      await doLoginState()
        .then((res: any) => {
          if (res.code === 0) {
            isLogin.value = true;
          } else {
            isLogin.value = false;
          }
          console.log('登录状态:' + isLogin.value);
          return Promise.resolve(isLogin.value);
        })
        .catch((err: any) => {
          console.log(err);
          isLogin.value = false;
          Promise.reject(err);
        });
  };

  const getUserInfo = () => {
      return userInfo;
  }

  const fetchCurrentUserInfo = async () => {
      await getCurrentUserInfo()
        .then((res: any) => {
          if (res.code === 0) {
            Object.assign(userInfo, res.data);

            if (userInfo.displayName == '') {
              if (userInfo.email != '') {
                userInfo.displayName = userInfo.email || '';
              }
              if (userInfo.phone != '') {
                userInfo.displayName = userInfo.phone == null ? '' : maskPhoneNumber(userInfo.phone);
              }
            }
            if (userInfo.displayName.length == 0) {
              userInfo.displayName = 'Guest';
            }
            userInfo.firstName = userInfo.displayName.substring(0, 1);
          }
        })
        .catch(err => {
          console.log(err);
          return Promise.reject(err);
        });
  };

  const login = async (formData: PasswordLoginBO) => {
    // const router = useRouter();
    await doPasswordLogin(formData)
      .then((res: any) => {
        if (res.code === 0) {
          setAuthToken(res.data.accessToken);
          console.info('登录成功');
        } else {
          MessageBox.Error('登录失败');
          console.log(res.message);
          return Promise.reject(new Error(res.message || 'Error'));
        }
      })
      .catch(err => {
        console.log(err);
        return Promise.reject(err);
      });
  };

  const logout  =  async()=>  {
    doLogout()
      .then(() => {
        cleanAuthToken();
        console.info('登出成功!');
        const router = useRouter();
        router.push('/');
      })
      .catch((err: any) => {
        console.log(err.message);
        return Promise.reject(err);
      });
  }

    return {
      getUserInfo,
      fetchCurrentUserInfo,
      login,
      logout,
      loginState,
      isLogin
    }
});
