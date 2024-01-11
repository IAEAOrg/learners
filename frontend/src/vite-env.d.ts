/// <reference types="vite/client" />

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
declare module "*.yaml" {
  const value: any;
  export default value;
}
declare module "*.yml" {
  const value: any;
  export default value;
}
