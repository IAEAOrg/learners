<template>
  <svg
    class="success-checkmark"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 52 52"
  >
    <circle
      class="success-checkmark-circle"
      cx="26"
      cy="26"
      r="25"
      fill="none"
    />
    <path
      class="success-checkmark-check"
      fill="none"
      d="M14.1 27.2l7.1 7.2 16.7-16.8"
    />
  </svg>
</template>

<script lang="ts">
export default {
  name: "SuccessIcon",
};
</script>

<style>
.success-checkmark {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: inline-block;
  stroke-width: 4;
  stroke: #fff;
  stroke-miterlimit: 10;
  box-shadow: inset 0px 0px 0px #4e792c;
  animation: success_fill 0.4s ease-in-out 0.4s forwards,
    scale 0.3s ease-in-out 0.9s both;
}

.success-checkmark-circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: #4e792c;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}
.success-checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}
@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}
@keyframes scale {
  0%,
  100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}
@keyframes success_fill {
  100% {
    box-shadow: inset 0px 0px 0px 30px #4e792c;
  }
}
</style>
