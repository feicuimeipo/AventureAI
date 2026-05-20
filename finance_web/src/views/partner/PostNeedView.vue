<template>
  <!-- ═══ VIEW: PUBLISH NEED ═══ -->
  <!--  <div :class="moduleStyle">-->
  <div class="publish_parent">
    <div class="publish-wrap">
      <div class="public-content">
        <form novalidate @submit.prevent="handleSubmit" class="m-0 p-0">
          <div class="field-group">
            <div class="field-label">需求名称 <span class="req">*</span></div>
            <div class="tag-grid">
              <input
                type="text"
                class="field-input"
                id="title"
                v-model="v$.title.$model"
                placeholder="请输入需求标题"
              />
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.title.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
          </div>
          <div class="field-group">
            <div class="field-label">寻找角色 <span class="req">*</span></div>
            <div class="tag-grid">
              <div v-for="(item, index) in needRoles" :key="index">
                <div
                  class="stag"
                  @click="toggleTag"
                  data-type="role"
                  :data-tag="item.tag"
                  :class="item.class"
                >
                  {{ item.name }}
                </div>
              </div>
              <input type="hidden" id="roleWanted" v-model="v$.roleWanted.$model" />
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.roleWanted.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
          </div>

          <div class="field-row">
            <div class="field-group">
              <div class="field-label">参与方式 <span class="req">*</span></div>
              <div class="tag-grid">
                <div v-for="(item, index) in participation" :key="index">
                  <div
                    class="stag"
                    @click="toggleTag"
                    data-type="participation"
                    :data-tag="item.tag"
                    :class="item.class"
                  >
                    {{ item.name }}
                  </div>
                </div>
                <input type="hidden" id="workType" v-model="v$.workType.$model" />
                <div class="field-error-hint">
                  <span v-for="(err, index) in v$.workType.$errors" :key="index">{{
                    err.$message
                  }}</span>
                </div>
              </div>
            </div>

            <div class="field-group">
              <div class="field-label">状态 <span class="req">*</span></div>
              <div class="tag-grid">
                <select class="field-input" id="status" v-model="formData.status">
                  <option
                    v-for="(item, index) in needStatus"
                    :key="index"
                    :value="item.value"
                    :selected="item.value === formData.status"
                  >
                    {{ item.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field-group">
            <div class="field-label">
              技能要求 <span class="req">*</span> <span class="opt-badge">可多选</span>
            </div>
            <div class="tag-grid" id="skillTagsInput">
              <div v-for="(item, index) in skillsTags" :key="index">
                <div
                  class="stag"
                  @click="toggleTag"
                  data-type="skill"
                  :data-tag="item.tag"
                  :class="item.class"
                >
                  {{ item.name }}
                </div>
              </div>
              <input type="hidden" id="skillReqs" v-model="v$.skillReqs.$model" />
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.skillReqs.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
          </div>

          <div class="field-group">
            <div class="field-label">
              需求描述
              <span class="req">*</span>
              <span class="field-hint" style="margin-top: 0"
                >建议 100-300 字，包含：项目现状、你的背景、具体期望</span
              >
            </div>
            <textarea
              class="field-input"
              id="description"
              v-model="v$.description.$model"
              rows="5"
              placeholder="项目现状：我们在做企业智能知识管理，MVP已完成，有100个种子客户。
我的背景：有过成功的创业经验，毕业于...之前在...做过...
我的需求：CTO，技术栈 Python/Node.js，能主导后端架构并懂LLM应用工程的联创/CTO，希望是有大厂经历且有创业热情的人……"
              style="resize: vertical"
            >
            </textarea>
            <div class="field-error-hint">
              <span v-for="(err, index) in v$.description.$errors" :key="index">{{
                err.$message
              }}</span>
            </div>
          </div>

          <div class="field-row">
            <div class="field-group">
              <div class="field-label">项目赛道</div>
              <select class="field-input" id="industry" v-model="v$.industry.$model">
                <option value="" disabled selected>--请选择赛道--</option>
                <option
                  v-for="(item, index) in industries"
                  :key="index"
                  :value="item.tag"
                  :selected="item.tag === formData.industry"
                >
                  {{ item.name }}}
                </option>
              </select>
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.industry.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
            <div class="field-group">
              <div class="field-label">地理要求</div>
              <select class="field-input" id="cityReqs" v-model="v$.cityReqs.$model">
                <option value="" disabled selected>--地理要求--</option>
                <option
                  v-for="(item, index) in cities"
                  :key="index"
                  :value="item.tag"
                  :selected="formData.cityReqs == item.tag"
                >
                  {{ item.name }}
                </option>
              </select>
              <div class="field-error-hint">
                <span v-for="(err, index) in v$.cityReqs.$errors" :key="index">{{
                  err.$message
                }}</span>
              </div>
            </div>
          </div>
          <div class="field-group">
            <div class="field-label">激励 <span class="opt-badge">可选，填写后更受关注</span></div>
            <input
              class="field-input"
              style="width: 100%"
              type="text"
              id="equityRange"
              v-model="v$.equityRange.$model"
              placeholder="股权比例，如：5% - 15%; 兑现：4年 1年cliff"
            />
          </div>
          <button class="btn-primary" type="submit" v-if="type == 'add'" :disabled="isSubmitted">
            发布需求 →
          </button>
          <button class="btn-primary" type="submit" v-else :disabled="isSubmitted">
            保存修改 →
          </button>
        </form>
      </div>
    </div>
  </div>
  <!--  </div>-->
</template>

<script setup lang="ts">
import {
  CitiesItems,
  NeedRoleItems,
  NeedStatusItem,
  ParticipationItems,
  SkillsTagsItems,
} from '@/utils/needData.ts';
import { onMounted, reactive, ref } from 'vue';
import { IndustryItems } from '@/utils/userData.ts';
import type { NeedDetailVO } from '@/types/needBO.ts';
import { useValidatePostNeeds } from '@/hooks/useValidateNeeds.ts';
import { editNeeds, getNeedDetail, postNeeds } from '@/api/need/need.ts';
import MessageBox from '@/utils/MessageBox.ts';

const needRoles = reactive(NeedRoleItems);
const participation = reactive(ParticipationItems);
const skillsTags = reactive(SkillsTagsItems);
const cities = reactive(CitiesItems);
const industries = reactive(IndustryItems);
const needStatus = reactive<{ value: string; name: string }[]>(NeedStatusItem);

const props = defineProps<{
  id?: string;
  type: string;
}>();

const formData = reactive<NeedDetailVO>({} as NeedDetailVO);

const setDefaultValue = (formData: any) => {
  needRoles.forEach(item => {
    if (item.tag === formData.roleWanted) {
      item.class = 'stag on';
    } else {
      item.class = 'stag';
    }
  });

  participation.forEach(item => {
    item.class = 'stag';
    if (item.tag == formData.workType) {
      item.class = 'stag on';
    }
  });

  const skillReqs = ',' + formData.skillReqs + ',';
  skillsTags.forEach(item => {
    item.class = 'stag';
    if (skillReqs.indexOf(',' + item.tag + ',') > -1) {
      item.class = 'stag on';
    }
  });
};

const emit = defineEmits(['closeModel']);
onMounted(() => {
  if (props.id && props.id && props.type === 'edit') {
    getNeedDetail(props.id).then((res: any) => {
      if (res.code === 0) {
        const item = res.data;
        // console.log(JSON.stringify(item));
        formData.id = item.id;
        formData.title = item.title;
        formData.roleWanted = item.role_wanted;
        formData.workType = item.work_type;
        formData.cityReqs = item.city_reqs;
        formData.description = item.description;
        formData.industry = item.industry;
        formData.skillReqs = item.skill_reqs;
        formData.equityRange = item.equity_range;
        formData.status = item.status;
        formData.expiredAt = item.expired_at;
        formData.createdAt = item.created_at;
        // console.log(JSON.stringify(formData));

        setDefaultValue(formData);
      } else {
        MessageBox.Error('需求不存在');
        emit('closeModel');
      }
    });
  } else {
    Object.assign(formData, {
      id: '',
      title: '',
      roleWanted: '',
      workType: '',
      cityReqs: '',
      description: '项目现状: \n' + '我的背景: \n' + '具体需求: ',
      industry: '',
      skillReqs: '',
      equityRange: '',
      status: 'active',
      viewCount: 0,
      expiredAt: '',
      createdAt: '',
      vesting: '',
    });
  }
});

const toggleTag = (e: any) => {
  const o = e.currentTarget;
  const type = o.dataset.type;
  const tag = o.dataset.tag;

  if (type == 'role') {
    for (let i = 0; i < needRoles.length; i++) {
      if (needRoles[i].tag == tag && needRoles[i].class.indexOf(`on`) <= -1) {
        needRoles[i].class = 'stag on';
      } else {
        needRoles[i].class = 'stag';
      }
    }
  }

  if (type == 'participation') {
    for (let i = 0; i < participation.length; i++) {
      if (participation[i].tag == tag && participation[i].class.indexOf(`on`) <= -1) {
        participation[i].class = 'stag on';
      } else {
        participation[i].class = 'stag';
      }
    }
  }

  if (type == 'skill') {
    for (let i = 0; i < skillsTags.length; i++) {
      if (skillsTags[i].tag == tag && skillsTags[i].class.indexOf(`on`) <= -1) {
        skillsTags[i].class = 'stag on';
      }
    }
  }
};

const { v$, doValidateForm } = useValidatePostNeeds(formData);

const setVariousTags = () => {
  formData.roleWanted = '';
  formData.workType = '';
  formData.skillReqs = '';

  for (let i = 0; i < needRoles.length; i++) {
    if (needRoles[i].class.indexOf(`on`) > -1) {
      formData.roleWanted += ',' + needRoles[i].tag;
    }
  }

  for (let i = 0; i < participation.length; i++) {
    if (participation[i].class.indexOf(`on`) > -1) {
      formData.workType += ',' + participation[i].tag;
    }
  }

  for (let i = 0; i < skillsTags.length; i++) {
    if (skillsTags[i].class.indexOf(`on`) > -1) {
      formData.skillReqs += ',' + skillsTags[i].tag;
    }
  }

  if (formData.roleWanted.length > 0) {
    formData.roleWanted = formData.roleWanted.substring(1);
  }
  if (formData.workType.length > 0) {
    formData.workType = formData.workType.substring(1);
  }
  if (formData.skillReqs.length > 0) {
    formData.skillReqs = formData.skillReqs.substring(1);
  }
};

const isSubmitted = ref<boolean>(false);
const handleSubmit = async (): Promise<void> => {
  setVariousTags();
  const isValid: boolean = await doValidateForm();
  if (isValid) {
    isSubmitted.value = true;
    if (props.type == 'edit') {
      if (!props.id || props.id == '') {
        MessageBox.Error('需求编号不能为空');
      } else {
        editNeeds(props.id, formData)
          .then((res: any) => {
            if (res.code === 0) {
              emit('closeModel', null);
              MessageBox.Success('需求修改成功!');
              window.location.reload();
            } else {
              console.log(res.message);
              MessageBox.Error(res.message);
            }
            isSubmitted.value = false;
          })
          .catch(err => {
            isSubmitted.value = false;
            console.log(err);
          });
      }
    } else {
      postNeeds(formData)
        .then((res: any) => {
          if (res.code === 0) {
            emit('closeModel', res.data.id);
            MessageBox.Success('需求发布成功!');
            window.location.reload();
          } else {
            MessageBox.Error(res.message);
          }
          isSubmitted.value = false;
        })
        .catch(err => {
          isSubmitted.value = false;
          console.log(err);
        });
    }
  }
};
</script>

<style scoped></style>
