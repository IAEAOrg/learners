export default {
  // General
  getLogo: (state) => state.logo,
  getJwt: (state) => state.jwt,
  getBackendUrl: (state) => state.backendUrl,
  getError: (state) => state.error,
  getTabs: (state) => state.tabs,
  getCurrentView: (state) => state.currentView || "",
  getTheme: (state) => state.theme,

  // Admin View
  getAdminForceReload: (state) => (tab) => {
    return state.adminForceReload[tab];
  },

  // Notifications
  getNotifications: (state) => {
    const filteredNotifications = state.notifications.filter((item) => {
      // Check positions argument
      return (
        item.positions.includes("all") ||
        item.positions.includes(state.currentView)
      );
    });
    return filteredNotifications;
  },
  getCurrentNotificationIndex: (state) => state.currentNotificationIndex || 0,
  getShowNotifications: (state) => state.showNotifications,
  getNotificationsLength: (state) => {
    if (state.notifications) return state.notifications.length;
    else return 0;
  },

  // Questionnaires
  getShowQuestionnaires: (state) => state.showQuestionnaires,
  getQuestionnaires: (state) => state.questionnaires || [],
  getCurrentQuestionnaireIndex: (state) => state.currentQuestionnaireIndex || 0,
  getQuestionnairesLength: (state) => {
    if (state.questionnaires) return state.questionnaires.length;
    else return 0;
  },
};
