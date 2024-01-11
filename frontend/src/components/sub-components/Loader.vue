<template>
  <div :style="style" class="preloader-container">
    <v-progress-circular
      class="my-3 mx-auto"
      :color="spinnerColor"
      indeterminate
      width="2"
    ></v-progress-circular>

    <span class="text-center" v-html="displayedText"></span>
  </div>
</template>

<script lang="ts">
export default {
  name: "Loader",
  props: {
    loadingTxt: {
      type: String,
      require: false,
      default: "Requesting data ...",
    },
    width: {
      type: String,
      require: false,
      default: "100%",
    },
    timeout: {
      type: Number,
      require: false,
      default: "10",
    },
    errorTxt: {
      type: String,
      require: false,
      default: "Loading takes unusually long ... ",
    },
  },
  data() {
    return {
      spinnerColor: "secondary",
      displayError: false,
    };
  },
  computed: {
    style() {
      return "width: " + this.width;
    },
    displayedText() {
      if (this.displayError) return this.errorTxt;
      else return this.loadingTxt;
    },
  },
  methods: {
    showError() {
      if (this.errorTxt) {
        this.displayError = true;
        this.spinnerColor = "info";
      }
    },
  },
  mounted() {
    setTimeout(() => {
      // this.$emit("timeout");
      this.showError();
    }, this.timeout * 1000);
  },
};
</script>

<style lang="scss">
.preloader-container {
  display: flex;
  flex-direction: column;
  margin-top: 10%;
  margin-left: auto;
  margin-right: auto;

  span {
    font-size: 90%;
    br {
      margin-bottom: 10px;
    }
  }
}
</style>
