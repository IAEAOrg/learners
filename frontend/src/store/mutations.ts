import { generateTabs } from "@/helpers";
import { INotificationObject, IQuestionnaireQuestionObject } from "@/types";

export default {
  SET_LOGO: (state: { logo: string }, logo: string) => (state.logo = logo),
  SET_JWT: (state: { jwt: string }, jwt: string) => (state.jwt = jwt),
  SET_BACKEND_URL: (state: { backendUrl: string }, backendUrl: string) =>
    (state.backendUrl = backendUrl),
  SET_ERROR: (state: { error: string }, error_msg: string) =>
    (state.error = error_msg),
  SET_TABS: (state: { tabs: any; currentView: string }, response: any) => {
    const { genTabs, genCurrentView } = generateTabs(
      state.tabs || [],
      response
    );
    state.tabs = genTabs;
    state.currentView = genCurrentView;
  },
  SET_THEME: (state: { theme: any }, theme: any) => (state.theme = theme),

  SET_CURRENT_VIEW: (state: { currentView: string }, currentView: string) =>
    (state.currentView = currentView),

  SET_OPENED_IN_TAB: (
    state: { tabs: any },
    payload: { tabId: string; opened: boolean }
  ) => {
    const tab = state.tabs.find((tab) => {
      return tab.id === payload.tabId;
    });
    tab.openedInTab = payload.opened;
  },

  SET_CURRENT_NOTIFICATION: (
    state: { currentNotificationIndex: number },
    currentNotificationIndex: number
  ) => (state.currentNotificationIndex = currentNotificationIndex),

  SET_CURRENT_NOTIFICATION_INDEX_TO_LAST: (state: {
    currentNotificationIndex: number;
    notifications: any;
  }) => (state.currentNotificationIndex = state.notifications.length - 1),

  DEC_CURRENT_NOTIFICATION: (state: { currentNotificationIndex: number }) => {
    if (state.currentNotificationIndex > 0) state.currentNotificationIndex -= 1;
  },
  INC_CURRENT_NOTIFICATION: (state: {
    currentNotificationIndex: number;
    notifications: any;
  }) => {
    if (state.currentNotificationIndex < state.notifications.length - 1)
      return (state.currentNotificationIndex += 1);
  },
  SET_NOTIFICATIONS: (state: { notifications: any }, payload: any) =>
    (state.notifications = payload),
  APPEND_TO_NOTIFICATIONS: (
    state: { notifications: any },
    payload: INotificationObject
  ) => state.notifications.push(payload),
  SET_SHOW_NOTIFICATIONS_STATE: (
    state: { showNotifications: boolean },
    newState: boolean
  ) => (state.showNotifications = newState),
  SET_ADMIN_FORCE_RELOAD: (
    state: { adminForceReload: any },
    newState: { tab: string; state: boolean }
  ) => (state.adminForceReload[newState.tab] = newState.state),
  APPEND_TO_QUESTIONNAIRES: (
    state: { questionnaires: any; showQuestionnaires: boolean },
    payload: IQuestionnaireQuestionObject
  ) => {
    state.questionnaires.push(payload);
    if (state.questionnaires.length) state.showQuestionnaires = true;
  },

  REMOVE_QUESTIONNAIRE: (
    state: { questionnaires: any },
    global_question_id: Number
  ) =>
    (state.questionnaires = state.questionnaires.filter(
      (q) => q.global_question_id != global_question_id
    )),

  SET_SHOW_QUESTIONNAIRE_STATE: (
    state: { showQuestionnaires: boolean },
    newState: boolean
  ) => (state.showQuestionnaires = newState),

  SET_CURRENT_QUESTIONNAIRE_INDEX_TO_LAST: (state: {
    currentQuestionnaireIndex: number;
    questionnaires: any;
    showQuestionnaires: boolean;
  }) => {
    state.currentQuestionnaireIndex = state.questionnaires.length - 1;
    if (state.questionnaires.length) {
      state.showQuestionnaires = true;
    } else {
      state.showQuestionnaires = false;
    }
  },

  SET_QUESTIONNAIRES: (state: { questionnaires: any }, payload: any) =>
    (state.questionnaires = payload),
};
