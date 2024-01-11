import { store } from "@/store";
import {
  INotificationObject,
  ITabObject,
  IQuestionnaireQuestionObject,
} from "@/types/index";
import axios from "axios";

export function initializeBackendUrl() {
  let backendUrl =
    import.meta.env.VITE_BACKEND ||
    (import.meta.env.VITE_BASEURL ? `${import.meta.env.VITE_BASEURL}/api` : "");

  backendUrl = !backendUrl.startsWith("http")
    ? `${window.location.origin}/${backendUrl}`.replace(/([^:])\/{2,}/g, "$1/")
    : backendUrl;

  return backendUrl;
}

export const generateTabs = (tabs, response) => {
  const newtabs = response.tabs;
  tabs = (newtabs || []).map((newtab) => {
    const i = tabs.findIndex((_element) => _element.id === newtab.id);
    if (i > -1) {
      return {
        ...tabs[i],
        ...newtab,
      };
    } else {
      return <ITabObject>{
        id: `${newtab?.id}`,
        icon: `${newtab?.icon}`,
        tooltip: `${newtab?.tooltip}`,
        _type: `${newtab?._type}`,
        url: `${newtab?.url}`,
        index: newtab?.index,
      };
    }
  });

  const currentView = response.landingpage;

  return { genTabs: tabs, genCurrentView: currentView };
};

export const extractNotifications = (responseData) => {
  let newNotifications;

  if (Array.isArray(responseData)) {
    newNotifications = (responseData || []).map((newNotification) => {
      return <INotificationObject>{
        event: `${newNotification?.event}`,
        _type: `${newNotification?._type}`,
        message: `${newNotification?.message}`,
        positions: newNotification?.positions,
      };
    });
  } else {
    newNotifications = <INotificationObject>{
      event: `${JSON.parse(responseData)?.event}`,
      _type: `${JSON.parse(responseData)?._type}`,
      message: `${JSON.parse(responseData)?.message}`,
      positions: JSON.parse(responseData)?.positions,
    };
  }

  return newNotifications;
};

export const extractQuestionnaires = (responseData) => {
  let newQuestionnaires;

  if (Array.isArray(responseData)) {
    newQuestionnaires = (responseData || []).map((newQuestionnaire) => {
      // event: `${newQuestionnaire?.event}`,
      return <IQuestionnaireQuestionObject>{
        id: newQuestionnaire?.id,
        question: newQuestionnaire?.question,
        multiple: newQuestionnaire?.multiple,
        answers: JSON.parse(newQuestionnaire?.answer_options),
        language: newQuestionnaire?.language,
        global_question_id: newQuestionnaire?.global_question_id,
        global_questionnaire_id: newQuestionnaire?.global_questionnaire_id,
        page_title: newQuestionnaire?.page_title,
      };
    });
  } else {
    newQuestionnaires = <IQuestionnaireQuestionObject>{
      id: (JSON.parse(responseData)?.question).id,
      question: (JSON.parse(responseData)?.question).question,
      multiple: (JSON.parse(responseData)?.question).multiple,
      answers: JSON.parse((JSON.parse(responseData)?.question).answer_options),
      language: (JSON.parse(responseData)?.question).language,
      global_question_id:
        (JSON.parse(responseData)?.question).global_question_id,
      global_questionnaire_id:
        (JSON.parse(responseData)?.question).global_questionnaire_id,
      page_title: (JSON.parse(responseData)?.question).page_title,
    };
  }

  return newQuestionnaires;
};

export const httpErrorHandler = (error) => {
  if (error === null) throw new Error("Unrecoverable error!! Error is null!");
  if (axios.isAxiosError(error)) {
    //here we have a type guard check, error inside this if will be treated as AxiosError
    const response = error?.response;
    const request = error?.request;
    const config = error?.config; //here we have access the config used to make the api call (we can make a retry using this conf)

    if (error.code === "ERR_NETWORK") {
      store.dispatch("setError", "connection problems...");
    } else if (error.code === "ERR_CANCELED") {
      store.dispatch("setError", "connection canceled...");
    }
    if (response) {
      //The request was made and the server responded with a status code that falls out of the range of 2xx the http status code mentioned above
      const statusCode = response?.status;
      if (statusCode === 404) {
        store.dispatch(
          "setError",
          "The requested resource does not exist or has been deleted"
        );
      } else if (statusCode === 401) {
        store.dispatch("setError", "Please login to access this resource");
        //redirect user to login
      }
    } else if (request) {
      //The request was made but no response was received, `error.request` is an instance of XMLHttpRequest in the browser and an instance of http.ClientRequest in Node.js
    }
  }
  //Something happened in setting up the request and triggered an Error
  console.error(error.message);
  // store.dispatch("setError", "Unknown error");
};

export const setStyles = async (root) => {
  // Get styles from server
  const response = await axios.get("setup/styles");
  store.dispatch("setLogo", response.data.logo);
  store.dispatch("setTheme", response.data.theme);

  const colors = response?.data.theme;
  for (const colorName in colors) {
    root.$vuetify.theme.themes.light.colors[colorName] = colors[colorName];
  }
};

export const generateColorScale = (steps: number): string[] => {
  const styles = store.getters.getTheme;
  const startColor = styles.secondary;
  const endColor = "#e8e8e8";

  // Parse the starting and ending colors
  const start = hexToRgb(startColor);
  const end = hexToRgb(endColor);

  // Calculate the step sizes for each color channel
  const stepSize = {
    red: (end.red - start.red) / (steps - 1),
    green: (end.green - start.green) / (steps - 1),
    blue: (end.blue - start.blue) / (steps - 1),
  };

  // Generate the color scale
  const colors: string[] = [];
  for (let i = 0; i < steps; i++) {
    const red = Math.round(start.red + stepSize.red * i);
    const green = Math.round(start.green + stepSize.green * i);
    const blue = Math.round(start.blue + stepSize.blue * i);
    colors.push(rgbToHex(red, green, blue));
  }

  return colors;
};

// Helper functions to convert between hex and RGB colors
function hexToRgb(hex: string): { red: number; green: number; blue: number } {
  const r = parseInt(hex.substring(1, 3), 16);
  const g = parseInt(hex.substring(3, 5), 16);
  const b = parseInt(hex.substring(5, 7), 16);
  return { red: r, green: g, blue: b };
}

function rgbToHex(r: number, g: number, b: number): string {
  const hex = [r, g, b]
    .map((c) => {
      const hex = c.toString(16);
      return hex.length === 1 ? "0" + hex : hex;
    })
    .join("");
  return "#" + hex;
}

export const sortTree = (tree: any) => {
  // Convert the tree to an array of objects
  const treeArray = Object.entries(tree).map(([key, value]) => ({
    key,
    ...(value as any),
  }));

  // Sort the array based on 'weight' or 'title'
  treeArray.sort((a, b) => {
    if (
      a.params &&
      JSON.parse(a.params)["weight"] &&
      b.params &&
      JSON.parse(b.params)["weight"]
    ) {
      return (
        JSON.parse(a.params)["weight"] - JSON.parse(b.params)["weight"] ||
        JSON.parse(a.params)["title"].localeCompare(
          JSON.parse(b.params)["title"]
        )
      );
    } else {
      return JSON.parse(a.params)["title"].localeCompare(
        JSON.parse(b.params)["title"]
      );
    }
  });

  // Recursively sort child nodes
  treeArray.forEach((node) => {
    if (Object.keys(node.childs).length > 0) {
      node.childs = sortTree(node.childs);
    }
  });

  // Convert the sorted array back to an object
  const sortedTree = {};
  treeArray.forEach((node) => {
    const { key, ...rest } = node;
    sortedTree[key] = rest;
  });

  return sortedTree;
};

export const initVisibility = async (iframe_list) => {
  const visibilityData = await axios.get("/pages");
  const pages = visibilityData.data.pages;

  iframe_list.forEach((_iframe) => {
    const functionCall = {
      function: "visibility",
      data: pages,
    };

    try {
      _iframe.contentWindow.postMessage(
        functionCall,
        new URL(_iframe.src).origin
      );
    } catch (error) {
      console.log(error);
    }
  });
};

export const sseHandlerContent = (ctx, event) => {
  // Broadcast to all iFrames
  ctx.iframes.forEach((_iframe) => {
    const functionCall = {
      function: "visibility",
      data: JSON.parse(event.data).message,
    };
    _iframe.contentWindow.postMessage(
      functionCall,
      new URL(_iframe.src).origin
    );
  });
};

export const sseHandlerNotification = (ctx, event) => {
  ctx.notificationClosed = false;
  const notification = extractNotifications(event.data);

  store.dispatch("appendToNotifications", notification);
  store.dispatch("setCurrentNotificationToLast");

  switch (notification._type) {
    case "submission":
      store.dispatch("setAdminForceReload", "submissions");
      break;
    case "comment":
      store.dispatch("setAdminForceReload", "feedback");
      break;
    default:
    //
  }
};

export const sseHandlerQuestionnaire = (ctx, event) => {
  ctx.questionnaireClosed = false;
  const newQuestionnaire = extractQuestionnaires(event.data);
  // Store actions
  store.dispatch("appendToQuestionnaires", newQuestionnaire);
  store.dispatch("setCurrentQuestionnaireToLast");
  store.dispatch("setAdminForceReload", "questionnaire");
};

export const sseHandlerQuestionnaireSubmission = (ctx, event) => {
  store.dispatch("setAdminForceReload", "questionnaire");
};
export const initSSE = (ctx) => {
  ctx.evtSource.addEventListener("content", (event) =>
    sseHandlerContent(ctx, event)
  );
  ctx.evtSource.addEventListener("notification", (event) =>
    sseHandlerNotification(ctx, event)
  );
  ctx.evtSource.addEventListener("questionnaire", (event) =>
    sseHandlerQuestionnaire(ctx, event)
  );
  ctx.evtSource.addEventListener("questionnaireSubmission", (event) =>
    sseHandlerQuestionnaireSubmission(ctx, event)
  );

  ctx.evtSource.onerror = (error) => {
    console.log("Connection to SSE source lost. ", error);
    ctx.evtSource.removeEventListener("content", (event) =>
      sseHandlerContent(ctx, event)
    );
    ctx.evtSource.removeEventListener("notification", (event) =>
      sseHandlerNotification(ctx, event)
    );
    ctx.evtSource.removeEventListener("questionnaire", (event) =>
      sseHandlerQuestionnaire(ctx, event)
    );
    ctx.evtSource.removeEventListener("questionnaireSubmission", (event) =>
      sseHandlerQuestionnaireSubmission(ctx, event)
    );
    ctx.evtSource = null;
    ctx.startSseSession(ctx);
  };
};
