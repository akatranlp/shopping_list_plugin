import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const formElement = document.querySelector("[data-form]")
const tableElement = document.querySelector("[data-table]")
const errorAlert = document.querySelector("[data-alert]");
const createUnitFormElement = document.querySelector("[data-create-unit-form]");
const createUnitTextElement = document.querySelector("[data-create-unit-text]");


const getAllUnits = async () => {
    const resp = await axiosInstance.get(baseURL + '/units')
    resp.data.forEach(unit => {
        const row = document.createElement("tr")
        const unitID = document.createElement("td")
        unitID.innerHTML = unit.id
        const unitName = document.createElement("td")
        unitName.innerHTML = unit.unit

        tableElement.appendChild(row)
        tableElement.appendChild(unitID)
        tableElement.appendChild(unitName)
    })
}

const init = async () => {
    const me = await user.getMe()

    if (me.is_admin) {
        createUnitFormElement.addEventListener('click', async (e) => {
            e.preventDefault()
            formElement.addEventListener("submit", async (e) => {
                e.preventDefault()
                const unit = createUnitTextElement.value
                try {
                    await axiosInstance.post(baseURL + '/units', {unit})
                    await getAllUnits()
                } catch (e) {
                    openErrorAlert(e.response.data.detail, e)
                }
            })

        })
    } else {
        createUnitFormElement.remove()
    }

    await getAllUnits()
}

const openErrorAlert = (text, e) => {
    errorAlert.className = "alert alert-danger p-1"
    if (e !== null) {
        errorAlert.innerText = text + ": " + e.response.status + " - " + e.response.statusText
    } else {
        errorAlert.innerText = text
    }
    errorAlert.removeAttribute("hidden")
}

init()
