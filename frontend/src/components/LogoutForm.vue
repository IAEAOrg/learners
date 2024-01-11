<template>
  <div>
    <v-row class="align-center justify-center" style="height: 100vh">
      <v-col>
        <v-row>
          <v-col offset="1">
            <h1 class="main-title text-primary">Logout</h1>
          </v-col>
        </v-row>

        <v-row>
          <v-col offset="1">
            <div class="welcomeText">
              We recommend completing any pending exercises, quizzes, or
              assignments and reviewing your course materials. Remember, logging
              out will end your current session, and you'll need to log in again
              to continue your learning journey. If you have any questions or
              need support, don't hesitate to reach out to our dedicated support
              team.
            </div>
          </v-col>
        </v-row>

        <v-row class="align-start justify-start">
          <v-col offset="1" xl="3" lg="4" md="6" cols="10">
            <v-form @submit.prevent="submitHandler">
              <v-btn
                color="success"
                size="large"
                type="submit"
                variant="elevated"
              >
                logout
              </v-btn>
            </v-form>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { store } from "@/store";
import axios from "axios";

export default {
  name: "LogoutForm",
  methods: {
    async submitHandler() {
      const response = await axios.post("logout");

      const logged_in = response.data.logged_in;
      if (!logged_in) {
        store.dispatch("unsetJwt");
        axios.defaults.headers.common["Authorization"] = "";
        this.$router.push("/login");
      }
    },
  },
  async beforeMount() {
    await axios.get("setup/login");
  },
};
</script>
