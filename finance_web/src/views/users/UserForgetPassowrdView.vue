<template>
  <div :class="moduleStyle">
    <div>
      <!-- TOP BAR -->
      <div class="top-bar">
        <AppHeader subtitle="系统登录" :cssmodule="moduleStyle" />
      </div>

      <!-- CONTENT -->
      <div class="flex justify-content-center" style="margin-top: 30px; width: 100vw;">
        <div style="width: 350px">
          <form
            novalidate
            @submit.prevent="confirmPhoneOrMailByCode"
            class="m-0 p-0"
            v-if="!formData.isVerified"
          >
            <div class="field-group">
              <input
                class="field-input"
                type="text"
                placeholder="请输入手机号或邮箱地址"
                id="phoneOrEmail"
                v-model="v$.phoneOrEmail.$model"
              />
              <div v-if="v$.phoneOrEmail.$error" class="field-error-hint">
                <span v-for="(err, index) in v$.phoneOrEmail.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
            <div class="field-group">
              <div class="flex flex-row gap-2">
                <input
                  class="field-input"
                  type="text"
                  id="verificationCode"
                  v-model="v$.verificationCode.$model"
                  placeholder="请输入验证码"
                  maxlength="6"
                />
                <BtnSendVerificationCode @send-verification-code="sendVerificationCode" />
              </div>
              <div v-if="v$.verificationCode.$error" class="field-error-hint">
                <span v-for="(err, index) in v$.verificationCode.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
            <div class="flex gap-2">
              <button class="btn-primary" type="submit">确 定</button>
              <div style="margin-top: 30px">
                <RegisterLogin :login-enable="false"></RegisterLogin>&nbsp;&nbsp;
                <span class="span-btn" @click="login">去登录</span>
              </div>
            </div>
          </form>

          <form
            novalidate
            @submit.prevent="handleSubmit"
            class="m-0 p-0"
            v-if="formData.isVerified"
          >
            <div class="field-group">
              <label class="field-label" for="password">设置密码 <span class="req">*</span></label>
              <input
                id="password"
                v-model="v$.password.$model"
                class="field-input"
                type="password"
                autocomplete="off"
                placeholder="至少6位,包含字母,数字和下划线中的任两类字符"
              />
              <div class="field-hint">
                <span>密码至少8位数,由数字，字母与下划线组成</span>
              </div>
              <div v-if="v$.password.$error" class="field-error-hint">
                <span v-for="(err, index) in v$.password.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
            <div class="field-group">
              <label class="field-label" for="confirmPassword"
                >确认密码 <span class="req">*</span></label
              >
              <input
                id="confirmPassword"
                v-model="v$.confirmPassword.$model"
                class="field-input"
                type="password"
                autocomplete="off"
                placeholder="请再次输入密码"
              />
              <div v-if="v$.confirmPassword.$error" class="field-error-hint">
                <span v-for="(err, index) in v$.confirmPassword.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
            <div class="flex gap-2">
              <input type="hidden" id="userId" v-model="formData.userId" />
              <button class="btn-primary" type="submit">确定修改</button>
              <div style="margin-top: 30px">
                <RegisterLogin :login-enable="false"></RegisterLogin> &nbsp;&nbsp;
                <span class="span-btn" @click="login">去登录</span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import '@/styles/module-login-register.scss';
import { useRouter } from 'vue-router';
import MessageBox from '@/utils/MessageBox.ts';
import {
  doConfirmPhoneOrMail,
  doResetPassword,
  sendForgetPasswordAuthCodeByEmail,
} from '@/api/user/userLoginApiI.ts';
import type { ForgetPasswordBO } from '@/types/userBO.ts';
import BtnSendVerificationCode from '@/components/BtnSendVerificationCode.vue';
import { useValidateForgetPassword } from '@/hooks/useValidateUserRegister.ts';

import RegisterLogin from '@/components/BtnRegisterLogin.vue';
import AppHeader from '@/components/AppHeader.vue';
import { ref } from 'vue';
import { getHomeModuleStyle } from '@/utils/menuUtils.ts';

const router = useRouter();
const moduleStyle = ref<string>(getHomeModuleStyle());

const initFormData: ForgetPasswordBO = {
  phoneOrEmail: '',
  certificationCode: '',
  password: '',
  confirmPassword: '',
  isVerified: false,
  userId: '',
};

const { formData, v$, doValidateForm, doValidateField } = useValidateForgetPassword(initFormData);

const sendVerificationCode = (callback: (arg0: boolean) => void) => {
  const ret = doValidateField('phoneOrEmail');
  if (!ret) {
    setTimeout(() => {
      callback(false);
    });
  } else {
    sendForgetPasswordAuthCodeByEmail(formData.phoneOrEmail)
      .then((res: any) => {
        console.log('json.code ===' + res.code);
        if (res.code === 0) {
          MessageBox.Success('验证码发送成功!');
          setTimeout(() => {
            callback(true);
          });
        } else {
          MessageBox.Error(res.message);
          setTimeout(() => {
            callback(false);
          });
        }
      })
      .catch((err: { message: any }) => {
        console.log(err.message);
        MessageBox.Error(err.message);
        setTimeout(() => {
          callback(false);
        });
      });
  }
};

const confirmPhoneOrMailByCode = async () => {
  const isValid = doValidateForm();
  if (isValid) {
    doConfirmPhoneOrMail(formData)
      .then((res: any) => {
        if (res.code == 0) {
          // MessageBox.Error(res.message);
          formData.userId = res.data.userId;
          formData.isVerified = true;
        } else {
          MessageBox.Error(res.message);
        }
      })
      .catch((err: any) => {
        console.log(err.message);
        MessageBox.Error(err.message);
      });
  }
};

const handleSubmit = async () => {
  const isValid = doValidateForm();
  if (isValid) {
    const params = {
      userId: formData.userId,
      password: formData.password,
      confirmPassword: formData.confirmPassword,
    };
    doResetPassword(params)
      .then((res: any) => {
        // console.log('json===' + JSON.stringify(res));
        if (res.code === 0) {
          MessageBox.Success('密码修改成功，请重新登录！');
          router.push('/login');
        } else {
          MessageBox.Error(res.message);
        }
      })
      .catch((err: any) => {
        console.log(err.message);
        MessageBox.Error(err.message);
      });
  }
};

const login = () => {
  router.push('/login');
};
</script>

<style scoped lang="scss">
.loginPanel {
  padding: 48px 64px;
  width: 28vw;
}

.form-login-type-toggle {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
}

.form-login-type-toggle .form-login-type {
  display: inline-block;
  font-size: 18px;
  font-weight: 600;
  line-height: 16px;
  margin-right: 20px;
  cursor: pointer;
  color: var(--muted2);
}

.form-login-type-toggle .select-toggle {
  color: #fa2c19;
  font-weight: 600;
}

.social-btn-small {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--white);
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 6px;
}

.span-btn {
  font-size: var(--font-size-base);
  color: var(--muted);
  cursor: pointer;
}
</style>
