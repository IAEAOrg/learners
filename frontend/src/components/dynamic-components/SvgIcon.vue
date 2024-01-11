<template>
  <div
    :class="{
      'sidebar-hero-icon': sidebar,
      'content-hero-icon': !sidebar,
      'notification-hero-icon': notification,
      'inline': inline,
      clickable: clickable,
    }"
    class="hero-icon"
  >
    <component :is="dynamicComponent" />
  </div>
</template>

<script lang="ts">
import { defineAsyncComponent } from "vue";

export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    clickable: {
      type: Boolean,
      required: false,
      default: false,
    },
    sidebar: {
      type: Boolean,
      required: false,
      default: false,
    },
    notification: {
      type: Boolean,
      required: false,
      default: false,
    },
    inline: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  computed: {
    dynamicComponent() {
      const name = this.name;
      return defineAsyncComponent(() => import(`./icons/${name}.svg`));
    },
  },
};
</script>

<style lang="scss">
.hero-icon {
  display: flex;
  justify-content: center;
  align-content: center;
}

.hero-icon.sidebar-hero-icon {
  width: 24px;
}

.hero-icon.content-hero-icon {
  width: 22px;
}

.hero-icon.notification-hero-icon {
  width: 40px;
  margin-right: 20px;
  svg {
    color: white;
  }
}

.inline {
  float: left;
  margin-right: 0.8rem;
  align-items: end;
}
</style>
