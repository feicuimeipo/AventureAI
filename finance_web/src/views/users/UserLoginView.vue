<template>
  <div :class="moduleStyle">
    <div class="shell">
      <!-- TOP BAR -->
      <div class="top-bar">
        <AppHeader subtitle="系统登录" :cssmodule="moduleStyle" />
      </div>

      <!-- CONTENT -->
      <div class="content-area" style="margin-top: 30px">
        <form novalidate @submit.prevent="handleSubmit" class="m-10 p-10">
          <div class="loginPanel" style="margin: 0 auto; width: 400px">
            <div class="form-login-type-toggle" v-if="login_type == 1">
              <div
                class="form-login-type select-toggle"
                style="white-space: nowrap"
                @click="loginToggle(1)"
              >
                密码登录
              </div>
              <div id="sms-login" class="form-login-type" style="white-space: nowrap">短信登录</div>
            </div>
            <div class="form-login-type-toggle" v-else>
              <div class="form-login-type" style="white-space: nowrap" @click="loginToggle(1)">
                密码登录
              </div>
              <div
                id="sms-login"
                class="form-login-type select-toggle"
                style="white-space: nowrap"
                @click="loginToggle(2)"
              >
                短信登录
              </div>
            </div>
            <br />
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
            <div class="field-group" v-if="login_type == 2">
              <div class="flex flex-row gap-2">
                <input
                  class="field-input"
                  type="text"
                  id="verificationCode"
                  v-model="v$.verificationCode.$model"
                  placeholder="请输入验证码"
                  maxlength="6"
                />
                <BtnSendVerificationCode />
              </div>
            </div>
            <div class="field-group" v-if="login_type == 1">
              <input
                class="field-input"
                type="password"
                placeholder="请输入密码"
                id="password"
                v-model="v$.password.$model"
                autocomplete="false"
              />
              <div v-if="v$.password.$error" class="field-error-hint">
                <span v-for="(err, index) in v$.password.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
            <div>
              <div class="flex gap-2">
                <button class="btn-primary" type="submit">登 录 →</button>
                <div style="margin-top: 30px">
                  <RegisterLogin :login-enable="false"></RegisterLogin>&nbsp;&nbsp;
                  <span class="span-btn" @click="forgetPassword">忘记密码</span>&nbsp;&nbsp;
                  <span class="span-btn" @click="register">注册新用户</span>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import '@/styles/module-login-register.scss';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';
import RegisterLogin from '@/components/BtnRegisterLogin.vue';
import BtnSendVerificationCode from '@/components/BtnSendVerificationCode.vue';
import type { PasswordLoginBO } from '@/types/userBO.ts';
import { helpers, required } from '@vuelidate/validators';
import { useValidate } from '@/hooks/useValidate.ts';
import { validEmail, validMobilePhone } from '@/utils/validate_utils.ts';
import { useCurrentUserStore } from '@/stores/currentUser.ts';
import AppHeader from '@/components/AppHeader.vue';
import { getHomeModuleStyle } from '@/utils/menuUtils.ts';


const moduleStyle = ref<string>(getHomeModuleStyle());

const router = useRouter();

const login_type = ref<number>(1);
const loginToggle = (val: number) => {
  login_type.value = val;
};

const initFormData: PasswordLoginBO = {
  phoneOrEmail: '',
  password: '',
};

const rules = computed(() => ({
  phoneOrEmail: {
    required: helpers.withMessage('邮箱不能为空', required),
    validatePhoneOrEmail: helpers.withMessage('手机号或邮件格式不正确', validatePhoneOrEmail),
  },
  password: {
    required: helpers.withMessage('密码不能为空', required),
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

const { formData, v$, doValidateForm } = useValidate(initFormData, rules);
const currentUser = useCurrentUserStore();
const handleSubmit = async () => {
  const isValid: boolean = doValidateForm();
  if (isValid) {
    await currentUser
      .login(formData)
      .then(() => {
        router.push('/platform');
      })
      .catch(error => {
        console.log(error);
      });
  }
};

const forgetPassword = () => {
  router.push({
    name: 'forget_password',
  });
};

const register = () => {
  router.push('/register');
};
</script>

<style scoped lang="scss">
.loginPanel {
  width: 28vw;
}
.outerPanel {
  text-align: center;
  align-items: center;
}

.form-login-type-toggle {
  display: flex;
  -ms-flex-pack: center;
  justify-content: center;
  -ms-flex-align: center;
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

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
