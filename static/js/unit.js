import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const formElement = document.querySelector("[data-form]");
const tableElement = document.querySelector("[data-table]");
const errorAlert = document.querySelector("[data-alert]");
const createUnitTextElement = document.querySelector("[data-create-unit-text]");
const createUnitBtn = document.querySelector("[data-create-unit-btn]");
const modalCreateBtnClose = document.querySelector("[data-modal-create-btn-close]");


const getAllUnits = async () => {
    const resp = await axiosInstance.get(baseURL + '/units')
    resp.data.forEach(unit => {
        tableElement.appendChild(getUnitElement(unit))
    })
}

const getUnitElement = (unit) => {
    const row = document.createElement("tr")
    const unitID = document.createElement("td")
    unitID.innerHTML = unit.id
    const unitName = document.createElement("td")
    unitName.innerHTML = unit.unit
    row.appendChild(unitID)
    row.appendChild(unitName)
    return row
}

const init = async () => {
    const me = await user.getMe()

    if (me.is_admin) {
        formElement.addEventListener("submit", async (e) => {
            e.preventDefault()
            const unit = createUnitTextElement.value
            try {
                const resp = await axiosInstance.post(baseURL + '/units', {unit})
                tableElement.appendChild(getUnitElement(resp.data))
                modalCreateBtnClose.click()
                createUnitTextElement.value = ''
                closeErrorAlertIfThere()
            } catch (e) {
                openErrorAlert(e.response.data.detail, e)
            }
        })
    } else {
        createUnitBtn.remove()
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

const closeErrorAlertIfThere = () => {
    errorAlert.setAttribute("hidden", "")
}

init()
