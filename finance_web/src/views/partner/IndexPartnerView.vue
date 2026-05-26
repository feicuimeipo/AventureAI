<template>
  <!-- Modal -->
  <div :class="moduleStyle">
    <!-- Modal 示例 -->
    <div
      class="modal fade"
      :class="{ show: myModalIsModalOpen }"
      style="display: block"
      v-if="myModalIsModalOpen"
    >
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ myModelTitle }}</h5>
            <div
              style="font-size: 12px; margin-top: 10px; margin-left: 5px; font-weight: bold"
              v-if="myModelType == 'add'"
            >
              发布并通过审核后可获得 <strong style="color: teal">+30 Token</strong> (每天限30 token)
            </div>
            <button type="button" class="btn-close" @click="handleCloseModal(null)"></button>
          </div>
          <div class="modal-body">
            <PostNeedView :id="needId" :type="myModelType" @closeModel="handleCloseModal" />
          </div>
        </div>
      </div>
    </div>

    <AppHeader
      subtitle=""
      cssmodule="module-teal"
      :menulist="menuList"
      @switchTabEvent="handleSwitchTab"
    />

    <div class="app" id="mainApp">
      <!-- SIDEBAR -->
      <div class="sidebar" id="partnerSidebar">
        <SidebarPartnerSearch @handleNeed="onOpenModal"  />
      </div>

      <!-- MAIN CONTENT -->
      <div class="main">
        <router-view />
      </div>
      <!-- .main -->
    </div>
    <!-- .app -->
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import '@/styles/module_partner.scss';
import AppHeader from '@/components/AppHeader.vue';
import { getPartnerMenus, getPartnerStyleClass } from '@/utils/menuUtils.ts';
import SidebarPartnerSearch from '@/views/partner/SidebarPartnerSearch.vue';
import { ref } from 'vue';
import { toogleElementById } from '@/utils';
import PostNeedView from '@/views/partner/PostNeedView.vue';
import type { NeedVO } from '@/types/needBO.ts';
import MessageBox from '@/utils/MessageBox.ts';

const myModalIsModalOpen = ref(false);
const myModelTitle = ref<string>();
const myModelType = ref<string>('add');
const needId = ref<string>();
const onOpenModal = (type: string, item: NeedVO) => {
  if (type == 'edit') {
    if (item.id == '' || !item.id) {
      MessageBox.Error('需求编好不能为空');
    } else {
      needId.value = item.id;
      myModelTitle.value = '编辑需求';
      myModelType.value = 'edit';
      myModalIsModalOpen.value = true;
    }
  } else {
    needId.value = '';
    myModelTitle.value = '发布需求';
    myModalIsModalOpen.value = true;
    myModelType.value = 'add';
  }
};

const handleCloseModal = (needId: string | null) => {
  myModalIsModalOpen.value = false;
  if (needId) {
    // console.log('needId=' + needId);
  }
};

const moduleStyle = getPartnerStyleClass();
const menuList = getPartnerMenus();
const handleSwitchTab = (path: any) => {
  if (path == 'message') {
    toogleElementById('partnerSidebar', false);
  } else {
    toogleElementById('partnerSidebar', true);
  }
};
</script>

<style scoped></style>
