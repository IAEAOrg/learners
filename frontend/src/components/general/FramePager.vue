<template>
  <div
    class="content-container pager exercises justify-center flex-wrap align-content-center"
    :class="{ invisible: !(currentView === tab.id) }"
    v-show="currentView === tab.id"
  >
    <iframe
      v-if="!tab.openedInTab"
      :id="tab.id"
      :src="iframeSrc"
      loading="lazy"
      frameborder="0"
      noresize="noresize"
      style="height: 100vh"
      width="100%"
      @load="
        iframeLoaded = true;
        $emit('loaded');
      "
    ></iframe>

    <div class="fullscreen-center" v-else>
      <div class="resume-info">
        <h3>
          Resume VNC Client <i>{{ tab.id }}</i> here
        </h3>
        <p>
          The VNC Client is currently opened in a different browser-tab. <br />
          Only one instance can be run simultaneously.
        </p>
        <v-btn
          class="mt-5 px-3 resume-btn"
          variant="flat"
          color="secondary"
          v-ripple="false"
          @click="resumeHere"
        >
          Resume here
        </v-btn>
      </div>
    </div>

    <transition name="fade">
      <div class="fullscreen-center" v-if="!iframeLoaded && !tab.openedInTab">
        <loader
          width="20%"
          class="mx-auto"
          :loadingTxt="iframeLoadingText"
          :errorTxt="iframeErrorText"
          :timeout="10"
        />
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import { ITabObject } from "@/types";
import { store } from "@/store";
import { PropType } from "vue";
import Loader from "@/components/sub-components/Loader.vue";

export default {
  name: "FramePager",
  props: {
    tab: { type: Object as PropType<ITabObject>, require: true, default: null },
    currentView: { type: String, require: false, default: "" },
  },
  components: {
    Loader,
  },
  data() {
    return {
      iframeLoaded: false,
      iframeLoadingText: "",
      iframeErrorText: "",
    };
  },
  computed: {
    iframeSrc() {
      const jwt = store.getters.getJwt;
      let src =
        this.tab._type !== "client" && this.tab.id !== "drawio" && jwt
          ? `${this.tab.url}?jwt=${jwt}`
          : this.tab.url;

      // Add backend prefix
      if (!src.startsWith("http")) {
        src = `${store.getters.getBackendUrl}/${src}`;
      }
      return src;
    },
  },
  methods: {
    resumeHere() {
      const respIFrame = document.getElementById(this.tab.id);

      if (respIFrame) {
        respIFrame.setAttribute("src", this.tab.url);
      }
      store.dispatch("setOpendInTab", {
        tabId: this.tab.id,
        opened: false,
      });

      const referTab = window.open("", `${this.tab.id}_tab`);
      if (referTab) referTab.close();
    },
  },
  beforeMount() {
    if (this.tab._type === "client") {
      this.iframeLoadingText = "connecting to client ... ";
      this.iframeErrorText =
        "The connection takes longer than expected.<br>There may be a certificate error. In order to resolve this, please open the current tab using the icon in the lower left corner of the screen and accept the certificate.<br>If the error persists, please contact the exercise team.";
    } else {
      this.iframeLoadingText = "loading content ... ";
      this.iframeErrorText =
        "The connection takes longer than expected.<br>Check your internet connection or try refreshing the page.<br>If the error persists, please contact the exercise team.";
    }
  },
};
</script>

<style lang="scss">
.fullscreen-center {
  display: flex;
  height: 100%;
  width: 100%;
  background-color: #f6f6f6;
  position: absolute;
  top: 0px;
  left: 0px;
  flex-direction: column;
}

.error {
  margin: auto auto;
  max-width: 30%;

  & h1,
  h2,
  h3,
  h4,
  h5 {
    color: rgb(var(--v-theme-warning));
    margin-bottom: 0.8rem;
  }
}

.resume-info {
  margin: auto auto;
  max-width: 30%;

  & h1,
  h2,
  h3,
  h4,
  h5 {
    color: rgb(var(--v-theme-secondary));
    margin-bottom: 0.8rem;
  }
}

.fade-leave-active {
  transition: opacity 1s;
}
.fade-leave-to {
  opacity: 0;
}
</style>
