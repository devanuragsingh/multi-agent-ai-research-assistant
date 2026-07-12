import { askQuestion } from "./api";

export async function sendMessage(query) {

  return await askQuestion(query);

}