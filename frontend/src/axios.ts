import axios from "axios";
import { store } from "@/store";

axios.defaults.baseURL = store.getters.getBackendUrl;

let token = store.getters.getJwt;
if (token) axios.defaults.headers.common["Authorization"] = "Bearer " + token;
