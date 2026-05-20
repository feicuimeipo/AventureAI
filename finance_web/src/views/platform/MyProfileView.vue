<template>
  <div class="screen">
    <div class="reg-split" style="min-height: 100%">
      <div class="reg-left">
        <form novalidate @submit.prevent="handleSubmit" class="m-0 p-0">
          <div class="reg-title" style="color: #1a1612">
            欢迎加入，请完善您的数据，AI立即为你即刻匹配
          </div>
          <div class="field-row">
            <div>
              <div class="sub-title">① 您的名字</div>
              <div class="tag-row" style="margin-bottom: 16px">
                <input
                  type="text"
                  id="displayName"
                  v-model="v$.displayName.$model"
                  class="field-input"
                  required
                  placeholder="请输入姓名"
                />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.displayName.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
            <div>
              <div class="sub-title">① 所在城市</div>
              <div class="tag-row" style="margin-bottom: 16px">
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
                  <span v-for="(err, index) in v$.city.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="sub-title">① 选择身份</div>
          <div class="role-grid">
            <div
              @click="selectRole"
              data-type="role"
              v-for="(item, index) in roleData"
              :key="index"
              :class="item.class"
              :data-tag="item.tag"
            >
              <div class="rc-ico">{{ item.icon }}</div>
              <div class="rc-n">{{ item.name }}</div>
              <div class="rc-d">{{ item.intro }}</div>
              <div class="rc-cnt">{{ item.personalCount }}人</div>
            </div>
            <div>
              <input type="hidden" id="role" v-model="v$.role.$model" />
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.role.$errors" :key="index">{{ err.$message }}</span>
              </div>
            </div>
          </div>

          <div class="field-row">
            <div>
              <div class="sub-title" v-if="formData.role == 'founder'">① 项目名称</div>
              <div class="tag-row" style="margin-bottom: 16px" v-if="formData.role == 'founder'">
                <input
                  type="text"
                  id="projectName"
                  v-model="v$.projectName.$model"
                  class="field-input"
                  required
                  placeholder="请输入姓名"
                />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.projectName.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
            <div>
              <div class="sub-title" v-if="formData.role == 'founder'">① 当前团队人数</div>
              <div class="tag-row" style="margin-bottom: 16px" v-if="formData.role == 'founder'">
                <select class="field-input" id="teamSize" v-model="v$.teamSize.$model">
                  <option disabled value="">请选择团队规范</option>
                  <option value="1人(单独创业)">1人(单独创业)</option>
                  <option value="2-5人">2-5人</option>
                  <option value="6-20人">6-20人</option>
                  <option value="20人以上">20人以上</option>
                </select>
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.teamSize.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="field-row">
            <div>
              <div class="sub-title">② 项目方向（点选，最多3个）</div>
              <div class="tag-row" style="margin-bottom: 16px">
                <div
                  data-type="industry"
                  @click="toggleTag"
                  v-for="(item, index) in industryData"
                  :class="item.class"
                  :key="index"
                  :data-tag="item.tag"
                >
                  {{ item.icon }} {{ item.name }}
                </div>
              </div>
              <div>
                <input type="hidden" id="industryTags" v-model="v$.industryTags.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.industryTags.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
            <div>
              <div class="sub-title" v-if="formData.role == 'founder'">③ 当前阶段</div>
              <div class="stage-row" v-if="formData.role == 'founder'" style="padding-top: 5px">
                <div
                  data-type="projectStage"
                  @click="toggleTag"
                  v-for="(item, index) in projectStageData"
                  :class="item.class"
                  :data-tag="item.tag"
                  :key="index"
                >
                  {{ item.icon }} {{ item.name }}
                </div>
              </div>
              <div>
                <input type="hidden" id="projectStage" v-model="v$.projectStage.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.projectStage.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="field-row">
            <div>
              <div class="sub-title" v-if="formData.role == 'founder'">④ 资金阶段</div>
              <div class="stage-row" v-if="formData.role == 'founder'">
                <div
                  data-type="fundingStage"
                  @click="toggleTag"
                  v-for="(item, index) in fundingStageData"
                  :class="item.class"
                  :data-tag="item.tag"
                  :key="index"
                >
                  {{ item.icon }} {{ item.name }}
                </div>
              </div>
              <div>
                <input type="hidden" id="fundingStage" v-model="v$.fundingStage.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.fundingStage.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
            <div>
              <div class="sub-title" v-if="formData.role == 'founder'">④ 当前需求（可多选）</div>
              <div class="stage-row" v-if="formData.role == 'founder'">
                <div
                  data-type="need"
                  @click="toggleTag"
                  v-for="(item, index) in needTagsData"
                  :class="item.class"
                  :data-tag="item.tag"
                  :key="index"
                >
                  {{ item.icon }} {{ item.name }}
                </div>
              </div>
              <div>
                <input type="hidden" id="needTags" v-model="v$.needTags.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.needTags.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="sub-title" v-if="formData.role == 'investor'">④ 投资偏好（可多选）</div>
          <div class="stage-row" v-if="formData.role == 'investor'">
            <div
              data-type="investmentTags"
              @click="toggleTag"
              v-for="(item, index) in investmentTagsData"
              :class="item.class"
              :data-tag="item.tag"
              :key="index"
            >
              {{ item.icon }} {{ item.name }}
            </div>
          </div>
          <div>
            <input type="hidden" id="investmentTags" v-model="v$.investmentTags.$model" />
            <div class="field-error-hint">
              <span v-for="(err, index) in v$.investmentTags.$errors" :key="index">{{
                err.$message
              }}</span>
            </div>
          </div>

          <div class="field-row">
            <div v-if="formData.role != 'gov' && formData.role != 'corp'">
              <div class="sub-title">④ 职位</div>
              <div class="tag-row">
                <div
                  data-type="title"
                  @click="toggleTag"
                  v-for="(item, index) in userTitles"
                  :class="item.class"
                  :data-tag="item.tag"
                  :key="index"
                >
                  {{ item.icon }} {{ item.name }}
                </div>
              </div>
              <div>
                <input type="hidden" id="title" v-model="v$.title.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.title.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>

            <div v-if="formData.role == 'expert' || formData.role == 'fa'">
              <div class="sub-title">工作方式</div>
              <div class="tag-row">
                <div
                  data-type="workType"
                  @click="toggleTag"
                  v-for="(item, index) in workTypes"
                  :class="item.class"
                  :data-tag="item.tag"
                  :key="index"
                >
                  {{ item.icon }} {{ item.name }}
                </div>
              </div>
              <div>
                <input type="hidden" id="workType" v-model="v$.workType.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.workType.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>
          </div>

          <div>
            <div class="sub-title">④ 相关技能（可多选）</div>
            <div class="stage-row">
              <div
                data-type="skill"
                @click="toggleTag"
                v-for="(item, index) in skillTagsData"
                :class="item.class"
                :data-tag="item.tag"
                :key="index"
              >
                {{ item.icon }} {{ item.name }}
              </div>
            </div>
            <div>
              <input type="hidden" id="skillTags" v-model="v$.skillTags.$model" />
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.skillTags.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
          </div>

          <div class="sub-title">⑤ 一句话介绍（100字内）</div>
          <textarea
            class="pitch-box"
            rows="3"
            style="color: #1a1612"
            id="bio"
            v-model="v$.bio.$model"
          >
          </textarea>
          <div class="field-error-hint">
            <span v-for="(err, index) in v$.bio.$errors" :key="index">{{ err.$message }}</span>
          </div>

<!--          <div class="field-error-hint">-->
<!--            <span v-for="(err, index) in v$.$errors" :key="index">{{ err.$message }}</span>-->
<!--          </div>-->
          <input type="hidden" id="userId" v-model="v$.userId.$model" />
          <button class="btn-primary" style="float: right">保存数据→</button>
        </form>
      </div>

      <div class="reg-right">
        <div class="gift-box">
          <div class="gb-ico">🎁</div>
          <div class="gb-body">
            <div class="gb-title">创始成员礼包</div>
            <div class="gb-sub">永久锁定创始权益</div>
          </div>
          <div>
            <div class="gb-amount">1,000</div>
            <div class="gb-unit">Token 已到账</div>
          </div>
        </div>
        <div class="rw-box">
          <div class="rw-head sub-title">
            <div class="rw-dot"></div>
            注册后立即解锁
          </div>
          <div class="rw-body">
            <div class="rw-stat-row">匹配投资人预览 <span>3位已解锁</span></div>
            <div class="rw-stat-row">联合创始人推荐 <span>5位高匹配</span></div>
            <div class="rw-stat-row">行业动态订阅 <span>每日AI摘要</span></div>
            <div class="rw-stat-row">客户资源对接 <span>142家目标企业</span></div>
          </div>
        </div>
        <div class="rw-box">
          <div class="rw-head sub-title">
            <div class="rw-dot"></div>
            广告主数据价值
          </div>
          <div class="rw-body">
            <div
              style="
                font-size: 11px;
                color: rgba(255, 255, 255, 0.3);
                margin-bottom: 8px;
                font-family: 'DM Mono', monospace;
                color: #7a7568;
              "
            >
              注册用户的结构化画像
            </div>
            <div class="rw-stat-row">AI方向创业者 <span style="color: #c9924a">340人</span></div>
            <div class="rw-stat-row">活跃融资项目 <span style="color: #c9924a">89个</span></div>
            <div class="rw-stat-row">投资人画像完整度 <span style="color: #48bb78">87%</span></div>
            <div style="font-size: 11px; color: #7a7568; margin-top: 8px; line-height: 1.6">
              京东金融、阿里、百度等已开始定向投放，精准触达高净值用户群体
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { doSaveUserProfile } from '@/api/user/userRegisterApiI.ts';
import type { UserProfileBO } from '@/types/userBO.ts';
import MessageBox from '@/utils/MessageBox.ts';
import { onMounted, reactive } from 'vue';
import {
  FundingStageItems,
  IndustryItems,
  InvestmentTagsItems,
  NeedTagsItems,
  ProjectStageItems,
  RoleItems,
  SkillTagsItems,
  UserTitles,
  WorkTypeItems,
} from '@/utils/userData.ts';
import { useValidateUserProfile } from '@/hooks/useValidateUserRegister.ts';
import { getCurrentUserDetail } from '@/api/user/currentUserApi.ts';
import { CitiesItems } from '@/utils/needData.ts';

const formData = reactive<UserProfileBO>({
  userId: '',
  role: '',
  title: '',
  avatarUrl: '',
  displayName: '',
  bio: '',
  city: '',
  skillTags: '',
  industryTags: '',
  projectName: '',
  projectStage: '',
  teamSize: '',
  fundingStage: '',
  needTags: '',
  investmentTags: '',
  workType: '',
});

const roleData = reactive(RoleItems);
const industryData = reactive(IndustryItems);
const projectStageData = reactive(ProjectStageItems);
const fundingStageData = reactive(FundingStageItems);
const needTagsData = reactive(NeedTagsItems);
const investmentTagsData = reactive(InvestmentTagsItems);
const skillTagsData = reactive(SkillTagsItems);
const workTypes = reactive(WorkTypeItems);
const userTitles = reactive(UserTitles);
const cities = reactive(CitiesItems);

async function initProfileData() {
  for (let i = 0; i < roleData.length; i++) {
    if (formData.role == roleData[i].tag) {
      roleData[i].class = 'rc on';
    } else {
      roleData[i].class = 'rc';
    }
  }

  // 初始化角色
  const industryTags = ',' + formData.industryTags;
  for (let i = 0; i < industryData.length; i++) {
    if (industryTags.indexOf(',' + industryData[i].tag) > -1) {
      industryData[i].class = 't-chip on';
    } else {
      industryData[i].class = 't-chip';
    }
  }

  const projectStage = ',' + formData.projectStage;
  for (let i = 0; i < projectStageData.length; i++) {
    if (projectStage.indexOf(',' + projectStageData[i].tag) > -1) {
      projectStageData[i].class = 't-chip on';
    } else {
      projectStageData[i].class = 't-chip';
    }
  }

  const fundingStage = ',' + formData.fundingStage;
  for (let i = 0; i < fundingStageData.length; i++) {
    if (fundingStage.indexOf(',' + fundingStageData[i].tag) > -1) {
      fundingStageData[i].class = 't-chip on';
    } else {
      fundingStageData[i].class = 't-chip';
    }
  }

  const needTags = ',' + formData.needTags;
  for (let i = 0; i < needTagsData.length; i++) {
    if (needTags.indexOf(',' + needTagsData[i].tag) > -1) {
      needTagsData[i].class = 't-chip on';
    } else {
      needTagsData[i].class = 't-chip';
    }
  }

  const investmentTags = ',' + formData.investmentTags;
  for (let i = 0; i < investmentTagsData.length; i++) {
    if (investmentTags.indexOf(',' + investmentTagsData[i].tag) > -1) {
      investmentTagsData[i].class = 'stg on';
    } else {
      investmentTagsData[i].class = 'stg';
    }
  }

  const skillTags = ',' + formData.skillTags;
  for (let i = 0; i < skillTagsData.length; i++) {
    if (skillTags.indexOf(',' + skillTagsData[i].tag) > -1) {
      skillTagsData[i].class = 'stg on';
    } else {
      skillTagsData[i].class = 'stg';
    }
  }

  const title = ',' + formData.title;
  for (let i = 0; i < userTitles.length; i++) {
    if (title.indexOf(',' + userTitles[i].tag) > -1) {
      userTitles[i].class = 't-chip on';
    } else {
      userTitles[i].class = 't-chip';
    }
  }

  const workType = ',' + formData.workType;
  for (let i = 0; i < workTypes.length; i++) {
    if (workType.indexOf(',' + workTypes[i].tag) > -1) {
      workTypes[i].class = 't-chip on';
    } else {
      workTypes[i].class = 't-chip';
    }
  }
}

// 2. 获取数据并更新
async function fetchInitData() {
  getCurrentUserDetail()
    .then((res: any) => {
      if (res.code === 0) {
        Object.assign(formData, res.data);

        console.log('res.data.displayName=' + formData.industryTags);
        if (formData.bio == '' || formData.bio == null) {
          formData.bio =
            'AI驱动的企业知识管理平台，帮助科技公司将内部文档转化为可交互智能助手。目前服务15家公司，融资Pre-A，寻找技术联合创始人和天使投资人。';
        }
        initProfileData();
      } else {
        console.error(res.message);
      }
    })
    .catch(err => {
      console.log(err);
    });
}

onMounted(() => {
  fetchInitData();
});

const setVariousTags = () => {
  formData.industryTags = '';
  formData.skillTags = '';
  formData.needTags = '';
  formData.fundingStage = '';
  formData.projectStage = '';
  formData.investmentTags = '';
  formData.title = '';
  formData.workType = '';

  for (let i = 0; i < industryData.length; i++) {
    if (industryData[i].class.indexOf(`on`) > -1) {
      formData.industryTags += ',' + industryData[i].tag;
    }
  }

  for (let i = 0; i < projectStageData.length; i++) {
    if (projectStageData[i].class.indexOf(`on`) > -1) {
      formData.projectStage += ',' + projectStageData[i].tag;
    }
  }

  for (let i = 0; i < fundingStageData.length; i++) {
    if (fundingStageData[i].class.indexOf(`on`) > -1) {
      formData.fundingStage += ',' + fundingStageData[i].tag;
    }
  }

  for (let i = 0; i < needTagsData.length; i++) {
    if (needTagsData[i].class.indexOf(`on`) > -1) {
      formData.needTags += ',' + needTagsData[i].tag;
    }
  }

  for (let i = 0; i < investmentTagsData.length; i++) {
    if (investmentTagsData[i].class.indexOf(`on`) > -1) {
      formData.investmentTags += ',' + investmentTagsData[i].tag;
    }
  }

  for (let i = 0; i < skillTagsData.length; i++) {
    if (skillTagsData[i].class.indexOf(`on`) > -1) {
      formData.skillTags += ',' + skillTagsData[i].tag;
    }
  }

  for (let i = 0; i < userTitles.length; i++) {
    if (userTitles[i].class.indexOf(`on`) > -1) {
      formData.title += ',' + userTitles[i].tag;
    }
  }

  for (let i = 0; i < workTypes.length; i++) {
    if (workTypes[i].class.indexOf(`on`) > -1) {
      formData.workType += ',' + workTypes[i].tag;
    }
  }

  if (formData.industryTags.length > 0) formData.industryTags = formData.industryTags.substring(1);
  if (formData.skillTags.length > 0) formData.skillTags = formData.skillTags.substring(1);
  if (formData.needTags.length > 0) formData.needTags = formData.needTags.substring(1);
  if (formData.fundingStage.length > 0) formData.fundingStage = formData.fundingStage.substring(1);
  if (formData.projectStage.length > 0) formData.projectStage = formData.projectStage.substring(1);
  if (formData.investmentTags.length > 0)
    formData.investmentTags = formData.investmentTags.substring(1);
  if (formData.title.length > 0) formData.title = formData.title.substring(1);
  if (formData.workType.length > 0) formData.workType = formData.workType.substring(1);
};

const { v$, doValidateForm } = useValidateUserProfile(formData);

const handleSubmit = async () => {
  setVariousTags();

  const isValid: boolean = await doValidateForm();
  if (isValid) {
    doSaveUserProfile(formData)
      .then((res: any) => {
        if (res.code === 0) {
          MessageBox.Success('客户棣案配置成功!');
        } else {
          MessageBox.Error(res.message);
        }
      })
      .catch(err => {
        console.log(err);
      });
  }
};

const selectRole = (e: any) => {
  const o = e.currentTarget;
  const tag = o.dataset.tag;
  if (o.dataset.type === 'role') {
    for (let i = 0; i < roleData.length; i++) {
      if (tag == roleData[i].tag) {
        roleData[i].class = 'rc on';
        formData.role = tag;
      } else {
        roleData[i].class = 'rc ';
      }
    }
  }
};

const toggleTag = (e: any) => {
  let industry_count = 0;
  const o = e.currentTarget;
  const type = o.dataset.type;
  const tag = o.dataset.tag;
  if (type == 'industry') {
    for (let i = 0; i < industryData.length; i++) {
      if (industryData[i].class.indexOf(`on`) > -1) {
        industry_count++;
      }
    }
    for (let i = 0; i < industryData.length; i++) {
      if (industryData[i].tag == tag && industryData[i].class.indexOf(`on`) > -1) {
        industryData[i].class = 't-chip';
      } else if (industryData[i].tag == tag && industry_count < 3) {
        industryData[i].class = 't-chip on';
      }
    }
  }

  if (type == 'projectStage') {
    for (let i = 0; i < projectStageData.length; i++) {
      if (projectStageData[i].tag == tag && projectStageData[i].class.indexOf(`on`) <= -1) {
        projectStageData[i].class = 't-chip on';
      } else {
        projectStageData[i].class = 't-chip';
      }
    }
  }

  if (type == 'fundingStage') {
    for (let i = 0; i < fundingStageData.length; i++) {
      if (fundingStageData[i].tag == tag && fundingStageData[i].class.indexOf(`on`) <= -1) {
        fundingStageData[i].class = 't-chip on';
      } else {
        fundingStageData[i].class = 't-chip';
      }
    }
  }

  if (type == 'need') {
    for (let i = 0; i < needTagsData.length; i++) {
      if (needTagsData[i].tag == tag && needTagsData[i].class.indexOf(`on`) <= -1) {
        needTagsData[i].class = 't-chip on';
      } else if (needTagsData[i].tag == tag) {
        needTagsData[i].class = 't-chip';
      }
    }
  }

  if (type == 'investmentTags') {
    for (let i = 0; i < investmentTagsData.length; i++) {
      if (investmentTagsData[i].tag == tag && investmentTagsData[i].class.indexOf(`on`) <= -1) {
        investmentTagsData[i].class = 'stg on';
      } else if (investmentTagsData[i].tag == tag) {
        investmentTagsData[i].class = 'stg';
      }
    }
  }

  if (type == 'skill') {
    for (let i = 0; i < skillTagsData.length; i++) {
      if (skillTagsData[i].tag == tag && skillTagsData[i].class.indexOf(`on`) <= -1) {
        skillTagsData[i].class = 'stg on';
      } else if (skillTagsData[i].tag == tag) {
        skillTagsData[i].class = 'stg';
      }
    }
  }

  if (type == 'workType') {
    for (let i = 0; i < workTypes.length; i++) {
      if (workTypes[i].tag == tag && workTypes[i].class.indexOf(`on`) <= -1) {
        workTypes[i].class = 't-chip on';
      } else if (workTypes[i].tag == tag) {
        workTypes[i].class = 't-chip';
      }
    }
  }

  if (type == 'title') {
    for (let i = 0; i < userTitles.length; i++) {
      if (userTitles[i].tag == tag && userTitles[i].class.indexOf(`on`) <= -1) {
        userTitles[i].class = 't-chip on';
      } else if (userTitles[i].tag == tag) {
        userTitles[i].class = 't-chip';
      }
    }
  }
};
</script>

<style scoped lang="scss">
.sub-title {
  font-size: var(--font-size-14);
  color: #7a7568;
  margin-bottom: 10px;
  margin-top: 10px;
  font-weight: bolder;
}
</style>
