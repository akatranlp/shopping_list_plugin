import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const listContainerElement = document.querySelector("[data-list-container]");
const createListFormElement = document.querySelector("[data-create-list-form]");
const createListNameElement = document.querySelector("[data-create-list-name]");
const formEdit = document.querySelector("[data-form-edit]");
const editListName = document.querySelector("[data-edit-list-name]");
const editUUIDElement = document.querySelector("[data-edit-uuid]");
const errorAlert = document.querySelector("[data-alert]");

//Speichert die Referenz zum todoObject, welches gerade das Editieren Fenster geöffnet hat
let editShoppingListElement;

const getAllLists = async () => {
    listContainerElement.innerHTML = ''
    const resp = await axiosInstance.get(baseURL + '/shoppingLists')
    resp.data.forEach(list => {
        listContainerElement.appendChild(getListContainer(list))
    })
}

const getListContainer = (list) => {
    const listContainer = document.createElement('div')
    listContainer.className = "border border-primary rounded p-2"

    const listNameElement = document.createElement('h2')
    listNameElement.innerText = list.name
    listContainer.appendChild(listNameElement)

    const listChangeBtnElement = document.createElement('button')
    listChangeBtnElement.className = 'btn btn-warning mr-sm-2 mb-1'
    listChangeBtnElement.innerText = 'Umbenennen'
    listChangeBtnElement.setAttribute("data-toggle", "modal")
    listChangeBtnElement.setAttribute("data-target", "#editModal")
    listContainer.appendChild(listChangeBtnElement)

    listChangeBtnElement.addEventListener('click', async () => {
        editListName.value = list.name
        editUUIDElement.value = list.uuid
        editShoppingListElement = listContainer
    })

    const listDeleteBtnElement = document.createElement('button')
    listDeleteBtnElement.className = 'btn btn-danger text-white mr-sm-2'
    listDeleteBtnElement.innerText = 'Löschen'
    listContainer.appendChild(listDeleteBtnElement)

    listDeleteBtnElement.addEventListener('click', async () => {
        try {
            await axiosInstance.delete(`${baseURL}/shoppingLists/${list.uuid}`)
            closeErrorAlertIfThere()
            listContainer.remove()
        } catch (e) {
            openErrorAlert(e.response.data.detail, e)
        }
    })

    listContainer.appendChild(getListEntriesContainer(list))
    return listContainer
}


const getListEntriesContainer = (list) => {
    const listEntriesContainer = document.createElement('div');

    if (list.entries) {
        list.entries.forEach(entry => {
            listEntriesContainer.appendChild(getEntryContainer(list, entry, listEntriesContainer));
        })
    }

    const addEntryBtnElement = document.createElement('button')
    addEntryBtnElement.className = 'btn btn-primary text-white mr-sm-2'
    addEntryBtnElement.innerText = '+'
    listEntriesContainer.appendChild(addEntryBtnElement)

    addEntryBtnElement.addEventListener('click', async () => {
        const createEntryFormElement = document.createElement('form')
        createEntryFormElement.className = 'mb-2'
        createEntryFormElement.action = ''
        createEntryFormElement.method = 'post'

        const createEntryProductSelectElement = await getSelectProductContainer()
        createEntryFormElement.appendChild(createEntryProductSelectElement)

        const createEntryProductAmountElement = document.createElement('input')
        createEntryProductAmountElement.type = 'number'
        createEntryProductAmountElement.className = "m-1"
        createEntryFormElement.appendChild(createEntryProductAmountElement)

        const createEntryProductBtnElement = document.createElement('input')
        createEntryProductBtnElement.type = 'submit'
        createEntryProductBtnElement.value = 'Hinzufügen'
        createEntryProductBtnElement.className = 'btn btn-success text-white mr-sm-2'
        createEntryFormElement.appendChild(createEntryProductBtnElement)

        createEntryFormElement.addEventListener('submit', async e => {
            e.preventDefault()
            const product_uuid = createEntryProductSelectElement.value
            const amount = createEntryProductAmountElement.value

            try {
                const resp = await axiosInstance.post(`${baseURL}/shoppingLists/${list.uuid}/entries`, {
                    product_uuid,
                    amount
                })
                listEntriesContainer.insertBefore(getEntryContainer(list, resp.data), createEntryFormElement)
                closeErrorAlertIfThere()
                createEntryFormElement.remove()
            } catch (e) {
                openErrorAlert(e.response.data.detail, e)
            }
        })

        const createEntryProductBtnCancelElement = document.createElement('button')
        createEntryProductBtnCancelElement.innerText = '×'
        createEntryProductBtnCancelElement.className = 'btn btn-danger text-white mr-sm-2'
        createEntryFormElement.appendChild(createEntryProductBtnCancelElement)

        createEntryProductBtnCancelElement.addEventListener('click', () => {
            createEntryFormElement.remove()
        })

        listEntriesContainer.insertBefore(createEntryFormElement, addEntryBtnElement)
    })

    return listEntriesContainer
}

const getEntryContainer = (list, entry, listEntriesContainer) => {
    const entryElement = document.createElement('div')

    if (entry.product_pic_url) {
        const entryImgElement = document.createElement('img')
        entryImgElement.src = entry.product_pic_url
        entryImgElement.style.maxHeight = "80px"
        entryImgElement.style.maxWidth = "80px"
        entryElement.appendChild(entryImgElement)
    }

    const table = document.createElement("table")
    const thead = document.createElement("thead")
    const tbody = document.createElement("tbody")
    const tr = document.createElement("tr")

    const elementAmount = document.createElement('td')
    elementAmount.innerText = entry.amount
    tr.appendChild(elementAmount)

    const divide1 = document.createElement('td')
    tr.appendChild(divide1)

    const elementUnitType = document.createElement('td')
    elementUnitType.innerText = entry.product_unit_type
    tr.appendChild(elementUnitType)

    const divide2 = document.createElement('td')
    tr.appendChild(divide2)

    const elementName = document.createElement('td')
    elementName.innerText = entry.product_name
    tr.appendChild(elementName)

    table.appendChild(thead)
    table.appendChild(tbody)
    tbody.appendChild(tr)
    entryElement.appendChild(table)


    const entryChangeBtnElement = document.createElement('button')
    entryChangeBtnElement.className = 'btn btn-warning mr-sm-2'
    entryChangeBtnElement.innerText = 'Bearbeiten'
    entryElement.appendChild(entryChangeBtnElement)

    entryChangeBtnElement.addEventListener('click', async () => {
        const old_amount = elementAmount.value
        elementAmount.innerHTML = ''

        const changeFormElement = document.createElement('form')
        changeFormElement.action = ''
        changeFormElement.method = 'post'

        const inputAmountElement = document.createElement('input')
        inputAmountElement.type = 'number'
        changeFormElement.appendChild(inputAmountElement)

        const inputBtnElement = document.createElement('input')
        inputBtnElement.type = 'submit'
        inputBtnElement.value = 'Ändern'
        inputBtnElement.className = 'btn btn-success text-white mr-sm-2'
        changeFormElement.appendChild(inputBtnElement)

        const cancelBtnElement = document.createElement('button')
        cancelBtnElement.innerText = 'Abbrechen'
        cancelBtnElement.className = 'btn btn-danger text-white mr-sm-2'
        changeFormElement.appendChild(cancelBtnElement)

        changeFormElement.addEventListener('submit', async e => {
            e.preventDefault()
            try {
                const amount = inputAmountElement.value
                const resp = await axiosInstance.put(`${baseURL}/shoppingLists/${list.uuid}/entries/${entry.uuid}`, {amount})
                const newEntryContainer = getEntryContainer(list, resp.data)

                listEntriesContainer.insertBefore(newEntryContainer, entryElement)
                closeErrorAlertIfThere()
                entryElement.remove()
            } catch (e) {
                openErrorAlert(e.response.data.detail, e)
            }
        })

        cancelBtnElement.addEventListener('click', () => {
            elementAmount.innerHTML = old_amount
        })

        elementAmount.appendChild(changeFormElement)
    })

    const entryDeleteBtnElement = document.createElement('button')
    entryDeleteBtnElement.className = 'btn btn-danger text-white mr-sm-2'
    entryDeleteBtnElement.innerText = 'Entfernen'
    entryElement.appendChild(entryDeleteBtnElement)
    const brk = document.createElement("hr")
    entryElement.appendChild(brk)

    entryDeleteBtnElement.addEventListener('click', async () => {
        try {
            await axiosInstance.delete(`${baseURL}/shoppingLists/${list.uuid}/entries/${entry.uuid}`)
            closeErrorAlertIfThere()
            entryElement.remove()
        } catch (e) {
            openErrorAlert(e.response.data.detail, e)
        }
    })
    return entryElement
}

const getSelectProductContainer = async () => {
    const resp = await axiosInstance.get(baseURL + '/products')

    const selectElement = document.createElement('select')
    selectElement.className = "m-1"
    resp.data.forEach(product => {
        const optionElement = document.createElement('option')
        optionElement.textContent = `${product.name} in ${product.unit_type}`
        optionElement.value = product.uuid

        selectElement.appendChild(optionElement)
    })
    return selectElement
}


const init = async () => {
    await getAllLists()

    createListFormElement.addEventListener('submit', async e => {
        e.preventDefault()

        const name = createListNameElement.value
        try {
            const resp = await axiosInstance.post(`${baseURL}/shoppingLists`, {name})
            listContainerElement.appendChild(getListContainer(resp.data))
            createListNameElement.value = ''
            $('#createModal').modal('hide');
            closeErrorAlertIfThere()
        } catch (e) {
            openErrorAlert(e.response.data.detail, e)
        }
    })

    formEdit.addEventListener("submit", async (event) => {
        event.preventDefault()
        try {
            const name = editListName.value
            const uuid = editUUIDElement.value
            const resp = await axiosInstance.put(`${baseURL}/shoppingLists/${uuid}`, {name})
            const newListContainer = getListContainer(resp.data)
            editListName.value = ''
            $('#editModal').modal('hide');
            closeErrorAlertIfThere()
            editShoppingListElement.parentNode.replaceChild(newListContainer, editShoppingListElement)
        } catch (e) {
            console.log(e)
            openErrorAlert(e.response.data.detail, e)
        }
    })
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
