<template>
  <div>
    <div class="progress-bar">
      <div class="progress-fill" id="progressFill" style="width: 25%"></div>
    </div>
    <form novalidate @submit.prevent="handleSubmit" class="register-form">
      <div class="form-header">
        <div class="form-label">STEP 01</div>
        <div class="form-title">创建你的账户</div>
      </div>
      <div class="field-group">
        <label class="field-label" for="phoneOrEmail">手机号/邮箱 <span class="req">*</span></label>
        <input
          id="phoneOrEmail"
          name="phoneOrEmail"
          v-model="v$.phoneOrEmail.$model"
          class="field-input"
          type="text"
          placeholder="请输入手机号或邮箱地址"
          required
        />
        <div v-if="v$.phoneOrEmail.$error" class="field-error-hint" id="phoneOrEmailErrorArea">
          <span v-for="(err, index) in v$.phoneOrEmail.$errors" :key="index">{{
            err.$message
          }}</span>
        </div>
      </div>
      <div class="field-group">
        <label class="field-label">验证码 <span class="req">*</span></label>
        <div class="flex flex-row gap-2">
          <input
            class="field-input"
            type="text"
            id="verificationCode"
            v-model="v$.verificationCode.$model"
            placeholder="6位验证码"
            maxlength="6"
          />
          <BtnSendVerificationCode @send-verification-code="sendVerificationCode" />
        </div>
        <div class="field-hint">验证码60秒内有效，如未收到请检查垃圾邮件</div>
        <div class="field-error-hint" v-if="v$.verificationCode.$error">
          <span v-for="(err, index) in v$.verificationCode.$errors" :key="index">{{
            err.$message
          }}</span>
        </div>
      </div>
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
          <span v-for="(err, index) in v$.password.$errors" :key="index">{{ err.$message }}</span>
        </div>
      </div>
      <div class="field-group">
        <label class="field-label" for="confirmPassword">确认密码 <span class="req">*</span></label>
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
      <!--
      <div class="divider"><span class="divider-text">或者</span></div>
      <div class="social-btns">
        <label class="social-btn">
          <div class="social-icon wechat">微</div>
          微信登录
        </label>
        <div class="social-btn">
          <div class="social-icon google">
            <svg width="14" height="14" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              ></path>
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              ></path>
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              ></path>
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              ></path>
            </svg>
          </div>
          Google 登录
        </div>
      </div>
      -->

      <div class="field-group">
        <label class="flex p-0 m-0">
          <input
            type="checkbox"
            class="custom-checkbox"
            id="isAgreement"
            v-model="v$.isAgreement.$model"
          />
          <span class="checkbox-label agreement-text"
            >我已阅读并同意 <a href="#">《用户服务协议》</a> 和 <a href="#">《隐私政策》</a></span
          >
        </label>
        <div v-if="v$.isAgreement.$error" class="field-error-hint">
          <span v-for="(err, index) in v$.isAgreement.$errors" :key="index">{{
            err.$message
          }}</span>
        </div>
      </div>

      <div>
        <button class="btn-primary" type="submit">下一步 →</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import '@/styles/module-login-register.scss';
import { useValidateUserRegister } from '@/hooks/useValidateUserRegister.ts';
import BtnSendVerificationCode from '@/components/BtnSendVerificationCode.vue';
import MessageBox from '@/utils/MessageBox.ts';
import { doRegister, sendAuthCodeByEmail } from '@/api/user/userRegisterApiI.ts';
import router from '@/router';
import type { UserBaseInfoBO } from '@/types/userBO.ts';

const initialFormData = {
  phoneOrEmail: '',
  password: '',
  confirmPassword: '',
  verificationCode: '',
  isAgreement: false,
} as UserBaseInfoBO;
const { formData, v$, doValidateForm, doValidateField } = useValidateUserRegister(initialFormData);

const sendVerificationCode = (callback: (arg0: boolean) => void) => {
  const ret = doValidateField('phoneOrEmail');
  if (!ret) {
    setTimeout(() => {
      callback(false);
    });
  } else {
    sendAuthCodeByEmail(formData.phoneOrEmail)
      .then((res: any) => {
        // console.log('json.code ===' + res.code);

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

const handleSubmit = () => {
  const isValid: boolean = doValidateForm();

  if (isValid) {
    doRegister(formData).then((res: any) => {
      if (res.code === 0) {
        // MessageBox.Success("注册成功，请登录平台完善资料")
        sessionStorage.setItem('register_userId', res.data.userId);
        router.push({
          name: 'register_role',
        });
      } else {
        MessageBox.Error(res.message);
      }
    });
  }
};
</script>

<style scoped lang="scss">
.register-form {
  margin: 0;
  padding: 0;
  width: 350px;
}

//协议确认
.custom-checkbox {
  display: none;
}

/* 自定义复选框样式 */
.checkbox-label {
  position: relative;
  padding-left: 25px;
  cursor: pointer;
  user-select: none;
}

/* 创建自定义复选框外观 */
.checkbox-label::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  border: 2px solid #ccc;
  border-radius: 3px;
  background-color: white;
  transition: background-color 0.2s ease;
}

/* 选中时的背景颜色 */
.custom-checkbox:checked + .checkbox-label::before {
  background-color: var(--gold);
  border-color: var(--gold);
}

/* 选中时添加对勾 */
.custom-checkbox:checked + .checkbox-label::after {
  content: '✓';
  position: absolute;
  left: 5px;
  top: 50%;
  transform: translateY(-50%);
  color: white;
  font-size: 14px;
  font-weight: bold;
}
</style>
