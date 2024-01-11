<template>
  <EasyDataTable
    :headers="headers"
    :rows-per-page="50"
    :items="items"
    id="submission-table"
  >
    <template #loading>
      <loader />
    </template>

    <template #customize-headers>
      <thead class="customize-headers">
        <tr>
          <th
            v-for="topheader in getHeaders()"
            :colspan="topheader['span']"
            class="top-header"
            :class="{ sticky: topheader['text'] == 'user' }"
          >
            <span v-html="topheader['text']" v-if="topheader['text'] != 'user'">
            </span>
          </th>
        </tr>
        <tr>
          <th
            v-for="subheader in headers"
            class="sub-header"
            :class="{ sticky: subheader.text == 'user' }"
          >
            <span v-html="subheader.text"> </span>
          </th>
        </tr>
      </thead>
    </template>

    <template
      v-for="header in headers"
      v-slot:[getSlotName(header.value)]="data"
    >
      <div :key="header.value" :data="data" class="content-col">
        <success-icon
          class="clickable"
          v-if="data[header.value].completed === 1"
          @click="
            $emit('showDetails', {
              userId: data['user_id'],
              exerciseId: header.value,
            })
          "
        />

        <fail-icon
          class="clickable"
          v-else-if="
            data[header.value].completed === -1 &&
            data[header.value].executions.len > 0
          "
        />
        <span v-else-if="header.value === 'username'">{{
          data[header.value]
        }}</span>

        <span v-else> - </span>
      </div>
    </template>
  </EasyDataTable>
</template>

<script lang="ts">
import type { Header, Item } from "vue3-easy-data-table";
import SuccessIcon from "@/components/sub-components/SuccessIcon.vue";
import FailIcon from "@/components/sub-components/FailIcon.vue";
import Loader from "@/components/sub-components/Loader.vue";

export default {
  name: "DataTable",
  components: {
    SuccessIcon,
    FailIcon,
    Loader,
  },
  props: {
    headers: {
      type: Array<any>,
      require: true,
    },
    items: {
      type: Array<Item>,
      require: true,
    },
  },

  methods: {
    getSlotName(value) {
      return `item-${value}`;
    },

    getHeaders() {
      let topHeaders = [] as { text: string; span: number }[];
      for (const item of this.headers || []) {
        const i = topHeaders.findIndex((elem) => elem.text === item.parent);
        if (i > -1) topHeaders[i].span += 1;
        else topHeaders.push({ text: item.parent, span: 1 });
      }
      return topHeaders;
    },
  },
};
</script>

<style lang="scss">
.top-header {
  // background-color: rgba(var(--v-theme-secondary), 0.5);
  background-color: rgba(var(--v-theme-secondary), 0.1);
  border-right: 2px solid white;
  padding: 8px;
  white-space: nowrap;
  text-align: center;
  font-weight: normal;
  max-width: 120px;

  & span {
    display: inline-block; // This is what you're missing
    max-width: 90%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    padding-top: 8px;
  }
}

.sub-header {
  // background-color: rgba(var(--v-theme-secondary), 0.1);
  border-right: 2px solid white;
  padding: 8px;
  text-align: left;
  vertical-align: bottom;
  font-weight: normal;

  &:not(:first-child) span {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    padding-bottom: 5px;
    border-bottom: 2px solid #cdcdcd;
  }
}

#submission-table {
  border-radius: 4px;
  border: none;
}

#submission-table table {
  table-layout: auto !important;
  th,
  td,
  thead th,
  tbody td,
  tfoot td,
  tfoot th {
    width: auto !important;
  }

  td:not(:first-child) {
    text-align: center;
  }
}

.sticky {
  left: 0px;
  z-index: 1;
  position: sticky;
  background-color: white;
  box-shadow: 5px 3px 3px 0px #0000001f;
}
</style>
