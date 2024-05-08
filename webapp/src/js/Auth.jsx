import { browser } from '$app/environment';
import { writable } from 'svelte/store';

class UserInfo {
    constructor(username, id) {
        this.username = username;
        this.id = id;
    }

    isLoggedIn() {
        return this.username !== "" && this.username !== null;
    }
}

function getCookie(name) {
  return document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || null;
}

function getUserInfo() {
    if (!browser)
        return writable(null);

    const { subscribe, set, update } = writable(null);

    const username = localStorage.getItem("username");
    const u = (username === "")
      ? new UserInfo("", "")
      : new UserInfo(username, localStorage.getItem("userID"));
    set(u);

    return {
        subscribe,
        login: (username, id) => {
            const u = new UserInfo(username, id);
            localStorage.setItem("username", username);
            localStorage.setItem("userID", id);
            set(u);
        },
        logout: (username, id) => {
            localStorage.setItem("username", "");
            localStorage.setItem("userID", "");
            set(new UserInfo("", ""));
        },
    }
}

export const userInfo = getUserInfo();

export function fetcher(url, settings = null) {
  const csrftoken = getCookie("csrftoken");
  if (csrftoken === null)
    return fetch(url, settings);

  if (settings === null)
    settings = {};

  if (settings.headers === null)
    settings.headers = {};

  settings.headers["X-CSRFToken"] = csrftoken;
  return fetch(url, settings);
}
