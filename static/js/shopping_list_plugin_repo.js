import {user as repoUser, axiosInstance as repoAxiosInstance} from "/static/js/repo.js";

const init = async () => {
    setTimeout(() => {
        const navLinksContainer = document.querySelector("[data-nav-links-container]");
        const unitLinkElement = document.createElement("a");
        unitLinkElement.className = "btn btn-warning mr-sm-2"
        unitLinkElement.innerText = "Units"
        unitLinkElement.href = "/plugin/shopping_list_plugin/unit"
        navLinksContainer.appendChild(unitLinkElement)
    },150)
}

init()

export const user = repoUser;
export const axiosInstance = repoAxiosInstance;
export const baseURL = '/plugin/shopping_list_plugin/api'