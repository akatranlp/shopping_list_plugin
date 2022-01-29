import {user as repoUser, axiosInstance as repoAxiosInstance} from "/static/js/repo.js";

const navbar = document.querySelector("[data-plugin-navbar]");

const init = async () => {
    if (!navbar)
        return
    const currentUser = await repoUser.getMe()
    navbar.innerHTML = `
    <!-- Logindaten -->
    <div class="row pl-3">
        <a class="btn btn-primary text-white mr-sm-2" href="/">Startseite</a>
        <a class="btn btn-danger text-white mr-sm-2" href="/logout">Ausloggen</a>
        <a class="btn btn-secondary text-white mr-sm-2" href="/account">Einstellungen</a>
        <div>
            <p class="text-white text-justify m-2 mr-4">Eingeloggt als:
                <b class="text-white" id="loggedUser">${currentUser.username}</b>
            </p>
        </div>
    </div>
    <!-- Kalender und Adressbuch -->
    <div>
        <a class="btn btn-info mr-sm-2" href="/todo">ToDo-Liste</a>
        <a class="btn btn-success text-white mr-sm-2" href="/calendar">Kalender</a>
        <a class="btn btn-warning mr-sm-2" href="/contact">Adressbuch</a>
        <a class="btn btn-warning mr-sm-2" href="/plugin/shopping_list_plugin/unit">Units</a>
        <a class="btn btn-warning mr-sm-2" href="/plugin/shopping_list_plugin/productt">Products</a>
        <a class="btn btn-warning mr-sm-2" href="/plugin/shopping_list_plugin/list">Shopping Lists</a>
    </div>
    `
}

init()

export const user = repoUser;
export const axiosInstance = repoAxiosInstance;
export const baseURL = '/plugin/shopping_list_plugin/api'