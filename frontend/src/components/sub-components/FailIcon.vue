<template>
  <svg
    class="fail_checkmark"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 52 52"
  >
    <circle class="fail_checkmark__circle" cx="26" cy="26" r="25" fill="none" />
    <g class="fail_checkmark__cross">
      <path d="m15.07675,36.98865l21.84649,-21.9773" fill="none"></path>
      <path d="m36.98865,36.92324l-21.9773,-21.84649" fill="none"></path>
    </g>
  </svg>
</template>

<script lang="ts">
export default {
  name: "SuccessIcon",
};
</script>

<style>
.fail_checkmark__circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: #ab4646;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}
.fail_checkmark {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: inline-block;
  stroke-width: 4;
  stroke: #fff;
  stroke-miterlimit: 10;
  box-shadow: inset 0px 0px 0px #ab4646;
  animation: fail_fill 0.4s ease-in-out 0.4s forwards,
    scale 0.3s ease-in-out 0.9s both;
}
.fail_checkmark__cross {
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
@keyframes fail_fill {
  100% {
    box-shadow: inset 0px 0px 0px 30px #ab4646;
  }
}
</style>
