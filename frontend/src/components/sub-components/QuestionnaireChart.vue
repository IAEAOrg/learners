<template>
  <div class="questionnaireChart">
    <apexchart
      ref="donut"
      width="100%"
      height="100%"
      type="donut"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<script lang="ts">
import VueApexCharts from "vue3-apexcharts";
import axios from "axios";
import { generateColorScale } from "@/helpers";
import { store } from "@/store";

export default {
  name: "QuestionnaireChart",
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    questionnaireId: { type: String, require: true },
  },
  data: function () {
    return {
      chartOptions: {
        labels: [],
        colors: [
          "#398eb6",
          "#ffa200",
          "#ffd600",
          "#fff301",
          "#A6E227",
          "#94C134",
          "#34C28C",
        ],
        legend: {
          show: true,
          showForNullSeries: true,
          showForZeroSeries: true,
          position: "top",
          horizontalAlign: "left",
          floating: false,
          fontSize: "12px",
          fontFamily: "Rubik",
          fontWeight: 400,
          offsetX: 0,
          offsetY: 0,
          formatter: function (seriesName, opts) {
            return [
              seriesName,
              "(",
              opts.w.globals.series[opts.seriesIndex],
              ")",
            ];
          },
          markers: {
            width: 12,
            height: 12,
            radius: 2,
            offsetX: -5,
            offsetY: 1,
          },
          onItemClick: {
            toggleDataSeries: true,
          },
          onItemHover: {
            highlightDataSeries: true,
          },
        },
        animations: {
          enabled: true,
          easing: "easeinout",
          speed: 800,
          animateGradually: {
            enabled: true,
            delay: 150,
          },
          dynamicAnimation: {
            enabled: true,
            speed: 350,
          },
        },
        dataLabels: {
          enabled: true,
          formatter: (val, { seriesIndex, w }) => w.config.series[seriesIndex],
          textAnchor: "middle",
          distributed: false,
          offsetX: 0,
          offsetY: 0,
          style: {
            fontSize: "16px",
            fontFamily: "Rubik",
            fontWeight: "700",
            colors: ["#fff"],
          },
          background: {
            enabled: true,
            foreColor: "#000",
            padding: 6,
            borderRadius: 2,
            borderWidth: 0,
            opacity: 0.95,
            dropShadow: {
              enabled: true,
              top: 1,
              left: 1,
              blur: 1,
              color: "#000",
              opacity: 0.45,
            },
          },

          dropShadow: {
            enabled: false,
          },
        },
        stroke: {
          width: 0,
        },
        states: {
          normal: {
            filter: {
              type: "none",
              value: 0,
            },
          },
          hover: {
            filter: {
              type: "darken",
              value: 0.9,
            },
          },
          active: {
            allowMultipleDataPointsSelection: true,
            filter: {
              type: "darken",
              value: 0.9,
            },
          },
        },
        tooltip: {
          enabled: true,
          shared: true,
          followCursor: false,
          intersect: false,
          inverseOrder: false,
          fillSeriesColor: false,
          theme: "dark",
          style: {
            fontSize: "12px",
            fontFamily: undefined,
          },
          onDatasetHover: {
            highlightDataSeries: false,
          },
          marker: {
            show: true,
          },
          items: {
            display: "flex",
          },
          fixed: {
            enabled: false,
            position: "topRight",
            offsetX: 0,
            offsetY: 0,
          },
        },
      },
      series: [],
    };
  },
  computed: {
    forceReload() {
      // this.updateData(false);
      return store.getters.getAdminForceReload("questionnaire");
    },
  },
  methods: {
    async updateData(initRun = false) {
      const url = `questionnaires/questions/${this.questionnaireId}`;
      const { data } = await axios.get(url);

      // On mounted also set colors and labels
      if (initRun) {
        let colorScale = generateColorScale(data.labels.length);
        this.chartOptions = {
          ...this.chartOptions,
          ...{
            labels: data.labels,
            colors: colorScale,
          },
        };
      }

      // Update values
      this.series = data.results;
    },
  },
  async mounted() {
    await this.updateData(true);
  },
  watch: {
    forceReload: {
      handler() {
        this.updateData(false);
      },
      immediate: true,
    },
  },
};
</script>

<style lang="scss">
.questionnaireChart {
  height: 90%;
}
.apexcharts-legend {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
}
.questionnaireChart .vue-apexcharts .apexcharts-canvas {
  margin: 35px auto;
}
.questionnaireChart .vue-apexcharts .apexcharts-tooltip .apexcharts-active {
  background: #00000030 !important;
  color: white;
}
</style>
