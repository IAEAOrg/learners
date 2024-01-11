import { createStore } from "vuex";
import VuexPersister from "vuex-persister";

import getters from "./getters";
import actions from "./actions";
import mutations from "./mutations";
import state from "./state";

const vuexPersister = new VuexPersister({
  overwrite: true,
  storage: sessionStorage,
});

export const store = createStore({
  state,
  mutations,
  actions,
  getters,
  plugins: [vuexPersister.persist],
});
