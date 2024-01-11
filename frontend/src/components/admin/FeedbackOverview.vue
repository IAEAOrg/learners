<template>
  <div>
    <h2 class="mb-5">
      Feedback Overview

      <v-progress-circular
        class="mx-2 mb-1"
        color="grey"
        indeterminate
        :width="3"
        :size="18"
        v-show="loading"
      ></v-progress-circular>
    </h2>

    <template v-for="(comments, page) in commentsDict">
      <div>
        <h3 v-html="page" class="my-4"></h3>
        <div
          v-for="comment in comments"
          :key="typeof comment === 'object' ? comment.user : ''"
          class="details-card-row"
        >
          <div class="details-card-label">
            User:
            {{ typeof comment === "object" ? unescape(comment.user) : "" }}
          </div>
          <div class="details-card-input">
            {{ typeof comment === "object" ? comment.comment : "" }}
          </div>
        </div>
      </div>
    </template>

    <div v-if="Object.keys(commentsDict).length === 0" class="no-data">
      No data.
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";

import Loader from "@/components/sub-components/Loader.vue";
import { store } from "@/store";

interface Comment {
  user: string;
  comment: string;
}

interface CommentsDict {
  comments: Comment[];
  page: string;
}

export default {
  name: "FeedbackOverview",
  components: {
    Loader,
  },
  data() {
    return {
      commentsDict: {} as CommentsDict,
      loading: false,
    };
  },
  props: {
    currentTab: { type: String, require: false },
  },
  computed: {
    forceReload() {
      return store.getters.getAdminForceReload("feedback");
    },
  },
  methods: {
    unescape(_string) {
      return _string.replaceAll("_", " ");
    },
    async getDataFromServer() {
      this.loading = true;
      axios
        .get("comments")
        .then((res) => {
          this.commentsDict = res.data.comments;
        })
        .finally(() => {
          this.loading = false;
          store.dispatch("unsetAdminForceReload", "feedback");
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
.drop-down-group-title {
  font-weight: bold;
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
