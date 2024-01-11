<template>
  <div
    class="notification-container"
    :class="{
      animating: animate,
      submission:
        currentNotification?._type == 'submission' ||
        currentNotification?._type == 'content' ||
        currentNotification?._type == 'comment',
    }"
  >
    <div class="notification-controls">
      <v-tooltip
        offset="16px"
        location="top"
        text="previous"
        transition="fade-transition"
      >
        <template #activator="{ props }">
          <v-btn
            class="notification-actions"
            fab
            tile
            icon
            x-small
            elevation="0"
            theme="dark"
            v-ripple="false"
            v-bind="props"
            @click="showPreviousNotification()"
          >
            <SvgIcon name="chevron-left"
          /></v-btn>
        </template>
      </v-tooltip>

      <v-tooltip
        offset="16px"
        location="top"
        text="next"
        transition="fade-transition"
      >
        <template #activator="{ props }">
          <v-btn
            class="notification-actions"
            fab
            tile
            icon
            x-small
            elevation="0"
            theme="dark"
            v-ripple="false"
            v-bind="props"
            @click="showNextNotification()"
          >
            <SvgIcon name="chevron-right"
          /></v-btn>
        </template>
      </v-tooltip>
      <v-tooltip
        offset="16px"
        location="top"
        text="hide"
        transition="fade-transition"
      >
        <template #activator="{ props }">
          <v-btn
            class="notification-actions"
            fab
            tile
            icon
            x-small
            elevation="0"
            theme="dark"
            v-ripple="false"
            v-bind="props"
            @click="$emit('hide')"
          >
            <SvgIcon name="x-mark"
          /></v-btn>
        </template>
      </v-tooltip>
    </div>
    <div class="notification-grid">
      <SvgIcon
        name="check-circle"
        notification
        v-if="currentNotification?._type == 'submission'"
      />
      <SvgIcon
        name="chat-bubble-bottom-center-text"
        notification
        v-if="currentNotification?._type == 'comment'"
      />
      <div
        class="notification-content"
        v-html="currentNotification?.message"
      ></div>
    </div>
  </div>
</template>

<script lang="ts">
import SvgIcon from "@/components/dynamic-components/SvgIcon.vue";
import { store } from "@/store";

export default {
  name: "Notification",
  components: {
    SvgIcon,
  },
  data() {
    return {
      contentChanging: false,
      timeoutId: null as ReturnType<typeof setTimeout> | null,
    };
  },
  computed: {
    currentNotification() {
      let notifications = store.getters.getNotifications;
      const difference =
        store.getters.getNotificationsLength - notifications.length;

      if (notifications) {
        let index = store.getters.getCurrentNotificationIndex;
        index = Math.max(index - difference, 0);
        this.triggerAnimation();
        const currentNotification = notifications[index];

        // Clear the existing timeout
        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
        }

        if (
          currentNotification?._type == "submission" ||
          currentNotification?._type == "content" ||
          currentNotification?._type == "comment"
        ) {
          this.timeoutId = setTimeout(() => {
            this.$emit("hide");
          }, 5000);
        }

        return notifications[index];
      }
    },
    animate() {
      return this.contentChanging;
    },
  },
  methods: {
    showPreviousNotification() {
      store.dispatch("decCurrentNotification");
    },
    showNextNotification() {
      store.dispatch("incCurrentNotification");
    },
    triggerAnimation() {
      this.contentChanging = true;
      setTimeout(() => {
        this.contentChanging = false;
      }, 300);
    },
  },
  beforeDestroy() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  },
};
</script>

<style lang="scss">
.notification-container {
  position: absolute !important;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  flex-wrap: wrap;
  z-index: 99 !important;
  bottom: 14px !important;
  left: 74px !important;
  pointer-events: none;
  padding: 8px 8px 16px 16px;
  border-radius: 4px;
  min-width: 400px;
  max-width: 40%;

  &.animating {
    animation: fade-in 300ms ease;
  }

  &.submission {
    background-color: rgba(75, 138, 102, 0.9);
  }
  h1,
  h2,
  h3,
  h4,
  h5,
  p {
    color: white;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.v-btn.notification-actions {
  pointer-events: all;
  height: 12px;
  width: 28px;
  margin-left: 4px;
  background: none;

  & .v-btn__overlay,
  .v-btn__underlay {
    display: none;
  }
}
.notification-content {
  color: white;
  width: 100%;
}
.notification-controls {
  display: flex;
  justify-content: end;
  align-content: center;
  width: 100%;
  height: 30px;
  padding: 4px;
  border-radius: 4px;
}

.notification-grid {
  display: flex;
  width: 100%;
}
</style>
