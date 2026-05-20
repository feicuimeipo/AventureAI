<template>
  <div class="progress-bar">
    <div class="progress-fill" id="progressFill" style="width: 75%"></div>
  </div>
  <form novalidate @submit.prevent="handleSubmit" class="m-0 p-0">
    <div class="section-panel" id="step3">
      <div class="form-header">
        <div class="form-label">STEP 03</div>
        <div class="form-title">完善你的档案</div>
        <div class="form-desc">信息越完整，AI匹配精准度越高。标 * 为必填项</div>
      </div>

      <!-- Common Fields -->
      <div class="field-3row">
        <div class="field-group">
          <div class="field-label">姓名 <span class="req">*</span></div>
          <input
            class="field-input"
            type="text"
            id="displayName"
            v-model="v$.displayName.$model"
            placeholder="你的真实姓名"
          />
          <div class="field-error-hint">
            <span v-for="(err, index) in v$.displayName.$errors" :key="index">{{
              err.$message
            }}</span>
          </div>
        </div>

        <div class="field-group">
          <div class="field-label">所在城市 <span class="req">*</span></div>

          <select class="field-input" id="city" v-model="v$.city.$model">
            <option value="" disabled selected>--地理要求--</option>
            <option
              v-for="(item, index) in cities"
              :key="index"
              :value="item.tag"
              :selected="item.tag === formData.city"
            >
              {{ item.name }}
            </option>
          </select>

          <div class="field-error-hint">
            <span v-for="(err, index) in v$.city.$errors" :key="index">{{ err.$message }}</span>
          </div>
        </div>

        <div class="field-group">
          <div class="field-label">岗位 <span class="req">*</span></div>
          <select id="title" class="field-input" v-model="v$.title.$model">
            <option disabled value="">请选择岗位</option>
            <option v-for="(item, index) in userTitles" :key="index" :value="item.tag">
              {{ item.name }}
            </option>
          </select>
          <div class="field-error-hint">
            <span v-for="(err, index) in v$.title.$errors" :key="index">{{ err.$message }}</span>
          </div>
        </div>
      </div>

      <div class="field-group">
        <div class="field-label">个人简介 <span class="req">*</span></div>
        <textarea
          class="field-input"
          rows="3"
          placeholder="用一两句话介绍自己，这段文字将用于AI语义匹配"
          style="resize: vertical; line-height: 1.6"
          id="bio"
          v-model="v$.bio.$model"
        ></textarea>
        <div class="field-hint">建议包含：背景经历、核心能力、当前关注领域</div>
        <div class="field-error-hint">
          <span v-for="(err, index) in v$.bio.$errors" :key="index">{{ err.$message }}</span>
        </div>
      </div>

      <!-- Role-specific: Founder -->
      <div class="profile-fields">
        <div class="field-group" v-if="formData.role == UserRoleEnum.INVESTOR">
          <div class="field-label">投资偏好</div>
          <select class="field-input" id="investmentTags" v-model="v$.investmentTags.$model">
            <option value="" disabled selected>请选择当前阶段</option>
            <option v-for="(item, index) in investmentTagsData" :key="index" :value="item.tag">
              {{ item.name }}
            </option>
          </select>
          <div class="field-error-hint">
            <span v-for="(err, index) in v$.investmentTags.$errors" :key="index">{{
              err.$message
            }}</span>
          </div>
        </div>
      </div>
      <div class="profile-fields">
        <!--        <div class="profile-tag" style="background: var(&#45;&#45;gold-dim); color: var(&#45;&#45;gold)">-->
        <!--          🚀 创业者专属信息-->
        <!--        </div>-->
        <div class="field-row" v-if="formData.role == UserRoleEnum.FOUNDER">
          <div class="field-group">
            <div class="field-label">项目名称 <span class="req">*</span></div>
            <input
              class="field-input"
              type="text"
              id="projectName"
              v-model="v$.projectName.$model"
              placeholder="请输入你的创业项目"
            />
            <div class="field-error-hint">
              <span v-for="(err, index) in v$.projectName.$errors" :key="index">{{
                err.$message
              }}</span>
            </div>
          </div>
          <div class="field-group">
            <div class="field-label">融资阶段</div>
            <select class="field-input" id="fundingStage" v-model="v$.fundingStage.$model">
              <option value="" disabled selected>请选择当前阶段</option>
              <option v-for="(item, index) in fundingStageData" :key="index" :value="item.tag">
                {{ item.name }}
              </option>
            </select>
            <div class="field-error-hint">
              <span v-for="(err, index) in v$.fundingStage.$errors" :key="index">{{
                err.$message
              }}</span>
            </div>
          </div>
        </div>
        <div class="field-group">
          <div class="field-label">
            所属赛道 <span class="req">*</span> <span class="opt">（最多选3个）</span>
          </div>
          <div class="tag-grid">
            <div
              class="tag"
              v-for="(item, index) in industryData"
              @click="toggleTag"
              :data-tag="item.tag"
              data-type="industry"
              :key="index"
            >
              {{ item.icon }} {{ item.name }}
            </div>
            <!--<div class="tag-more">+ 更多赛道</div>-->
          </div>
          <input type="hidden" id="industryTags" v-model="v$.industryTags.$model" />
          <div class="field-error-hint">
            <span v-for="(err, index) in v$.industryTags.$errors" :key="index">{{
              err.$message
            }}</span>
          </div>
        </div>
        <div class="field-group">
          <div class="field-label">当前需求 <span class="opt">（可多选）</span></div>
          <div class="tag-grid">
            <div
              class="tag"
              v-for="(item, index) in needTagsData"
              :key="index"
              @click="toggleTag"
              :data-tag="item.tag"
              data-type="need"
            >
              {{ item.icon }} {{ item.name }}
            </div>
          </div>
        </div>
        <input type="hidden" id="needTags" v-model="v$.needTags.$model" />
        <div class="field-error-hint">
          <span v-for="(err, index) in v$.needTags.$errors" :key="index">{{ err.$message }}</span>
        </div>
      </div>

      <div class="field-group" style="margin-top: 24px">
        <div class="field-label">
          技能标签 <span class="opt">（描述你的核心能力，可多选）</span>
        </div>
        <div class="tag-grid">
          <div
            class="tag"
            v-for="(item, index) in skillTagsData"
            @click="toggleTag"
            :data-tag="item.tag"
            data-type="skill"
            :key="index"
          >
            {{ item.icon }} {{ item.name }}
          </div>
        </div>
        <input type="hidden" id="skillTags" v-model="v$.skillTags.$model" />
        <div class="field-error-hint">
          <span v-for="(err, index) in v$.skillTags.$errors" :key="index">{{ err.$message }}</span>
        </div>
      </div>

      <div class="form-actions">
        <input type="hidden" id="userId" v-model="v$.userId.$model" />
        <input type="hidden" id="role" v-model="v$.role.$model" />
        <button class="btn-primary" type="submit">完成注册→</button>
        <button class="btn-secondary" @click="previousStep">← 返回</button>
        <span class="btn-skip" @click="skipFinishRegister">跳过，稍后完善</span>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { type UserProfileBO, UserRoleEnum } from '@/types/userBO.ts';
import { useValidateUserProfile } from '@/hooks/useValidateUserRegister.ts';
import { doSaveUserProfile } from '@/api/user/userRegisterApiI.ts';
import MessageBox from '@/utils/MessageBox.ts';
import {
  FundingStageItems,
  IndustryItems,
  InvestmentTagsItems,
  NeedTagsItems,
  SkillTagsItems,
  UserTitles,
} from '@/utils/userData.ts';
import { reactive, ref } from 'vue';
import { CitiesItems } from '@/utils/needData.ts';

const router = useRouter();

const getUserId = (): string => {
  const userId = sessionStorage.getItem('register_userId');
  return userId == null ? '' : userId;
};
const getRoleId = (): string => {
  const role = sessionStorage.getItem('register_role');
  return role == null ? '' : role;
};

const userTitles = ref(UserTitles);
const cities = reactive(CitiesItems);
const industryData = reactive(IndustryItems);
const fundingStageData = reactive(FundingStageItems);
const needTagsData = reactive(NeedTagsItems);
const investmentTagsData = reactive(InvestmentTagsItems);
const skillTagsData = reactive(SkillTagsItems);

const initFormData: UserProfileBO = {
  userId: getUserId(),
  role: getRoleId(),
  title: '',
  displayName: '',
  avatarUrl: '',
  bio: '',
  city: '',
  skillTags: '',
  industryTags: '',
  projectName: '',
  projectStage: '-',
  fundingStage: '',
  needTags: '',
  investmentTags: '-',
  teamSize: '-',
  workType: '全部',
};

const { formData, v$, doValidateForm } = useValidateUserProfile(initFormData);

const setVariousTags = () => {
  formData.skillTags = '';
  formData.needTags = '';
  formData.industryTags = '';
  document.querySelectorAll('.tag').forEach((e: any) => {
    if (e.classList.contains('selected')) {
      const type = e.dataset.type;
      const tag = e.dataset.tag;
      if (type == 'skill') {
        formData.skillTags += ',' + tag;
      } else if (type == 'need') {
        formData.needTags += ',' + tag;
      } else if (type == 'industry') {
        formData.industryTags += ',' + tag;
      }
    }
  });
  if (formData.skillTags != '') formData.skillTags = formData.skillTags.substring(1);
  if (formData.needTags != '') formData.needTags = formData.needTags.substring(1);
  if (formData.industryTags != '') formData.industryTags = formData.industryTags.substring(1);
};

const handleSubmit = async () => {
  setVariousTags();
  const isValid: boolean = await doValidateForm();
  // alert(isValid);
  if (isValid) {
    doSaveUserProfile(formData)
      .then((res: any) => {
        if (res.code === 0) {
          MessageBox.Success('客户棣案配置成功!');
          router.push({
            name: 'register_finish',
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

const previousStep = () => {
  //业务处理
  router.push({
    name: 'register_role',
  });
};

const skipFinishRegister = () => {
  router.push({
    name: 'register_finish',
  });
};

function toggleTag(e: any) {
  const event = e.currentTarget;

  let skillCount = 0;
  let needCount = 0;
  let industryCount = 0;

  document.querySelectorAll('.tag.selected').forEach((target: any) => {
    const type = target.dataset.type;
    if (type == 'skill') {
      skillCount++;
    } else if (type == 'need') {
      needCount++;
    } else if (type == 'industry') {
      industryCount++;
    }
  });
  if (industryCount >= 3 && event.dataset.type == 'industry') {
    return;
  }
  if (event.classList.contains('selected')) {
    event.classList.remove('selected');
  } else {
    event.classList.add('selected');
  }
}
</script>

<style scoped></style>
