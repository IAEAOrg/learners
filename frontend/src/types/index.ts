export interface ITabObject {
  id: string;
  icon: string;
  tooltip: string;
  _type: string;
  url: string;
  index?: number;
  openedInTab?: boolean;
}

export interface IExerciseObject {
  id: number;
  exercise_type: string;
  page_title: string;
  root_weight: number;
  child_weight: number;
  local_exercise_id: number;
  global_exercise_id: string;
  exercise_name: string;
  parent_page_title: string;
  parent_weight: number;
  order_weight: number;
  completion_percentage: number;
}

export interface INotificationObject {
  event: string;
  _type: string;
  message: string;
  positions: Array<string>;
}

// event: string;
export interface IQuestionnaireQuestionObject {
  id: number;
  question: string;
  multiple: boolean;
  language: string;
  answers: Array<string>;
  global_question_id: string;
  global_questionnaire_id: string;
  page_title: string;
}
