<template>
  <div>
    <h2 class="mb-5">
      Questionnaire Overview

      <v-progress-circular
        class="mx-2 mb-1"
        color="grey"
        indeterminate
        :width="3"
        :size="18"
        v-show="loading"
      ></v-progress-circular>
    </h2>

    <v-expansion-panels>
      <v-expansion-panel
        v-for="questionnaire in questionnaires"
        :key="questionnaire.page_title"
      >
        <v-expansion-panel-title>
          <span v-html="questionnaire.page_title"></span>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-container class="px-0">
            <v-row
              v-for="question in extractRows(questionnaire.questions)"
              :key="question.id"
              class="questionnaire-row"
            >
              <v-col cols="4">
                <span class="question-id">
                  {{ question.id }}
                </span>
                <span v-html="question.question"> </span>
              </v-col>
              <v-col cols="6">
                <ol class="answers">
                  <li v-for="answer in JSON.parse(question.answer_options)">
                    {{ answer }}
                  </li>
                </ol>
              </v-col>
              <v-col cols="1">
                {{ question.language }}
              </v-col>
              <v-col cols="1" class="d-flex justify-end">
                <v-btn
                  v-if="!question.active"
                  @click="activateQuestion(question.global_question_id)"
                  color="success"
                >
                  send
                </v-btn>
                <v-btn
                  v-else
                  @click="viewQuestion(question.global_question_id)"
                  color="success"
                  variant="outlined"
                >
                  <SvgIcon name="eye" class="mr-2" />
                  view
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <div v-if="Object.keys(questionnaires).length === 0" class="no-data">
      No data.
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
      <questionnaire-card :questionnaireId="selectedQuestionnaire" />
    </v-dialog>
  </div>
</template>

<script lang="ts">
interface Question {
  id: number;
  global_question_id: string;
  question: string;
  answer_options: string;
  language: string;
  active: boolean;
  options: string[];
}

import axios from "axios";

import QuestionnaireCard from "@/components/admin/QuestionnaireCard.vue";
import Loader from "@/components/sub-components/Loader.vue";
import SvgIcon from "@/components/dynamic-components/SvgIcon.vue";
import { store } from "@/store";
import { IQuestionnaireQuestionObject } from "@/types";

export default {
  name: "QuestionnaireOverview",
  components: {
    QuestionnaireCard,
    Loader,
    SvgIcon,
  },
  data() {
    return {
      questionnaires: [] as any[],
      // Loader conditions
      questionnaireLoading: false,
      // Form
      form: false,
      dialog: false,
      selectedQuestionnaire: "",
    };
  },
  props: {
    currentTab: { type: String, require: false },
  },
  computed: {
    loading() {
      return this.questionnaireLoading;
    },
    forceReload() {
      return store.getters.getAdminForceReload("questionnaire");
    },
  },
  methods: {
    extractRows(questions) {
      let updatedRows = [] as Question[];
      questions.forEach((question) => {
        let found_index = updatedRows.findIndex(
          (q) => q.global_question_id === question.global_question_id
        );
        if (found_index > -1) {
          const current_language = updatedRows[found_index]["language"];
          if (!current_language.includes(question.language))
            updatedRows[found_index]["language"] =
              current_language + ", " + question.language;
        } else updatedRows.push(question);
      });
      return updatedRows;
    },
    async activateQuestion(global_question_id) {
      await axios.put(`questionnaires/questions/${global_question_id}`);
    },
    async viewQuestion(global_question_id) {
      this.selectedQuestionnaire = global_question_id;
      this.dialog = true;
    },
    async getDataFromServer() {
      this.questionnaireLoading = true;
      axios
        .get("questionnaires")
        .then((res) => {
          this.questionnaires = res.data.questionnaires;
        })
        .finally(() => {
          this.questionnaireLoading = false;
          store.dispatch("unsetAdminForceReload", "questionnaire");
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

<style lang="scss">
.answers {
  list-style: lower-alpha;
  margin-left: 1rem;

  & li {
    padding-left: 10px;
    &::marker {
      color: rgba(var(--v-theme-secondary), 1);
    }
  }
}

.question-id {
  font-weight: bold;
  color: rgba(var(--v-theme-secondary), 1);
  padding-right: 15px;
  height: 100%;
  float: left;
}

.drop-down-group-title {
  font-weight: bold;
}

.questionnaire-row {
  transition: all 100ms ease;
  padding: 16px 24px 16px 16px;
  cursor: pointer;

  &:not(:last-child) {
    border-bottom: 1px solid #919191;
  }

  &:hover {
    background-color: rgba(var(--v-theme-secondary), 0.05);
  }
}

.v-list-item {
  padding-top: 0px !important;
  padding-bottom: 0px !important;
}
.v-list-item__content {
  display: flex;
  flex-direction: row-reverse;
  justify-content: start;
  align-content: center;
}

.v-list-item-title {
  flex: 1;
  align-self: center;
  height: 100%;
  width: 100%;
}
.v-list-item-subtitle {
  flex: 1;
  align-self: center;
}

.v-list-item-action {
  align-content: center;
  justify-content: center;
  display: flex;
  height: 45px;
  max-width: 20%;
}

.v-input.v-checkbox {
  display: flex;
}

.initial-notifications-list-item {
  position: relative;
  background-color: #f6f6f6;
  margin-top: 0px;
  border-radius: 4px;
}

.list-hover-container {
  display: flex;
  position: absolute;
  background-color: rgba(var(--v-theme-secondary), 0);
  width: 100%;
  height: 100%;
  transition: all 150ms ease;
  border-radius: 4px;

  &:hover {
    background-color: rgba(var(--v-theme-secondary), 0.1);
  }

  button.v-btn {
    background-color: white;
    border: solid 1px #555;
  }
}

.autocomplete-inputs .v-input__control {
  min-height: 60px;
}
</style>
