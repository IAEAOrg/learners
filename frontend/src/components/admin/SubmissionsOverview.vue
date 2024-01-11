<template>
  <div>
    <h2>
      Submissions Overview
      <v-progress-circular
        class="mx-2 mb-1"
        color="grey"
        indeterminate
        :width="3"
        :size="18"
        v-show="loading"
      ></v-progress-circular>
    </h2>
    <v-card class="pa-5 my-5">
      <data-table
        class="mt-3"
        :headers="exercises"
        :items="submissions"
        @showDetails="showDetails"
      />
    </v-card>

    <!-- Dialog -->
    <v-dialog v-model="dialog" width="60%">
      <v-btn
        icon
        rounded
        size="x-small"
        class="ml-auto"
        color="white"
        variant="text"
        @click="dialog = false"
        ><SvgIcon name="x-mark" clickable
      /></v-btn>
      <submission-card
        :userId="detailsIdentifier.userId"
        :exerciseId="detailsIdentifier.exerciseId"
      />
    </v-dialog>
  </div>
</template>

<script lang="ts">
import SubmissionCard from "@/components/admin/SubmissionCard.vue";
import Loader from "@/components/sub-components/Loader.vue";
import DataTable from "@/components/sub-components/DataTable.vue";
import SvgIcon from "@/components/dynamic-components/SvgIcon.vue";
import { store } from "@/store";
import axios from "axios";

export default {
  name: "SubmissionsOverview",
  components: {
    SubmissionCard,
    Loader,
    DataTable,
    SvgIcon,
  },
  data() {
    return {
      exercises: <any>[
        {
          value: "username",
          text: "user",
          parent: "user",
          fixed: true,
          sortable: true,
        },
      ],
      submissions: <any>[],
      dialog: false,
      detailsIdentifier: { userId: 0, exerciseId: "" },
      loading: false,
    };
  },
  props: {
    currentTab: { type: String, require: false },
  },
  computed: {
    forceReload() {
      return store.getters.getAdminForceReload("submissions");
    },
  },
  methods: {
    showDetails({ exerciseId, userId }) {
      this.dialog = true;
      this.detailsIdentifier = { userId: userId, exerciseId: exerciseId };
    },
    async getDataFromServer() {
      this.loading = true;
      axios.get("exercises").then((res) => {
        let _exercises = <any>[
          {
            value: "username",
            text: "user",
            parent: "user",
            fixed: true,
            sortable: true,
          },
        ];
        const exercises = res.data.exercises;
        exercises.sort((a, b) => (a.order_weight > b.order_weight ? 1 : -1));
        exercises.forEach((exercise) => {
          _exercises.push({
            value: exercise.global_exercise_id,
            text: exercise.exercise_name,
            parent: exercise.parent_page_title,
          });
        });
        this.exercises = _exercises;
      });

      axios
        .get("submissions")
        .then((res) => {
          let _submissions = <any>[];
          const submissions = res.data.submissions;
          submissions.forEach((submission) => {
            if (!this.submissions.includes(submission, 0))
              _submissions.push(submission);
          });
          this.submissions = _submissions;
        })
        .finally(() => {
          this.loading = false;
          store.dispatch("unsetAdminForceReload", "submissions");
        });
    },
  },
  watch: {
    forceReload: {
      handler(new_state, old_state) {
        if (new_state === true || old_state === undefined) {
          this.getDataFromServer();
        }
      },
      immediate: true,
    },
  },
};
</script>
