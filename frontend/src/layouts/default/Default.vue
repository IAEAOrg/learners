<template>
  <v-container fluid class="pa-0">
    <v-navigation-drawer
      model-value
      rail
      permanent
      color="primary"
      rail-width="60"
      style="border: none"
    >
      <sidebar :tabs="tabs" :currentView="currentView" :loaded="loaded" />
    </v-navigation-drawer>

    <v-main>
      <router-view :tabs="tabs" :currentView="currentView" />
    </v-main>
  </v-container>
</template>

<script lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { store } from "@/store";

export default {
  name: "DefaultLayout",
  components: {
    Sidebar,
  },
  data() {
    return {
      loaded: false,
      currentView: "",
    };
  },
  props: {
    routeHash: {
      type: String,
      required: false,
      default: "",
    },
  },
  computed: {
    tabs: () => store.getters.getTabs,
  },
  mounted() {
    this.loaded = true;
    store.dispatch("reinitBackendUrl");
    store.dispatch("getTabsFromServer");
  },
  watch: {
    "$route.hash": {
      handler(new_state, old_state) {
        const tabs = store.getters.getTabs;

        // Set new view_id when routehash, currentView or query changed
        let view_id = new_state
          ? new_state.substring(1)
          : this.routeHash || store.getters.getCurrentView || "";

        // Verify the id exists in tabs, if not choose the first tab
        if (tabs.length && !tabs.some((tab) => tab.id === view_id)) {
          view_id = tabs[0].id;
        }

        this.currentView = view_id;
        store.dispatch("setCurrentView", view_id);
      },
      immediate: true,
    },
  },
};
</script>
