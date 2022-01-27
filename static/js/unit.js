import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const unitContainerElement = document.querySelector("[data-unit-container]");

const createUnitFormElement = document.querySelector("[data-create-unit-form]");
const createUnitTextElement = document.querySelector("[data-create-unit-text]");


const getAllUnits = async () => {
    unitContainerElement.innerHTML = ''
    const resp = await axiosInstance.get(baseURL + '/units')
    resp.data.forEach(unit => {
        const unitElement = document.createElement('div');
        unitElement.className = "d-flex flex-row"

        {
            const tempElement = document.createElement('p')
            tempElement.innerText = unit.id
            unitElement.appendChild(tempElement)
        }
        {
            const tempElement = document.createElement('p')
            tempElement.innerText = unit.unit
            unitElement.appendChild(tempElement)
        }
        unitContainerElement.appendChild(unitElement);
    })
}


const init = async () => {
    const me = await user.getMe()

    if (me.is_admin) {
        createUnitFormElement.addEventListener('submit', async e => {
            e.preventDefault()
            const unit = createUnitTextElement.value
            if (!unit) {
                alert('Keine Eingabe gemacht!')
                return
            }
            try {
                await axiosInstance.post(baseURL + '/units', {unit})
                await getAllUnits()
            } catch (e) {
                alert(e.response.data.detail)
            }
        })
    } else {
        createUnitFormElement.remove()
    }

    await getAllUnits()
}

init()
