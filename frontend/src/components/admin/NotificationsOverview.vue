<template>
  <div>
    <h2 class="mb-3">
      Notifications Overview

      <v-progress-circular
        class="mx-2 mb-1"
        color="grey"
        indeterminate
        :width="3"
        :size="18"
        v-show="loading"
      ></v-progress-circular>
    </h2>

    <div>
      <v-card class="pa-5 my-5">
        <h3>Choose a predefined Notification</h3>
        <p>
          Click on one of the predefined notifications to use it as message
          content.
        </p>

        <v-container class="pt-5 pb-0">
          <v-row class="text-grey d-none d-sm-flex pb-3">
            <v-col cols="2">Title</v-col>
            <v-col cols="10">Message</v-col>
          </v-row>

          <template
            v-for="(notification, index) in initialNotifications"
            :key="index"
          >
            <div>
              <v-hover>
                <template v-slot="{ isHovering, props }">
                  <v-row
                    class="initial-notifications-list-item mb-3"
                    v-bind="props"
                  >
                    <v-col cols="2">{{ notification.title }}</v-col>
                    <v-col cols="10">{{ notification.msg }}</v-col>

                    <div
                      v-show="isHovering"
                      class="list-hover-container align-center justify-center"
                    >
                      <v-btn
                        color="secondary"
                        @click="message = notification.msg"
                      >
                        use
                      </v-btn>
                    </div>
                  </v-row>
                </template>
              </v-hover>
            </div>
          </template>
        </v-container>
      </v-card>

      <v-card class="pa-5">
        <h3>Create a new Notification</h3>
        <p>
          Select the user to whom the notification is to be sent. Multiple and
          group selection is possible (duplicate selections will be ignored).
          The position can be used to select the view on which the notification
          is to be displayed.
        </p>

        <div class="mt-5">
          <v-form v-model="form" @submit.prevent="submitHandler">
            <v-container>
              <v-row>
                <v-col cols="8" class="pl-0 pt-0">
                  <v-autocomplete
                    class="autocomplete-inputs"
                    v-model="recipients"
                    :items="resipientsOptions"
                    chips
                    closable-chips
                    label="Recipients"
                    item-title="name"
                    item-value="value"
                    multiple
                    clearable
                    variant="outlined"
                  >
                    <template v-slot:chip="{ props, item }">
                      <v-chip v-bind="props" :text="item.raw.name"></v-chip>
                    </template>

                    <template v-slot:item="{ props, item, index }">
                      <div
                        v-if="props.title && props.title['header']"
                        class="drop-down-group-title pl-5 pt-5 pb-3 ml-1"
                      >
                        {{ props.title["header"] }}
                      </div>
                      <div
                        v-else-if="props.title && props.title['divider']"
                        class="drop-down-divider pt-5 pb-2"
                      >
                        <hr />
                      </div>
                      <v-list-item v-else v-bind="props">
                        <template v-slot:default="{ isActive }">
                          <v-list-item-action>
                            <v-checkbox
                              :modelValue="isActive"
                              color="secondary"
                            ></v-checkbox>
                          </v-list-item-action>
                        </template>
                      </v-list-item>
                    </template>
                  </v-autocomplete>
                </v-col>
                <v-col cols="4" class="pa-0">
                  <v-select
                    class="autocomplete-inputs"
                    label="Position"
                    v-model="positions"
                    :items="positionOptions"
                    multiple
                    clearable
                    closable-chips
                    variant="outlined"
                    chips
                  ></v-select>
                </v-col>
                <v-col cols="12" class="pa-0">
                  <v-textarea
                    label="Message"
                    id="message-textarea"
                    variant="outlined"
                    :model-value="message"
                    @input="message = $event.target.value"
                  >
                  </v-textarea>
                </v-col>
                <v-col cols="12" class="pa-0 d-flex justify-end">
                  <v-btn
                    :disabled="!form"
                    color="success"
                    size="large"
                    type="submit"
                    variant="elevated"
                  >
                    submit
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </div>
      </v-card>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";

import Loader from "@/components/sub-components/Loader.vue";
import { store } from "@/store";

interface Notification {
  title: string;
  msg: string;
}

export default {
  name: "NotificationsOverview",
  components: {
    Loader,
  },
  data() {
    return {
      initialNotifications: [] as Array<Notification>,
      // Loader conditions
      notificationLoading: false,
      usersLoading: false,
      groupsLoading: false,
      // Form
      form: false,
      // Recipients
      recipients: [],
      resipientsUsersOptions: <any>[],
      resipientsGroupsOptions: <any>[],
      // resipientsOptions: <any>[],

      // Positions
      positions: ["all"],
      positionOptions: [
        "documentation",
        "injects",
        "exercises",
        "clients",
        "all",
      ],
      // Message
      message: "",
    };
  },
  props: {
    currentTab: { type: String, require: false },
  },
  computed: {
    loading() {
      return (
        this.usersLoading || this.groupsLoading || this.notificationLoading
      );
    },
    forceReload() {
      return store.getters.getAdminForceReload("notifications");
    },
    resipientsOptions() {
      return [...this.resipientsUsersOptions, ...this.resipientsGroupsOptions];
    },
  },
  methods: {
    async submitHandler() {
      if (!this.form) return;

      const recipients = this.recipients.flatMap((num) => num);
      const dedubRecipients = [...new Set(recipients)];

      const response = await axios.post("notifications", {
        recipients: dedubRecipients,
        message: this.message,
        positions: this.positions,
      });
    },
    async getDataFromServer() {
      this.notificationLoading = true;
      axios
        .get("setup/notifications")
        .then((res) => {
          this.initialNotifications = res.data.initialNotifications;
        })
        .finally(() => {
          store.dispatch("unsetAdminForceReload", "notifications");
          this.notificationLoading = false;
        });

      this.usersLoading = true;
      let resipientsOptions = <any>[];
      let UsersOptions = <any>[];
      axios
        .get("users")
        .then((res) => {
          const users = res.data.users;
          UsersOptions.push({
            header: "Users",
          });
          users.forEach((user) => {
            UsersOptions.push({
              name: user.name,
              value: user.id,
            });
          });
          UsersOptions.push({
            divider: true,
          });
        })
        .finally(() => {
          this.resipientsUsersOptions = UsersOptions;
          this.usersLoading = false;
        });

      this.groupsLoading = true;
      let GroupsOptions = <any>[];
      axios
        .get("usergroups")
        .then((res) => {
          const groups = res.data.groups;
          GroupsOptions.push({
            header: "Groups",
          });
          groups.forEach((group) => {
            GroupsOptions.push({
              name: group.name,
              value: group.ids,
            });
          });
          GroupsOptions.push({
            divider: true,
          });
        })
        .finally(() => {
          this.resipientsGroupsOptions = GroupsOptions;
          this.groupsLoading = false;
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
