import axios from "axios";
import { Commit } from "vuex";
import {
  extractNotifications,
  extractQuestionnaires,
  initializeBackendUrl,
} from "@/helpers";
import { INotificationObject, IQuestionnaireQuestionObject } from "@/types";

export default {
  // Setup/General Actions
  setLogo: ({ commit }: { commit: Commit }, logo: string) =>
    commit("SET_LOGO", logo),

  setJwt: ({ commit }: { commit: Commit }, jwt: string) =>
    commit("SET_JWT", jwt),

  unsetJwt: ({ commit }: { commit: Commit }) => commit("SET_JWT", ""),

  setError: ({ commit }: { commit: Commit }, error_msg: string) =>
    commit("SET_ERROR", error_msg),

  setCurrentView: ({ commit }: { commit: Commit }, currentView: string) =>
    commit("SET_CURRENT_VIEW", currentView),

  reinitBackendUrl({ commit }) {
    const backendUrl = initializeBackendUrl();
    console.log("Backend is set to:", backendUrl);
    commit("SET_BACKEND_URL", backendUrl);
  },

  // Tabs
  async getTabsFromServer({ commit }) {
    await axios
      .get("setup/tabs")
      .then((response) => {
        commit("SET_TABS", response.data);
      })
      .catch((error) => commit("SET_TABS", []));
  },

  // Styles
  setTheme: ({ commit }: { commit: Commit }, theme: any) =>
    commit("SET_THEME", theme),

  async getStylesFromServer({ commit }) {
    await axios
      .get("setup/styles")
      .then((response) => {
        commit("SET_LOGO", response.data.logo);
        commit("SET_THEME", response.data.theme);
      })
      .catch((error) =>
        commit(
          "SET_LOGO",
          '<svg viewBox="0 0 343.71 136.32" style="enable-background:new 0 0 200 200;" xml:space="preserve" xmlns="http://www.w3.org/2000/svg"><polygon points="343.71 41.4 343.71 0 236 0 236 41.4 268.17 41.4 268.17 136.32 311.54 136.32 311.54 41.4 343.71 41.4" style="fill: #fff;"/><rect x="184.69" width="43.37" height="136.32" style="fill: #fff;"/><polygon points="133.38 136.32 176.75 136.32 176.75 0 136.22 0 0 136.32 55.97 136.32 133.38 58.82 133.38 136.32" style="fill: #fff;"/></svg>'
        )
      );
  },

  resetTabs: ({ commit }: { commit: Commit }) => commit("SET_TABS", []),

  setOpendInTab: (
    { commit }: { commit: Commit },
    { tabId: string, opened: boolean }
  ) => commit("SET_OPENED_IN_TAB", { tabId: string, opened: boolean }),

  // Notifications
  setCurrentNotification: (
    { commit }: { commit: Commit },
    currentNotificationIndex: number
  ) => commit("SET_CURRENT_NOTIFICATION", currentNotificationIndex),

  setCurrentNotificationToLast: ({ commit }: { commit: Commit }) =>
    commit("SET_CURRENT_NOTIFICATION_INDEX_TO_LAST"),

  decCurrentNotification: ({ commit }: { commit: Commit }) =>
    commit("DEC_CURRENT_NOTIFICATION"),

  incCurrentNotification: ({ commit }: { commit: Commit }) =>
    commit("INC_CURRENT_NOTIFICATION"),

  appendToNotifications: (
    { commit }: { commit: Commit },
    payload: INotificationObject
  ) => commit("APPEND_TO_NOTIFICATIONS", payload),

  async getNotificationsFromServer({ commit }) {
    await axios.get("notifications").then((response) => {
      commit(
        "SET_NOTIFICATIONS",
        extractNotifications(response.data.notifications)
      );
      commit("SET_CURRENT_NOTIFICATION_INDEX_TO_LAST");
    });
  },

  enableNotifications: ({ commit }: { commit: Commit }) =>
    commit("SET_SHOW_NOTIFICATIONS_STATE", true),

  disableNotifications: ({ commit }: { commit: Commit }) =>
    commit("SET_SHOW_NOTIFICATIONS_STATE", false),

  // Questionnaires
  appendToQuestionnaires: (
    { commit }: { commit: Commit },
    payload: IQuestionnaireQuestionObject
  ) => commit("APPEND_TO_QUESTIONNAIRES", payload),

  setCurrentQuestionnaireToLast: ({ commit }: { commit: Commit }) =>
    commit("SET_CURRENT_QUESTIONNAIRE_INDEX_TO_LAST"),

  removeQuestionnaire: (
    { commit }: { commit: Commit },
    global_question_id: Number
  ) => {
    commit("REMOVE_QUESTIONNAIRE", global_question_id);
    commit("SET_CURRENT_QUESTIONNAIRE_INDEX_TO_LAST");
  },

  async getQuestionnairesFromServer({ commit }) {
    await axios.get("questionnaires/questions").then((response) => {
      commit(
        "SET_QUESTIONNAIRES",
        extractQuestionnaires(response.data.questions)
      );
      commit("SET_CURRENT_QUESTIONNAIRE_INDEX_TO_LAST");
    });
  },

  enableQuestionnaire: ({ commit }: { commit: Commit }) =>
    commit("SET_SHOW_QUESTIONNAIRE_STATE", true),

  disableQuestionnaire: ({ commit }: { commit: Commit }) =>
    commit("SET_SHOW_QUESTIONNAIRE_STATE", false),

  // Admin View Actions
  setAdminForceReload: ({ commit }: { commit: Commit }, tab: string) =>
    commit("SET_ADMIN_FORCE_RELOAD", { tab: tab, state: true }),

  unsetAdminForceReload: ({ commit }: { commit: Commit }, tab: string) =>
    commit("SET_ADMIN_FORCE_RELOAD", { tab: tab, state: false }),
};
