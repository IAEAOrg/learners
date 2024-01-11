<template>
  <div
    class="content-container pager exercises flex-wrap"
    :class="{ invisible: !(currentView === 'admin') }"
    v-show="currentView === 'admin'"
    style="overflow-y: scroll"
  >
    <v-container class="pa-5 mt-5">
      <v-row>
        <v-col cols="12">
          <h1>Admin Area</h1>
        </v-col>
        <v-col>
          <v-tabs
            @click="triggerUpdate(currentTab)"
            v-model="currentTab"
            mandatory
            class="admin-tabs-container"
          >
            <v-tab value="Submissions">Submissions Overview</v-tab>
            <v-tab value="Exercises">Exercises</v-tab>
            <v-tab value="Pages">Pages</v-tab>
            <v-tab value="Notifications">Notifications</v-tab>
            <v-tab value="Questionnaire">Questionnaire</v-tab>
            <v-tab value="Feedback">Feedback</v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="currentTab">
              <v-window-item value="Submissions">
                <submissions-overview
                  :currentTab="currentTab"
                  class="tab-container"
                />
              </v-window-item>
              <v-window-item value="Exercises">
                <exercises-overview
                  :currentTab="currentTab"
                  class="tab-container"
                />
              </v-window-item>
              <v-window-item value="Pages">
                <pages-overview
                  :currentTab="currentTab"
                  class="tab-container"
                />
              </v-window-item>
              <v-window-item value="Notifications">
                <notifications-overview
                  :currentTab="currentTab"
                  class="tab-container"
                />
              </v-window-item>
              <v-window-item value="Questionnaire">
                <questionnaire-overview
                  :currentTab="currentTab"
                  class="tab-container"
                />
              </v-window-item>
              <v-window-item value="Feedback">
                <feedback-overview
                  :currentTab="currentTab"
                  class="tab-container"
                />
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import SubmissionsOverview from "@/components/admin/SubmissionsOverview.vue";
import ExercisesOverview from "@/components/admin/ExercisesOverview.vue";
import PagesOverview from "@/components/admin/PagesOverview.vue";
import NotificationsOverview from "@/components/admin/NotificationsOverview.vue";
import QuestionnaireOverview from "@/components/admin/QuestionnaireOverview.vue";
import FeedbackOverview from "@/components/admin/FeedbackOverview.vue";
import { store } from "@/store";

export default {
  name: "AdminArea",
  components: {
    SubmissionsOverview,
    ExercisesOverview,
    PagesOverview,
    NotificationsOverview,
    QuestionnaireOverview,
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
