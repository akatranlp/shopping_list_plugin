import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const listContainerElement = document.querySelector("[data-list-container]");
const createListFormElement = document.querySelector("[data-create-list-form]");
const createListNameElement = document.querySelector("[data-create-list-name]");
const formEdit = document.querySelector("[data-form-edit]")
const editListName = document.querySelector("[data-edit-list-name]")

const getAllLists = async () => {
    listContainerElement.innerHTML = ''
    const resp = await axiosInstance.get(baseURL + '/shoppingLists')
    resp.data.forEach(list => {
        const listContainer = document.createElement('div')
        listContainer.className = "border border-primary rounded-3"

        const listNameElement = document.createElement('div')
        listNameElement.innerText = list.name
        listContainer.appendChild(listNameElement)

        const listChangeBtnElement = document.createElement('button')
        listChangeBtnElement.className = 'btn btn-success text-white mr-sm-2'
        listChangeBtnElement.innerText = 'Umbenennen'
        listChangeBtnElement.setAttribute("data-toggle", "modal")
        listChangeBtnElement.setAttribute("data-target", "#editModal")
        listContainer.appendChild(listChangeBtnElement)

        listChangeBtnElement.addEventListener('click', async () => {

            editListName.value = list.name

            formEdit.addEventListener("submit", async (event) => {
                event.preventDefault()
                try {
                    const name = editListName.value
                    await axiosInstance.put(`${baseURL}/shoppingLists/${list.uuid}`, {name})
                    window.location = "/plugin/shopping_list_plugin/list"
                } catch (e) {
                    alert(e)
                    window.location = "/plugin/shopping_list_plugin/list"
                }
            })
        })

        const listDeleteBtnElement = document.createElement('button')
        listDeleteBtnElement.className = 'btn btn-danger text-white mr-sm-2'
        listDeleteBtnElement.innerText = 'Löschen'
        listContainer.appendChild(listDeleteBtnElement)

        listDeleteBtnElement.addEventListener('click', async () => {
            try {
                await axiosInstance.delete(`${baseURL}/shoppingLists/${list.uuid}`)
                await getAllLists()
            } catch (e) {
                alert(e)
                await getAllLists()
            }
        })

        listContainer.appendChild(getListEntriesContainer(list))

        listContainerElement.appendChild(listContainer)
    })
}


const getListEntriesContainer = (list) => {
    const listEntriesContainer = document.createElement('div');

    list.entries.forEach(entry => {
        listEntriesContainer.appendChild(getEntryContainer(list, entry));
    })

    const addEntryBtnElement = document.createElement('button')
    addEntryBtnElement.className = 'btn btn-primary text-white mr-sm-2'
    addEntryBtnElement.innerText = '+'
    listEntriesContainer.appendChild(addEntryBtnElement)

    addEntryBtnElement.addEventListener('click', async () => {
        const createEntryFormElement = document.createElement('form')
        createEntryFormElement.action = ''
        createEntryFormElement.method = 'post'

        const createEntryProductSelectElement = await getSelectProductContainer()
        createEntryFormElement.appendChild(createEntryProductSelectElement)

        const createEntryProductAmountElement = document.createElement('input')
        createEntryProductAmountElement.type = 'number'
        createEntryFormElement.appendChild(createEntryProductAmountElement)

        const createEntryProductBtnElement = document.createElement('input')
        createEntryProductBtnElement.type = 'submit'
        createEntryProductBtnElement.value = 'Add Entry'
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
                createEntryFormElement.remove()
            } catch (e) {
                alert(e)
                window.location = "/plugin/shopping_list_plugin/list"
            }
        })

        const createEntryProductBtnCancelElement = document.createElement('button')
        createEntryProductBtnCancelElement.innerText = 'Cancel'
        createEntryFormElement.appendChild(createEntryProductBtnCancelElement)

        createEntryProductBtnCancelElement.addEventListener('click', () => {
            createEntryFormElement.remove()
        })

        listEntriesContainer.insertBefore(createEntryFormElement, addEntryBtnElement)
    })

    return listEntriesContainer
}

const getEntryContainer = (list, entry) => {
    const entryElement = document.createElement('div')

    {
        const tempElement = document.createElement('p')
        tempElement.innerText = entry.product_name
        entryElement.appendChild(tempElement)
    }

    if (entry.product_pic_url) {
        const entryImgElement = document.createElement('img')
        entryImgElement.src = entry.product_pic_url
        entryImgElement.style.maxHeight = "80px"
        entryImgElement.style.maxWidth = "80px"
        entryElement.appendChild(entryImgElement)
    }

    const entryAmountElement = document.createElement('p')
    entryAmountElement.innerText = entry.amount
    entryElement.appendChild(entryAmountElement)

    {
        const tempElement = document.createElement('p')
        tempElement.innerText = entry.product_unit_type
        entryElement.appendChild(tempElement)
    }

    const entryChangeBtnElement = document.createElement('button')
    entryChangeBtnElement.className = 'btn btn-warning mr-sm-2'
    entryChangeBtnElement.innerText = 'Bearbeiten'
    entryElement.appendChild(entryChangeBtnElement)

    entryChangeBtnElement.addEventListener('click', async () => {
        const old_amount = entryAmountElement.value

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
                await axiosInstance.put(`${baseURL}/shoppingLists/${list.uuid}/entries/${entry.uuid}`, {amount})
                window.location = "/plugin/shopping_list_plugin/list"
            } catch (e) {
                alert(e)
                window.location = "/plugin/shopping_list_plugin/list"
            }
        })

        cancelBtnElement.addEventListener('click', () => {
            entryAmountElement.hidden = false
            changeFormElement.remove()
        })

        entryElement.insertBefore(changeFormElement, entryAmountElement)

        entryAmountElement.hidden = true
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
            entryElement.remove()
        } catch (e) {
            alert(e)
            await getAllLists()
        }
    })
    return entryElement
}

const getSelectProductContainer = async () => {
    const resp = await axiosInstance.get(baseURL + '/products')

    const selectElement = document.createElement('select')
    resp.data.forEach(product => {
        const optionElement = document.createElement('option')
        optionElement.innerText = product.name
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
            await axiosInstance.post(`${baseURL}/shoppingLists`, {name})
            window.location = "/plugin/shopping_list_plugin/list"
            createListNameElement.value = ''
        } catch (e) {
            alert(e)
            window.location = "/plugin/shopping_list_plugin/list"
        }
    })
}

init()
