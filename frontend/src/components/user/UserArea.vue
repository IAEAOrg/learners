<template>
  <div
    class="content-container pager exercises flex-wrap"
    :class="{ invisible: !(currentView === 'user') }"
    v-show="currentView === 'user'"
    style="overflow-y: scroll"
  >
    <v-container class="pa-5 mt-5">
      <v-row>
        <v-col cols="12">
          <h1>User Area</h1>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import SubmissionsOverview from "@/components/admin/SubmissionsOverview.vue";
import ExercisesOverview from "@/components/admin/ExercisesOverview.vue";
import NotificationsOverview from "@/components/admin/NotificationsOverview.vue";
import FeedbackOverview from "@/components/admin/FeedbackOverview.vue";
import { store } from "@/store";

export default {
  name: "UserArea",
  components: {
    SubmissionsOverview,
    ExercisesOverview,
    NotificationsOverview,
    FeedbackOverview,
  },
  props: {
    currentView: { type: String, require: false, default: "" },
  },
  methods: {
    triggerUpdate(tab) {
      store.dispatch("setAdminForceReload", tab.toLowerCase());
    },
  },
  data() {
    return {
      currentTab: "Submissions",
    };
  },
  mounted() {
    document.body.style.overflowY = "auto";
  },
};
</script>
