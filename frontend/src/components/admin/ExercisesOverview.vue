<template>
  <div>
    <h2 class="mb-4">
      Exercises Overview
      <v-progress-circular
        class="mx-2 mb-1"
        color="grey"
        indeterminate
        :width="3"
        :size="18"
        v-show="loading"
      ></v-progress-circular>
    </h2>
    <div
      v-for="(exerciseGroup, exerciseGroupName, index) in exerciseGroups"
      class="mb-8"
    >
      <h3 class="text-secondary">
        {{ exerciseGroupName }}
      </h3>

      <v-card class="pa-0 mt-2 mb-5">
        <v-container class="pa-5">
          <v-row class="text-grey d-none d-sm-flex">
            <v-col sm="1" class="d-none d-lg-flex">Type</v-col>
            <v-col sm="5">Name</v-col>
            <v-col sm="3">Page</v-col>
            <v-col sm="3">Progress</v-col>
          </v-row>

          <v-row
            v-for="exercise in exerciseGroup.childExercises"
            :key="exercise"
            class="py-0 mt-0 exercise-row"
            @click="showDetails(exercise)"
          >
            <v-col sm="1" class="d-none d-lg-flex">
              <!-- Script/Form -->
              <SvgIcon
                v-if="exercise.exercise_type === 'script'"
                name="command-line"
                class="mr-2"
              />
              <SvgIcon
                v-if="exercise.exercise_type === 'form'"
                name="book-open"
                class="mr-2"
              />
              <!-- Group/Single -->
              <SvgIcon v-if="exercise.team" name="user-group" class="mr-2" />
              <SvgIcon v-else name="user" class="mr-2" />
            </v-col>
            <v-col cols="12" sm="5">
              <h3 v-html="exercise.exercise_name"></h3>
            </v-col>
            <v-col cols="12" sm="3">
              <span v-html="exercise.page_title"> </span>
            </v-col>
            <v-col cols="8" sm="3" class="process">
              <v-progress-linear
                v-model="exercise.completion_percentage"
                color="success"
                height="25"
              >
                {{ exercise.completion_percentage }}
              </v-progress-linear>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </div>

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
      <exercise-card :exercise="selectedExercise" />
    </v-dialog>
  </div>
</template>

<script lang="ts">
import ExerciseCard from "@/components/admin/ExerciseCard.vue";
import SuccessIcon from "@/components/sub-components/SuccessIcon.vue";
import FailIcon from "@/components/sub-components/FailIcon.vue";
import Loader from "@/components/sub-components/Loader.vue";
import SvgIcon from "@/components/dynamic-components/SvgIcon.vue";
import axios from "axios";
import { store } from "@/store";
import { IExerciseObject } from "@/types";

export default {
  name: "ExercisesOverview",
  components: {
    SuccessIcon,
    FailIcon,
    SvgIcon,
    Loader,
    ExerciseCard,
  },
  data() {
    return {
      tabledata: { cols: <any>[], rows: <any>[] },
      submissions: [],
      exerciseGroups: <any>[],
      detailsIdentifier: { exerciseId: "" },
      loading: false,
      dialog: false,
      selectedExercise: Object as () => IExerciseObject,
    };
  },
  props: {
    currentTab: { type: String, require: false },
  },
  computed: {
    showLoader() {
      const viewCondition = store.getters.getCurrentView === "admin";
      const tabCondition = this.currentTab === "Exercises";
      const eventCondition = this.loading;
      return viewCondition && tabCondition && eventCondition;
    },
    forceReload() {
      return store.getters.getAdminForceReload("exercises");
    },
  },
  methods: {
    showDetails(exercise) {
      this.selectedExercise = exercise;
      this.dialog = true;
    },
    async getDataFromServer() {
      this.loading = true;
      axios
        .get("exercises")
        .then((res) => {
          const exercises = res.data.exercises;

          this.exerciseGroups = exercises.reduce((exerciseGroups, item) => {
            const exerciseGroup = exerciseGroups[item.parent_page_title] || {
              childExercises: [],
              completionPercentage: 0,
            };
            exerciseGroup.childExercises.push(item);
            exerciseGroup.completionPercentage += item.completion_percentage;
            exerciseGroups[item.parent_page_title] = exerciseGroup;
            return exerciseGroups;
          }, {});
        })
        .finally(() => {
          this.loading = false;
          store.dispatch("unsetAdminForceReload", "exercises");
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
