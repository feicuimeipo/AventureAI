<template>
  <div class="progress-bar">
    <div class="progress-fill" id="progressFill" style="width: 50%"></div>
  </div>
  <form novalidate @submit.prevent="handleSubmit" class="m-0 p-0">
    <div class="section-panel" id="step1">
      <div class="form-header">
        <div class="form-label">STEP 02</div>
        <div class="form-title">你是哪种角色？</div>
        <div class="form-desc">角色决定你的专属功能和匹配维度，后续可在设置中更改</div>
      </div>

      <div class="role-grid" id="roleGrid">
        <div v-for="(item, index) in roleData" :key="index">
          <div data-role="founder" @click="selectRole(item.tag.toLowerCase())" :class="item.class">
            <div class="role-check">✓</div>
            <span class="role-emoji">{{ item.icon }}</span>
            <div class="role-name">{{ item.name }}</div>
            <div class="role-en">{{ item.tag.toUpperCase() }}</div>
            <div class="role-desc">{{ item.intro }}</div>
          </div>
        </div>
      </div>
      <div>
        <input type="hidden" id="role" v-model="v$.role.$model" />
        <div class="field-error-hint">
          <span v-for="(err, index) in v$.role.$errors" :key="index">{{ err.$message }}</span>
        </div>
      </div>
      <div class="form-actions">
        <input type="hidden" id="userId" v-model="formData.userId" />
        <button class="btn-primary">确认角色 →</button>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { useValidate } from '@/hooks/useValidate.ts';
import { doSaveRole } from '@/api/user/userRegisterApiI.ts';
import type { RoleBO } from '@/types/userBO.ts';
import { helpers, required } from '@vuelidate/validators';
import { computed, reactive } from 'vue';
import MessageBox from '@/utils/MessageBox.ts';
import { RoleItems } from '@/utils/userData.ts';

const route = useRoute();
const router = useRouter();
const roleData = reactive(RoleItems);

console.log('userId: route.params.userId =' + route.params.userId);
const initialFormData: RoleBO = {
  userId: sessionStorage.getItem('register_userId') || '',
  role: 'founder',
};

const rules = computed(() => ({
  userId: {
    required: helpers.withMessage('用户编号不能为空', required),
  },
  role: {
    required: helpers.withMessage('请主选择一个角色', required),
  },
}));

const { formData, v$, doValidateForm } = useValidate(initialFormData, rules);

const handleSubmit = async () => {
  const isValid: boolean = await doValidateForm();
  if (isValid) {
    doSaveRole({
      userId: formData.userId,
      role: formData.role,
    })
      .then((res: any) => {
        if (res.code === 0) {
          sessionStorage.setItem('register_role', res.data.role);
          sessionStorage.setItem('register_userId', res.data.userId);
          router.push({
            name: 'register_profile',
          });
        } else {
          console.log(res.message);
          MessageBox.Error(res.message);
        }
      })
      .catch(err => {
        console.log(err.message);
        MessageBox.Error(err.message);
      });
  }
};

const selectRole = (val: string) => {
  formData.role = null;

  roleData.forEach((c: any) => {
    if (c.tag == val && c.class.indexOf('selected')<=-1) {
      c.class = 'role-card selected';
      formData.role = val;
    } else {
      c.class = 'role-card';
    }
  });
};
</script>

<style scoped>
.form-header {
}

.form-label {
  font-size: var(--font-size-base);
  color: var(--gold);
  letter-spacing: 0.15em;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
  line-height: 1.3;
}

.form-desc {
  font-size: var(--font-size-14);
  color: var(--muted);
  line-height: 1.7;
}

.form-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  padding-top: 8px;
}
</style>
